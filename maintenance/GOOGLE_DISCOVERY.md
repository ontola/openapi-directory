# Google Discovery refresh

The 2026-10-29 request explicitly authorizes refreshing the Google family.
It supersedes the historical Google-regeneration exclusion in AGENTS.md.
Other parked work and vendor-content protections remain unchanged.

`google_discovery.py` converts Google Discovery v1 directly to OpenAPI 3.0.3.
It avoids the old Discovery → Swagger converter's silent method collisions
and loss of parameter patterns/formats. Google's concrete `flatPath` routes
disambiguate methods sharing `/{+name}`. The original resource-name template,
full parameter patterns, component bindings and singleton constants remain
in each operation's `x-google-discovery` metadata. Clients needing whole
resource names can reconstruct them from that metadata.

Schema/property identities, request/response references, recursive schemas,
query formats/patterns, exact integer bounds, defaults, repeated parameters,
OAuth scopes and method descriptions survive conversion. Reference siblings
use `allOf`; implicit and authorization-code flows are alternatives. Their
endpoints follow [Google's OAuth documentation](https://developers.google.com/identity/protocols/oauth2/web-server).
The independent checker compares every native schema field and query
parameter as well as all method IDs, HTTP verbs, body references, scopes,
path variables and local references. Ordinary full OpenAPI validation is a
separate check. Typed YAML comparison distinguishes booleans, integers and
floats, including integers beyond JavaScript's safe range.

Discovery does not specify response status codes, so successful responses
use the OpenAPI `2XX` range. JSON bodies and binary downloads are represented
directly. Media-upload protocols, streaming/subscription details, regional/
mTLS metadata, enum descriptions/deprecation and method-specific required
annotations remain explicit `x-google-*` metadata. These extensions retain
the source information; this converter does not implement those protocols
or turn per-method required annotations into global schema constraints.
Non-REST or irreconcilably colliding descriptions fail rather than dropping
operations. Unrepresentable or invalid constraints fail full validation.

## Reviewed compatibility corrections

`google_compatibility.py` has two exact-node recipes. A vendor fix or other
change to an asserted node requires review before replay:

- Admin Reports `reports_v1`: three optional `orgUnitID` parameters declare
  an empty-string default that violates their own unchanged pattern. Preserve
  that impossible annotation as `x-google-discovery-default`; do not invent
  a replacement/default value. Type, pattern, requiredness, descriptions and
  deprecation are unchanged. All allowed/rejected value constraints remain.
- PageSpeed v5: translate the exact RE2 `(?i)` URL pattern into an equivalent
  ECMA-262 expression. Preserve Unicode simple folding (including U+017F
  long s) and RE2's non-LF dot semantics. Retain the original expression in
  `x-google-re2-pattern`. Tests use the actual RE2 and ECMA engines, positive
  and negative witnesses, and exhaust all Unicode scalar characters for the
  pattern's literal case-fold classes. This does not weaken/remove a pattern.

See [RE2 syntax](https://github.com/google/re2/wiki/Syntax) and the
[Reports parameter reference](https://developers.google.com/workspace/admin/reports/reference/rest/v1/activities/list).

## Review or import a pinned source snapshot

Use Python with `maintenance/requirements.txt` installed. Clone the official
mirror, fetch and review a full commit, and check out that exact revision:

```sh
git clone https://github.com/googleapis/discovery-artifact-manager.git /tmp/google-discovery
git -C /tmp/google-discovery checkout FULL_REVIEWED_COMMIT_SHA
python maintenance/google_refresh.py \
  --source-checkout /tmp/google-discovery \
  --source-revision FULL_REVIEWED_COMMIT_SHA
```

Default execution only reviews and caches candidates. It verifies the
official origin, clean source files and exact source commit, then checks
each source's raw bytes against its pinned Git blob. Reports include the
original SHA-256, Discovery revision, actual baseline, paths, methods,
schemas, reference counts, explicit removals, compatibility corrections and
candidate hashes. All dates/revisions describe the observed snapshot, not
an assertion that runtime endpoints or account permissions were tested.

Add `--only SERVICE` (repeatable) for a bounded pilot; `--workers` accepts
1–8 processes. Add `--report FILE` to select the JSON report destination.
After reviewing candidates and removals, repeat with `--write` to import
validated files locally. A working-tree edit or changed candidate/source
hash stops replacement; no credentials, Git writes or network calls occur.
Committing, PR creation, CI review and merging remain separate operations.

Existing APIs.guru info/contact curation, externalDocs and tags survive.
New descriptions get no invented curation. New vendor versions have their
own directories. Missing historical sources remain unchanged and are listed
as `source_unavailable`; missing indexed artifacts are reported separately.
Neither absence proves that an API is retired. A newer stored live Discovery
revision is retained when the mirror lags it (the separate Keep refresh is
one such case). No timestamp-only rewrite is needed for identical content.

Increase the conversion-profile version when changing published conversion
behavior. Source provenance lives in each artifact's `info.x-origin` and
`info.x-conversion`; it does not depend on this guide or YAML comments.

## Exact-head CI

The read-only `Google API validation` workflow executes tooling from the
PR's trusted base. It reads changed Google files from the exact head,
fetches their immutable official source URLs, verifies source hashes and
reconstructs each generated description with the base's curation. Every
field must match, with full OAS/native/schema/reference/typed checks. Reports
label older manually authored artifacts as `legacy-oas-only`; generated
artifacts are `native-projection`. The PR gate requires the actual workflow
job to succeed for Google API changes, including manual batch branches.
The full machine report is uploaded; no write permission or publication
step is added. An infrastructure PR with no API changes checks zero API
artifacts explicitly rather than claiming a generated-head validation.
