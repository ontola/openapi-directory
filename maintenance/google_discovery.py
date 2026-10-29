"""Lossless-metadata Google Discovery v1 -> OpenAPI 3.0.3 conversion.

Discovery resource names use URI reserved expansion. Its flatPath supplies
the concrete HTTP route; using path alone overwrites unrelated operations.
Unsupported Discovery annotations/protocol details remain in x-google-*
extensions, rather than being discarded or interpreted as new constraints.
"""
import copy
import json
import re

METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
VARIABLE = re.compile(r"\{\+?([^{}]+)\}")
SCHEMA_FIELDS = {"type", "description", "format", "readOnly", "deprecated", "pattern",
                 "enum", "default", "minimum", "maximum"}
AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


def methods(source):
    result = []

    def visit(resource, tag=None):
        for method in resource.get("methods", {}).values():
            result.append((method, tag))
        for name, child in resource.get("resources", {}).items():
            visit(child, tag or name)

    visit(source)
    ids = [method["id"] for method, _ in result]
    if len(set(ids)) != len(ids):
        raise ValueError("Discovery contains duplicate method IDs")
    return result


def numeric(value):
    if isinstance(value, str):
        parsed = json.loads(value)
        if type(parsed) not in {int, float}:
            raise ValueError("A numeric constraint is not a number")
        return parsed
    if type(value) not in {int, float}:
        raise ValueError("A numeric constraint is not a number")
    return value


def schema(value):
    if not isinstance(value, dict):
        raise ValueError("Discovery schema must be an object")
    result = {}
    for key, item in value.items():
        if key == "$ref":
            if not isinstance(item, str) or item.startswith(("#", "/")) or ":" in item:
                raise ValueError("Expected a local Discovery schema name")
            result[key] = "#/components/schemas/" + item.replace("~", "~0").replace("/", "~1")
        elif key == "properties":
            result[key] = {name: schema(child) for name, child in item.items()}
        elif key in {"items", "additionalProperties"}:
            result[key] = schema(item) if isinstance(item, dict) else item
        elif key == "type" and item == "any":
            result["x-google-discovery-type"] = "any"
        elif key in {"minimum", "maximum"}:
            result[key] = numeric(item)
        elif key == "default":
            if isinstance(item, str) and value.get("type") in {"boolean", "integer", "number", "array", "object"}:
                result[key] = json.loads(item)
            else:
                result[key] = copy.deepcopy(item)
        elif key in SCHEMA_FIELDS:
            result[key] = copy.deepcopy(item)
        elif key == "id":
            result["x-google-discovery-id"] = item
        elif key == "enumDescriptions":
            result["x-google-enum-descriptions"] = copy.deepcopy(item)
        elif key == "enumDeprecated":
            result["x-google-enum-deprecated"] = copy.deepcopy(item)
        elif key == "annotations":
            # required here names METHODS, not globally required properties.
            result["x-google-annotations"] = copy.deepcopy(item)
        elif key.startswith("x-"):
            result[key] = copy.deepcopy(item)
        else:
            result["x-google-discovery-" + key] = copy.deepcopy(item)
    if "$ref" in result and len(result) > 1:
        # OAS 3.0 Reference Object siblings otherwise have no effect.
        reference = result.pop("$ref")
        result["allOf"] = [{"$ref": reference}]
    return result


def parameter(name, value):
    location = value.get("location")
    if location not in {"query", "path"}:
        raise ValueError("Unsupported Discovery parameter location")
    fields = {key: child for key, child in value.items()
              if key not in {"location", "required", "repeated", "description", "deprecated"}}
    item = schema(fields)
    if value.get("repeated"):
        item = {"type": "array", "items": item}
    result = {"name": name, "in": location, "schema": item}
    for key in {"description", "deprecated", "required"} & value.keys():
        result[key] = copy.deepcopy(value[key])
    if location == "path":
        result["required"] = True
    if value.get("repeated"):
        result.update(style="form" if location == "query" else "simple", explode=location == "query")
    return result


def route(method):
    """Return concrete path, translated path parameters, native expansion metadata."""
    original = method["path"].lstrip("/")
    concrete = method.get("flatPath", method["path"]).lstrip("/").replace("{+", "{")
    tokens = list(VARIABLE.finditer(original))
    pieces, offset = [], 0
    for token in tokens:
        pieces.append(re.escape(original[offset:token.start()]))
        pieces.append("(.+?)" if original[token.start():token.end()].startswith("{+") else r"(\{[^{}]+\})")
        offset = token.end()
    pieces.append(re.escape(original[offset:]))
    matched = re.fullmatch("".join(pieces), concrete)
    if not matched:
        raise ValueError("flatPath cannot be mapped back to the original Discovery path: " + method["id"])
    bindings, constants = {}, {}
    native = method.get("parameters", {})
    if {name for name, value in native.items() if value.get("location") == "path"} != {token.group(1) for token in tokens}:
        raise ValueError("Native path parameter inventory does not match its template")
    translated = {}
    for token, expansion in zip(tokens, matched.groups()):
        owner = token.group(1)
        if owner not in native or native[owner].get("location") != "path":
            raise ValueError("Discovery path parameter is missing: " + owner)
        names = VARIABLE.findall(expansion)
        if not names:
            # Singleton resources have literal flat paths (ragEngineConfig,
            # for example), even when the original method takes {+name}.
            constants[owner] = expansion
        for name in names:
            if name in translated:
                raise ValueError("Duplicate concrete path parameter: " + name)
            if expansion == "{" + owner + "}" and name == owner:
                translated[name] = parameter(name, native[owner])
            else:
                # A whole-resource pattern cannot be applied to one ID component.
                # Preserve it with the original template/binding for aware clients.
                description = "Component of the original `" + owner + "` resource name."
                if native[owner].get("description"):
                    description += " " + native[owner]["description"]
                translated[name] = {"name": name, "in": "path", "required": True,
                                    "description": description, "schema": {"type": "string"}}
            bindings[name] = owner
    variables = VARIABLE.findall(concrete)
    if len(variables) != len(set(variables)) or set(variables) != set(translated):
        raise ValueError("Concrete path parameter inventory does not match")
    metadata = {"path": method["path"]}
    if "flatPath" in method:
        metadata["flatPath"] = method["flatPath"]
    if concrete != original.replace("{+", "{"):
        metadata["resourceNameBindings"] = bindings
        if constants:
            metadata["resourceNameConstants"] = constants
        metadata["resourceNameParameters"] = {name: copy.deepcopy(value) for name, value in native.items()
                                               if value.get("location") == "path"}
    return "/" + concrete, list(translated.values()), metadata


def convert(source):
    if source.get("discoveryVersion") != "v1" or source.get("protocol") != "rest":
        raise ValueError("Expected a REST Google Discovery v1 document")
    for name in ["name", "version", "rootUrl", "servicePath", "schemas"]:
        if name not in source:
            raise ValueError("Missing Discovery field: " + name)
    base = source["rootUrl"].rstrip("/") + "/" + source["servicePath"].lstrip("/")
    document = {
        "openapi": "3.0.3",
        "info": {"title": source.get("title", source["name"]),
                 "version": source["version"], "description": source.get("description", ""),
                 "contact": {"name": source.get("ownerName", "Google"),
                             "url": "https://" + source.get("ownerDomain", "google.com")}},
        "servers": [{"url": base.rstrip("/")}],
        "paths": {},
        "components": {"schemas": {name: schema(value) for name, value in source["schemas"].items()},
                       "parameters": {}, "securitySchemes": {}},
    }
    if source.get("documentationLink"):
        document["externalDocs"] = {"url": source["documentationLink"]}
    for name, value in source.get("parameters", {}).items():
        if value.get("location") != "query":
            raise ValueError("A global parameter is not a query parameter")
        document["components"]["parameters"][name] = parameter(name, value)
    scopes = {key: value["description"] for key, value in source.get("auth", {}).get("oauth2", {}).get("scopes", {}).items()}
    if scopes:
        document["components"]["securitySchemes"] = {
            "Oauth2": {"type": "oauth2", "flows": {"implicit": {
                "authorizationUrl": AUTHORIZATION_URL, "scopes": copy.deepcopy(scopes)}}},
            "Oauth2c": {"type": "oauth2", "flows": {"authorizationCode": {
                "authorizationUrl": AUTHORIZATION_URL, "tokenUrl": TOKEN_URL, "scopes": copy.deepcopy(scopes)}}},
        }
    tags = []
    for method, tag in methods(source):
        verb = method["httpMethod"].lower()
        if verb not in METHODS:
            raise ValueError("Unsupported HTTP method")
        path, parameters, metadata = route(method)
        item = document["paths"].setdefault(path, {})
        if verb in item:
            raise ValueError("Discovery methods still collide at " + verb.upper() + " " + path)
        for name in method.get("parameterOrder", []):
            if name not in method.get("parameters", {}):
                raise ValueError("parameterOrder names an absent parameter")
        parameters.extend(parameter(name, value) for name, value in method.get("parameters", {}).items()
                          if value.get("location") != "path")
        operation = {"operationId": method["id"]}
        if "description" in method:
            operation["description"] = method["description"]
        if "deprecated" in method:
            operation["deprecated"] = method["deprecated"]
        if parameters:
            operation["parameters"] = parameters
        if tag:
            operation["tags"] = [tag]
            if tag not in tags:
                tags.append(tag)
        if "scopes" in method:
            if any(scope not in scopes for scope in method["scopes"]):
                raise ValueError("Method names an undefined OAuth scope")
            operation["security"] = [{flow: [scope]} for scope in method["scopes"] for flow in ["Oauth2", "Oauth2c"]]
        if "request" in method:
            request = {key: value for key, value in method["request"].items() if key != "parameterName"}
            operation["requestBody"] = {"content": {"application/json": {"schema": schema(request)}}}
            if "parameterName" in method["request"]:
                metadata["requestParameterName"] = method["request"]["parameterName"]
        response = {"description": "Successful response; Discovery does not specify an HTTP status code."}
        if "response" in method:
            response["content"] = {"application/json": {"schema": schema(method["response"])}}
        if method.get("supportsMediaDownload"):
            response.setdefault("content", {})["*/*"] = {"schema": {"type": "string", "format": "binary"}}
        operation["responses"] = {"2XX": response}
        known = {"id", "description", "deprecated", "httpMethod", "path", "flatPath", "parameters",
                 "parameterOrder", "request", "response", "scopes"}
        metadata.update({key: copy.deepcopy(value) for key, value in method.items() if key not in known})
        if "parameterOrder" in method:
            metadata["parameterOrder"] = copy.deepcopy(method["parameterOrder"])
        operation["x-google-discovery"] = metadata
        item[verb] = operation
    global_refs = [{"$ref": "#/components/parameters/" + name.replace("~", "~0").replace("/", "~1")}
                   for name in source.get("parameters", {})]
    for item in document["paths"].values():
        if global_refs:
            item["parameters"] = copy.deepcopy(global_refs)
    if tags:
        document["tags"] = [{"name": tag} for tag in tags]
    projected = {"discoveryVersion", "protocol", "description", "title", "version", "schemas", "resources",
                 "methods", "parameters", "auth", "ownerName", "ownerDomain", "documentationLink"}
    document["x-google-discovery"] = {key: copy.deepcopy(value) for key, value in source.items() if key not in projected}
    return document


def check(source, document):
    """Independent inventory/projection checks, in addition to full OAS validation."""
    def equal(left, right):
        if type(left) is not type(right):
            return False
        if isinstance(left, dict):
            return left.keys() == right.keys() and all(equal(left[k], right[k]) for k in left)
        if isinstance(left, list):
            return len(left) == len(right) and all(equal(a, b) for a, b in zip(left, right))
        return left == right

    def verify_schema(native, actual):
        for key, value in native.items():
            if key == "properties":
                if actual.get(key, {}).keys() != value.keys():
                    raise ValueError("Schema property inventory changed")
                for name, child in value.items():
                    verify_schema(child, actual[key][name])
                continue
            if key in {"items", "additionalProperties"} and isinstance(value, dict):
                verify_schema(value, actual[key])
                continue
            if key == "$ref":
                reference = actual.get("$ref")
                if reference is None:
                    reference = actual.get("allOf", [{}])[0].get("$ref")
                expected = "#/components/schemas/" + value.replace("~", "~0").replace("/", "~1")
                if reference != expected:
                    raise ValueError("Schema reference changed")
                continue
            target = key
            expected = value
            if key == "type" and value == "any":
                target = "x-google-discovery-type"
                if "type" in actual:
                    raise ValueError("An unconstrained Discovery value acquired a type")
            elif key in {"minimum", "maximum"} and isinstance(value, str):
                expected = json.loads(value)
            elif key == "default" and isinstance(value, str) and native.get("type") in {"boolean", "integer", "number", "array", "object"}:
                expected = json.loads(value)
            elif key == "id":
                target = "x-google-discovery-id"
            elif key == "annotations":
                target = "x-google-annotations"
            elif key == "enumDescriptions":
                target = "x-google-enum-descriptions"
            elif key == "enumDeprecated":
                target = "x-google-enum-deprecated"
            elif key not in SCHEMA_FIELDS and key not in {"items", "additionalProperties"} and not key.startswith("x-"):
                target = "x-google-discovery-" + key
            if target not in actual or not equal(expected, actual[target]):
                raise ValueError("Schema field changed: " + key)

    def verify_parameter(native, actual):
        if actual["in"] != native["location"]:
            raise ValueError("Parameter location changed")
        for key in {"description", "deprecated"} & native.keys():
            if not equal(native[key], actual.get(key)):
                raise ValueError("Parameter annotation changed")
        expected = {key: value for key, value in native.items()
                    if key not in {"location", "description", "deprecated", "required", "repeated"}}
        projected = actual["schema"]
        if native.get("repeated"):
            if projected.get("type") != "array" or actual.get("explode") != (native["location"] == "query"):
                raise ValueError("Repeated parameter serialization changed")
            projected = projected["items"]
        verify_schema(expected, projected)

    for name, native in source["schemas"].items():
        if name not in document["components"]["schemas"]:
            raise ValueError("Conversion lost or invented schemas")
        verify_schema(native, document["components"]["schemas"][name])
    for name, native in source.get("parameters", {}).items():
        verify_parameter(native, document["components"]["parameters"][name])
    actual = {}
    for path, item in document["paths"].items():
        for verb, operation in item.items():
            if verb in METHODS:
                key = operation["operationId"]
                if key in actual:
                    raise ValueError("Duplicate converted operation ID")
                actual[key] = (path, verb, operation)
    expected = {method["id"]: method for method, _ in methods(source)}
    if actual.keys() != expected.keys():
        raise ValueError("Conversion lost or invented methods")
    if document["components"]["schemas"].keys() != source["schemas"].keys():
        raise ValueError("Conversion lost or invented schemas")
    for name, method in expected.items():
        path, verb, operation = actual[name]
        if verb.upper() != method["httpMethod"]:
            raise ValueError("HTTP method changed")
        if operation.get("description") != method.get("description"):
            raise ValueError("Operation description changed")
        declared = {p["name"] for p in operation.get("parameters", []) if p["in"] == "path"}
        if set(VARIABLE.findall(path)) != declared:
            raise ValueError("Operation path parameters do not match its template")
        scopes = [scope for requirement in operation.get("security", []) for values in requirement.values() for scope in values]
        if set(scopes) != set(method.get("scopes", [])):
            raise ValueError("Operation scopes changed")
        parameters = {p["name"]: p for p in operation.get("parameters", [])}
        for parameter_name, native in method.get("parameters", {}).items():
            if native["location"] == "query":
                verify_parameter(native, parameters[parameter_name])
        if operation["x-google-discovery"].get("resourceNameParameters"):
            original_parameters = {name: value for name, value in method.get("parameters", {}).items() if value["location"] == "path"}
            if not equal(original_parameters, operation["x-google-discovery"]["resourceNameParameters"]):
                raise ValueError("Original resource-name constraints changed")
        for part, target in [("request", "requestBody"), ("response", "responses")]:
            if part in method:
                result = operation[target] if part == "request" else operation[target]["2XX"]
                ref = result["content"]["application/json"]["schema"]
                verify_schema({key: value for key, value in method[part].items() if key != "parameterName"}, ref)
                while "allOf" in ref:
                    ref = ref["allOf"][0]
                if "$ref" in method[part] and ref.get("$ref") != "#/components/schemas/" + method[part]["$ref"]:
                    raise ValueError("Operation body schema changed")
    refs = 0

    def visit(value):
        nonlocal refs
        if isinstance(value, dict):
            if isinstance(value.get("$ref"), str):
                reference = value["$ref"]
                if not reference.startswith("#/"):
                    raise ValueError("Non-local generated reference")
                node = document
                for segment in reference[2:].split("/"):
                    key = segment.replace("~1", "/").replace("~0", "~")
                    node = node[int(key)] if isinstance(node, list) else node[key]
                refs += 1
            for key, child in value.items():
                if key not in {"default", "example", "examples", "enum"} and not key.startswith("x-"):
                    visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(document)
    return {"operations": len(actual), "paths": len(document["paths"]),
            "schemas": len(source["schemas"]), "references": refs}
