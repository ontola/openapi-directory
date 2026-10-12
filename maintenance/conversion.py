"""Convert already fetched, self-contained Swagger using a locked local tool."""
import copy
import hashlib
import json
import subprocess
from pathlib import Path

import bundle
import embedded

TOOL_VERSION = "7.0.8"
HERE = Path(__file__).resolve().parent


def prepare(source, spec, metadata, cache, resolve_path=None):
    config = source["conversion"]
    if config.get("tool") != "swagger2openapi" or config.get("version") != TOOL_VERSION:
        raise ValueError("Unsupported conversion recipe")
    sibling_mode = config.get("ref_siblings")
    if sibling_mode is not None and sibling_mode != "allOf":
        raise ValueError("Unsupported reference-sibling conversion mode")
    if spec.get("swagger") != "2.0" or "openapi" in spec:
        raise ValueError("Conversion recipe requires Swagger 2.0; review changed source format")
    if any(not ref.startswith("#") for ref in bundle.refs(spec)):
        raise ValueError("External references require pinned bundling before conversion")

    def operations(document):
        found = set()
        for path, item in document["paths"].items():
            if "$ref" in item and resolve_path is None:
                raise ValueError("Referenced path items require a local resolver")
            item = resolve_path(document, item) if resolve_path else item
            for method in {"get", "put", "post", "delete", "options", "head", "patch", "trace"} & item.keys():
                operation = item[method]
                if not isinstance(operation, dict) or not isinstance(operation.get("responses"), dict) or not operation["responses"]:
                    raise ValueError("Operation has no responses; refusing to let the converter invent one: " + method.upper() + " " + path)
                found.add(method.upper() + " " + path)
        return found

    original_operations = operations(spec)

    def reserved(value):
        if isinstance(value, dict):
            return "x-s2o-warning" in value or any(reserved(v) for v in value.values())
        if isinstance(value, list):
            return any(reserved(v) for v in value)
        return False

    if reserved(spec):
        raise ValueError("Source contains converter warning markers; review before conversion")
    for field in ("expected_warnings", "expected_patches"):
        count = config.get(field, 0)
        if type(count) is not int or count < 0:
            raise ValueError("Conversion expectations must be nonnegative integer counts")
    nullable_guards = config.get("nullable_extensions")
    control = None
    if nullable_guards is not None:
        if not isinstance(nullable_guards, list) or not nullable_guards:
            raise ValueError("Nullable extension guards must be a nonempty list")
        control = copy.deepcopy(spec)
        native_paths, converted_paths = set(), set()
        for guard in nullable_guards:
            if (not isinstance(guard, dict) or set(guard) != {"from", "to", "schema"}
                    or not isinstance(guard["schema"], dict) or guard["schema"].get("x-nullable") is not True
                    or guard["from"] in native_paths or guard["to"] in converted_paths):
                raise ValueError("Invalid or duplicate nullable extension guard")
            native_paths.add(guard["from"])
            converted_paths.add(guard["to"])
            actual = embedded.pointer(spec, guard["from"])
            if json.dumps(actual, sort_keys=True) != json.dumps(guard["schema"], sort_keys=True):
                raise ValueError("Native nullable schema changed: " + guard["from"])
            del embedded.pointer(control, guard["from"])["x-nullable"]

        def extension_paths(value, pointer="#"):
            found = set()
            if isinstance(value, dict):
                # Only true extensions are translated into counted repairs; false ones
                # become nullable:false in both conversions and stay covered by the
                # complete control-output equality below.
                if value.get("x-nullable") is True:
                    found.add(pointer)
                for key, child in value.items():
                    found |= extension_paths(child, pointer + "/" + key.replace("~", "~0").replace("/", "~1"))
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    found |= extension_paths(child, pointer + "/" + str(index))
            return found

        if extension_paths(spec) != native_paths:
            raise ValueError("Native nullable extension locations changed")
    package = HERE / "node_modules/swagger2openapi/package.json"
    if not package.exists() or json.loads(package.read_text())["version"] != TOOL_VERSION:
        raise ValueError("Install the pinned converter with npm ci --prefix maintenance --ignore-scripts")
    workspace = (cache / source["id"] / metadata.get("snapshot_sha256", metadata["sha256"])).resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(spec, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    input_path, output_path = workspace / "conversion-input.json", workspace / "conversion-result.json"
    input_path.write_bytes(raw)
    process = subprocess.run(["node", str(HERE / "convert-swagger.cjs"), str(input_path), str(output_path)] + ([sibling_mode] if sibling_mode else []),
                             cwd=workspace, capture_output=True, text=True, timeout=120)
    (workspace / "converter.log").write_text(process.stdout + process.stderr)
    if process.returncode:
        raise ValueError("Swagger conversion failed: " + process.stderr[-1500:])
    result = json.loads(output_path.read_text())
    converted = result["openapi"]
    if converted.get("openapi") != "3.0.0" or "swagger" in converted:
        raise ValueError("Converter did not produce the configured OpenAPI version")
    if set(converted["paths"]) != set(spec["paths"]) or operations(converted) != original_operations:
        raise ValueError("Conversion changed paths or operations; review before importing")
    warnings, patches = result["warnings"], result["patches"]
    if not isinstance(warnings, list) or type(patches) is not int:
        raise ValueError("Invalid converter observations")
    if len(warnings) != config.get("expected_warnings", 0) or patches != config.get("expected_patches", 0):
        raise ValueError("Converter warning/patch count changed; review conversion-result.json before updating the recipe")
    control_observation = None
    if control is not None:
        control_input = workspace / "nullable-control-input.json"
        control_output = workspace / "nullable-control-result.json"
        control_raw = (json.dumps(control, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
        control_input.write_bytes(control_raw)
        check = subprocess.run(["node", str(HERE / "convert-swagger.cjs"), str(control_input), str(control_output)] + ([sibling_mode] if sibling_mode else []),
                               cwd=workspace, capture_output=True, text=True, timeout=120)
        (workspace / "nullable-control.log").write_text(check.stdout + check.stderr)
        if check.returncode:
            raise ValueError("Nullable control conversion failed")
        control_result = json.loads(control_output.read_text())
        if control_result["patches"] != 0 or control_result["warnings"] != []:
            raise ValueError("Nullable control must have zero warnings and patches; unrelated repair detected")
        without_nullable = copy.deepcopy(converted)
        for guard in nullable_guards:
            expected = {k: v for k, v in guard["schema"].items() if k != "x-nullable"}
            expected["nullable"] = True
            actual = embedded.pointer(without_nullable, guard["to"])
            if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
                raise ValueError("Converted nullable schema changed: " + guard["to"])
            del actual["nullable"]
        if json.dumps(without_nullable, sort_keys=True) != json.dumps(control_result["openapi"], sort_keys=True):
            raise ValueError("Conversion changed content beyond guarded nullable translations")
        control_observation = {"input_sha256": hashlib.sha256(control_raw).hexdigest(),
                               "result_sha256": hashlib.sha256(control_output.read_bytes()).hexdigest(),
                               "warnings": [], "patches": 0,
                               "locations": [{"from": g["from"], "to": g["to"]} for g in nullable_guards],
                               "complete_output_equality_except_nullable": True}
    output = (json.dumps(converted, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    (workspace / "converted.json").write_bytes(output)
    metadata["conversion"] = {"tool": "swagger2openapi", "version": TOOL_VERSION,
                              "from": "2.0", "to": "3.0.0",
                              "options": {"patch": True, "warnOnly": True, "resolve": False, "targetVersion": "3.0.0"},
                              "warnings": warnings, "patches": patches,
                              "input_sha256": hashlib.sha256(raw).hexdigest(),
                              "converted_sha256": hashlib.sha256(output).hexdigest()}
    if sibling_mode:
        metadata["conversion"]["options"]["refSiblings"] = sibling_mode
    if control_observation is not None:
        metadata["conversion"]["nullable_control"] = control_observation
    step = ("Converted Swagger 2.0 to OpenAPI 3.0.0 with swagger2openapi " + TOOL_VERSION
            + " (patch:true, warnOnly:true, resolve:false, targetVersion:3.0.0); "
            + str(len(warnings)) + " warnings and " + str(patches) + " converter patches. "
            + "External resolution is disabled; the complete converted document must pass validation. "
            + "Converted SHA-256 " + metadata["conversion"]["converted_sha256"] + ".")
    if sibling_mode:
        step += " Used refSiblings:allOf to retain vendor schema-reference descriptions/titles in schema composition rather than dropping them."
    if control_observation is not None:
        step += (" Verified " + str(len(nullable_guards)) + " exact x-nullable:true to nullable:true translations; "
                 "independent control conversion with only those extensions removed has zero warnings/patches "
                 "and identical complete output except those nullable annotations. No null semantics removed.")
    return converted, step
