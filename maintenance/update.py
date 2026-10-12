#!/usr/bin/env python3
"""Compare official sources with a Git tree and import one validated API at a time."""

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml
from validation import validate, describe_error, DESCRIPTION as SCHEMA_VALIDATION_DESCRIPTION
import bundle
import samples
import releases
import report
import health
import conversion
import embedded
import response_keys

ROOT = Path(__file__).resolve().parents[1]
VALIDATION_DESCRIPTION = (SCHEMA_VALIDATION_DESCRIPTION
                          + ", plus security requirement name resolution across operations, callbacks and webhooks")
METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
CURATION = {
    "x-apisguru-categories", "x-logo", "x-preferred", "x-permalink",
    "x-providerName", "x-serviceName", "x-hasEquivalentPaths",
}
PROVENANCE = {"x-origin", "x-conversion"}
MAP_FIELDS = {
    "schemas", "properties", "patternProperties", "$defs", "definitions",
    "parameters", "responses", "headers", "requestBodies", "securitySchemes",
    "callbacks", "links", "examples", "paths", "dependentSchemas",
}


class Loader(getattr(yaml, "CSafeLoader", yaml.SafeLoader)):
    pass


# A bare equals sign is a string in YAML 1.2. PyYAML's legacy value
# resolver gives it a tag with no safe constructor, including in mapping keys.
# Remove only implicit resolution; explicit unsupported tags still fail.
Loader.yaml_implicit_resolvers = {
    k: [(t, r) for t, r in v if t not in {"tag:yaml.org,2002:timestamp", "tag:yaml.org,2002:bool",
                                        "tag:yaml.org,2002:value", "tag:yaml.org,2002:int",
                                        "tag:yaml.org,2002:float"}]
    for k, v in Loader.yaml_implicit_resolvers.items()
}
Loader.add_implicit_resolver("tag:yaml.org,2002:bool",
                             re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"), list("tTfF"))
# YAML 1.1 sexagesimal values such as 1:10 are strings in YAML 1.2.
# Decimal leading zeros are decimal, and octal uses the explicit 0o prefix.
YAML12_INTEGER = re.compile(r"^(?:[-+]?[0-9]+|0o[0-7]+|0x[0-9a-fA-F]+)$")
Loader.add_implicit_resolver("tag:yaml.org,2002:int", YAML12_INTEGER,
                             list("-+0123456789"))


def construct_yaml12_integer(loader, node):
    value = loader.construct_scalar(node)
    radix = 8 if value.startswith("0o") else 16 if value.startswith("0x") else 10
    return int(value[2:] if radix != 10 else value, radix)


Loader.add_constructor("tag:yaml.org,2002:int", construct_yaml12_integer)
# YAML 1.2 supports scientific notation without a decimal point, and excludes
# YAML 1.1 sexagesimal floats. Keep the core schema's decimal/infinity/NaN forms.
YAML12_FLOAT = re.compile(
    r"^(?:[-+]?(?:\.[0-9]+|[0-9]+(?:\.[0-9]*)?)(?:[eE][-+]?[0-9]+)?"
    r"|[-+]?\.(?:inf|Inf|INF)|\.(?:nan|NaN|NAN))$")
Loader.add_implicit_resolver("tag:yaml.org,2002:float", YAML12_FLOAT,
                             list("-+0123456789."))


class Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)


# Quote vendor strings that YAML 1.2 readers would otherwise turn into numbers.
# Keep SafeDumper's other conservative quoting rules (dates, yes/on, etc.).
Dumper.add_implicit_resolver("tag:yaml.org,2002:int", YAML12_INTEGER,
                             list("-+0123456789"))
Dumper.add_implicit_resolver("tag:yaml.org,2002:float", YAML12_FLOAT,
                             list("-+0123456789."))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    # Inspect the original bytes. Invalid control characters are a failure, not a
    # license to silently rewrite vendor content during automated imports.
    text = raw.decode("utf-8-sig")
    try:
        spec = json.loads(text)
    except json.JSONDecodeError:
        spec = yaml.load(text, Loader=Loader)
    if not isinstance(spec, dict) or not (spec.get("openapi") or spec.get("swagger")):
        raise ValueError("Download is not an OpenAPI/Swagger description")
    if not isinstance(spec.get("info"), dict) or not isinstance(spec.get("paths"), dict):
        raise ValueError("Description must have info and paths objects")
    spec["info"]["version"] = str(spec["info"].get("version", ""))
    return spec


def request(url):
    origin = urllib.parse.urlsplit(url)
    if origin.scheme != "https":
        raise ValueError("Sources must use HTTPS")
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ontola-openapi-maintenance"})
            if (origin.hostname == "api.github.com" and origin.port in (None, 443)
                    and origin.username is None and origin.password is None):
                token = os.environ.get("GITHUB_TOKEN")
                if token:
                    # urllib drops unredirected headers on every redirect, including
                    # cross-origin redirects. Never send this token to vendor hosts,
                    # raw files, archives or redirected destinations.
                    req.add_unredirected_header("Authorization", "Bearer " + token)
            with urllib.request.urlopen(req, timeout=30) as response:
                if urllib.parse.urlsplit(response.url).scheme != "https":
                    raise ValueError("Source redirected away from HTTPS")
                return response.read(), {
                    "url": response.url, "etag": response.headers.get("ETag"),
                    "last_modified": response.headers.get("Last-Modified"),
                }
        except urllib.error.HTTPError as error:
            if error.code not in {429, 500, 502, 503, 504} or attempt == 2:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(attempt + 1)


def fetch(source):
    catalog = None
    if "github" in source:
        config = source["github"]
        repository = config["repository"]
        ref = urllib.parse.quote(config["ref"], safe="")
        raw_commit, _ = request("https://api.github.com/repos/" + repository + "/commits/" + ref)
        revision = json.loads(raw_commit)["sha"]
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Invalid source revision")
        path = config["path"]
        if config.get("release_catalog"):
            if source.get("bundling") or source.get("code_samples"):
                raise ValueError("Release catalogs with external artifact recipes require explicit support")
            path, catalog = releases.select(config, revision, request)
        url = "https://raw.githubusercontent.com/" + repository + "/" + revision + "/" + path
    else:
        revision = None
        url = source["url"]
    raw, metadata = request(url)
    metadata.update(revision=revision, sha256=sha256(raw), fetched_at=now())
    if catalog:
        metadata["release_catalog"] = catalog
    return raw, metadata


def stored(path, base):
    files = set(git("ls-tree", "-r", "--name-only", base, "APIs").decode().splitlines())
    if path not in files:
        return None
    return parse(git("show", base + ":" + path))


def reference_objects(value, trail=()):
    """Skip example payloads and extensions, but retain extension-named schemas."""
    if isinstance(value, dict):
        if isinstance(value.get("$ref"), str):
            yield value["$ref"]
        mapping = bool(trail and trail[-1] in MAP_FIELDS)
        for key, child in value.items():
            if not mapping and (str(key).startswith("x-") or key == "example"):
                continue
            # Example Objects carry literal arbitrary data in value.
            if key == "value" and len(trail) >= 2 and trail[-2] == "examples":
                continue
            yield from reference_objects(child, trail + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from reference_objects(child, trail + (index,))


def pointer(spec, ref):
    if not ref.startswith("#/"):
        raise ValueError("Only local JSON Pointer references can be dereferenced here")
    current = spec
    for token in urllib.parse.unquote(ref[2:]).split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(current, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError("Invalid array index in " + ref)
            current = current[int(token)]
        else:
            current = current[token]
    return current


def assert_unreferenced(spec, targets):
    """Conservatively reject JSON Pointer uses before removing an unused node."""
    def tokens(fragment):
        if re.search(r"%(?![0-9a-fA-F]{2})", fragment):
            raise ValueError("Malformed percent escape in reference guard")
        decoded = urllib.parse.unquote(fragment, errors="strict")
        if decoded == "":
            return ()
        if not decoded.startswith("/") or re.search(r"~(?![01])", decoded):
            raise ValueError("Invalid JSON Pointer in reference guard")
        return tuple(token.replace("~1", "/").replace("~0", "~")
                     for token in decoded[1:].split("/"))

    if not isinstance(targets, list) or not targets:
        raise ValueError("Unreferenced preconditions require a nonempty pointer list")
    guarded = {}
    for ref in targets:
        if not isinstance(ref, str) or not ref.startswith("#/"):
            raise ValueError("Unreferenced target must be a local JSON Pointer")
        key = tokens(ref[1:])
        if key in guarded:
            raise ValueError("Duplicate unreferenced target")
        try:
            pointer(spec, ref)
        except (KeyError, IndexError, TypeError, ValueError) as error:
            raise ValueError("Unreferenced target missing; review recipe: " + ref) from error
        guarded[key] = ref

    def strings(value):
        # Include literal examples, extensions, discriminator mappings and keys.
        # A false positive requires review; these must not conceal a new use.
        if isinstance(value, dict):
            for key, child in value.items():
                yield from strings(key)
                yield from strings(child)
        elif isinstance(value, list):
            for child in value:
                yield from strings(child)
        elif isinstance(value, str):
            yield value

    for value in strings(spec):
        if "#" not in value:
            continue
        fragment = value.split("#", 1)[1]
        decoded = urllib.parse.unquote(fragment)
        if decoded and not decoded.startswith("/"):
            continue  # A named anchor or prose, not a JSON Pointer.
        used = tokens(fragment)
        for target, ref in guarded.items():
            # Direct uses, descendants and referenced enclosing nodes all block.
            common = min(len(target), len(used))
            if target[:common] == used[:common]:
                raise ValueError("Unreferenced target is used; review recipe: " + ref)


def dereference(spec, value):
    seen = set()
    while isinstance(value, dict) and "$ref" in value:
        ref = value["$ref"]
        if ref in seen:
            raise ValueError("Reference cycle in a parameter or path item")
        seen.add(ref)
        value = pointer(spec, ref)
    return value


def security_requirement_errors(spec):
    """Check scheme names in actual requirements, never in schemas or examples."""
    components = spec.get("components", {})
    if not isinstance(components, dict):
        components = {}
    schemes = components.get("securitySchemes", {})
    if not isinstance(schemes, dict):
        schemes = {}
    missing = {}
    seen_paths, seen_callbacks = set(), set()

    def check(owner, location):
        requirements = owner.get("security", [])
        # The structural validator reports malformed lists/objects separately.
        if not isinstance(requirements, list):
            return
        for requirement in requirements:
            if isinstance(requirement, dict):
                for name in requirement:
                    if name not in schemes:
                        missing.setdefault(name, []).append(location)

    def callback(value, location):
        value = dereference(spec, value)
        if not isinstance(value, dict) or id(value) in seen_callbacks:
            return
        seen_callbacks.add(id(value))
        for expression, item in value.items():
            if not str(expression).startswith("x-"):
                path_item(item, location + "/" + expression)

    def path_item(value, location):
        value = dereference(spec, value)
        if not isinstance(value, dict) or id(value) in seen_paths:
            return
        seen_paths.add(id(value))
        for method in sorted(METHODS & value.keys()):
            operation = value[method]
            if not isinstance(operation, dict):
                continue
            label = method.upper() + " " + location
            check(operation, label)
            for name, value in operation.get("callbacks", {}).items():
                callback(value, label + " callback " + name)

    try:
        check(spec, "document")
        for field, mapping in (("paths", spec.get("paths", {})),
                               ("webhooks", spec.get("webhooks", {})),
                               ("components/pathItems", components.get("pathItems", {}))):
            for name, item in mapping.items():
                if field != "paths" or not str(name).startswith("x-"):
                    path_item(item, field + "/" + name)
        for name, value in components.get("callbacks", {}).items():
            callback(value, "components/callbacks/" + name)
    except (KeyError, IndexError, TypeError, ValueError, AttributeError) as error:
        return ["Security requirement traversal: " + str(error)]
    return ["Undefined security scheme " + str(name) + " in " + str(len(locations))
            + " requirement(s); first locations: " + "; ".join(locations[:3])
            for name, locations in sorted(missing.items(), key=lambda item: str(item[0]))]


def validate_document(spec):
    errors = []
    refs = list(reference_objects(spec))
    external = sorted({ref.split("#")[0] for ref in refs if not ref.startswith("#")})
    if external:
        return ["External OpenAPI references require bundling: " + ", ".join(external[:8])]
    if not str(spec.get("openapi", "")).startswith(("3.0.", "3.1.")):
        return ["No conversion recipe for this OpenAPI/Swagger version"]
    try:
        validate(spec)
    except Exception as error:
        errors.append("OpenAPI validation: " + describe_error(error, spec))
    errors.extend(security_requirement_errors(spec))
    try:
        for path, item in spec["paths"].items():
            item = dereference(spec, item)
            if not isinstance(item, dict):
                errors.append("Invalid path item: " + path)
                continue
            expected = set(re.findall(r"\{([^}]+)\}", path))
            if any(name.startswith("+") for name in expected):
                errors.append("Reserved expansion in " + path)
            for method in METHODS & item.keys():
                operation = item[method]
                if not operation.get("responses"):
                    errors.append(method.upper() + " " + path + " has no responses")
                parameters = item.get("parameters", []) + operation.get("parameters", [])
                declared = {param["name"] for raw in parameters
                            for param in [dereference(spec, raw)] if param.get("in") == "path"}
                if expected != declared:
                    errors.append(method.upper() + " " + path + " has mismatched path parameters")
    except (KeyError, IndexError, TypeError, ValueError) as error:
        errors.append("Reference/parameter validation: " + str(error))
    return errors


def comparison_content(spec):
    result = copy.deepcopy(spec)
    info = result["info"]
    for key in CURATION | PROVENANCE:
        info.pop(key, None)
    contact = info.get("contact")
    if isinstance(contact, dict):
        contact.pop("x-twitter", None)
        if not contact:
            info.pop("contact", None)
    return result


def canonical(spec):
    return json.dumps(spec, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def serialize_document(spec):
    text = yaml.dump(spec, Dumper=Dumper, default_flow_style=False,
                     sort_keys=False, allow_unicode=True, width=100000)
    if canonical(parse(text.encode("utf-8"))) != canonical(spec):
        raise ValueError("YAML serialization changed document values or types; refusing to write")
    return text


def operation_set(spec):
    return {method.upper() + " " + path for path, item in spec["paths"].items()
            for method in METHODS & item.keys()}


def stats(spec):
    return {"version": spec["info"]["version"], "paths": len(spec["paths"]),
            "operations": len(operation_set(spec)), "format": spec.get("openapi", spec.get("swagger"))}


def without_examples(value, parent=None):
    """Copy without OpenAPI example/examples values (not schema properties of that name)."""
    if isinstance(value, dict):
        return {k: without_examples(v, k) for k, v in value.items()
                if parent == "properties" or k not in {"example", "examples"}}
    if isinstance(value, list):
        return [without_examples(v) for v in value]
    return value


def compare(old, new, source=None):
    if old is None:
        return {"status": "missing", "source": stats(new)}
    old_view = comparison_content(old)
    new_view = comparison_content(preserve_curation(old, new))
    changed = canonical(old_view) != canonical(new_view)
    volatile = False
    if changed and source is not None and source.get("volatile_examples") is True:
        # Reviewed opt-in for vendors that regenerate random example IDs/timestamps
        # (and, with stable_directory, a per-build version stamp) on every build:
        # such changes alone are not content drift. Everything else still counts.
        a, b = without_examples(old_view), without_examples(new_view)
        if source.get("version_policy") == "stable_directory":
            a["info"].pop("version", None)
            b["info"].pop("version", None)
        if canonical(a) == canonical(b):
            changed, volatile = False, True
    result = {
        "status": "changed" if changed else "matches_source",
        "stored": stats(old), "source": stats(new),
        "added_paths": sorted(set(new["paths"]) - set(old["paths"])),
        "removed_paths": sorted(set(old["paths"]) - set(new["paths"])),
        "added_operations": sorted(operation_set(new) - operation_set(old)),
        "removed_operations": sorted(operation_set(old) - operation_set(new)),
    }
    if volatile:
        result["volatile_example_changes_only"] = True
    return result


def destination(source, spec):
    version = spec["info"]["version"]
    if not version or version in {".", "..", "None"} or not re.fullmatch(r"[A-Za-z0-9_.+-]+", version):
        raise ValueError("A safe nonempty vendor version is required")
    target = Path(source["target"])
    if target.parts[:2] != ("APIs", source["provider"]) or target.name != "openapi.yaml" or ".." in target.parts:
        raise ValueError("Target must be an OpenAPI YAML path inside the provider directory")
    policy = source.get("version_policy")
    if policy == "stable_directory":
        # Vendors that stamp every release (e.g. Moneybird "v2-<date>-<hash>")
        # keep one reviewed API-major directory, refreshed in place; the exact
        # vendor version stays recorded in the document and its provenance.
        return target
    if policy != "vendor":
        raise ValueError("This importer supports only declared vendor versions or a reviewed stable directory")
    return target.parent.parent / version / "openapi.yaml"


def baseline(source, spec, base):
    initial = source.get("initial_baseline")
    if initial is not None:
        path = Path(initial) if isinstance(initial, str) else None
        if (path is None or path.parts[:2] != ("APIs", source["provider"])
                or ".." in path.parts or path.name not in {"swagger.yaml", "openapi.yaml"}
                or str(path) != initial):
            raise ValueError("Initial baseline must be a canonical spec path inside the provider directory")
    dest = str(destination(source, spec))
    current = stored(dest, base)
    if current is not None:
        return dest, current
    current = stored(source["target"], base)
    if current is not None:
        return source["target"], current
    if initial is not None:
        current = stored(initial, base)
        if current is None:
            raise ValueError("Configured initial baseline is absent from the comparison tree: " + initial)
        return initial, current
    return source["target"], None


def advance_target(manifest, source, dest):
    """Plan a reviewed baseline change without reformatting unrelated configuration."""
    if str(dest) == source["target"]:
        return None
    original = manifest.read_bytes()
    document = json.loads(original)
    matches = [row for row in document["sources"] if row["id"] == source["id"]]
    if len(matches) != 1 or matches[0] != source:
        raise ValueError("Source configuration changed during import; retry after review")
    old_token = json.dumps(source["target"]).encode()
    if original.count(old_token) != 1:
        raise ValueError("Ambiguous target in manifest; update the reviewed baseline manually")
    updated = original.replace(old_token, json.dumps(str(dest)).encode(), 1)
    matches[0]["target"] = str(dest)
    if json.loads(updated) != document:
        raise ValueError("Manifest target update changed unrelated configuration")
    return original, updated


def preserve_curation(old, new):
    result = copy.deepcopy(new)
    if old:
        for key in sorted(CURATION):
            if key in old["info"]:
                result["info"][key] = copy.deepcopy(old["info"][key])
        twitter = old["info"].get("contact", {}).get("x-twitter")
        if twitter is not None:
            result["info"].setdefault("contact", {})["x-twitter"] = twitter
        for key in ("externalDocs", "tags"):
            if key in old and key not in result:
                result[key] = copy.deepcopy(old[key])
        if "tags" in old and "tags" in result:
            tags = {tag["name"]: copy.deepcopy(tag) for tag in old["tags"]}
            for tag in result["tags"]:
                tags.setdefault(tag["name"], {}).update(tag)
            result["tags"] = list(tags.values())
    return result


def import_document(source, new, metadata, old, baseline_path=None):
    if source.get("import_blocker"):
        raise ValueError(source["import_blocker"])
    errors = validate_document(new)
    if errors:
        raise ValueError("Import blocked:\n" + "\n".join(errors))
    result = preserve_curation(old, new)
    result["info"]["x-origin"] = [{"format": "openapi", "url": metadata["url"],
                                     "version": ".".join(new["openapi"].split(".")[:2])}]
    if metadata.get("conversion"):
        result["info"]["x-origin"].insert(0, {"format": "swagger", "url": metadata["url"], "version": "2.0"})
    revision = " at commit " + metadata["revision"] if metadata.get("revision") else " on " + metadata["fetched_at"]
    result["info"]["x-conversion"] = [
        "Fetched from " + metadata["url"] + revision + "; entry source SHA-256 " + metadata["sha256"] + ".",
    ]
    if metadata.get("release_catalog"):
        catalog = metadata["release_catalog"]
        result["info"]["x-conversion"].append(
            "Selected numeric release " + catalog["selected_version"] + " from the reviewed vendor catalog "
            + catalog["url"] + "; catalog SHA-256 " + catalog["sha256"]
            + ". Preview/prerelease directories and releases below " + catalog["minimum_version"] + " are excluded.")
    result["info"]["x-conversion"].extend(metadata.get("transformations", []))
    result["info"]["x-conversion"].append("Validated with " + VALIDATION_DESCRIPTION + "; no schema constraints removed.")
    if old:
        result["info"]["x-conversion"].append("Preserved existing APIs.guru curation metadata from "
                                           + (baseline_path or source["target"]) + ".")
    result["info"]["x-conversion"].append(
        "Serialized as YAML with PyYAML 6.0.3" + ("." if metadata.get("conversion") else "; no OpenAPI version conversion.")
        if metadata.get("transformations") else
        "Parsed the vendor document and serialized it as YAML with PyYAML 6.0.3; no API content patches or OpenAPI version conversion.")
    errors = validate_document(result)
    if errors:
        raise ValueError("Preserving curation produced an invalid document:\n" + "\n".join(errors))
    return result


def load_sources(path):
    manifest = json.loads(path.read_text())
    if manifest.get("schema_version") != 1:
        raise ValueError("Unsupported source manifest version")
    ids = [entry["id"] for entry in manifest["sources"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate source IDs")
    return manifest["sources"]


def cache_snapshot(cache, source_id, raw, metadata):
    cached = cache / source_id / metadata.get("snapshot_sha256", metadata["sha256"])
    cached.mkdir(parents=True, exist_ok=True)
    (cached / "source").write_bytes(raw)
    (cached / "fetch.json").write_text(json.dumps(metadata, indent=2) + "\n")
    if metadata.get("release_catalog"):
        (cached / "release-catalog.json").write_bytes(metadata["release_catalog"]["response_text"].encode("utf-8"))


def prepare_document(source, raw, metadata=None, cache=None):
    """Replay reviewed exact replacements; source changes require recipe review."""
    transformations = []
    if source.get("embedded_document"):
        if metadata is None or cache is None:
            raise ValueError("Embedded documents require fetch metadata and a source cache")
        raw, step = embedded.prepare(source, raw, metadata, cache)
        transformations.append(step)
    if source.get("bundling") and source.get("code_samples"):
        raise ValueError("Combined schema bundling and code sample recipes require explicit support")
    if source.get("bundling"):
        if metadata is None or cache is None:
            raise ValueError("Bundling requires fetch metadata and a source cache")
        raw, step = bundle.prepare(source, raw, metadata, cache, request, Loader)
        transformations.append(step)
    spec = parse(raw)
    if "yaml_response_keys" in source:
        transformations.append(response_keys.prepare(source, spec))
    if metadata and metadata.get("release_catalog"):
        if spec["info"]["version"] != metadata["release_catalog"]["selected_version"]:
            raise ValueError("Declared API version does not match the selected release directory")
    if source.get("conversion"):
        if metadata is None or cache is None:
            raise ValueError("Conversion requires fetch metadata and a source cache")
        spec, step = conversion.prepare(source, spec, metadata, cache, dereference)
        transformations.append(step)
    if source.get("code_samples"):
        if metadata is None or cache is None:
            raise ValueError("Code samples require fetch metadata and a source cache")
        transformations.append(samples.prepare(source, spec, raw, metadata, cache, request))
    seen = set()
    for filename in source.get("patches", []):
        path = (ROOT / filename).resolve()
        directory = (ROOT / "maintenance/patches").resolve()
        if directory not in path.parents or path.suffix != ".json":
            raise ValueError("Patch recipes must be JSON files under maintenance/patches")
        recipe_raw = path.read_bytes()
        recipe = json.loads(recipe_raw)
        operations = recipe.get("operations") if isinstance(recipe, dict) else None
        if (not isinstance(recipe, dict)
                or set(recipe) - {"schema_version", "description", "assertions", "unreferenced", "operations"}
                or recipe.get("schema_version") != 1 or not recipe.get("description")
                or not isinstance(operations, list) or not operations):
            raise ValueError("Invalid patch recipe: " + filename)
        if "assertions" in recipe:
            assertions = recipe["assertions"]
            if not isinstance(assertions, list) or not assertions:
                raise ValueError("Patch assertions require a nonempty list: " + filename)
            asserted = set()
            for assertion in assertions:
                if not isinstance(assertion, dict) or set(assertion) != {"pointer", "value"}:
                    raise ValueError("Exact patch assertions require pointer and value")
                ref = assertion["pointer"]
                if not isinstance(ref, str) or not ref.startswith("#/") or ref in asserted:
                    raise ValueError("Invalid or duplicate patch assertion pointer: " + str(ref))
                asserted.add(ref)
                try:
                    actual = pointer(spec, ref)
                except (KeyError, IndexError, TypeError, ValueError) as error:
                    raise ValueError("Patch assertion target missing; review recipe: " + ref) from error
                if canonical(actual) != canonical(assertion["value"]):
                    raise ValueError("Patch assertion changed; review recipe: " + ref)
        if "unreferenced" in recipe:
            assert_unreferenced(spec, recipe["unreferenced"])
        # Work on a separate parsed document. No caller's object or original
        # cached bytes are modified, even if a later precondition fails.
        for operation in operations:
            replacing = set(operation) == {"pointer", "from", "value", "context"}
            removing = set(operation) == {"pointer", "from", "remove", "context"} and operation["remove"] is True
            if not replacing and not removing:
                raise ValueError("Exact patches require pointer, from, context, and value or remove:true")
            ref = operation["pointer"]
            if not isinstance(ref, str) or not ref.startswith("#/") or ref in seen:
                raise ValueError("Invalid or duplicate patch pointer: " + str(ref))
            seen.add(ref)
            parent_ref, token = ref.rsplit("/", 1)
            parent = pointer(spec, parent_ref)
            token = urllib.parse.unquote(token).replace("~1", "/").replace("~0", "~")
            context = operation["context"]
            if not isinstance(parent, dict) or not isinstance(context, dict) or not context:
                raise ValueError("Patch requires an object parent and nonempty context: " + ref)
            for key, expected in context.items():
                if key not in parent or canonical(parent[key]) != canonical(expected):
                    raise ValueError("Patch context changed; review recipe: " + ref)
            # JSON comparison distinguishes false from 0 and preserves types.
            if token not in parent or canonical(parent[token]) != canonical(operation["from"]):
                raise ValueError("Patch source value changed; review recipe: " + ref)
            if removing:
                del parent[token]
            else:
                parent[token] = copy.deepcopy(operation["value"])
        transformations.append("Applied " + filename + " (SHA-256 " + sha256(recipe_raw)
                               + "): " + recipe["description"])
    return spec, transformations


def audit(source, base, cache, health_checker=None):
    result = {"id": source["id"], "target": source["target"], "checked_at": now(),
              "validation_profile": VALIDATION_DESCRIPTION,
              "coverage": source.get("coverage", "Configured service only; freshness of the whole provider is not established.")}
    result.update((health_checker or health.Checker(request, now, cache)).check(source))
    if source.get("source_health"):
        result["declared_source_health"] = source["source_health"]
    try:
        raw, metadata = fetch(source)
        result.update(fetch=metadata, last_successful_fetch=metadata["fetched_at"])
        cache_snapshot(cache, source["id"], raw, metadata)
        spec, transformations = prepare_document(source, raw, metadata, cache)
        metadata["transformations"] = transformations
        cache_snapshot(cache, source["id"], raw, metadata)
        dest = str(destination(source, spec))
        baseline_path, old = baseline(source, spec, base)
        result.update(compare(old, spec, source), fetch=metadata, destination=dest,
                      baseline=baseline_path)
        result["last_successful_comparison"] = now()
        result["validation_errors"] = validate_document(spec)
        if not result["validation_errors"]:
            result["last_successful_validation"] = now()
        if source.get("import_blocker"):
            result["import_blocker"] = source["import_blocker"]
    except Exception as error:
        result.update(status="failed", error=str(error))
    return result


def write_report(path, results, base):
    previous = {}
    if path.exists():
        previous = {row["id"]: row for row in json.loads(path.read_text()).get("sources", [])}
    revision = git("rev-parse", base).decode().strip()
    for result in results:
        result["base_revision"] = revision
        for field in ("last_successful_fetch", "last_successful_comparison", "last_successful_validation",
                      "last_successful_source_health_check"):
            if field not in result and field in previous.get(result["id"], {}):
                result[field] = previous[result["id"]][field]
    path.parent.mkdir(parents=True, exist_ok=True)
    merged = {**previous, **{row["id"]: row for row in results}}
    document = {"generated_at": now(), "base": base, "base_revision": revision,
                "sources": list(merged.values())}
    path.write_text(json.dumps(document, indent=2) + "\n")
    summary_path = path.with_suffix(".md")
    if summary_path == path:
        summary_path = path.with_suffix(".summary.md")
    summary_path.write_text(report.render(document))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "import"))
    parser.add_argument("--source", action="append", help="Manifest ID; repeat to select sources")
    parser.add_argument("--manifest", type=Path, default=ROOT / "maintenance/sources.json")
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--cache", type=Path, default=ROOT / "cache/maintenance")
    parser.add_argument("--report", type=Path, default=ROOT / "cache/maintenance/report.json")
    args = parser.parse_args(argv)
    sources = load_sources(args.manifest)
    if args.source:
        unknown = set(args.source) - {source["id"] for source in sources}
        if unknown:
            parser.error("Unknown source IDs: " + ", ".join(sorted(unknown)))
        sources = [source for source in sources if source["id"] in args.source]
    if args.command == "import":
        if len(sources) != 1:
            parser.error("Import exactly one source at a time using --source")
        source = sources[0]
        observation = health.Checker(request, now, args.cache).check(source)
        if observation.get("source_health_issue"):
            raise ValueError(observation["source_health_issue"])
        if source.get("import_blocker"):
            raise ValueError(source["import_blocker"])
        raw, metadata = fetch(source)
        cache_snapshot(args.cache, source["id"], raw, metadata)
        spec, transformations = prepare_document(source, raw, metadata, args.cache)
        metadata["transformations"] = transformations
        cache_snapshot(args.cache, source["id"], raw, metadata)
        dest = destination(source, spec)
        old_dest = stored(str(dest), args.base)
        baseline_path, old = baseline(source, spec, args.base)
        manifest_change = advance_target(args.manifest, source, dest)
        if old_dest and compare(old_dest, spec, source)["status"] == "matches_source":
            if manifest_change:
                errors = validate_document(spec)
                if errors:
                    raise ValueError("Import blocked:\n" + "\n".join(errors))
                if args.manifest.read_bytes() != manifest_change[0]:
                    raise ValueError("Manifest changed during validation; refusing to advance target")
                args.manifest.write_bytes(manifest_change[1])
                print("Source already matches; advanced the manifest target to " + str(dest))
                return 0
            print("Already matches the source; no file written.")
            return 0
        output = ROOT / dest
        if output.exists():
            expected = git("show", args.base + ":" + str(dest)) if old_dest else None
            if expected != output.read_bytes():
                raise ValueError("Refusing to overwrite local changes: " + str(dest))
        result = import_document(source, spec, metadata, old, baseline_path)
        serialized = serialize_document(result)
        if manifest_change and args.manifest.read_bytes() != manifest_change[0]:
            raise ValueError("Manifest changed during validation; refusing to write the import")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized)
        if manifest_change:
            args.manifest.write_bytes(manifest_change[1])
        print(str(dest))
        print(json.dumps(compare(old, spec), indent=2))
        return 0
    health_checker = health.Checker(request, now, args.cache)
    results = [audit(source, args.base, args.cache, health_checker) for source in sources]
    write_report(args.report, results, args.base)
    for result in results:
        print(result["id"] + ": " + result["status"] +
              ("; import blocked" if result.get("import_blocker") or result.get("validation_errors") or result.get("source_health_issue") else ""))
    print("Report: " + str(args.report))
    return 1 if any(row["status"] == "failed" or row.get("validation_errors") or row.get("import_blocker") or row.get("source_health_issue") for row in results) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
