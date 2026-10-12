#!/usr/bin/env python3
"""Generate the readable Moneybird record subset from the official OpenAPI spec.

This is deliberately data driven: routes and schemas are copied from the source
spec, while the classification rules below only decide which GET operations are
primary list/detail records for an importer.
"""
from __future__ import annotations

import copy
import json
import re
import argparse
import hashlib
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "v2" / "openapi.yaml"
OUT = HERE / "openapi.yaml"
MANIFEST = HERE / "coverage.json"
COLLECTIONS = HERE / "collections.json"

SOURCE_DOCUMENT = {}

PRIMARY_LIST_NAMES = {
    "administrations", "assets", "contacts", "custom_fields", "document_styles",
    "general_documents", "general_journal_documents", "purchase_invoices",
    "receipts", "typeless_documents", "estimates", "external_sales_invoices",
    "financial_accounts", "financial_mutations", "identities", "ledger_accounts",
    "products", "projects", "purchase_transactions", "recurring_sales_invoices",
    "sales_invoices", "subscription_templates", "subscriptions", "task_lists",
    "task_list_templates", "tax_rates", "time_entries", "users", "verifications",
    "webhooks", "workflows",
}

def normalized_path(path: str) -> str:
    return path.replace("{format}", ".json")

def path_kind(path: str, op_id: str) -> tuple[str, str]:
    p = path.lower()
    if "/synchronization" in p:
        return "sync_helper", "ID/version synchronization endpoint"
    if p.endswith("/downloads{format}"):
        return "primary_list", "JSON download records, not attachment bytes"
    if any(x in p for x in ("/download", "/checkout_identifier", "customer_contact_portal")):
        return "binary_or_helper", "download, portal-link, or checkout helper"
    if "/reports/" in p:
        return "report", "report dataset rather than a primary record collection"
    if p.endswith("/default{format}"):
        return "child_or_singleton", "default singleton endpoint"
    if p.endswith("/payments/{id}{format}") or "/contact_people/" in p or "/additional_charges" in p or "/moneybird_payments_mandate" in p:
        return "child_or_singleton", "child resource or singleton-only endpoint"
    if re.search(r"/(find_by_[^/]+|customer_id)/", p):
        return "lookup_helper", "duplicate lookup for a primary collection"
    if p.endswith("/doubles{format}"):
        return "lookup_helper", "possible-duplicate record lookup for a primary collection"
    # Collection paths have no terminal path parameter; detail paths do.
    if re.search(r"/\{[^}]+\}\{format\}$", path):
        return "primary_detail", "primary record detail endpoint"
    if "/filter{format}" in path:
        return "lookup_helper", "alternate filtered collection endpoint"
    return "primary_list", "primary JSON list collection"

def deref_name(ref: str) -> str | None:
    return ref.rsplit("/", 1)[-1] if isinstance(ref, str) and ref.startswith("#/components/schemas/") else None

def evaluated_properties(schema, seen=None):
    """Static evaluated property names for the source's allOf object shapes."""
    seen = set() if seen is None else seen
    if any(key in schema for key in ("anyOf", "oneOf", "patternProperties")):
        raise ValueError("Conditional evaluated properties need a separate dialect conversion")
    names = dict(schema.get("properties", {}))
    if "$ref" in schema and schema["$ref"] not in seen:
        reference = schema["$ref"]
        seen.add(reference)
        target = SOURCE_DOCUMENT
        for part in reference.removeprefix("#/").split("/"):
            target = target[part.replace("~1", "/").replace("~0", "~")]
        names.update(evaluated_properties(target, seen))
    for branch in schema.get("allOf", []):
        names.update(evaluated_properties(branch, seen))
    return names

def nullable_to_30(node):
    """Convert OpenAPI 3.1 type arrays to valid 3.0 nullable schemas."""
    if isinstance(node, dict):
        out = {k: nullable_to_30(v) for k, v in node.items()}
        if out.get("required") == []:
            out.pop("required")  # Empty required is a no-op in 3.1, invalid in 3.0.
        if "unevaluatedProperties" in out:
            # allOf activates every branch, so declaring the union of its
            # property names preserves closure while retaining each constraint.
            if any(k in out for k in ("$ref", "allOf", "anyOf", "oneOf")):
                for name in sorted(evaluated_properties(node)):
                    out.setdefault("properties", {}).setdefault(name, nullable_to_30(evaluated_properties(node)[name]))
            out["additionalProperties"] = out.pop("unevaluatedProperties")
        typ = out.get("type")
        if typ == "null":
            out.update({"type": "object", "nullable": True, "enum": [None]})
        if isinstance(typ, list):
            nullable = "null" in typ
            branches = [t for t in typ if t != "null"]
            if len(branches) == 1:
                out["type"] = branches[0]
            elif branches:
                out.pop("type", None)
                # OpenAPI 3.0 does not allow a union-valued `type`, and
                # `nullable` on a parent oneOf is not portable across parsers.
                # Use anyOf for overlapping primitive types (integer/number).
                out["anyOf"] = [{"type": t} for t in branches]
                # OpenAPI 3.0 cannot express a nullable union directly. A
                # dedicated nullable branch avoids oneOf rejecting values
                # that match more than one branch.
                if nullable:
                    out["anyOf"].append({"type": "object", "nullable": True, "enum": [None]})
            if nullable and not branches:
                out["type"] = "object"
                out["nullable"] = True
                out["enum"] = [None]
            if nullable and len(branches) == 1:
                out["nullable"] = True
        if isinstance(out.get("examples"), list):
            examples = out.pop("examples")
            out["x-source-examples"] = examples
            if examples and "example" not in out:
                out["example"] = examples[0]
        if out.get("type") == "boolean" and "default" in out and not isinstance(out["default"], bool):
            if out["default"] is not None or not out.get("nullable"):
                # The upstream is_trusted response schema contains the literal
                # word "default", not a boolean default. Preserve the source
                # annotation without inventing an API default value.
                out["x-source-default"] = out.pop("default")
        return out
    if isinstance(node, list):
        return [nullable_to_30(x) for x in node]
    return node

def main():
    global SOURCE, OUT, MANIFEST, COLLECTIONS, SOURCE_DOCUMENT
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--coverage", type=Path, default=MANIFEST)
    parser.add_argument("--collections", type=Path, default=COLLECTIONS)
    args = parser.parse_args()
    SOURCE, OUT, MANIFEST, COLLECTIONS = args.source, args.output, args.coverage, args.collections
    src = yaml.safe_load(SOURCE.read_text())
    SOURCE_DOCUMENT = src
    routes = []
    output_paths = {}
    imported_routes = {}
    for path, item in src["paths"].items():
        for method, operation in item.items():
            if method.lower() != "get":
                continue
            kind, reason = path_kind(path, operation.get("operationId", ""))
            route = {
                "path": normalized_path(path),
                "method": "GET",
                "operationId": operation.get("operationId"),
                "summary": operation.get("summary"),
                "kind": kind,
                "reason": reason,
                "imported": (path != "/administrations{format}" and (kind in {"primary_list"} or (kind == "child_or_singleton" and "/additional_charges" in path))),
                "route_in_openapi": kind in {"primary_list", "primary_detail", "child_or_singleton"},
                "parameters": [p.get("$ref", p.get("name")) for p in operation.get("parameters", [])],
            }
            routes.append(route)
            # Import primary list/detail endpoints. Filtered and lookup routes are
            # retained in the manifest but do not create duplicate importer routes.
            if kind not in {"primary_list", "primary_detail", "child_or_singleton"}:
                continue
            op = copy.deepcopy(operation)
            op.pop("parameters", None)
            params = []
            for param in operation.get("parameters", []):
                if param.get("$ref", "").endswith("/format"):
                    continue
                p = copy.deepcopy(param)
                if "$ref" not in p:
                    p = nullable_to_30(p)
                params.append(p)
            if params:
                op["parameters"] = params
            # Preserve contact integration identity from v2-readonly.
            if path == "/{administration_id}/contacts{format}":
                op["operationId"] = "get_administration_contacts"
            elif path == "/{administration_id}/contacts/{id}{format}":
                op["operationId"] = "get_administration_contact"
            op = nullable_to_30(op)
            route_path = normalized_path(path)
            if "/contacts/{id}/additional_charges" in route_path:
                route_path = route_path.replace("/contacts/{id}/", "/contacts/{contact_id}/")
                op["parameters"] = [({**p, "name": "contact_id"} if p.get("in") == "path" and p.get("name") == "id" else p) for p in op.get("parameters", [])]
            output_paths[route_path] = {"get": op}
            imported_routes[route_path] = (op, kind)

    # Keep every component reachable from the selected operations, including
    # nested response schemas, while excluding unused write-request dialects.
    raw_components = copy.deepcopy(src["components"])
    raw_components["schemas"]["contact"] = copy.deepcopy(raw_components["schemas"].get("contact_response", {}))
    output_paths = json.loads(json.dumps(output_paths).replace("#/components/schemas/contact_response", "#/components/schemas/contact"))
    def references(node):
        if isinstance(node, dict):
            if "$ref" in node:
                yield node["$ref"]
            for child in node.values():
                yield from references(child)
        elif isinstance(node, list):
            for child in node:
                yield from references(child)
    queue = list(references(output_paths))
    components = {"securitySchemes": copy.deepcopy(raw_components.get("securitySchemes", {}))}
    seen = set()
    while queue:
        reference = queue.pop()
        if reference in seen:
            continue
        seen.add(reference)
        if not reference.startswith("#/components/"):
            raise ValueError("Unsupported component reference: " + reference)
        section, name = reference[len("#/components/"):].split("/", 1)
        name = name.replace("~1", "/").replace("~0", "~")
        value = copy.deepcopy(raw_components[section][name])
        components.setdefault(section, {})[name] = value
        queue.extend(references(value))
    components = nullable_to_30(components)
    schemas = components.get("schemas", {})
    doc = {
        "openapi": "3.0.3",
        "info": {"title": "Moneybird readable record collections", "version": src["info"]["version"], "description": "Generated from the official Moneybird OpenAPI v2 specification."},
        "servers": copy.deepcopy(src["servers"]),
        "security": copy.deepcopy(src.get("security", [{"bearerAuth": []}])),
        "paths": output_paths,
        "components": components,
    }
    OUT.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    MANIFEST.write_text(json.dumps({"source": "APIs/moneybird.com/v2/openapi.yaml", "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "source_get_count": len(routes), "imported_route_count": len(output_paths), "routes": routes}, indent=2) + "\n")
    collections = []
    for path, (operation, kind) in imported_routes.items():
        # Only array responses are importer collections; detail routes remain in
        # openapi.yaml but do not create another collection entry.
        schema = operation.get("responses", {}).get("200", {}).get("content", {}).get("application/json", {}).get("schema", {})
        if path == "/administrations.json" or kind == "primary_detail" or (kind == "child_or_singleton" and "/additional_charges" not in path):
            continue
        response_is_array = schema.get("type") == "array"
        item_schema = schema.get("items", {}) if response_is_array else schema
        ref = item_schema.get("$ref") or schema.get("$ref")
        rest = path.removeprefix("/{administration_id}/")
        resource = rest.split("/", 1)[0].replace(".json", "") or "administrations"
        if path.startswith("/administrations"):
            resource = "administrations"
        if resource == "documents":
            parts = path.split("/documents/", 1)[1].split("/", 1)[0].replace(".json", "")
            resource = parts
        if "/additional_charges" in path:
            resource = "contact_additional_charges" if "/contacts/" in path else "subscription_additional_charges"
        q = []
        dynamic = []
        pagination = {"page": False, "per_page": False, "max_per_page": 100}
        for p in operation.get("parameters", []):
            if p.get("$ref"):
                name = p["$ref"].rsplit("/", 1)[-1]
                p = src["components"].get("parameters", {}).get(name, p)
                if name in {"page", "per_page"}:
                    pagination[name] = True
            elif p.get("in") == "query":
                name = p.get("name")
                if name in {"page", "per_page"}:
                    pagination[name] = True
                elif name == "include_archived" and "contacts" in path:
                    q.append({"name": name, "value": True, "reason": "include archived contacts"})
                elif name == "active" and resource in {"assets", "products"}:
                    q.append({"name": name, "value": False, "reason": "include inactive records"})
                elif name == "filter" and resource == "projects":
                    q.append({"name": name, "value": "state:all", "reason": "include archived projects"})
                elif name == "include_billed" and "/additional_charges" in path:
                    q.append({"name": name, "value": True, "reason": "include billed and unbilled charges"})
                elif p.get("required"):
                    dynamic.append(name)
        candidate_detail = path.rsplit(".json", 1)[0] + "/{id}.json"
        collections.append({
            "name": resource,
            "path": path,
            "operationId": operation.get("operationId"),
            "schema": ("contact" if resource == "contacts" else (ref or "").rsplit("/", 1)[-1]),
            "response_path": "$",
            "item_path": "$[*]" if response_is_array else "$",
            "response_is_array": response_is_array,
            "identity_field": "id",
            "detail_path": candidate_detail if candidate_detail in output_paths else None,
            "pagination": pagination,
            "constant_query": q,
            "required_dynamic_query": dynamic,
            "notes": "child collection" if kind == "child_or_singleton" else "primary record collection",
        })
    COLLECTIONS.write_text(json.dumps({"source": "APIs/moneybird.com/v2/openapi.yaml", "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(), "collections": collections}, indent=2) + "\n")
    print(f"generated {OUT} ({len(output_paths)} routes, {len(schemas)} schemas)")
    print(f"wrote {MANIFEST} ({len(routes)} GET operations)")
    print(f"wrote {COLLECTIONS} ({len(collections)} collections)")

if __name__ == "__main__":
    main()
