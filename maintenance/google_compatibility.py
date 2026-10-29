"""Two exact reviewed Discovery -> OAS compatibility corrections.

No generic default suppression or regex weakening. A changed vendor node
requires review, including a vendor fix. Original annotations remain explicit.
"""
import copy

import google_discovery as google

PAGESPEED_PATTERN = r"(?i)(url:|origin:)?http(s)?://.*"
PORTABLE_PATTERN = r"([uU][rR][lL]:|[oO][rR][iI][gG][iI][nN]:)?[hH][tT][tT][pP]([sSſ])?://[^\n]*"
ORG_UNIT_PARAMETERS = {
    "reports.activities.list": {
        "default": "", "description": "ID of the organizational unit to report on. Activity records will be shown only for users who belong to the specified organizational unit. Data before Dec 17, 2018 doesn't appear in the filtered results.",
        "location": "query", "pattern": "(id:[a-z0-9]+)", "type": "string",
    },
    "reports.activities.watch": {
        "default": "", "deprecated": True,
        "description": "`Deprecated`. This field is deprecated and is no longer supported. ID of the organizational unit to report on. Activity records will be shown only for users who belong to the specified organizational unit. Data before Dec 17, 2018 doesn't appear in the filtered results.",
        "location": "query", "pattern": "(id:[a-z0-9]+)", "type": "string",
    },
    "reports.userUsageReport.get": {
        "default": "", "description": "ID of the organizational unit to report on. User activity will be shown only for users who belong to the specified organizational unit. Data before Dec 17, 2018 doesn't appear in the filtered results.",
        "location": "query", "pattern": "(id:[a-z0-9]+)", "type": "string",
    },
}
PAGESPEED_PARAMETER = {"description": "Required. The URL to fetch and analyze", "location": "query",
                       "pattern": PAGESPEED_PATTERN, "required": True, "type": "string"}


def prepare(source):
    prepared = copy.deepcopy(source)
    key = (source["name"], source["version"])
    notes = []
    operations = {method["id"]: method for method, _ in google.methods(prepared)}
    if key == ("admin", "reports_v1"):
        actual = {name: method.get("parameters", {}).get("orgUnitID") for name, method in operations.items()
                  if "orgUnitID" in method.get("parameters", {})}
        if actual != ORG_UNIT_PARAMETERS:
            raise ValueError("Review changed Admin Reports orgUnitID nodes before replaying compatibility correction")
        for name in ORG_UNIT_PARAMETERS:
            parameter = operations[name]["parameters"]["orgUnitID"]
            parameter["x-google-discovery-default"] = parameter.pop("default")
        notes.append("Three optional orgUnitID query parameters declare an empty-string default that violates their own unchanged (id:[a-z0-9]+) pattern. Preserved that annotation as x-google-discovery-default; chose no replacement or runtime default. All value constraints, requiredness, descriptions and deprecation remain unchanged.")
    if key == ("pagespeedonline", "v5"):
        method = operations.get("pagespeedonline.pagespeedapi.runpagespeed", {})
        parameter = method.get("parameters", {}).get("url")
        if parameter != PAGESPEED_PARAMETER:
            raise ValueError("Review changed PageSpeed URL parameter before replaying regex compatibility correction")
        parameter["pattern"] = PORTABLE_PATTERN
        parameter["x-google-re2-pattern"] = PAGESPEED_PATTERN
        notes.append("Converted the exact PageSpeed URL RE2 (?i) pattern to an equivalent ECMA-262 pattern with explicit case-fold classes, including U+017F long s, and a non-LF dot class. Preserved the original as x-google-re2-pattern. Native RE2, ECMA-262 and Unicode case-fold witnesses are checked; no constraint was removed.")
    return prepared, notes
