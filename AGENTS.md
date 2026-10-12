# AGENTS.md — working on this OpenAPI directory fork

Instructions for an agent picking up work in this repo. Read this first.

**Repo**: `ontola/openapi-directory` (fork of `APIs-guru/openapi-directory`).
Note the git remote resolves via an old org rename — `localthought/openapi-directory` redirects to `ontola`. Pushes print a "This repository moved" notice; harmless.

**Handover to Claude — 2026-10-08:** The user asked to "wrap up your work and
leave a handover in the repo" because they are moving the work to Claude. Codex
maintenance is stopped after completing #234 and this handover. The existing local
hourly automation `maintain-openapi-directory-for-one-week` was PAUSED through
`automation_update`, with saved status verified; schedule/prompt/history preserved,
no new automation created. Do not resume it based on older heartbeat instructions.
Start with [HANDOVER.md](HANDOVER.md) for current delivery, remaining work, protections,
local evidence and restart commands. This supersedes ongoing Codex execution notes
below; standing repository conventions and parked-item/owner-choice protections remain.

**Claude maintenance on the claude-build VPS — 2026-10-08:** Claude (Opus 5.5) took over
at Michiel's request. Fresh blobless sparse checkout `~/work/openapi-directory-maint`,
Python 3.12 venv `~/work/.venv-openapi-maint` (pip-less venv + user pip) and `npm ci`.
The laptop-only caches (`cache/maintenance/drafts/`, `reports/...`, `discovery/...`) are
**not** on the VPS: the pending/refresh tools correctly hold any pre-existing generated
draft there. No receipts were recreated. New generated drafts created on the VPS keep
their own original cache root under `cache/maintenance/claude-drafts/`. Codex's paused
automation was not resumed; no scheduled publication or auto-merge was added.

Baseline at main `528504bfe813` (after another session's GitLab v4 read-only subset #236,
which is not maintenance work): **206 tests pass** locally (38.4 s). Full fresh read-only
audit of all **65 artifacts** (11:40–11:46 UTC): **42 matches_source, 13 valid unblocked
content drifts, 11 recorded blocks, zero fetch/prepare failures**. Drifts: DigitalOcean
(+4 ops), Figma (new vendor 0.44.0), Atlas, Sentry (+1 path/op), Intercom, Datadog v2
(+3/+3), Discord, Grafana, Twilio REST, Twilio Verify, Asana, Zendesk Support (+4/+4),
Coinbase CDP; no endpoint removals in any of them. The eleven blocks are unchanged in
kind; Meraki's source is now 1.75.0 (733 paths / 1,035 ops, still 2 native errors), Okta
2026.09.2 and Cloudflare 2,299 / 3,663, all still blocked. Inventory recomputed:
**733 domains / 4,298 files / 2,121 openapi.yaml / 2,168 swagger.yaml** (+4 files from
#236). Report: VPS `cache/maintenance/reports/claude-baseline-2026-10-08/`.

Registered nine new sources in a separate infrastructure PR: the eight remaining Xero
services the official README lists as In Release (five stale 2.9.4 refreshes, plus
Projects, Payroll UK, Payroll NZ), and YNAB's hosted 1.87.0 description (documented
`/budgets` → `/plans` rename per vendor changelog v1.79.0). All nine validate natively
with no patches. Monitoring becomes **74 artifacts**. API files follow one PR per service.

**Recorded blocks re-validated — 2026-10-08 19:01 UTC (Claude, VPS):** all eleven were
fetched fresh and validated against main. **None is clean; no import made, no vendor
content patched beyond existing recipes.** Current observations supersede older counts:
Cohere still `TruncationStrategy.oneOf: []` (source unchanged at `734aafbe`); Square still
invalid `info.externalDocs` plus undefined schemas; Slack Web archived/unsupported Swagger;
**Meraki now 1.75.0 / 733 paths / 1,035 ops (`c88b7cf5`): the undefined `oauth2` scheme is
in 849 requirements and a new defect appeared, a string `maximum` on
`GET /devices/{serial}/appliance/performance` parameter 3**; Vercel 324 paths / 447 ops,
still unsupported `patternProperties`/3.0 keywords; Mailchimp Marketing still boolean
defaults on string notification fields; Auth0 still the Guardian device-name default vs
pattern; Cloudflare 2,300 / 3,664 (`76115f48`), same DNS-order default and undefined
`assets_jwt`/`pages_upload_token`; **Okta now 2026.09.2 (`d788e33f`), same hook-keys
inline path parameter missing `required`**; Twilio Messaging and Zendesk Conversations
validate but stay held on push protection (Q-102). Report:
VPS `cache/maintenance/reports/claude-blocks-1008T1901/`.

**Ongoing authorization — 2026-10-06:** The user explicitly said "you can continue
past friday, no problem". The original 2026-10-09 deadline is superseded: continue
local maintenance until the user asks to stop or pause. The existing hourly heartbeat
was updated through automation_update, its end date removed, and its saved active
schedule/prompt verified. No additional automation was created. Preserve laptop-sleep
behavior, no power changes/cloud-host move, quiet notifications, all parked work and
publication/merge protections. Older one-week/deadline notes below are historical.

**Explicit pending draft head updater delivered — 2026-10-08:** Separate
infrastructure [#234](https://github.com/ontola/openapi-directory/pull/234) merged as
`b4c28a81c3fe14b67b8c9c3764b09ae28b2f2ad9` from actual head `648db85cef1bea5d4b3888b0973ac5e4ab483d9e`,
advertised base `f4283c35b670a1712b38c9eb53c647822ed41464`. **206 tests pass locally
(204.911 seconds) and in actual hosted CI**, including 18 new real-Git updater cases
(run `37768566573`, tests job `113282140755`, actual unittest step executed).
Exact seven infrastructure files/head/base/CLEAN/MERGEABLE were verified before
matching-head merge; REST confirms the result. APIs and source configuration remain
byte-identical, and all workflow permissions remain read-only. The generated-API job
correctly skipped this infrastructure branch; actual updated-production-head CI and
its new Actions summary are not claimed by this infrastructure delivery.

`maintenance/refresh_pr.py` defaults to fresh read-only review. Explicit `--publish`
updates only an untouched owned generated draft with successful retained evidence,
same original/current/advertised base, fixed vendor version, no endpoint/schema-name
removals or server/auth/callback changes, intact complete native/typed-YAML/recipe/Git
checks and no review work. Exact previous-head Git lease preserves concurrent commits;
private index preserves checkout/staging. It keeps original PR title/body and records
an immutable bounded history back to successful creation, validating predecessor full
Git trees/messages/native/manifest content. New protocol 2 labels descriptions initial
submission snapshots; current provenance/counts/deltas appear in exact-head CI JSON
and summary. Legacy bodies and any main advance are held. No REST writes, ready,
comment, close or merge command, new automation or scheduled publisher was added.

Rejected/uncertain push outcomes retain guards. If success/failure receipts cannot be
saved, the interrupted lock remains. Human PR metadata can race with the Git push;
post-push state changes are held and human edits preserved, never blindly restored.
Source snapshots, successful candidate/receipt history, required Git objects and all
failure/interruption evidence must remain available; missing objects are held rather
than reconstructed or silently treated as permission. Real-Git regression cases prove
successful one- and two-update history, companion all-or-nothing checks, concurrent
commits, human changes and evidence-write failures. **No production API draft was
updated or manufactured**: only unrelated #179 was open during the selected checks.

Default-mode live checks on the committed infrastructure head fetched three selected
artifacts at **11:08 UTC**; all report `no_pending_pr` / `matches_source` against API
bytes unchanged from actual main `f4283c35b670`. GitHub companions share pinned source
`2eba8c3ba02f022011539cf01efc43e0251502f8`, native 3.0.3 / vendor 1.1.4 / 816 paths /
1,232 operations each; HF Endpoints native 3.1.0 / 2.0.0 / 40 / 46 remains hosted-health
not_assessed. Original raw/health hashes, complete independent vendor-plus-curation
projection, native/stored validation, typed YAML and all **20,872 OpenAPI reference
objects** pass. A separate broad literal-string scan also resolved examples containing
`$ref`; those example strings are not counted as OpenAPI Reference Objects. No
conversion, repair, invented revision or timestamp-only API write. These are three
selected observations, not a full 65-artifact or post-merge network audit.

Evidence, original live snapshots and independent verifiers, local and actual CI logs,
PR states and merged receipts remain under ignored
`cache/maintenance/reports/guarded-pending-draft-updates/`. Required #234 attachment
attempt failed at the existing 100 cap; preserve its GitHub link without claiming app
linkage or removing history. Monitoring remains **65 artifacts / 64 services** and
full fetched-tree inventory **733 providers / 4,294 API files / 2,120 openapi.yaml /
2,168 swagger.yaml**. Preserve all eleven blocks, unanswered owner choices, §5 parked
items, deprecated Grant exclusion, original creation cache and the other session's #179.
Continue deliberate merged-branch handling and scheduled publication separately, and
extend official-source freshness/discovery. Keep local ongoing authorization and
laptop-sleep behavior; no execution-host or power change.

**Resumed — 2026-10-08:** The user explicitly said "resume" after the 2026-10-06
pause. The existing hourly local maintenance automation is ACTIVE again, with the
ongoing prompt and quiet notifications preserved; no new automation was created.
Fetched main remains `b511912dbb26ef97747a9f3331e1313f030db584` (#229). Only
unrelated #179 is open. Saved uncommitted pending-review work was preserved and
continued on `codex/pending-api-refresh-review`; no completed HCP addition is repeated.

**Pending-draft review infrastructure delivered — 2026-10-08:** New
`maintenance/pending_pr.py` is read-only. It requires retained successful creation
evidence, an intact full generated Git tree/message/single parent, complete native
and typed-YAML validation, exact target-only manifest edits, original title/body,
unchanged source recipe, and no discussion/review requests/submitted reviews. Fresh
vendor content is compared against the verified pending artifact, including explicit
companions; timestamp-only changes do not count. Main service/manifest changes,
missing objects, pagination/snapshot changes, manual work and prior publication
failure/interruption guards are held. Separate fresh/original cache roots prevent
overwriting creation receipts. All results explicitly deny publication authorization.

This does not update/rebase/close/comment/ready/merge PRs or enable a scheduled writer.
Automatic pending updates and scheduled publication remain subsequent separate work.
Separate infrastructure [#231](https://github.com/ontola/openapi-directory/pull/231)
merged as `3a799dee7d0d158fb53ad769a7c55dab54245e7d` from exact head
`e57b9ff59730c91ca9b5c156627c4c482f635311`. **188 tests pass locally and in actual
hosted CI**, including 23 new real-Git pending-review cases (local suite 174.794 seconds;
actual CI run `37760060636`, tests job `113254014549`, unittest step executed).
Exact five infrastructure files/head/advertised base/CLEAN/MERGEABLE were verified
before matching-head merge; REST confirmed the result. No API, source-manifest or
workflow permissions changed. Required attachment attempt failed at the existing 100 cap.
Evidence is retained under ignored
`cache/maintenance/reports/pending-api-refresh-review/`. All eleven source/native/
publication blocks, unanswered owner choices, §5 parked items and deprecated Grant
exclusion remain; preserve laptop sleep and the other session's #179.

**GitHub fixed-version content refresh delivered — 2026-10-08:** The default and
2022-11-28 public REST companion specs are refreshed together in API-only
[#232](https://github.com/ontola/openapi-directory/pull/232). Actual generated head
`b3ec9d312975b3723ffae6f8d18226d73b763870`, single parent/base
`3a799dee7d0d158fb53ad769a7c55dab54245e7d`; actual generated-head validation run
`37761289776`, validate job `113258045044`, exact-head/API-scope step executed successfully.
Ready state, exact head/base/two API files and CLEAN/MERGEABLE were rechecked before
matching-head merge; REST confirms merge `3f6cbeebce0b3281a7779a9368e3d710cb46ea38`.

Both remain native **3.0.3 / vendor 1.1.4 / 816 paths / 1,232 operations**.
Unchanged version/counts concealed five complete changed nodes in each source:
three descriptions (requester-based rate limits and coverage timing), add existing
code-quality/code-coverage schemas as detailed-rule alternatives preserving all older
entries/order, and add optional nullable proof-of-presence/verifier data. No endpoint,
authentication or server removals, version invention, conversion, repair or runtime
lifecycle inference. Official source revision is shared/pinned
`2eba8c3ba02f022011539cf01efc43e0251502f8`; original entry SHA-256 values are
`ba5ddc1eeeede9f3858abd96325359891f38a2bd8e20fd111abf4230741db194` and
`0d2fa885d4a15f57a6fe06811cbd13e7e0f580d292530199db1a59cfc2b7d14e` respectively.
Public/unarchived/undisabled source health, whole vendor/curation/provenance equality,
complete native validation, typed YAML and all **20,618 local refs** pass. Fresh
publication fetch dates remain **10:02–10:03 UTC**; no timestamp-only commit.

The delivered reviewer was then exercised on this **actual still-draft #232**, using
the original successful creation receipt in `cache/maintenance/drafts/`. Fresh vendor
fetches at **10:07–10:08 UTC** produced `pending_matches_source` for both companions
after full retained Git/receipt/recipe/body/file/native checks. It performed no Git/PR
mutation and explicitly reported `publication_authorized:false`. Only afterwards was
the PR marked ready and merged under the standing human authorization and independent
actual CI/content review. This is a real pending-draft observation, not a synthetic
GitHub test PR or an implemented update/scheduled writer. Keep successful receipts and
all publication guards; the merged generated branch remains, and future branch reuse
must be deliberately designed rather than deleting it to force another publication.

The earlier selected **three-artifact** check also found HF Endpoints matches native
3.1.0 / 2.0.0 / 40 paths / 46 ops; hosted health remains not_assessed, no Git revision
invented. Original snapshots, full five-node diffs, independent native/import/Git/ref
checks, live pending-review result, actual CI logs/states and merged receipts remain
under ignored `cache/maintenance/reports/pending-api-refresh-review/`; actual generated
creation evidence is in `cache/maintenance/drafts/`. Required #231/#232 app attachment
attempts failed with `thread attachment identity count exceeds 100`; retain their actual
GitHub links without claiming app linkage or removing history.

Main advanced during this run through **another session's #230**, Airtable read-only
Web API, merge `e3b52673e85c2b1a10decb87de1b1445ed02a21d`. Verified its sole API file
and preserved its exact bytes; do not duplicate it or claim it as this run's delivery.
Post-merge Git/content checks verify only the two GitHub files changed since #231,
source recipes stayed unchanged, and all generated bytes/Airtable remain intact.
These are original checked snapshots and post-merge Git checks, **not a new post-merge
network audit or a full 65-artifact freshness audit**. Monitoring remains **65 artifacts /
64 services**. Only unrelated #179 remains open. Continue safe pending updates, deliberate
merged-branch handling and scheduled publication as separate infrastructure; extend
official-source audits/discovery while preserving all eleven blocks, unanswered owner
choices, §5 parked items, deprecated Grant exclusion and local sleep behavior.

**Last updated**: 2026-10-08 (Europe/Amsterdam). Inventory of fetched `origin/main` at `3f6cbeebce0b` (PR #232 merged):
733 provider domains; 4,294 files under `APIs/`, including 2,120
`openapi.yaml` and 2,168 `swagger.yaml` files. These are dated observations,
not live counts. Recompute against fetched `origin/main` when resuming work.


**Four HCP service sources reviewed — 2026-10-06:** Separate infrastructure branch
`codex/hcp-platform-service-sources` registers the four actual references linked by the
[official overview](https://developer.hashicorp.com/hcp/docs/hcp/api): HVN, Operations,
RBAC Resource Manager (`/hcp/api-docs/rbac`) and Webhook. Original public HTML contains
vendor Swagger strings, not reconstructed SDK types/rendered operations; no private
hcp-specs is accessed or Git revision invented. Page and current/latest release are
stable; exact service titles, versions and base paths are guarded individually.
Full fetched Git tree has only the already delivered HCP Identity; all five method/path
sets are disjoint. **165 local updater tests pass**; registration is not API delivery. Verify actual
hosted CI/PR state next.

Native / converted 2.0 -> 3.0.0 with locked swagger2openapi 7.0.8:
HVN **2020-09-07 / 24 paths / 31 ops / 82 schemas / 173 converted local refs**;
Operations **2020-05-05 / 3 / 3 / 12 / 18**;
Resource Manager **1.0 / 27 / 35 / 89 / 153** (keep 1.0 despite dated routes);
Webhook **2023-05-31 / 4 / 7 / 26 / 40**. Every native description and full converted
import validate; all refs, complete independent original schema/operation/parameter/
body/response projection, auth/server fields and typed vendor-plus-provenance equality
pass. Full source descriptions retained, including operations not shown in abbreviated
rendered navigation. No invented curation. Preserve native Authorization bearer apiKey
and protocol-relative server; Swagger omits schemes. Explicit refSiblings:allOf retains
all 82 / 10 / 60 / 17 annotated schema refs respectively, without dropping their prose.

First three convert with zero warnings/patches. Webhook's one increment was traced to
converter line 59 nullable translation of the original optional boolean
`CreateWebhookRequestBody.enabled`. Exact full-schema/location guard and a second
conversion removing only that extension must produce zero warnings/patches and the
same complete output except that nullable flag. True requires successful verification,
false disables without verification, unset enables only on success; no null semantics
removed or unrelated repair accepted. Original HTML/native/conversion/control bytes,
real dates, trace, preflight imports and independent checks are under ignored
`cache/maintenance/discovery/hashicorp-hcp/other-services/`; hosted source health remains
not_assessed. Monitoring becomes **65 artifacts / 64 services**, not a full 65-source
audit or whole-HCP/platform coverage claim. Deliver infrastructure separately, then one
actual generated API-only PR per service with actual CI before ready/merge. Keep all
11 prior blocks, owner choices, parked items, deprecated Grant exclusion, independent
#179 and original local one-week deadline/laptop-sleep behavior unchanged.


**Four HCP services delivered — 2026-10-06:** Separate source infrastructure
[#224](https://github.com/ontola/openapi-directory/pull/224) merged as
`4f69481eb35d38058afe121adf84d0ac62274371` from actual head
`86e94290e2f436cd4ef20c03b3559c7ff556040e`; **165 tests passed locally and in actual hosted CI**
(run `37478604741`, tests job `112320533311`, actual test step executed).
No API files changed in that infrastructure PR. The create-only generator then
published four separate API-only drafts, each a single-parent commit based on that
infrastructure merge. Actual generated-head validation and independent original
HTML/native/conversion/control/vendor/import/typed-YAML/ref checks passed individually:

- **operations [#225](https://github.com/ontola/openapi-directory/pull/225)**: actual head `1f23f573b8d1097806821a1f15ed6e324e799296`;
  actual CI run `37479322723`, validate job `112322998499`;
  confirmed merge `eb8b8db3781b2f77f58e822225cda4ad894684d1`.
- **hvn [#226](https://github.com/ontola/openapi-directory/pull/226)**: actual head `00cd3d5ccc0a22a6bc41634b280f53b7e25da966`;
  actual CI run `37479294718`, validate job `112322900542`;
  confirmed merge `80e2f0a3444b8b149dde4c324ce37ab42ba7817e`.
- **rbac [#227](https://github.com/ontola/openapi-directory/pull/227)**: actual head `3eda43c31c0e8aed91f4695396409d84b0a5bf15`;
  actual CI run `37479496785`, validate job `112323597747`;
  confirmed merge `45471e89a15b66bcb2f4c8719341758a55957ad9`.
- **webhook [#228](https://github.com/ontola/openapi-directory/pull/228)**: actual head `e2795ea4454d452a645e9208d52f93501444b077`;
  actual CI run `37479549454`, validate job `112323765828`;
  confirmed merge `2704d663d3594fd00c31cbf6802832ae93028653`.

Each draft was marked ready after actual CI success, then exact ready head, advertised
base, API-only file list and CLEAN/MERGEABLE state were checked before matching-head
merge. Subsequent main changes were independently verified to be only the disjoint
already merged HCP additions, preserving their exact generated bytes and unchanged
source recipes. REST confirmed every merge; generator left local checkout/index intact.
No publication rejection, retry, source repair waiver or automatic merge policy.
Required #224–#228 attachment attempts failed at the existing 100 cap; retain actual
GitHub links without claiming app linkage or deleting history to make room.

Fresh selected **four-source** network audit against actual main `2704d663d359` reports
**four matches_source / zero validation errors**. Original HTML/native/conversion/control
hashes, full stored/native validation, all **384 converted local refs**, typed roundtrip,
complete vendor equality and JSON/Markdown parity pass again. Only these four new API
files changed since prior main `2bb9cdeaff645`; full fetched Git-tree inventory above was
recomputed. These four add **58 paths / 76 operations**; all five descriptions linked by
the reviewed HCP overview (including Identity) total **115 / 156**. This is those five
separate services, not whole-platform/product coverage. Monitoring is **65 artifacts /
64 services**, with 22 configured hosted artifacts; only four hosted observations were
refreshed here and remain not_assessed for repository health. This is not a full
65-artifact freshness audit. No Git revision is invented for embedded publications.

Original pages/strings/recipes, Webhook nullable trace/control, preflight imports,
generated candidates/results, actual CI logs/jobs/states, ready/premerge/merged receipts,
selected reports and independent verification scripts remain under ignored
`cache/maintenance/discovery/hashicorp-hcp/other-services/`. Do not duplicate completed
#224–#228 or the prior Identity #221/#222. Only unrelated #179 remains open.

**Continue next:** safe pending-PR updates and scheduled publication remain authorized
separate infrastructure work, neither enabled yet. Extend official-source freshness
reviews and bounded major-vendor discovery; preserve reviewed native semantics and
per-service scope, including services found via original embedded publications rather
than SDK reconstruction. All eleven source/native/publication blocks, unanswered owner
choices, §5 parked items and deprecated Grant exclusion remain. The user's extension
above supersedes the original one-week deadline; retain local laptop-sleep behavior.

---

**HCP Identity delivered — 2026-10-06:** Separate extraction/conversion registration
[#221](https://github.com/ontola/openapi-directory/pull/221) merged as
`3f273fbdce5896da25132942c65e770507be5bac` from actual head
`a51812b1cf969edd98c1153c20378819b0d8cd45`. **165 tests passed locally and in actual hosted CI**
(run `37470826309`, tests job `112293536667`, all test steps executed).
The generator then created separate API-only
[#222](https://github.com/ontola/openapi-directory/pull/222), actual head
`ab93ee0ec00ec650de2feb2dcefa9aa1bf2b0583`, based on the delivered infrastructure merge.
Actual generated-draft validation run `37471227660`, job `112294949493`, passed that
exact commit. Independent original HTML/native/conversion/control hashes, full reviewed
native schema/operation projection, complete vendor-plus-provenance equality, typed YAML,
all 253 local refs and full validation pass. Six nullable translations and all 53 vendor
reference annotations remain; no vendor prose, constraints or auth field is removed.
Draft was marked ready only after actual CI success; exact head/base/files/CLEAN/MERGEABLE
were checked before matching-head merge. REST confirmed API merge
`f3d66a9eff358441ef3dd86954daaf0a9c96ac92`. Generator left local checkout/index unchanged.
Do not duplicate either completed PR. The source-review notes below remain evidence.

Fresh selected post-delivery network audit against that actual merged main reports
**one matches_source / zero errors**. Original source dates remain real; source HTML/native/
conversion/control hashes, stored equality, full validation, typed YAML and JSON/Markdown
parity pass again. This is **not a full 61-artifact audit or a whole-directory freshness
claim**. Only the new HCP API file changed since main `8f68c71c2e8d`; full Git-tree inventory
above was recomputed. Monitoring is **61 artifacts / 60 services**. Configuration contains
18 hosted artifacts that need separate health assessment; only HCP's hosted observation
was refreshed here, and it remains not_assessed by repository checks. No Git revision is
claimed for this embedded public publication. All eleven blocks and owner choices remain.

An initial local merge-receipt assertion expected the wrong CI log formatting, delaying
infrastructure merge. Before publication, the generator rejected the old main's missing
new module at its input guard. This was **planning refusal before any push/PR mutation**,
not push protection, unknown publication or approval rejection. Corrected the receipt
check, verified actual 165-test CI, merged infrastructure and built the real new-base
draft successfully. Original planning-failure evidence is retained as
`prior-unmerged-base-plan-rejection.json`; latest candidate/result and merged receipts
supersede it. No publication rejection/guard was bypassed or automatically retried.
Required #221/#222 attachment attempts failed with the existing 100-cap error; retain
GitHub links, without claiming app linkage or removing history to make room.

Original publication/decoded document, conversion/control inputs/results/logs, preflight
and actual generated/import checks, source reports, actual CI logs/states and merged
receipts/verifiers remain under ignored
`cache/maintenance/discovery/hashicorp-hcp/identity-delivery/`. Next: review other services
linked by the official HCP overview (HVN, Operations, RBAC Resource Manager, Webhook) for
public original artifacts, lifecycle/scope and native validity individually; do not assume
this IAM artifact covers them, import private hcp-specs, reconstruct SDK types or register
guessed URLs. Safe pending-PR updates and scheduled publication remain separate authorized
infrastructure work. Preserve parked items, Grant exclusion and the original local
one-week deadline/laptop-sleep behavior. Only unrelated #179 remains open.

---

**HCP Identity source/recipe reviewed — 2026-10-06:** The source/recipe
review is retained from `codex/hcp-identity-source-extraction`; infrastructure/API
#221/#222 and actual CI are now complete as recorded above. **165 local tests pass**. The official reference
publishes its original Swagger string at the previously recorded pointer. Fresh original
HTML hash `d8d60b5046b3e2ba762c08d0868f55a8d54b250f445e1ff998d4f42b0f3f9148`; exact decoded native hash remains
`b64b033f744447aab8bbcb26964e23a4c4ec35e03fd52ee2cfd3b5ccdf53dc35`. Native **2.0 / vendor 1.0 /
57 paths / 80 ops / 113 schemas / 248 refs** becomes **3.0.0 / same version/counts /
253 local refs**, none external (the converter factors repeated request bodies).
Do not invent a version from dated route segments or replace native bearer apiKey auth
with an inferred OAuth scheme. Swagger omits `schemes`; the protocol-relative converted
server `//api.cloud.hashicorp.com` is preserved. No existing HCP/HashiCorp provider or
service was found in the full fetched Git tree; no curation is borrowed.

All eight diagnostic counter increments were traced to nullable handling in locked
swagger2openapi 7.0.8: six exact original `x-nullable:true` schemas, with two inline
workload-provider timestamps visited twice. They are **nullable translations, not eight
invented schema repairs**. The source recipe guards full original schemas and converted
locations. A second conversion removes only those six extensions: it must produce zero
warnings/patches and exactly the same complete output except those six nullable flags.
Unexpected same-count repairs cannot pass by merely accepting eight. Original native,
input/output/control bytes/logs/hashes are retained; null semantics are unchanged.

Full vendor projection also found the converter default discards **53 descriptions/titles
on 52 schema refs**. Explicit vendor-tool `refSiblings:allOf` preserves all of them as
schema composition, with zero additional patches. Independent comparisons now verify
every original schema, operation attribute, query/path parameter, request body, response,
auth/server value and resolved reference, plus native validation and typed YAML import
roundtrip. No prose, constraints or auth fields are removed. The extractor executes no
HTML/vendor code, retains exact HTML and JSON-string bytes, requires a single complete
application/json script, rejects duplicate script attributes/JSON keys, and checks exact
page identity, stable page/current-release lifecycle and `2019-12-10` service version.
Generated-draft guards now include the extraction module and `.cjs` converter input.

The public page's versionAlert names `hashicorp/hcp-specs` and a concrete source path;
a public repository metadata request returned 404. This does not prove deletion or
make a private source public. Use the actual hosted original publication, preserve real
fetch dates and `not_assessed` repository health; do not claim a Git revision or all-HCP
GA coverage. Native IAM/principal/SCIM/permission/workload identity content is complete;
other HashiCorp products need separate reviews. Target is
`APIs/hashicorp.com/hcp-identity/1.0/openapi.yaml`; delivered registry **61 artifacts /
60 services**, not a whole-directory freshness claim. Evidence and independent verifier
remain under ignored `cache/maintenance/discovery/hashicorp-hcp/identity-delivery/`;
prior original discovery/trace remains in `hashicorp-hcp/public-docs/`. All eleven blocks,
unanswered publication choices, parked items and the local one-week deadline are unchanged.

---

**Compute Pool delivered — 2026-10-06 12:27 UTC:** Separate source registration
[#218](https://github.com/ontola/openapi-directory/pull/218) merged as
`3a019a1d1e317145857d55001017799c7f0c5466` from actual full head
`3961d38b53130538eefa2777628f18937ee2603a`; **151 local and hosted tests pass**
(run `37462713260`, tests job `112266006314`, actual test steps executed).
The create-only generator then published separate API-only
[#219](https://github.com/ontola/openapi-directory/pull/219), actual generated head
`103927f96dded4a64b330d1a7fe585aee9335b26`, base `3a019a1d1e317145857d55001017799c7f0c5466`.
Its real **Generated API draft validation** run `37463240868`, job `112267777732`,
passed against that exact head, using trusted base tools. This is the first actual API
use of the delivered validation workflow, beyond its regression tests. Native validation,
typed YAML roundtrip, single-parent/full Git-tree/API-only scope, all 216 local refs,
original entry/helper/bundle/health hashes and complete vendor-plus-provenance comparison
also pass independently. The generator left the checkout/index unchanged. Draft was
marked ready only after CI success; exact head/files/CLEAN/MERGEABLE were rechecked before
matching-head merge. REST confirmed API merge `960c763bab32285a05a0d61effa3629796cc0f21`.
No automatic merge policy, source repair, invented curation or constraint waiver was added.

Fresh selected post-delivery network audit against this actual main reports **one
matches_source / zero errors**; original source/health dates are retained in the report.
Markdown/JSON parity, original entry/helper/health hashes and native/stored equality pass.
Only Compute Pool's new API file changed since main `4e938868656b`; fetched full tree
inventory above was recomputed. This is **not a new full 60-artifact audit**. Monitoring
is now **60 artifacts / 59 services**; Snowflake imported coverage is **12 distinct
descriptions / 116 paths / 148 operations**, not its whole platform. Required #218 and
#219 attachment attempts both failed with the 100-attachment-cap error; retain the
GitHub links without claiming app linkage. Only unrelated #179 remains open.

Original preflight, generated candidate/result, source/health/bundle snapshots, actual CI
logs/states, premerge/merged receipts and independent import/post-delivery verification
remain under ignored `cache/maintenance/discovery/snowflake-compute-pool/`.
Next independent work: review all eight HCP Identity converter repairs and guarded
original HTML/string extraction before registering/importing; continue pending-PR update
and scheduled-publishing infrastructure separately. All eleven blocks, unanswered owner
protection choices, §5 parked items, Grant exclusion and the original local one-week
deadline/laptop-sleep behavior remain unchanged. Do not duplicate #218 or #219.

---

**Compute Pool original source review — 2026-10-06:** Native official Snowflake
Compute Pool is **3.0.0 / vendor 0.0.1 / 10 paths / 13 operations / 216 local refs**,
none external. All operations are disjoint from the prior eleven Snowflake services.
The individual guide explicitly marks generally available and unavailable in government
regions; current full reference includes three tag operations omitted by its intro table.
Retain both deprecated `:stopallservices` and replacement `:stop-all-services`, get-tags
warehouse requirement, all native auth/tenant/read-only/capacity/nullable/required fields
and deprecated error-code compatibility prose. Source is public/unarchived/undisabled
at vendor `990e25d97236a11826c9eed40e587c2b859e5680`; entry + `common.yaml` bundle with
Redocly 2.57.0, zero warnings/patches/conversion. Independent full dereferenced entry/
original component comparisons, native/stored preflight validation and typed vendor
roundtrip pass; no invented curation. **151 local tests pass**. Source registration and the separate generated API-only draft
are now delivered as #218/#219 above; retain this original review as evidence.
Monitoring is **60 artifacts / 59 services**; no full expanded audit is claimed.

Entry hash `f7293eef7951904a8943f1ea63adc80297a11cb9456fc8f95dbcaf55b357362e`;
two-file snapshot `34d7dd7fd49aa7ddaac9d263a46d29045bdeade4f7335a1e751e16fb30b6b209`.
Original docs/health/archive/entry/helper/bundle, native diagnostics, metadata and full
verification remain under ignored `cache/maintenance/discovery/snowflake-compute-pool/`.
All eleven prior blocks, unanswered protection choices, §5 parked items and deprecated
standalone Grant exclusion remain unchanged. Only unrelated #179 remains open.

**New concrete HCP publication lead:** The official overview links
`https://developer.hashicorp.com/hcp/api-docs/identity`. Its original HTML `__NEXT_DATA__`
contains an actual vendor Swagger 2.0 document as JSON string at
`/props/pageProps/schemaFileString`: **vendor 1.0 / 57 paths / 80 operations /
113 definitions / 248 refs**, host `api.cloud.hashicorp.com`; page releaseStage is
`stable`. This is an original public description, not SDK-type reconstruction or the
old absent SDK filename pointer. Page hash
`d8d60b5046b3e2ba762c08d0868f55a8d54b250f445e1ff998d4f42b0f3f9148`;
decoded exact native string hash
`b64b033f744447aab8bbcb26964e23a4c4ec35e03fd52ee2cfd3b5ccdf53dc35`.
No HCP source is registered/imported yet. Pinned swagger2openapi 7.0.8 diagnostic
preserves 57 paths / 80 ops, yields native 3.0.0 and passes full validation, but applies
**eight converter repairs**, with zero warnings. The normal zero-patch expectation
correctly blocks preparation; no allowance was enabled. Review all eight exact native
locations/semantics, auth/lifecycle and a reproducible guarded HTML/string extraction
recipe before delivery. Keep the original document, conversion input/result/log and
`identity-conversion-review.json`; do not just raise an expected count to get an import.
Original page/overview/Next data/native string plus exact pointer/provenance review are
cached under `cache/maintenance/discovery/hashicorp-hcp/public-docs/`. A first recursive
object scan found no OAD because this specific original document is encoded as a string;
do not report absence or build a schema from rendered operationGroups. The bounded HCP
SDK result remains historical. No HCP authentication, account request or vendor message
was performed. Continue this genuine official source lead after independent delivery.

---

**Guarded draft generator delivered — 2026-10-06 11:42 UTC:** Separate infrastructure
[#216](https://github.com/ontola/openapi-directory/pull/216) is merged as
`5b7502f802c3feeb0953e3e4ce8adbc8b44f1b48` from actual full head
`cdb44afeec430c28ff6db14901d41f5755bd1d16`. **151 tests passed locally and in
actual hosted CI** (run `37458009707`, tests job `112250269760`, all test steps executed).
Exact intended seven files, actual head/base and CLEAN/MERGEABLE state were checked
before matching-head merge; REST confirmed the merged result. No API file changed,
and full fetched Git-tree inventory above was recomputed. Only the two explicit GitHub
publication-group fields changed in source configuration. Required #216 attachment
attempt failed at the 100 cap; preserve its GitHub link, not an app linkage claim.

`maintenance/draft_pr.py` is now delivered: default official-source dry run; explicit
create-only `--publish`; one reviewed API/group; all existing PRs/branches held without
duplicate/overwrite; source/native/serialization/tree/configuration guards; exact draft
head/base/repository/files verified after pagination; durable locks/failure receipts and
no automatic retry, redaction, protection bypass or merge command. API-only generated
drafts have separate read-only offline CI using delivered base tools and exact head.
That branch-specific CI job correctly skipped this infrastructure branch; its real-Git
validation path is exercised by the 29 new regression cases in the passing hosted suite.
No actual API draft was published this run, since the three selected live sources match.

Original selected live checks at `bd7b851c319b` retain their **11:36–11:37 UTC dates**:
GitHub companions at one vendor `836ce198db13a6fb194547e53eea99c6ddae495b`, each native
3.0.3 / 1.1.4 / 816 paths / 1,232 ops; HF Endpoints native 3.1.0 / 2.0.0 / 40 / 46.
All three original hashes, complete native/stored validation, typed YAML and independently
projected full vendor content pass; shared repository-health response hash/flags pass,
HF hosted health remains unassessed. API files are byte-identical between prior real main,
the checked infrastructure commit and merged main. No full 59-artifact freshness audit
or new discovery scan is claimed. Evidence/receipts/scripts/CI logs remain under ignored
`cache/maintenance/reports/guarded-draft-generation/`, including `live/independent-verification.json`
and `delivery-summary.json`. Do not repeat completed generator delivery or source checks.

**Continue:** automatic safe pending-PR updates and scheduled PR publication remain
authorized separate infrastructure work; neither is enabled yet. Keep local cache/guards
and explicit per-API review, ensure actual API CI runs, and preserve weekly/monthly
read-only permissions until a reviewed writer exists. Continue independent major-vendor
official-source discovery/freshness reviews. All eleven prior blocks, unanswered owner
choices, §5 parked items and fully deprecated Grant exclusion remain unchanged. Only
unrelated #179 remains open. No vendor message, constraint waiver, blanket auto-merge,
extra recurring chat task, power change or execution-host move. Original local one-week
deadline and laptop-sleep behavior remain unchanged. Prepared notes below are historical.

---

**Snowflake Database Role delivery confirmed — 2026-10-06:** Monitoring
[#213](https://github.com/ontola/openapi-directory/pull/213) merged as
`c3a19b3dbd5bc5bbbc2a4dfecb69560ca783dbfb` from actual head
`ec01adf82a7daa3251fd8f2a302e7536e4e961b1`. **122 tests passed locally and
in actual hosted CI** (run `37448672338`, tests job `112219572344`). Only source
manifest, maintenance README and AGENTS changed. API-only
[#214](https://github.com/ontola/openapi-directory/pull/214) merged from exact
head `3847e7eb47a7adf3558ca6afb06f0a93ce95a8fe` as
`3a2d767b152f44859a554d47cda32e6f7ed0637a`. Actual full heads, intended file
lists and CLEAN/MERGEABLE state were checked before matching-head merges;
REST confirmed merged results. Do not repeat these completed deliveries.
API-only PRs do not trigger maintenance CI; full independent source/bundle/import/
serialization verification passes, including all **270 refs**, native **3.0.0 /
0.0.1 / 10 paths / 13 operations**, zero patches/conversion/bundler warnings.

Fresh selected **one-source network audit** against real merged main
`3a2d767b152f` reports **matches_source with zero validation errors**. Original
entry/helper/fresh repository metadata hashes, complete stored/native validation,
typed roundtrip, full vendor equality and JSON/Markdown parity pass. Since previous
main `33aaf78f428e`, the only API change is Database Role's new file; all ten older
Snowflake descriptions remain byte-identical. Monitoring is now **59 artifacts /
58 services**. Snowflake has **11 descriptions / 106 paths / 135 operations**;
this is not a full 59-artifact audit, new catalog scan, complete SQL or platform
coverage. Prior source-fetch dates and the monthly 41-candidate report stay historical.

Grant remains **unregistered and unimported**: all seven original operations declare
`deprecated:true`, and independent HTML heading extraction confirms seven Deprecated
headings in the current full reference. Its introduction omits the warning. Native
bundle validation succeeds; lifecycle is the reason for skipping a new current-priority
addition. Source/guide/reference originals, hashes and exact decision remain under
`cache/maintenance/discovery/snowflake-database-role-grant/grant-lifecycle-decision.json`.
Reconsider only with new official lifecycle/source evidence; do not infer an endpoint
retirement date or restore/concatenate this description into Role/User/Database Role.

Durable ignored evidence directory above also contains `selected-postdelivery.json/.md`,
`postdelivery-verification.json`, `database-role-actual-import-verification.json`,
`preflight.json`, `verification.json`, original archive/helper files and docs/health,
`local-tests.log`, `infra-ci.log`, `infra-ci-status.json`, `verify.py`,
`verify-actual-import.py` and `verify-postdelivery.py`. Required attachment attempts
for #213/#214 failed at the existing 100 cap; preserve GitHub links, not a linkage claim.
Only unrelated #179 remains open. All eleven prior blocks, unanswered protection
owner choices and §5 parked items remain unchanged. No vendor messages, constraint
waivers, blanket auto-merging, protection bypass, power change or extra chat automation.

**Draft generation infrastructure prepared — 2026-10-06:** Separate infrastructure
branch `codex/guarded-api-draft-generation` implements `maintenance/draft_pr.py`.
Default is a fresh official-source dry run; explicit `--publish` can create only a new
draft for one reviewed API. Both public GitHub REST artifacts now share explicit
`github-public-rest` grouping; companion repository/ref artifacts share one pinned
source commit. **151 local regression tests passed** after implementation, including
29 new real-Git/REST/outcome/CI cases; hosted CI is still pending. Source-health/native/bundle/recipe/import/YAML/vendor
comparisons are reused, local tools/configuration must equal the comparison tree, and
full Git objects plus a temporary private index preserve sparse paths and staged work.
Only API files and exactly reconstructed baseline-target edits are allowed. Full open
PR/file pagination holds overlapping historical/current API PRs and existing branches
without duplicating or overwriting them. Atomic empty-ref lease prevents race overwrites.
Returned PR repository/head/base/draft state/files are verified. An exclusive local lock
and durable failed/uncertain-publication guard forbid automatic retry/protection bypass.
Keep publication cache across runs; never delete guards to force another push/POST.

Generated API-only drafts have separate read-only CI using delivered base tools, exact
head/parent, native validation, typed YAML and allowed tree/manifest checks. This is
offline validation, not fresh vendor comparison. There is no merge operation, scheduled
writer, automatic pending-PR update, extra chat automation or vendor message. Required
desktop attachment is the caller's responsibility, including returned created URLs after
verification failures; preserve actual attachment outcomes. Infrastructure remains
separate from API deliveries. Fresh selected live dry runs at committed infrastructure head `bd7b851c319b` found
all **three artifacts match**, with no pending API PR and no checkout/index changes.
Both GitHub files use vendor `836ce198db13a6fb194547e53eea99c6ddae495b`, native 3.0.3 /
1.1.4 / 816 paths / 1,232 ops each; shared fresh repository health is available. HF
Endpoints remains native 3.1.0 / 2.0.0 / 40 paths / 46 ops, hosted health unassessed.
Source times remain 11:36–11:37 UTC; this is not a full 59-artifact freshness audit.
Original snapshots/candidates/results, full tests and verification retained under ignored
`cache/maintenance/reports/guarded-draft-generation/`. Infrastructure PR/actual CI/merge
still need confirmation; do not treat this note as proof of hosted success or delivery.

**Next work:** finish verification and delivery of this infrastructure; then deliberate
pending-PR updates and scheduled publication remain authorized separate infrastructure.
Existing read-only weekly/monthly jobs keep their permissions. Continue bounded public
HCP publication discovery and individual major-provider reviews. All eleven prior blocks,
unanswered owner choices, §5 parked items and Grant lifecycle exclusion remain unchanged.
Preserve original local one-week deadline/sleep behavior and avoid duplicate PRs.

---

**Snowflake Database Role review — 2026-10-06:** Separate monitoring infrastructure
registers `snowflake-database-role`, native **3.0.0 / vendor 0.0.1 / 10 paths /
13 operations / 270 local refs**, none external. **122 local tests pass**;
fresh selected network audit against actual main reports this valid missing service. API import remains separate until
infrastructure CI/merge; verify actual PR state before continuing. Fresh official
vendor branch resolves to `990e25d97236a11826c9eed40e587c2b859e5680`, same public/
unarchived/undisabled repository. Entry + `common.yaml` bundle with Redocly 2.57.0,
zero warnings and no patches/conversion. Full native diagnostics/validation, all refs,
whole-entry dereferenced equality, every original named component, typed serialized
vendor equivalence and no invented curation pass. All ten existing Snowflake operation
sets are disjoint from this distinct database-scoped role service.

[Guide](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/database-role/database-role-introduction)
and [full reference](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/database-role)
have no preview designation in the generally available catalog (checked 2026-10-06).
Retain cloning, grants/future privileges, restrict/cascade semantics and parallel-grant
limitations, all four native authentication alternatives, tenant/database/name
constraints, deprecated error_code compatibility prose and get-tags warehouse
requirement. Introductory table omits three tag actions present in full source/reference;
do not truncate. Literal document 0.0.1 is not evidence of unchanged content or full SQL.

**Grant lifecycle finding, do not import blindly:** Fresh official `grant.yaml` is
native 3.0.0 / 0.0.1 / 7 paths / 7 operations / 171 local refs. Its two-file bundle
fully validates, but **all seven operations declare deprecated:true**, independently
confirmed by every operation heading in the current full
[Grant reference](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/grant).
Its introductory guide omits that warning, so checking only the overview would be
misleading. This entire deprecated candidate is **not registered or imported** for
current-priority coverage; healthy publication and validation do not establish runtime
availability or recommendation. Preserve the raw artifact and lifecycle decision;
reconsider only when new official source/lifecycle evidence justifies it. Existing
Role/User and Database Role retain their separate resource-specific grant operations.
This is a discovery decision, not a native validation block or vendor schema fix.

Database Role entry SHA-256 `9e72bc5202b70e2abff1376b8f255d56b6bfff601e4f7db3d2262af68bea4f3f`,
snapshot `d0003e3330b60d4c36386d83f13c82b340534cc9d8be30119e148eedc3ca6cf4`.
Grant entry `e7d9ffd1eaa183e064e6ef3efe394a0e22299108296c721072334866b35e4bb9`,
snapshot `32283f209ec24e2401f9b3da14b10a2315f9770b469d65f72dadacc788490e35`.
Common helper `df3b8b533f189f6ae4229d4657d1251535e74a25318d5d73de24d0788dcb0b21`.
Original docs/health/entry/archive/bundle/preflight/verification and lifecycle decision
retained in ignored `cache/maintenance/discovery/snowflake-database-role-grant/`.
Monitoring will be **59 artifacts / 58 services** with this registration. No new full
freshness audit or catalog scan is claimed. Prior #209–#212 are merged; don't duplicate.
All eleven native/source/publication blocks, unanswered protection owner choices,
#179 and §5 parked items remain unchanged. No vendor messages, constraint waivers,
protection bypass, power-setting change or new recurring chat automation; original
local one-week deadline/sleep behavior remains unchanged.

---

**Snowflake User / Role delivery confirmed — 2026-10-06 09:22 UTC:** Monitoring
[#209](https://github.com/ontola/openapi-directory/pull/209) is merged as
`1922538d26f9ceea4f83202e045375dd171896a3` from actual head
`bbf10c1d75454db300dd759076b1d2e2a7d8095f`. **122 tests passed locally and
in hosted CI** (run `37442095028`, tests job `112198055612`). Intended files
were only source manifest, maintenance README and AGENTS; no API duplication.
API-only [#210 User](https://github.com/ontola/openapi-directory/pull/210) merged
from `a20b6f520ab27a4ac863e7f8e134456b7b53c92b` as
`2f5b83f376e25e41044a16d89d8035b46d25d848`; API-only
[#211 Role](https://github.com/ontola/openapi-directory/pull/211) merged from
`3c84b8c93e01e4b71cf56c673998f502dbafbf20` as
`b2869282bdbf7c52160af2bc7d08ea5f1edbefab`. Each intended file list, actual
full head and CLEAN/MERGEABLE status were verified before matching-head merges;
REST confirmed merged results. API-only PRs do not trigger maintenance CI; full
independent native/bundle/import/serialization checks are recorded below.
Do not duplicate these completed deliveries.

Fresh selected **two-source network audit** against real merged main
`b2869282bdbf` at 09:21 UTC finds **two matches_source, zero validation errors**;
original entry/helper hashes, fresh repository metadata hash, full stored validation,
all refs, complete typed vendor content and Markdown/JSON parity pass. Both fresh
source revisions/hashes equal the individually reviewed discovery and import snapshots.
The only API changes since previous main `de4b8225ebbc` are these two new files;
all eight prior Snowflake services remain byte-identical. No patches or conversion.
User 7 / 11 / 222 refs; Role 11 / 14 / 277; native 3.0.0 / literal vendor 0.0.1.
Snowflake now has **10 distinct descriptions / 96 paths / 122 operations**, not
whole-platform or full SQL coverage. Monitoring now **58 artifacts / 57 services**;
this selected check is not a full 58-artifact freshness audit or a new catalog scan.
The prior 41-candidate monthly report retains its original date; User/Role are
now registered so subsequent discovery will skip them rather than duplicate them.

Durable ignored source/docs/health/archive/bundle/import/CI/report/verifier evidence:
`cache/maintenance/discovery/snowflake-user-role/`, including
`selected-postdelivery.json/.md`, `postdelivery-verification.json`,
`user-actual-import-verification.json`, `role-actual-import-verification.json`,
`infra-ci.log`, `local-tests.log`, `verify.py`, `verify-actual-import.py` and
`verify-postdelivery.py`. Required attachment attempts for #209–#211 failed at
the existing 100 cap; preserve GitHub links and do not claim successful app linkage.
No protected push rejection, owner-choice retry/redaction/unblock, vendor message,
native constraint waiver, blanket auto-merge, power setting change or extra recurring
chat automation. Unrelated #179 and all eleven recorded blocks remain unchanged.

**Next work:** deliberately review another distinct public Snowflake candidate
(Database Role is separate from the completed Role API) against its individual
current lifecycle guide and full native diagnostics before registering/importing.
Continue bounded public HCP publication discovery independently of its internal
SDK-generation references. Per-API PR generation remains unfinished infrastructure
work and must remain separate from imports. Preserve §5 parked items and original
local one-week deadline/sleep behavior.

---

**Snowflake User / Role reviewed registrations — 2026-10-06:** Separate updater
infrastructure registers two distinct official resource-management services from the
monthly discovery queue. API files are not in this infrastructure PR; deliver each
in its own API PR after actual infrastructure CI/merge. Native **3.0.0 / 0.0.1**:
User **7 paths / 11 operations / 222 local refs**; Role **11 / 14 / 277**. No
external refs remain. **122 local tests pass**; selected pre-import network checks
against actual main report two valid missing services and no validation errors. Fresh public/unarchived/undisabled vendor repository check and
entry/archive comparison pin both to `990e25d97236a11826c9eed40e587c2b859e5680`.
Each bundle has exactly two files (entry + `common.yaml`), zero Redocly 2.57.0
warnings, no patches, no conversion, no prior service baseline or invented curation.
Full native bundle validation, all ref targets, typed YAML roundtrip and independent
whole-entry dereferenced comparison plus every original named component pass.

[User guide](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/users/users-introduction)
and [Role guide](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/roles/roles-introduction)
and full references carry no preview designation in the generally available catalog.
Introductory endpoint tables omit three tag actions each; full references and native
specs include them, so do not truncate the vendor artifact. Preserve KeyPair,
ExternalOAuth, SnowflakeOAuth and ProgrammaticAccessToken alternatives, tenant
server, privilege/revocation rules, deprecated error_code compatibility prose and
get-tags active-warehouse requirement. These are distinct from Database Role and
other resource services, not full SQL or whole-platform coverage.

User entry SHA-256 `c18785aebdbfc298e589ea971760c405f3b233597615efc5fbb0b10c07c35379`,
snapshot `07cef2f86c93fe1f87cb63ce0fd9f3b7095504a83869159a3b799899d7b6ac29`.
Role entry `3449df2f72bd72e7160adf4f5200933a58f69604b535d8dfd263f58c2b463e00`,
snapshot `1e059cb3e71beb9301e3b599d460bdbc35e729622e13e173fe340d5f6274f87c`.
Common helper hash `df3b8b533f189f6ae4229d4657d1251535e74a25318d5d73de24d0788dcb0b21`.
Ignored original docs/health/entry/archive/bundle/review evidence lives in
`cache/maintenance/discovery/snowflake-user-role/`; verifier
`/tmp/verify-snowflake-user-role.py`, preflight `/tmp/review-snowflake-user-role.py`.
The docs-advertised User reference Markdown URL returned 404; actual HTML references
were fetched and retained, not reconstructed. Monitoring will be **58 artifacts /
57 services** with these registrations; no full new freshness audit claimed.

**Monthly discovery delivery receipt:** #208 is merged as
`de4b8225ebbc74fcbc1d024148697e5b604558fb` from actual head
`8f7ff107c08be91f0a3be4fd00b7785345b5d6cd`, **122 local/CI tests** passed
(run `37436119089`). First actual merged-main monthly workflow `37436278655`
also passed 122 tests and all three scans; its 41 review candidates / 8 skips /
6 Snowflake helpers agree with the earlier local snapshot. Original 60 blob/context
hashes, three repository health/commit/tree snapshots and Markdown/JSON parity
independently checked. Report base is actual main `de4b8225ebbc`; durable ignored
copy `cache/maintenance/discovery/monthly-hosted-37436278655/` includes verifier,
verification/logs and unmodified downloaded report. This is discovery, not a fresh
56-service-content audit; do not repeat #208 or claim full directory coverage.
All eleven blocks, unanswered protection owner choices, #179 and §5 parked items
remain unchanged. Original local deadline/sleep behavior remains unchanged.

---

**Monthly discovery implementation — 2026-10-06:** Separate infrastructure delivery
[#208](https://github.com/ontola/openapi-directory/pull/208) implements
`maintenance/discovery.py`, reviewed `maintenance/discovery.json`, and the read-only
`.github/workflows/discovery.yml` (first day 07:23 UTC/manual; contents:read only).
Consult the PR for actual CI/merge state before continuing; do not duplicate this
implementation. It runs the pinned suite before discovery and is covered by normal
PR tests. It creates no APIs or PRs, applies no patches and authorizes no merges.
Per-service PR generation remains separate unfinished infrastructure work.

**122 local tests pass**, including ten new discovery regressions: complete Git-backed
sparse inventory, exact-content versus endpoint-shape grouping, native/external-ref
obstacles, public identity/archive/disable/private blocks, tree identity/truncation/
limits, Git blob size/hash/symlink/parse failures, submodules, unsafe configs and real
successful-date retention on failed scans. Explicit blob/context limits, unchanged
HTTP timeout/retry/auth policy and 15/20-minute CI job limits bound the scan. Context
files are evidence, never executed or followed to guessed URLs. Commit metadata's exact
root tree SHA is requested and verified, rather than assuming commit and tree IDs are
interchangeable; mismatches fail before artifact inspection.

Initial live run against actual main `fdb039f769ac0b65bf02b25f16493765e0cdea04`
completed all three configured repository scans: **41 Snowflake candidate groups**, each
requiring external-reference bundling and individual lifecycle/purpose/compatibility
review; **8 already registered sources** skipped without a freshness claim; **6 shared
Snowflake helpers** excluded after parsing proves no OAD root. HCP scan inspected its
7 JSON/YAML configuration files, none OADs. Anthropic's bounded OpenAPI/Swagger/
specification filename scope found no candidates. These are bounded publication leads,
not proof no vendor OAD exists elsewhere. Identical vendor content groups retain all
source URLs; matching endpoint sets against stored files and other candidates are
annotated, not assumed equivalent products or stable releases.

HCP public Makefile contains test/lint tasks, not a spec-generation input. Its pinned
public sync workflow references `hashicorp/hcp-sdk-go-internal`, retained internal docs/
scripts and `cmd/transform-swagger` tooling. This does not establish a downloadable
public OAD; no internal repository or SDK-type reconstruction was used. Public HCP
product docs/embedded publication remain the next discovery lead. Current Anthropic
.stats.yml still lacks the older Stainless pointer; preserve the prior warning.

Independent verification checked **60 original blob hashes, including six context
inputs**, all three repository-health/commit/tree snapshots, source registrations,
complete full-depth inventory and JSON/Markdown parity. Source bytes are unchanged,
API files and the **56-artifact/55-service** maintenance registry are unchanged.
This is discovery, not a new full freshness audit. Reports, source snapshots, context
inputs and verification/log copies are retained in ignored
`cache/maintenance/discovery/monthly/` and
`cache/maintenance/discovery/monthly-initial/` (`report.json/.md`, `verification.json`,
`verify.py`, local-tests.log). Attachment #208 failed at the existing 100 cap; preserve
its GitHub link. No vendor messages, protection bypasses, constraint waivers, power
changes or extra recurring chat automations.

Next: deliberately review promising distinct Snowflake candidates from this queue
against individual official public product guides, then bundle/validate/register and
import one API per PR if stable scope is confirmed. Compatibility descriptions and
preview-only resources need separate judgment, not automatic import. Current main's
Confluence v1/v2 and earlier recorded refreshes are complete. All eleven native/source/
publication blocks, unanswered Messaging/Conversations choices, unrelated #179 and
explicitly parked §5 items remain unchanged. Keep the original local one-week deadline.

---

**Latest follow-up — 2026-10-06 07:52 UTC:** Confluence Cloud **v1 is now delivered**,
separate from v2. Do not repeat its prepared/import queue below. Updater
[#205](https://github.com/ontola/openapi-directory/pull/205) merged at
`8fd1bcd65def291af1c181ba9d53db282a829fee` after actual head
`6db22972d34b9cc606bc893d1972dc867e9feea9` passed **112 local and hosted CI tests**
(run `37432049207`, tests job `112164954722`). API-only
[#206](https://github.com/ontola/openapi-directory/pull/206) merged at
`c73359aaf5e914eebb772bfe993784229f99ea2f`, exact head
`fbcb5887c71ccc57c54639c8b29420e80b965e6d`; only new file
`APIs/atlassian.com/confluence-v1/1.0.0/openapi.yaml`. Both PRs were explicitly
verified CLEAN/MERGEABLE and merged with their actual matching head; no auto-merge.

Native 3.0.1 / document 1.0.0 / **89 paths / 130 operations / 511 local refs**,
no external refs. All original content survives except three exact invalid null
defaults (required label `name`, optional label `type`, optional group `accessType`)
and added provenance. Requiredness/types/enums remain; recipe assertions stop vendor
corrections. Source hash `6c66a606fa7535268512f07f599fe1e3f9de2ba0b1da7eb6ead405509875577e`,
recipe hash `46315783f6954dad648794827c5f969905188b38fbd03e17113f12caac921bcf`.
Complete native/serialized validation, typed roundtrip, all references and full
curated vendor comparison pass. Native auth/scopes, tenant server, permissions,
seven experimental flags and two deprecated descendant operations remain. Publication
does not establish runtime availability of deprecated endpoints. No conversion,
bundling, new curation, nullable widening or inferred omission behavior.

**Monitoring now registers 56 artifacts / 55 services.** Fresh selected Confluence
v1 audit against real merged main `c73359aaf5e9` at 07:51 UTC reports
`matches_source` with no validation errors. This is **one newly checked artifact**,
not a second full network audit. Preserve the earlier 55-artifact network audit and
cached reconciliation below with their actual dates/bases; the other 55 registrations
and all previously stored APIs are unchanged by #205/#206. Known 11 blocks and
unanswered Twilio Messaging/Zendesk Conversations owner choices remain untouched.
Only independent #179 remains open after delivery. No vendor messages/issues sent.

Durable ignored evidence, original native source/HTTP metadata, current official
intro/label/group/descendants references, all-error enumeration, independent preflight
and actual import comparisons, verifier copies/local and CI logs, and selected
before/after JSON+Markdown audit reports are in
`cache/maintenance/discovery/confluence/v1-current/`. Old scratch venv disappeared;
pinned local Python environment is now `/tmp/openapi-maintenance-py312/`.
Attachment attempts #205/#206 failed at the existing 100 cap; preserve GitHub links,
do not claim app linkage success or repeat ineffective legacy-URL removals.

Next meaningful work: official-source discovery for well-known providers (HCP generation
inputs/official docs and current Anthropic publication remain bounded leads), or separate
authorized updater PR-generation/monthly-discovery infrastructure. Confluence v1/v2 are
complete. Keep all native-defect blocks and explicitly parked §5 work intact. The original
local one-week deadline and laptop-sleep behavior remain unchanged.

---

**Earlier resume state — 2026-10-06 (before #205/#206):** This supersedes earlier prepared/draft/runner-outage
notes retained below as historical evidence. All six API deliveries and three updater
recipes in the following table are merged; do not duplicate them.

| API / delivery | Merged PRs | Current scope |
|---|---|---|
| Zendesk Support | [#195 updater](https://github.com/ontola/openapi-directory/pull/195), [#196 API](https://github.com/ontola/openapi-directory/pull/196) | 2.0.0; 455 paths / 657 ops / 2534 refs; exact null-only and unused-parameter guards |
| Coinbase CDP | [#197 updater](https://github.com/ontola/openapi-directory/pull/197), [#198 API](https://github.com/ontola/openapi-directory/pull/198) | 2.0.0; 140 paths / 169 ops / 2594 refs; four redundant optional-header flag removals |
| Confluence Cloud v2 | [#199 updater](https://github.com/ontola/openapi-directory/pull/199), [#200 API](https://github.com/ontola/openapi-directory/pull/200) | 2.0.0; 151 paths / 218 ops / 682 refs; two exact invalid-prefix-default removals |
| Sentry | [#201](https://github.com/ontola/openapi-directory/pull/201) | v0; 155 / 249 unchanged; five monitor max_runtime limits now 10080 minutes (7 days), previously 40320 |
| Discord HTTP | [#202](https://github.com/ontola/openapi-directory/pull/202) | 10; 153 / 246 unchanged; guild message search permits OAuth2 alongside BotToken |
| Atlas Admin | [#203](https://github.com/ontola/openapi-directory/pull/203) | 2.0; 339 / 549 unchanged; vendor x-xgen-sha refresh, metadata-only; curated tag order retained |

The hosted runner outage cleared. Initial retry heads actually executed tests; after
resolving concurrent source/test/doc conflicts, updated Support CI run 37421730254
passed **108 tests**, and combined Coinbase CI run 37421998779 passed **110 tests**.
Confluence run 37421251233 passed 102. All new serialized files and refreshes passed
full validation, typed YAML roundtrip, reference and complete curated-vendor comparisons;
no blanket auto-merge, push-protection bypass, native constraint waiver or power-setting
change. Live rechecks confirmed Support/CDP match their reviewed source hashes before
merging. Only independent PR #179 remains open, unchanged and outside this workstream.

**Current monitoring: 55 artifacts / 54 services.** Full network audit against real
merged main `791051c64138` (after the three additions) found **41 matches / 3 valid
drifts / 11 known blocks**, no fetch/prepare failures. The three drifts were reviewed
and delivered in #201–#203. Atlas's 58 tag objects have identical per-name content:
source order changes plus x-xgen-sha are the entire vendor diff, not invented API
behavior. All 55 original source hashes, 26 repository-health snapshots and report
Markdown/JSON parity were independently checked; **16 hosted artifacts** have health
not_assessed. Original audit is `/tmp/main-55-local-audit.json/.md`, verification
`/tmp/verify-main-55-local-audit.py`, review `/tmp/main-55-local-audit-review.json`;
ignored durable copy `cache/maintenance/reports/main-55-791051c64138/`.

Post-delivery **cached-source reconciliation** against `2af2c554a035` yields **44
matches / 11 known blocks / no remaining drift against those snapshots**. This is
not a second network audit: source-fetch/health observations retain their real dates.
Git diff proves only the three reviewed API files changed since the full audit;
those stored files and cached native sources were revalidated and compared again.
Script `/tmp/reconcile-main-55-cached-audit.py`; report/review
`/tmp/main-55-cached-reconciliation.json/.md`,
`/tmp/main-55-cached-reconciliation-review.json`, retained copy
`cache/maintenance/reports/main-55-reconciled-2af2c554a035/`. Do not claim coverage
or freshness for the whole 731-provider historical directory.

Blocks remain Cohere, Square, Slack Web, Meraki, Vercel, Mailchimp Marketing, Auth0,
Cloudflare, Okta, Twilio Messaging and Zendesk Conversations. The last two are valid
prepared deliveries held by unanswered push-protection owner choices; do not retry,
unblock or redact. Preserve all other native defects and explicitly parked §5 items.
No vendor messages/issues were sent. Attachment cap remains 100; required attachment
calls for #197–#203 failed. Canonical removals returned app errors; legacy redirect
removals reported success without removing actual attachments. Preserve GitHub links
and this resume record; do not claim app linkage success or delete history to make room.

**Continue with meaningful work:** extend official-source audit/discovery for major
providers; Confluence v1 is now a concrete native-invalid candidate (separate from
v2, which is complete). Review exact schema/default defects and lifecycle before
any recipe/import; do not fix blindly after only the first diagnostic. A fresh bounded
HashiCorp SDK lead checked public/unarchived/undisabled `hashicorp/hcp-sdk-go` at
`94ea63cdc563d9ee06bc879d5565523f63219ed7`: complete untruncated tree contains no
OpenAPI/Swagger-named artifact, and the lone specification-named file is a generated
Go node model. Original metadata/tree/README cached under
`cache/maintenance/discovery/hashicorp-hcp/`. SDK preview/stable release language is
not proof of a current downloadable OAD; inspect generation inputs/official HCP docs
next, do not derive schemas from SDK types or register guessed URLs. Anthropic's live
SDK stats no longer expose the old Stainless download pointer (recorded in #196).
Scheduled PR generation/monthly discovery remain authorized implementation work;
keep infrastructure separate from API PRs and require deliberate per-API review.
The original local one-week deadline and laptop-sleep behavior remain unchanged.

---

## 1. The standing task

Keep this fork current for well-known industry APIs. Prioritize direct comparisons with
official vendor sources and discovery of missing official OpenAPI descriptions (OADs).
Use the upstream `APIs-guru/openapi-directory` backlog as a secondary source of leads;
the previous backlog sweep was low-yield (§3). Follow the current queue in §4 and the
maintenance implementation instructions in §9.

**Filter criterion the user set, which governs everything:**
> "you can skip additions of niche APIs, I'm more interested in additions or corrections of well-known industry APIs."

**Delivery pattern:** one PR per API, against our own `main`, upstream issue/PR link in the **PR body, not the title**. Merge when clean.

**When the backlog runs dry, the task does not stop.** Two standing jobs:

1. **Find specs we don't have.** Search the web for official OpenAPI descriptions of large,
   well-known APIs. "Official" means published by the vendor, ideally in their own git repo
   — see §8 for how to tell a real one from a third-party scrape.
2. **Check what we already have is current.** Most of the value found so far was here, not
   in new additions: Stripe was 4 years stale, Square was 94 paths behind, Meraki and
   Mailchimp both needed version bumps. Walk `APIs/` against upstream sources and compare
   `info.version`, paths, operations, and schema content. An unchanged version or path
   count does not prove an unchanged API.

**Autonomy level as of the last instruction:** the user said *"i don't need to review them, you can merge them when you think they look good."* That applies to straightforward additions of official vendor specs. It does **not** extend to the deferred/judgment items in §5 — those were explicitly declined or parked and need a fresh go-ahead.

---

## 2. What's done

PRs **#7–#42** were this workstream (#1–#6 predate it).

- **#7–#17** — ported upstream PRs (typo fixes, `x-origin` corrections, small API additions: Oneauto, tensorpix, viesapi, Famxplor, Wikidata, Interfaces One).
- **#18–#21** — Cloudflare, Auth0 Management, Discord, OpenAI 2.3.0.
- **#22–#25** — Nylas v3, Picsart Image 2.0, Picsart GenAI 1.0, Eventbrite v3.
- **#26–#38** — **all 13 PayPal specs** from `paypal/paypal-rest-api-specifications`, one PR each.
- **#39** — Datadog v2 (1008 paths / 1591 ops), under `APIs/datadoghq.com/v2/1.0/`.
- **#41** — Cisco Meraki 1.74.0 (new version dir; 1.32.0 left in place).
- **#42** — Mailchimp 3.0.91 (new version dir; 3.0.55 left in place).

**#40 (Google Vertex AI) was closed, not merged** — see §5.

**#44–#54 — the first coverage-gap batch. All merged.** Found by auditing what we already
have against vendors' own published specs, not from the upstream backlog.

| PR | API | Paths / ops | Note |
|---|---|---|---|
| #44 | Stripe `2026-08-26.dahlia` | 419 / 594 | refresh; was pinned at `2022-11-15`, ~4 years stale |
| #45 | Figma `0.42.0` | 47 / 54 | new; source already YAML |
| #46 | Sentry `v0` | 147 / 234 | new; upstream artifact is deref'd, so no `$ref`s at all |
| #47 | PagerDuty `2.0.0` | 273 / 465 | new |
| #48 | MongoDB Atlas Admin `2.0` | 333 / 541 | new; filed under `mongodb.com/atlas-admin/` |
| #50 | Grafana `0.0.1` | 207 / 314 | new; Swagger 2.0 -> OpenAPI 3 |
| #51 | Square `2.0` | 253 / 332 | refresh, **in-place, −16 paths** (Square's retired v1 + Transactions APIs) |
| #52 | DocuSign eSignature `v2.1` | 213 / 414 | refresh, in-place; Swagger 2.0 -> OpenAPI 3 |
| #53 | — | — | this file; replaced `HANDOFF-upstream-triage.md`, added §5b |
| #54 | Intercom `2.14` | 106 / 150 | new |

**#55–#58 also merged**, closing out the batch:

| PR | API | Paths / ops | Note |
|---|---|---|---|
| #55 | Elasticsearch `9.5` | 581 / 845 | new; version taken from the release branch — see §4 |
| #56 | — | — | AGENTS.md status |
| #57 | Elasticsearch Serverless `2026-09` | 289 / 460 | new; **snapshot date, not a vendor version** — see §4 |
| #58 | **HubSpot — 59 specs** | 507 / 676 | new; selected down from a 122-entry catalog — see §4 |

**Upstream spec defects found and fixed in this batch** (all verified present in the
vendor's own published file first, then fixed to match that vendor's own style):
- Square `PUT /v2/vendors/{vendor_id}` — declared `parameters: []`, leaving its path variable undeclared.
- Square `POST /oauth2/revoke` — security scopes as `null` instead of `[]`.
- Intercom `GET /export/reporting_data/{job_identifier}` and `/download/...` — omitted the path parameter.

**Deliberately NOT fixed**, and why:
- Square `$ref`s `CurrencyExchange` and `AppFeeAllocation` without defining them. Inventing schemas would be fabricating API surface.
- HubSpot **HubDB** `$ref`s `HubDbTableRowV3Wrapper` four times without ever defining it. Same reasoning as Square.
- DocuSign descriptions carry double-encoded UTF-8 (mojibake). It is **DocuSign's own bug, in the source file** — refreshing does not fix it, and rewriting vendor prose is a bigger change than it looks.

Grafana (#50) was initially blocked by GitHub push protection over a fake example token in
Grafana's own spec; the repo owner reviewed it and allowed it. See §7.

**October maintenance work merged:**

| PR | Result | Scope |
|---|---|---|
| #60 / #64 | Maintenance instructions and progress | Repo instructions and audit findings |
| #61 | Initial reproducible updater | Six service sources, pinned dependencies, validation, weekly read-only audit artifacts |
| #62 | Hugging Face Inference Endpoints `2.0.0` | New management API; 40 paths / 46 operations |
| #63 | Plaid `2020-09-14_1.740.1` | New version directory; 360 paths / 351 operations; historical version preserved |
| #65 | GitHub public REST, both default and `2022-11-28` artifacts | Fixed `1.1.4` version refreshed in place; each 815 paths / 1,231 operations; seven monitored artifacts across six services |
| #66 | Exact patch replay in updater | Checked JSON replacements, context assertions, recipe hashes/provenance; 16 passing regression tests |
| #67 | Xero Accounting `19.1.0` | New version directory; 138 paths / 235 operations; historical version preserved |
| #69 | Pinned repository reference bundling | Locked Redocly 2.57.0, source-file hashes, archive/reference checks, exact field removal; 21 tests pass locally and in CI |
| #70 | DigitalOcean `2.0` | Fixed version refreshed in place; 515 paths / 757 operations; curation preserved |
| #71 | Snowflake SQL `2.0.0` | New SQL execution service; 3 paths / 3 operations; no bundling or patches |
| #72 | Snowflake Warehouse `0.0.1` | New management service; 12 paths / 15 operations; `common.yaml` bundled with zero warnings |
| #74 / #75 | Pinned Fern snippet materialization and YAML scientific numbers | Source snapshots include code artifacts; fetch-helper integration verified; 27 tests pass locally and in CI |
| #76 | Cohere `1.0` | New OpenAPI 3.1 description; 32 paths / 42 operations; seven TypeScript samples materialized without execution |
| #77 | Mistral `1.0.0` | New public OpenAPI 3.1 artifact; 212 paths / 299 operations; eleven checked streaming-reference corrections |
| #78 | YAML string preservation and import round-trip guard | Quote scientific-looking vendor strings, reject serialization type/value changes; 29 tests pass locally and in CI |
| #79 | GitHub example string types | Eight quote repairs across both public artifacts; paths/operations unchanged, vendor JSON values retained |
| #80 | Deterministic curation serialization and progress | Identical imports across three Python hash seeds; 30 tests pass locally and in CI |
| #81 | Four more official-source registrations | Stripe public GA, Figma, PagerDuty REST and Atlas Admin; 15 artifacts / 14 services monitored |
| #82 | Figma `0.43.0` | New version directory; 47 paths / 54 operations; composed color values and `COLOR_OPACITY` scope |
| #83 | Stripe `2026-09-30.endive` | New version directory; 454 paths / 644 operations; includes vendor GA v1+v2 coverage |
| #84 | PagerDuty `2.0.0` | Fixed version refreshed in place; 274 paths / 466 operations; checked removal of one invalid default |
| #85 | Expanded audit progress | Source revisions, completed imports and Atlas validator/dialect blocker recorded |
| #86 | Numeric vendor release discovery; Intercom/Sentry monitoring | Catalog and artifact pinned to one commit; 35 local/CI tests; 17 artifacts / 16 services registered |
| #87 | Sentry public Web API `v0` | Fixed version refreshed in place; 151 paths / 245 operations; 4 paths / 11 ops added, none removed |
| #88 | Intercom `2.16` | New directory; 168 paths / 235 operations; 62 paths / 85 ops added, none removed; reporting parameter patch replayed |
| #89 | Fork contribution and maintenance documentation | Distinguishes actual fork import process/coverage from upstream publication and guidance |
| #90 | Readable audit reports and three Snowflake registrations | Markdown artifact and job summary, per-row comparison bases, retained success dates; 39 tests pass locally and in CI |
| #91 | Snowflake Database `0.0.1` | New resource API; 15 paths / 18 operations; two-file bundle, zero warnings, no patches |
| #92 | Snowflake Schema `0.0.1` | New resource API; 7 paths / 10 operations; two-file bundle, zero warnings, no patches |
| #93 | Snowflake Table `0.0.1` | New resource API; 19 paths / 22 operations; two-file bundle, zero warnings, no patches |
| #94 / #98 | Maintenance progress | Snowflake and source-health checks, audit evidence and remaining queue recorded |
| #95 | Live repository-health checks | Exact metadata snapshots, archived/disabled/identity findings, import guards and retained success dates; 47 tests pass locally/CI |
| #96 | Accurate repeat-import provenance | Record the current stored curation baseline instead of an older manifest fallback; 48 tests pass locally/CI |
| #97 | Intercom `2.16` wording refresh | Two vendor contact-verification descriptions; version, 168 paths / 235 operations unchanged |
| #99 | Reproducible Swagger conversion; Grafana/Square monitoring | Locked converter, zero-default warning/patch expectations, response/path safeguards, format-chain provenance; 57 tests pass locally/CI; 22 artifacts / 21 services registered |
| #100 | Grafana `0.0.1` content refresh | New certificate field, ASN.1 documentation and RBAC wording; fixed version, 207 paths / 314 operations unchanged; zero converter warnings/patches |
| #102 / #103 / #104 | Current baseline tracking; Plaid/Intercom refreshes | 61 tests; reviewed baseline advances with imports; Plaid 1.762.0 and Intercom company-deletion clarification; details in §9 |
| #105 | Baseline/import audit progress | 22-source audit evidence and next-run queue |
| #106 | ECMAScript and cyclic-schema validation | Pinned validator/regex engine; scoped cycle guard; 69 local/CI tests; Cohere's empty union now correctly blocks import |
| #107 | MongoDB Atlas Admin `2.0` | Fixed version refreshed; 339 paths / 549 ops; 6 paths / 8 ops added, none removed; no source patches |
| #109 | — | Registered official Snowflake View / Stage sources and lifecycle evidence; 69 local/CI tests pass |
| #110 | Snowflake View `0.0.1` | New, 5 paths / 7 ops; entry + common.yaml bundled, no warnings/patches |
| #111 | Snowflake Stage `0.0.1` | New, 4 paths / 6 ops; entry + common.yaml + common-file-format.yaml bundled, no warnings/patches |
| #113 | Discord HTTP monitoring | Official stable-public v10 artifact registered; description remains preview-labelled; 69 local/CI tests pass |
| #114 | Discord HTTP `10` authorization refresh | GET channel messages now permits OAuth2 as an alternative to BotToken; 153 paths / 246 ops unchanged |
| #116 | Datadog v2 monitoring | Existing official public SDK-generation source registered; vendor unstable annotations retained; 69 local/CI tests pass |
| #117 | Datadog v2 `1.0` refresh | 1042 paths / 1647 ops; 35 paths / 57 ops added, one path / op retired; fixed version, no source patches |
| #119 | Security requirement validation / Meraki monitoring | Scheme-name resolution across document, operations, callbacks and webhooks; 74 local/CI tests; native Meraki import blocked on undefined OAuth |
| #121 / #122 | Snowflake Task monitoring / `0.0.1` addition | New distinct resource API, 13 paths / 16 ops; two-file bundle, no warnings/patches; deprecated graph routes retained |
| #123 | GitHub REST review re-request endpoint | Both public artifacts: one path / operation added, 816 paths / 1232 ops; no removals, fixed version |
| #124 | DigitalOcean ADK documentation deprecation | Three parsed source changes, documented enums narrowed; runtime values still accepted per vendor; 515 paths / 757 ops unchanged |
| #126 / #127 | Twilio classic REST monitoring / refresh | Declared version reset to 1.0.0; 121 paths / 197 ops, +3 paths/ops and private healthcheck omitted; history retained |
| #129 | Twilio Messaging monitoring | Public resource-management artifact, including vendor-labelled Public Beta configuration; 30 registered artifacts / 29 services |
| #130 | Twilio Messaging delivery guard | Fully validated 32-path / 58-op import retained locally; owner review needed for published example flagged by push protection |
| #132 / #133 | Twilio Verify v2 monitoring / refresh | 33 paths / 57 ops, four private-beta Passkeys additions, none removed; actual vendor 1.0.0, history/curation retained |
| #135 | Asana REST monitoring / response-code key repair | Maintained official source replaces archive; checked JSON representation; 79 tests pass |
| #136 | Asana REST `1.0` refresh | Fixed version; 177 paths / 251 ops; 52 paths / 87 ops added, one path / three ops moved/renamed; curation retained |
| #138 | Vercel REST monitoring / bounded validation diagnostics | Hosted invalid artifact guarded; exact nested schema/default/ref pointers; 83 local/CI tests pass |
| #140 / #141 | Zoom Meetings monitoring / vendor `2` addition | Distinct current product; 131 paths / 186 ops, checked documented enum repair; legacy broader Zoom retained |

GitHub's refresh adds 322 paths / 488 operations and removes 58 paths / 102 operations
in each artifact. These removals are present in the official source, including retired
Projects classic, team discussions, tag protection, and product billing endpoints, plus
path changes for environment secrets/variables and Pages deployments. The full removed
path list and vendor retirement links are in #65. Other GitHub products were not refreshed.
Both source files and metadata-preserving imports passed full validation and parsed YAML
content comparisons; #65's GitHub test run passed.

Xero adds 8 paths / 15 operations and drops the 2 Employees paths / 4 operations in its new
release. Its documented boolean patch is described in §4. #66's 16 tests passed locally
and in GitHub CI, and the serialized Xero import passed full validation and comparison.
After #67, a fresh updater audit against `origin/main` at `8e40681fb` reported
`matches_source` with no validation errors for both GitHub artifacts, Plaid, Xero, and
Hugging Face Inference Endpoints. This confirms the patched comparison does not keep
proposing Xero's already-imported release.

DigitalOcean adds 338 paths / 473 operations and removes 6 paths / 6 operations. Four
registry paths move under `/repositories/`, retaining operation IDs; two App Platform
tier paths were removed from the official source and marked deprecated in its own SDK.
The reproducible build selects 3,134 data files from vendor commit
`0267e38174220ec9ae115185ccb9717b3909c89a`. Its 21 naming warnings disambiguate different
definitions sharing basenames. Comparison with the official published bundle found no
reference-resolved API or shared-component content differences; only 14 generated aliases
have different names between bundler versions. Two invalid GenAI `stop` null defaults are
removed by a checked recipe, preserving all declared alternatives and nullable annotations.
The bundled source and final YAML passed full validation and curation/content comparisons.

Snowflake SQL and Warehouse use vendor commit `990e25d97236a11826c9eed40e587c2b859e5680`.
Warehouse's two-file bundle has no patches or warnings. Both serialized specs passed full
validation and source-content comparison; both source registrations passed 21-test CI.
Other Snowflake services remain to be audited; these additions do not cover its whole API.
Fresh local checks after #72 report `matches_source` with no validation errors for
DigitalOcean and both Snowflake services. A full GitHub audit is recorded in §9.

**Snowflake core-resource additions (#91–#93):** Database, Schema and Table use the same
official vendor commit `990e25d97236a11826c9eed40e587c2b859e5680`, with declared version
`0.0.1` retained verbatim for each service. The repository was unarchived when checked on
2026-10-02. These distinct APIs are listed in the generally available REST reference;
their individual public guides and source artifacts have no preview designation. Each
bundle contains only its own entry plus `common.yaml`, with zero warnings and no patches
or version conversion. Shared helper files are not additional APIs. The serialized
imports match the cached vendor bundles, retain all original path/operation counts and
pass complete validation with no external references. No new curation was invented.

The documented public guides are
[Database](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/databases/db-introduction),
[Schema](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/schemas/schemas-introduction),
and [Table](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/tables/tables-introduction).
Snapshot hashes respectively: `f6d644eee01cc2e9a3cdda65004c7dd3b294de32ce67b74ffb8cf831b93f86d1`,
`08d1eb8d0ace124c5bcee97d79786314e6839aea6ab17e5a17e9e10548411309`, and
`bef7f216bc08a628ffaf339d427ecc0062fec846d6b22f9e70fd447de967c353`.
The first five Snowflake service descriptions total 56 paths / 68 operations.
View and Stage (#110/#111) bring imported coverage to seven descriptions, 65 paths /
81 operations, as of 2026-10-03.
The [View guide](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/view/view-introduction)
and [Stage guide](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/stages/stages-introduction)
carry no preview designation (checked 2026-10-03). Both are distinct services in the
generally available REST reference. The View guide lists only four core operations;
the [full reference](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/view)
and pinned vendor spec also include set/unset/get tag actions. Retain the complete spec,
not a hand-built slice of the guide. Stage bundles the shared file-format helper too.
Both use commit `990e25d97236a11826c9eed40e587c2b859e5680`, declare `0.0.1`, and pass
full validation, pinned bundling (zero warnings), raw hash and typed YAML roundtrip
checks, plus full bundled-content equivalence. No source patches, conversion or curation
were added. View entry/snapshot hashes: `d0798ce6502634ee22625a1a6229b2ca494e94001b8b50594420e649343c86e6` /
`7ac9ef64f84a51fe952145630f84a5126e71186b82f956b7e49603df4010557e`.
Stage entry/snapshot hashes: `85634e14fda822de7354f90fe9829f1b8a46d12efcecd2f45916185c6db6881e` /
`a7436cc6afa9dbd8f4e8a123743649a3561dbc7986ddcf36f3c6bda201f0b563`.

Remaining catalog products need their own release/scope review; do not blindly import
every filename, preview-only resource or compatibility description.

---

**Support delivery prepared on 2026-10-05:** [API PR #196](https://github.com/ontola/openapi-directory/pull/196) is a draft with only the new API and these progress notes; mark ready after updater #195 CI/merge, then recheck exact head/files/CLEAN/MERGEABLE before merge. Do not duplicate this PR. Separate updater
[#195](https://github.com/ontola/openapi-directory/pull/195) adds conservative unused
pointer guards and a checked compatibility recipe; 106 local tests pass, exact-head
CI run 37362766037 is queued. The API-only branch `codex/zendesk-support-api-only`
adds official Support/Ticketing 2.0.0, native 3.0.3, **455 paths / 657 operations**,
2,534 resolved local refs, zero external refs. All endpoint/auth/server/role/plan/tag/
deprecation content remains. Only the documented null-only alternative and the exact
unused invalid UserLogin parameter are corrected, plus provenance. Do not merge this
API before #195 CI/merge; no infrastructure changes are duplicated in its PR diff.

Original source SHA-256
`3258ec97eed69d58deceee500efe090ea0e0b16fd616dddf15107ab209688fdc`, recipe SHA-256
`38d1641799c8a082fdb21f71f500b400e1bd9f752b5e6024e60eaa0dff2b47e5`.
Independent full native/prepared/import comparisons, complete validation and typed
YAML roundtrip pass; no version conversion or invented curation. Native basic-only
security remains a documented limitation relative to current public OAuth guidance.
All four deprecated operations and API-token lifecycle prose retained. Original raw
bytes cached unchanged; hosted source health unassessed and no Git revision claimed.
Detailed implementation/import/audit progress is also retained on pushed branch
`codex/add-zendesk-support` at `2a61ee7eb`, based on updater head `d4f05b3ec`.
The separate API-only branch avoids including pending infrastructure in its diff.

Full **53-source local audit** at the prepared API commit `dd7b9568238c` (not main)
finds **42 matches / 11 known blocks / no new unblocked drift or fetch/prepare failure**.
All source/26 repository metadata hashes, per-row bases/profiles, endpoint deltas and
Markdown/JSON parity checked; 14 hosted sources unassessed. Support matches its
pending import, Atlas its delivered refresh. Only Stripe repository revision advanced
(`3d9ffbb79e0ff25254c498b3b7623f710401a1fb`), independently re-fetched pinned bytes
unchanged. Preserve the earlier 52-source CI snapshot as historical. Durable ignored
report/review `cache/maintenance/reports/zendesk-support-53-local-dd7b9568238c/`;
verifier/log `/tmp/verify-zendesk-support-53-local-audit.py`,
`/tmp/zendesk-support-53-local-audit-verification.log`; import review/verifier/log
`/tmp/zendesk-support-import-review.json`, `/tmp/verify-zendesk-support-import.py`,
`/tmp/zendesk-support-import-verification.log`. Existing Conversations/Messaging
owner choices remain unanswered; neither rejected push retried or redacted.

**Anthropic discovery lead checked, no import:** search snippets still show an old
Stainless GCS spec URL in official SDK `.stats.yml`. Fresh pinned TypeScript
`d49bdab458000bcdffe77bd84b03293f31824fb3`, Python
`18f25547f20cf5f01da69ac611e700e3bc9ebf21` and CLI
`f8457f464b72d3ac54a13f45a90e1e686d724dcb` all publish only configured-endpoint counts
in that file; the pointer has been removed. All three repos are public/unarchived/
undisabled; complete untruncated filename trees contain no OpenAPI/Swagger artifact
names. Do not register the older search-snippet URL as a maintained current source
or reconstruct a spec from generated SDK types. This is a bounded search result,
not proof the vendor publishes no spec anywhere. Original metadata/stats/tree bytes
and hashes retained under ignored `cache/maintenance/discovery/anthropic/`; review
`/tmp/anthropic-live-sdk-publication-review.json`. Continue current official-source
publication discovery separately. Attachment cap: verified merged superseded
AGENTS-only #60 and #194 unlinked; GitHub history/API/updater attachments retained.

---

**CI infrastructure failure and bounded retry:** updater #195 run 37362766037
attempt 1 ended failure because the hosted job was never assigned a runner: GitHub's
annotation says "The job was not acquired by Runner of type hosted even after
multiple attempts". Test steps/logs never existed; this is not a test assertion
failure or an approval-review rejection. Same exact head was retried once with
`gh run rerun --failed`; attempt 2 also failed on 2026-10-05 19:53 UTC with the
same hosted-runner acquisition annotation and zero test steps. Both attempts ended
before executing tests. Keep #195 unmerged and API #196 draft until the actual job
passes; 106 local tests and full independent API validation remain successful. Do not waive CI, change runner/power/host settings,
or repeatedly retry during a hosted-runner outage. Recheck the existing run on the
next heartbeat; if still unavailable, preserve ready work and continue independently.
Failure annotation `/tmp/zendesk-support-guards-ci-runner-failure.json`;
run/job state `/tmp/zendesk-support-guards-ci-status.json`; retry annotation/final state
`/tmp/zendesk-support-guards-ci-retry-runner-failure.json`,
`/tmp/zendesk-support-guards-ci-final-run.json`. Durable ignored failure evidence
`cache/maintenance/reports/zendesk-support-53-local-dd7b9568238c/ci/`.

**New official Coinbase CDP candidate (discovery/diagnostics only):** maintained,
public/unarchived/undisabled `coinbase/cdp-sdk` at
`d40fb3975395033409643654faacfb3d4e4349ee` publishes root `openapi.yaml`; its pinned
Makefile links the canonical CDN `https://drla6sbl8l00t.cloudfront.net/openapi.yaml`
and adds a timestamp query to avoid stale caching. Root SDK snapshot is **native
3.1.0 / 2.0.0 / 126 paths / 154 ops**, hash
`229ed860a74b63b3c430c4fc2122e2870bcc0f7b398398d2ec31021be9e1ee4a`.
Fresh official CDN, both plain URL and timestamp-busted URL, has identical typed
content and hash `156440e9f8df1eb23aa0c30c78157dbe8fbd4e96929f2c1ff0b409963f704302`:
**140 paths / 169 ops / 2,594 resolved local refs**, none external. It adds 14 paths /
15 operations versus the SDK snapshot (delegation revoke and payment mandates),
removes none. Do not choose the lagging SDK artifact merely to get a convenient
Git revision or freeze the old source. Source choice/cache freshness must be reviewed.

Current [public introduction](https://docs.cdp.coinbase.com/api-reference/v2/introduction)
distinguishes non-custodial public APIs from custodial groups needing verified business
accounts, Prime-only payment methods and Beta groups. Artifact retains private-beta
fiat deposit destinations and complete native auth/tenant/permission/lifecycle content.
No blanket GA claim, financial action or endpoint trimming. This is CDP v2, not
Coinbase Exchange or all Coinbase APIs. Coinbase provider is absent from main's tree.

Native CDN validation fails on four Parameter Reference Objects with unsupported
`required:false` siblings pointing to `#/components/parameters/XDeveloperAuth`.
The referenced header parameter itself declares exactly `required:false` already.
Diagnostic removal of only those four redundant flags fully validates and passes
typed YAML roundtrip; auth/requiredness and all referenced constraints remain.
Diagnostic inlining also validated but is not adopted. A future exact recipe should
remove only those four original false values after complete referenced-parameter
assertions and exact reference contexts, prove positive/negative requiredness and
reject vendor fixes/new requiredness. No recipe, registration, API PR or imported
file yet; outside the configured 53-source audit. Do not fabricate missing schemas,
relocate auth or infer optionality without the reviewed target.

Complete original repo metadata/commit/tree/README/Makefile and native SDK/CDN bytes,
retrieval headers/hashes and reviews cached under ignored
`cache/maintenance/discovery/coinbase-cdp/`. Scripts/logs/reviews
`/tmp/discover-coinbase-cdp.py`, `/tmp/review-coinbase-cdp-official-spec.py`,
`/tmp/review-coinbase-cdp-cdn-and-ref-siblings.py`,
`/tmp/review-coinbase-cdp-current-publication.py`,
`/tmp/coinbase-cdp-current-publication-review.json`,
`/tmp/coinbase-cdp-current-publication-review.log`.

---

## 3. Triage progress

Working dataset was `/tmp/all_issues.tsv` — **this is in `/tmp` and will not survive a reboot.** Regenerate with:

```bash
gh api --method GET "repos/APIs-guru/openapi-directory/issues?state=open&per_page=100" --paginate --jq '.[] | select(.pull_request == null) | [.number, .created_at, .comments, .title] | @tsv' | sort -t$'\t' -k2 > /tmp/all_issues.tsv
```

1991 rows, oldest first (#42 from 2016 → #3395 from 2026-09-22).

Batches read in full: rows 1–375, i.e. issues **#42 through #1578**. Everything relevant from those is either done (§2) or parked (§5).

Rows 376–1991 (#1580–#3395) were **not** read line by line — they were keyword-swept for known vendor names instead. **Conclusion: don't bother reading them.** That range is essentially one automated third-party *scraper* spam campaign — hundreds of near-duplicate "Add LinkedIn / Reddit / TikTok / Amazon / Shopify / GitHub Intelligence API" submissions, auto-reposted in bursts at :30 past the hour. None are the platforms' own APIs. Even the "Stripe Radar Rules API" issues are part of it (body is two lines, no URL).

Only two genuine signals in that entire range:
- [#2393](https://github.com/APIs-guru/openapi-directory/issues/2393) — Google specs stale repo-wide (Sheets v4 untouched 3 years). Same family as #611 / #1189 / #1300.
- [#2444](https://github.com/APIs-guru/openapi-directory/issues/2444) — Google Health v4; the discovery URL does resolve (HTTP 200).

---

## 4. Next up — the agreed direction

Batch triage was abandoned as low-yield. The user agreed the better lead is a **direct coverage-gap audit**, and gave the go-ahead to take the list "the same way as PayPal: one PR per API".

**The vendor table below was partly wrong and has been corrected.** Three entries labelled "new" already existed in the repo. The original audit used `[ -d "APIs/$d" ]` inside the worktree — and **the worktree has sparse-checkout enabled**, so almost nothing is materialized on disk and nearly every vendor reads as "missing". This is the same class of mistake as #40.

### ⚠️ Audit correctly, against the index — not the working tree

Sparse-checkout means `ls`/`[ -d ]`/`find` under `APIs/` are all unreliable here.
Check `git sparse-checkout list` first. Fetch main and audit its tree, rather than a
possibly stale feature branch's index:

```bash
git fetch origin main
git ls-tree -r --name-only origin/main APIs | cut -d/ -f2 | sort -u > /tmp/have_domains.txt
for v in stripe square figma sentry pagerduty docusign mongodb grafana shopify okta \
         intercom hubspot salesforce zendesk notion airtable heroku snowflake elastic \
         hashicorp coinbase dropbox newrelic anthropic huggingface nvidia; do
  printf "%-14s " "$v"; m=$(grep -i "$v" /tmp/have_domains.txt | tr '\n' ' ')
  [ -n "$m" ] && echo "HAVE: $m" || echo "missing"
done
```

After PR #93 on 2026-10-02: 729 distinct provider domains, 4,260 tracked files under `APIs/`.
To add a new spec you must first widen the cone: `git sparse-checkout add APIs/<domain>`,
otherwise `git add` refuses with "paths ... outside of your sparse-checkout definition".

### Verified live official specs (HTTP 200 confirmed 2026-09-22)

| Vendor | Source | Status |
|---|---|---|
| **Stripe** | `.../stripe/openapi/master/latest/openapi.spec3.yaml` | **REFRESHED, PR #83**, `2026-09-30.endive`, 454 paths / 644 ops. Vendor-recommended public GA v1+v2 artifact; prior #44 used the maintained v1-only `openapi/spec3.yaml`. Use YAML, excluding preview and SDK variants. |
| Figma | `.../figma/rest-api-spec/main/openapi/openapi.yaml` | **REFRESHED, PR #82**, `0.43.0`, 47 paths / 54 ops. OpenAPI 3.1.0; historical `0.42.0` preserved. |
| Sentry | `.../getsentry/sentry-api-schema/main/openapi-derefed.json` | **REFRESHED, PR #87**, fixed `v0`, 151 paths / 245 ops. Vendor dereferenced artifact; inlining is upstream's doing. Weekly content checks registered in #86. |
| PagerDuty | `.../PagerDuty/api-schema/main/reference/REST/openapiv3.json` | **REFRESHED, PR #84**, fixed `2.0.0`, 274 paths / 466 ops. Checked invalid-default removal is registered with the source. |
| MongoDB Atlas | `.../mongodb/openapi/main/openapi/v2.json` | **REFRESHED, PR #107**, fixed `2.0`, 339 paths / 549 ops, as `mongodb.com/atlas-admin/2.0`. Validator/dialect compatibility resolved in #106; no source patches. |
| Grafana | `.../grafana/grafana/main/public/api-merged.json` | **REFRESHED, PR #100.** Canonical Swagger 2.0, monitored through #99's locked conversion recipe, zero warnings/patches. Fixed placeholder `0.0.1`, 207 paths / 314 operations. This legacy artifact does not cover every new `/apis` resource or Grafana Cloud. See the push-protection note below. |
| Square | `.../square/connect-api-specification/master/api.json` | Stored refresh #51; **monitoring registered #99**, direct OpenAPI 3.0.0. Fixed `2.0`, 253 paths / 332 operations. Three source metadata additions detected, but refresh blocked by two missing vendor schemas; do not invent them. |
| DocuSign | `.../docusign/OpenAPI-Specifications/master/esignature.rest.swagger-v2.1.json` | **DONE, PR #52** — a *refresh*, we already had `docusign.net/v2.1`. Swagger 2.0. |
| Intercom | `.../intercom/Intercom-OpenAPI/main/descriptions/2.16/api.intercom.io.yaml` | **REFRESHED, PR #88**, public `2.16`, 168 paths / 235 ops. #86 discovers numeric release directories; preview directory `0` excluded. Historical `2.14` preserved. |

**October follow-up audit:** all four newly registered vendor repositories were checked
on 2026-10-02 and were maintained/unarchived. #81 registers their moving official sources,
so future release/schema changes are checked weekly instead of relying on old import dates.

**Stripe source selection:** vendor commit `6f855712dfc6a235a407136e630bf36a01c069a3`.
The repository's README now recommends `latest/openapi.spec3.yaml` for public GA v1+v2
coverage. The old `openapi/spec3.yaml` is still maintained but v1-only. At the same commit,
the selected artifact retains all 431 v1-only paths / 612 operations and adds 23 v2 paths /
32 operations. Shared v1 path items differ only by 1,079 explicit `explode` annotations;
every one matches its OpenAPI-defined default. Compared with stored Dahlia, #83 adds
35 paths / 50 operations and removes none. Historical versions and curation are preserved;
no API patches or conversion. Do not accidentally switch back to the v1-only artifact or
select preview/SDK variants.

**Figma:** vendor commit `2a90e5adc67d8117d7c2da624f03a9bfa3027fb6`. `0.43.0` adds
`VariableComposedColor` to variable-value unions and `COLOR_OPACITY` to the scope enum,
despite unchanged endpoint counts. It passes full OpenAPI 3.1 and serialization checks.
The vendor labels its description itself beta; this is its public REST artifact.

**PagerDuty:** vendor commit `6ab7c72fb78ff76ba65670795a51d925c8b4df12`. #84 adds
`GET /incidents/{id}/scribe_transcripts`, with no path/operation removals. The source assigns
the invalid string default `20 - incident_summary` to the integer `sre_memories_limit`
parameter (range 1–100). `maintenance/patches/pagerduty.json` removes only that exact
default after type/range/value assertions. No replacement default or server behavior is
inferred. The complete patched source validates and round-trips; a simulated vendor fix
to integer `20` stops replay for deliberate recipe review.

**MongoDB Atlas blocker resolved (#106/#107):** the old validator recursed while collecting
properties through cyclic compositions. Diagnostic 0.9.0 initially rejected ECMAScript
regex syntax through Python regex, then exposed the same property-collection cycle once
the official `ecma-regex` extra was installed. #106 pins OpenAPI spec/schema validators
0.9.0 and regress 2026.9.1. Its scoped subclass iterates the same upstream property edges
with a resolved-object cycle guard; no schema constraints are removed, recursion limit
raised, global classes monkey-patched or formats disabled. The document backend is
explicitly Python jsonschema. Pattern syntax/default matching uses ECMAScript with no
flags, tested against Node (named captures, identity escapes, Unicode-property escape
behavior). Do not infer Unicode mode universally; it changes semantics and rejects some
vendor identity escapes. Missing backends/changed reviewed engine pins fail validation.
69 regressions pass locally and in GitHub CI. Python 3.10+ is now required; CI uses 3.11,
and the clean local environment is `/tmp/openapi-maintenance-ecma` (bundled Python 3.12).
The older Python 3.9 venv does not satisfy these dependencies; recreate rather than
silently using it. `maintenance/requirements.txt` is the reproducible dependency source.

#107 refreshes the fixed `2.0` Atlas Admin file from 333 paths / 541 operations to 339 / 549,
adding six paths / eight operations and removing none. Private endpoint connection strings,
Stream Processing workspace private endpoints and ephemeral clusters account for the
added paths; vendor schema/parameter/documentation changes also remain. Source commit
`ab07390d4ef9ba960d467a156ef99d5e0afb4e10`, entry SHA-256
`db2c6f2500a5f05fc74f8dd818db4f9db38d0e67140a6b9ce82364e9738cca66`.
Complete validation, parsed vendor-content equivalence, curation preservation and YAML
round-trip pass without source patches or OpenAPI conversion. Provenance records the
validation profile. This is Atlas Administration only, not every MongoDB product.

**Newly exposed Cohere defect:** validator 0.9.0 correctly rejects the existing official
`components.schemas.TruncationStrategy.oneOf: []`, with an empty discriminator mapping.
The same invalid empty union is present at official source commit
`734aafbe1fe2ca5c7356609009ec0d9b74e6ac57`; live re-fetch/source comparison confirms it.
Its description claims a default of 'none', but no union variants are defined there.
Cohere still matches its source; a matching hash is not successful validation. Do not
invent alternatives or waive validation. Look for a vendor correction or a separately
reviewed, exactly checked correction with demonstrated semantics. Keep the existing
import in place; no destructive removal or new Cohere refresh PR was created.

**Intercom release discovery and import:** official
[introduction](https://developers.intercom.com/docs/references/introduction) and
[changelog](https://developers.intercom.com/docs/references/changelog) select public `2.16`
and distinguish Preview. Vendor repository `intercom/Intercom-OpenAPI` was maintained and
unarchived on 2026-10-02. #86 adds a reviewed `numeric-directories` recipe: select canonical
major.minor releases numerically from the pinned `descriptions` catalog, exclude releases
below `2.16` and prerelease names (Preview is `0`), and require `info.version` to match.
The complete original catalog response/hash is cached alongside the artifact and included
in import provenance. Empty, inconsistent, truncated or failed catalogs block instead of
falling back to an old version. Combined catalog/bundling or code-sample recipes still
require explicit support. Verify a future selected release against official docs before
manual import/merge; numeric selection alone is not universal evidence of stable status.
Tests cover ordering, unsafe paths, exclusions, failure, revision pinning, cache evidence
and mismatched declared versions. All 35 tests pass locally and in #86's CI.

#88 imports vendor commit `6d8b0b8d27a779a6005716249ed21755f29292d9`, adding 62 paths /
85 operations with none removed. The vendor's two reporting status/download operations
still omit required `job_identifier` path declarations. The exact recipe
`maintenance/patches/intercom.json` prepends the same required string declaration used
in #54, preserving all original header/query parameters and asserting their complete lists
plus operation summaries/tags. A simulated vendor correction stops replay. The complete
patched source and serialized import validate and preserve values/types and curation;
historical `2.14` is unchanged. The vendor changelog describes breaking schema changes
between API releases, so no old version is replaced or declared equivalent.

**Sentry refresh:** maintained/unarchived `getsentry/sentry-api-schema` was checked on
2026-10-02; vendor commit `41d82c69208a3f24dafa36f584cca981d30cfde5` grows fixed `v0` from
147 paths / 234 ops to 151 / 245, adding four project codeowner/inbound-filter paths and
eleven operations, removing none. #87 preserves vendor schema/description changes,
including experimental labels, without API patches or conversion. The parsed import
matches the official cached source and passes full validation and serialization checks.
This is the public Web API artifact, not Sentry's SDK ingestion protocol or whole platform.

**Square and DocuSign are the cautionary entries here.** Both were originally recorded as
"new" by an audit that ran `[ -d "APIs/$d" ]` inside a sparse-checkout worktree. Both were
in fact already present, and both needed **in-place refreshes** (their vendors pin
`info.version` forever, so the new-directory rule cannot apply and the diff carries real
deletions). Audit against the index, per the warning above.

#### Grafana: GitHub push protection (resolved, but it will recur)

`git push` is rejected with `GH013 / GITHUB PUSH PROTECTION — Grafana Project Service
Account Token`, pointing at `APIs/grafana.com/0.0.1/openapi.yaml:14966`. That line is:

```yaml
key:
  type: string
  example: glsa_<REDACTED IN THIS DOC>_<8 hex>   # upstream spells out i-N-V-a-l-i-D repeatedly
```

It is a **false positive**: a deliberately fake placeholder published by Grafana in their
own public spec — the body of the value literally spells "invalid" over and over — which
happens to carry the real `glsa_` prefix the scanner keys on. It is not a live credential.

(The literal value is redacted *in this document* only because quoting it verbatim makes
this file itself unpushable. The spec file on `add-grafana-api` still has it as published.)

On 2026-09-22 the repo owner reviewed it and allowed it via the unblock URL, so #50 is
merged with the example byte-for-byte as Grafana publishes it. **Expect this again** — vendor
specs routinely carry fake example credentials that match real patterns. Two ways forward,
both the user's call:
1. **Allow it** via the unblock URL in the push error (repo owner only) — keeps the vendor spec byte-for-byte as published.
2. **Redact the example** — but that means editing vendor content, which cuts against how every other spec here was added.

Do not bypass push protection unilaterally.

### Elastic — two specs, two different version problems (DONE, #55 / #57)

Elastic ships **both** files with `info.version` empty. They were solved differently, and
the difference is the point:

- **Stateful** (`elasticsearch-openapi.json`) → `elastic.co/9.5`. The repo has release
  branches (`7.14` … `9.5`), so fetch from the branch for the release you want and set
  `info.version` to match. The version is **sourced**, not invented.
- **Serverless** (`elasticsearch-serverless-openapi.json`) → `elastic.co/serverless/2026-09`.
  Rolling product, no release branches, nothing to borrow. `2026-09` is a **snapshot date we
  chose**, and `x-conversion` says so in as many words — a bare date in a version directory
  otherwise reads exactly like a real vendor date-version (Stripe's `2022-11-15` is one).
  **Refresh by adding a new date directory, never in place**: with no version to diff
  against, an in-place edit silently destroys the only evidence of when the file was current.

Neither has a `servers` block, because Elastic publishes none — Elasticsearch is self-hosted
and the base URL is the user's own cluster. Left absent rather than inventing a host.

### HubSpot — 122 catalog entries, 59 real specs (DONE, #58)

`https://api.hubspot.com/public/api/spec/v1/specs` is a **catalog index**, not a spec. The
122 headline number is misleading in two separate ways:

| Step | Count |
|---|---|
| Products in catalog | 122 |
| …with a **STABLE** version | 93 |
| …minus 34 per-object CRM slices | **59 imported** |

- **29 products are pre-release only.** No stable version at all. The internal test APIs
  (`At Tests`, `At Debug`) fall out here too, so no special-casing was needed for them.
- **35 of the 93 are not distinct APIs.** They are one generic CRM endpoint re-emitted per
  object type: Contacts is `/crm/objects/2026-03/contacts`, Deals is the identical shape at
  `/crm/objects/2026-03/0-3` (HubSpot's internal numeric object-type id). Same six
  operations each.
- **One of the 35 was kept**: `Custom Objects`, the only one exposing
  `/crm/objects/{version}/{objectType}` as a genuinely templated path. Beware when
  re-deriving this — a filter for `{objectType}`/`{fromObjectType}` anywhere in the paths
  matches 28 of them, because most carry a templated *associations* sub-path. Match on the
  object-collection path itself.

### Still to do

- **Monitor the refreshed priority APIs below**, extending the reusable updater in §9.
  All four confirmed stale APIs are done: Plaid #63, GitHub REST #65, Xero #67, and
  DigitalOcean #70. The table retains the original audit snapshots, not current stored counts.
- **Extend the official coverage audit.** Hugging Face Inference Endpoints (#62), Snowflake
  SQL/Warehouse (#71/#72), Cohere (#76), and Mistral (#77) are done. Audit remaining
  distinct stable Snowflake services and other well-known providers before importing more.
- **Extend the refresh audit across the rest of `APIs/`.** The October check was a sample,
  not a complete audit. Compare content as well as versions and path counts.
- **Locate specs for the vendors below**, minding the 404 warning.
- **HubSpot's 34 per-object CRM slices remain deliberately skipped.** Do not expand this
  scope without a fresh user instruction.

### Initial confirmed refresh queue (2026-10-02 audit; all four now refreshed)

| API | Stored version / paths | Source version / paths | Official source |
|---|---|---|---|
| GitHub REST | `1.1.4` / 551 | `1.1.4` / 815 | [api.github.com.json](https://raw.githubusercontent.com/github/rest-api-description/main/descriptions/api.github.com/api.github.com.json) |
| DigitalOcean | `2.0` / 183 | `2.0` / 515 | [DigitalOcean-public.v2.yaml](https://raw.githubusercontent.com/digitalocean/openapi/main/specification/DigitalOcean-public.v2.yaml) |
| Plaid | `2020-09-14_1.345.1` / 201 | `2020-09-14_1.740.1` / 360 | [2020-09-14.yml](https://raw.githubusercontent.com/plaid/plaid-openapi/master/2020-09-14.yml) |
| Xero Accounting | `2.9.4` / 132 | `19.1.0` / 138 | [xero_accounting.yaml](https://raw.githubusercontent.com/XeroAPI/Xero-OpenAPI/master/xero_accounting.yaml) |

GitHub's `api.github.com.2022-11-28` counterpart was included in #65 and is now registered
alongside the default public artifact. Audit other GitHub products separately.
DigitalOcean's relative references are now handled by its registered pinned bundling recipe.
Copying only the entry file remains insufficient. Future imports must use the updater.
The counts include all path entries, not necessarily one operation per path. New paths
and removed paths must be reported separately; net growth can conceal removals.

**Plaid completed:** PR #63 added `2020-09-14_1.740.1` with 360 paths / 351 operations,
preserving the historical version and curation. **Xero completed:** PR #67 added `19.1.0`
with 138 paths / 235 operations, preserving the historical version and curation. The official
`19.1.0` source has 23 boolean properties with string defaults/examples `'false'`, starting
with `Account.HasAttachments`. The recipe in `maintenance/patches/xero-accounting.json`
fixes exactly those 46 values, asserting the original string and sibling `type: boolean`.
It was verified against vendor commit `fd9d44b04bf4934a7509b8e7ece51a9e0e462e4f`.
The complete patched source passes validation. If a future vendor source fixes a value or
changes its type, the recipe intentionally fails and needs review; remove or revise it
deliberately. Never disable validation or coerce arbitrary vendor values.

**DigitalOcean completed:** #70 refreshes fixed version `2.0` in place. The recipe in
`maintenance/patches/digitalocean.json` removes only the two invalid null defaults in
`chat_completion_request.stop` and `create_response_request.stop`, after asserting their
source values and complete `oneOf` alternatives. It invents no replacement defaults or
server behavior. A changed bundler warning count (currently 21) or patch precondition stops
the updater for review. Logs, original data, source hashes, and the bundle remain cached.

### Verified missing official OADs (downloaded and parsed 2026-10-02)

| Provider | Official source | Import notes |
|---|---|---|
| Snowflake | [specifications directory](https://github.com/snowflakedb/snowflake-rest-api-specs/tree/main/specifications) | SQL `2.0.0` (3 paths / 3 ops), Warehouse `0.0.1` (12 / 15), Database (15 / 18), Schema (7 / 10) and Table (19 / 22) are DONE in #71/#72/#91–#93. View (5 / 7) and Stage (4 / 6), also `0.0.1`, are DONE in #110/#111. Stage also bundles common-file-format.yaml. Audit remaining distinct public APIs separately; helper files are not APIs. |
| Cohere | [cohere-openapi.yaml](https://raw.githubusercontent.com/cohere-ai/cohere-developer-experience/main/cohere-openapi.yaml) | DONE #76: OpenAPI 3.1, version `1.0`, 32 paths / 42 ops. Seven referenced TypeScript snippets are explicitly materialized as code strings and included in freshness snapshots. |
| Mistral | [official docs repository](https://github.com/mistralai/platform-docs-public) | DONE #77: OpenAPI 3.1, version `1.0.0`, 212 paths / 299 ops. `openapi-public-doc.yaml` is the verified public download; do not substitute or concatenate the separate 131-path `openapi.yaml`. |
| Hugging Face Inference Endpoints | [openapi.json](https://api.endpoints.huggingface.cloud/openapi.json) | OpenAPI 3.1, version `2.0.0`, 40 paths. This describes endpoint management, not the entire Hugging Face Hub or each model's inference API. |

None of these four providers was present at the initial audit, before PR #62 added
Hugging Face Inference Endpoints `2.0.0` (40 paths / 46 operations). All four now have
validated imports; Snowflake's remaining catalog still needs per-service review. Parsing
alone is not completion of reference resolution or spec validation.
Search the full tree by domain, brand, service, and aliases again before adding anything.

**Cohere details:** vendor commit `734aafbe1fe2ca5c7356609009ec0d9b74e6ac57`.
The `code_samples` recipe operates only on Fern operation-level code sample references,
fetches UTF-8 artifacts from the same pinned commit, preserves their text without execution,
and hashes entry plus snippets together. Source snapshot
`a5f38e5f74280d88f3d3a5231c178ebfa05c63674dddb90979cc268973e333c3` includes all seven.
No external references remain. Missing or unsafe snippets block refresh, and snippet-only
changes are detected. PR #75 corrected a live-import fetch-helper contract mismatch after
#74; its regression test exercises the real HTTP helper with a mocked response.

**Mistral selection and patch:** vendor commit `ce5bfddb42fe91b964f88cb16ab42f41bd415501`.
The [publishing script](https://github.com/mistralai/platform-docs-public/blob/ce5bfddb42fe91b964f88cb16ab42f41bd415501/src/scripts/copy-openapi.ts)
explicitly copies `openapi-public-doc.yaml` to the public download. The documentation
build selects the same source; its bytes exactly matched `https://docs.mistral.ai/openapi.yaml`
(SHA-256 `fa73befe1c61e1bf4847c532e6375612ae5c7a4a83f96db4a1087ee0115db8b7`).
This is the full public artifact, including vendor-labeled beta/public-preview APIs,
not a stable-only subset. Nine references and two discriminator mappings in the speech
streaming response point at nonexistent document-root `$defs`, while the vendor's
definitions exist under that response schema. `maintenance/patches/mistral.json` applies
eleven exact checked pointer replacements to those existing definitions; no schemas are
invented. All 1,939 local references resolve after the patch and full validation passes.
Changed source values/context stop replay. Scientific bounds such as `1e-08` are valid
YAML 1.2 numbers; #74 fixes the loader's old string interpretation instead of patching
vendor numeric content. No OpenAPI version conversion was used.

Snowflake's [REST reference](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference)
is generally available, but that umbrella page also lists individual preview products:
[Code Bundles and their REST clients were announced in preview on 2026-09-24](https://docs.snowflake.com/en/release-notes/2026/other/2026-09-24-code-bundles).
Check each service's own release status before importing more catalog entries. Do not
treat compatibility specs named Cortex Generic Anthropic/OpenAI as those vendors' own OADs.

### Source health requires a separate check

Slack's stored spec matches its official source in version and path set, but
[`slackapi/slack-api-specs`](https://github.com/slackapi/slack-api-specs) is archived;
its Web API spec last changed on 2020-10-06. Current Slack docs describe methods absent
from that artifact. Record this as an archived source with incomplete current coverage,
not as a current API merely because re-fetching produces no changes. Look for a maintained
official replacement; do not silently substitute a third-party reconstruction.

PR #95 now checks GitHub repository metadata on every audit and import, independently
of content comparison. It records identity, archive/disabled flags, activity observations,
retrieval time and exact response bytes/hash, deduplicating shared repositories within
each run. `repository_available` means the same public repository is reachable and is
neither archived nor disabled; it does **not** establish vendor ownership, artifact
maintenance or current API coverage. Archive/disabled/identity changes and metadata
failures block imports. Failed attempts preserve the last successful health-check date;
content comparison continues independently. Hosted sources, currently Hugging Face,
remain explicitly unassessed by this repository check. File-specific deprecation and
replacement discovery still need review.

### Missing, official spec not yet located

Shopify, Airtable, Heroku, HashiCorp, Dropbox, New Relic, Anthropic,
NVIDIA. Snowflake and Hugging Face Inference Endpoints now have verified sources above.
Zendesk Support and Coinbase CDP are now imported and monitored (latest resume state
above). Zendesk Conversations has a validated recipe but remains held by push protection.

**Probed and 404'd on 2026-09-22** — these exact URLs, not the vendors themselves:
guessed paths in `snowflakedb/snowflake-rest-api-specs` (`main`, `releases/8.40/...`; resolved
on 2026-10-02 by inspecting the repository's `specifications/` directory),
`zendesk/developer_docs` (`master`, `api-reference/ticketing/oas.yaml`),
`hashicorp/vault` (`main/openapi.json`), `Shopify/shopify-app-js` (`main/openapi.json`),
`dropbox/dropbox-api-spec` (`master/openapi.json`).
Older 404s: `okta/okta-management-openapi-spec`, `api.hubspot.com/api-catalog-public/v1/apis`,
`api.heroku.com/schema`.

> **Read this before trusting any 404 above.** The handoff previously recorded
> `intercom/Intercom-OpenAPI` as dead and said not to retry it. That was wrong: the repo is
> real and current, and only the two *version paths* tried (`descriptions/2.11`, `2.13`)
> were bad. `2.14` resolved fine and is now merged as #54. **A 404 on a guessed path inside
> a vendor repo is evidence about the path, not about the repo.** Check the repo root and
> its branches/tags before concluding a vendor publishes nothing.

Note also that `okta.local/1.0.0` and `salesforce.local/einstein/2.0.1` exist in `APIs/` but
are community submissions, not the vendors' official APIs — a name grep will mislead you in
that direction too.

## 5. Parked — do NOT action without a fresh go-ahead

Each of these was either explicitly declined or deliberately deferred.

- **Google spec regeneration** (#611 OAuth `Oauth2c` malformed security, #1189 Gmail path structure, #1300 DisplayVideo `kpiType` enum, #2393 general staleness, #1356 Vertex AI). User said **"don't do the DisplayVideo regeneration."** This is a systemic ~457-file problem, not per-file typos.
  - **PR #40 was closed for exactly this reason.** Vertex AI was proposed as a new addition; it was actually a *regeneration* — `APIs/googleapis.com/aiplatform/v1/` already exists (the search used "vertex"; the dir is `aiplatform`). It would also have stripped curated metadata. The conversion itself worked (214 paths / 271 ops / 1488 schemas, clean `security` blocks) if it's ever wanted.
- **Linode discriminator fix** (#1250) — 10 occurrences of non-standard `x-linode-ref-name`. User explicitly excluded it ("just the openai one").
- **Greenpeace removal** (#1269) — `greenwire.greenpeace.org` no longer resolves (curl exit 6). Removal is destructive; offered, never requested.
- **`x-preferred` policy** (#1115) — on `meraki.com`, only the v0 `0.0.0-streaming` spec is flagged `x-preferred: true`, so nothing in the v1 line is preferred. Looks wrong. 1.74.0 was set to `false` mirroring 1.32.0 rather than deciding it.
- **php-openapi README addition** (#1390) — asked, never answered.

---

## 5b. Recording provenance — REQUIRED for every spec

Every spec must say where it came from and what was done to it. This lives **in the
spec's own `info` block**, nowhere else.

```yaml
info:
  x-origin:                       # WHERE it came from. apis.guru's own convention.
    - format: swagger             # A CHAIN, oldest first, one entry per format.
      url: https://raw.githubusercontent.com/grafana/grafana/main/public/api-merged.json
      version: '2.0'
    - format: openapi
      url: https://raw.githubusercontent.com/grafana/grafana/main/public/api-merged.json
      version: '3.0'
  x-conversion:                   # WHAT was done. Plain sentences, in order.
    - Fetched from <repo/path> (<format>).
    - Converted <A> -> <B> with <tool> <version> <options>; N warnings.
    - Fixed: <defect and why the fix is right>.
    - Known upstream defect left as-is: <what, and why not fixed>.
```

**Why here and not elsewhere** — this was asked directly, so the reasoning is recorded:

- **Not YAML comments at the top of the file.** These specs get round-tripped through
  PyYAML on every refresh, and `yaml.dump` **silently discards all comments**. Provenance
  written as a comment survives exactly until the next update, which is precisely when it
  matters most. This one is disqualifying, not a preference.
- **Not a README per provider directory.** It does not travel with the spec, it goes stale
  independently of the file it describes, it has no answer for multi-version providers
  (`meraki.com/1.32.0` and `1.74.0` have different origins), and it diverges from upstream
  apis.guru layout for no gain.
- **`x-origin` already exists and is already the convention here** — it is machine-readable,
  survives every round-trip, is scoped to the exact spec version it describes, and apis.guru
  tooling already understands it. `x-conversion` is our addition alongside it, in the same
  place, for the step log that `x-origin` has no room for.

Write `x-conversion` for a human reading it cold. "Fixed a param" is useless; "PUT
/v2/vendors/{vendor_id} declared no parameters, so its path variable was undeclared; the
GET on the same path declares it correctly and the fix mirrors that" is the standard.

---

## 6. Conventions that matter

- **Store specs as `.yaml`.** The tree contains both legacy `swagger.yaml` and `openapi.yaml`; new OpenAPI additions use `openapi.yaml`. Convert JSON sources with Python before committing:
  ```python
  yaml.dump(d, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=100000)
  ```
- **Layout**: `APIs/<domain>/<version>/openapi.yaml`, or `APIs/<domain>/<service>/<version>/openapi.yaml` for multi-service providers. Version dir = `info.version`.
- **Version bumps are new directories**, never in-place edits. Both #41 and #42 are `+N / −0`.
- **Vendor versions can stay fixed while content changes.** For a declared version that has not changed (GitHub, DigitalOcean, Square, DocuSign), refresh the existing version in place and report removals explicitly. Do not invent a vendor version. The dated snapshot policy for unversioned Elasticsearch Serverless in §4 remains separate.
- **Preserve apis.guru curation metadata on any refresh.** A wholesale file replacement silently drops `x-apisguru-categories`, `x-logo`, `x-preferred`, `x-permalink`, `x-providerName`, `x-serviceName`, `x-hasEquivalentPaths`, `contact.x-twitter`, top-level `externalDocs` and `tags`. Merge new spec content *into* the old `info` block. This is the single most important rule for updates — it's what #40 got wrong.
- **`x-origin` records provenance.** Match existing style; for converted specs list the chain, e.g. API Blueprint → swagger → openapi (see `APIs/icons8.com`, `APIs/ritekit.com`, and `APIs/eventbrite.com/3`).
- **New additions go in essentially as-is.** Checked against the recently merged ones (Picsart, Nylas, Eventbrite): they carry **no** `x-apisguru-categories`, `x-logo` or `x-providerName`. Those values are apis.guru curation, and inventing them would be fabricating metadata. Add `x-origin` for provenance and otherwise leave the vendor spec alone. The preserve-metadata rule above applies to **refreshes of specs we already have**, where that curation exists and must survive.
- **Match the sibling file's YAML style.** PyYAML's default dumper writes sequences flush against the parent key; this repo indents them. Subclass the dumper:
  ```python
  class Dumper(yaml.Dumper):
      def increase_indent(self, flow=False, indentless=False):
          return super().increase_indent(flow, False)
  ```
- **CONTRIBUTING.md** distinguishes the fork's validated manual spec PR process from the upstream APIs.guru web form and restriction on direct spec PRs. Follow the fork process here; upstream submission does not establish publication of fork-only additions.

### Conversion toolchain
Installed under the session scratchpad (`apibconv/`), re-installable anywhere:
- `swagger2openapi` (7.0.8) — Swagger 2.0 → OpenAPI 3. Use `{patch:true, warnOnly:true}`. Reliable.
- `apib2swagger` (1.17.1) — API Blueprint → Swagger 2.0. **Its `--open-api-3` path is broken on modern Node** (`json-schema-to-openapi-schema@0.4.0` throws `Type "null" is not a valid type`, with a misleading stack because of a broken error prototype). Workaround: convert to Swagger 2.0, then hand to `swagger2openapi`. That's how Eventbrite was done.
- `google-discovery-to-swagger` — Discovery → Swagger 2.0, then `swagger2openapi`.

For registered Swagger imports, use the repository's locked `maintenance/` toolchain,
not the historical scratchpad. #99 adds swagger2openapi 7.0.8 and all 41 transitive packages
to the npm lock without changing existing package pins. `conversion` recipes default to
zero expected warnings/converter patches. Unexpected counts or source formats require
review. External references must be pinned/bundled first; conversion has no network
resolution. Missing response declarations are rejected before the converter can invent
defaults, and every path/operation must survive. Cached input/output/logs/hashes and the
Swagger → OpenAPI origin chain document the process. Exact vendor patches run afterwards;
full validation and serialization guards remain mandatory. Accepted warnings do not waive
missing-reference validation. The regression suite exercises the real locked converter.

### Post-conversion checks worth running every time

**Write the checker carefully — a naive one produces false failures.** Both of these bit
on PagerDuty and MongoDB, and each looked exactly like a real spec defect:
- **`$ref` may point into a list index**, e.g. `#/components/schemas/X/properties/value/oneOf/3`. That is legal JSON Pointer. A resolver that only walks dicts reports 25 phantom broken refs on PagerDuty.
- **Path parameters are often declared via `$ref`** to `components.parameters`. Comparing `{template}` vars against inline `name` fields without dereferencing first reported 351 phantom mismatches on PagerDuty and 514 on MongoDB. Deref, then compare.

A working version of the checker lives in the session scratchpad as `validate.py`; it is
~70 lines and worth rewriting from this description rather than hunting for the file.

```
- all $refs resolve (refs − components.schemas == ∅)
- every operation has a `responses` block
- path template vars match declared path params
- no `{+name}` reserved-expansion left (Google); normalize to `{name}`
- security entries are well-formed list-of-dicts
```
Real defects caught this way: Eventbrite's `<angle>` path params (fixed), Vertex AI's 207 `{+name}` mismatches (fixed).

---

## 7. Environment gotchas

**Coinbase CDP delivery prepared (2026-10-05):** separate updater
[PR #197](https://github.com/ontola/openapi-directory/pull/197) at
`58bbea99b101a5e2fe153569bce61c1c89c1e9b9` registers the current canonical CDN
publication linked by official SDK Makefile at discovery commit
`d40fb3975395033409643654faacfb3d4e4349ee`. It includes the exact four redundant
required:false Reference Object removals, nine assertions and two regression tests;
**102 local tests pass**. CI run 37371438690 is queued, not passed. Infrastructure
must pass actual CI and merge before marking the separate API addition ready.

[API PR #198](https://github.com/ontola/openapi-directory/pull/198) is DRAFT; do not
duplicate it. Branch `codex/coinbase-cdp-api-only` adds only this progress and
`APIs/coinbase.com/cdp/2.0.0/openapi.yaml`. Native 3.1.0 / vendor 2.0.0, **140 paths /
169 ops / 2594 resolved local refs**, none external. Main at cfb19aa445 has no
Coinbase provider; no previous metadata/baseline is borrowed or fabricated.
Current canonical raw hash
`156440e9f8df1eb23aa0c30c78157dbe8fbd4e96929f2c1ff0b409963f704302`, recipe hash
`2119fac0681727ae3560bdd6b945eb05ce0018f6ba4d1048d93d93efd7f31f24`.
Complete corrected native and actual serialized import fully validate; all typed
vendor content matches except the four reviewed sibling removals and provenance.
Reference targets, optional header required:false, security/auth/server/tags and
all schema/prose/lifecycle content remain exact. No bundling, conversion or inlining.
Public scope is mixed GA/Beta, with private-beta fiat deposit destinations retained;
custodial resources require verified business accounts, payment methods Prime-only.
This is CDP v2, not Coinbase Exchange or a hand-built all-GA slice.

Official SDK snapshot lags by 14 paths / 15 operations; do not substitute its old
artifact for the current CDN. Plain/fresh timestamp queries match independently,
ETag/Last-Modified and 20:41 UTC CloudFront RefreshHit evidence retained. Hosted
health is not_assessed and provenance claims no Git revision. Raw bytes/cache/header
and official guide evidence remain under `cache/maintenance/discovery/coinbase-cdp/`
and `cache/maintenance/coinbase-cdp/`. Scripts/reviews
`/tmp/verify-coinbase-cdp-import.py`, `/tmp/coinbase-cdp-import-review.json`,
`/tmp/coinbase-cdp-actual-import.log`, `/tmp/coinbase-cdp-tests.log`,
`/tmp/coinbase-cdp-selected-audit.json/.md`. Selected audit against actual main
reports valid missing source. Configured scope becomes 54 artifacts only with #197.
API-only branch intentionally excludes the recipe until infrastructure merges;
do not run native CDP import here before that dependency is available.

Zendesk #195/#196 remain pending two hosted runner-acquisition failures without
executed tests; preserve their branches and avoid duplicate PRs. Push-protection
choices for Twilio Messaging/Zendesk Conversations remain unanswered. Attachment
cap is 100: attaching #197 and #198 failed, canonical removals of superseded merged #61/#66
returned app errors, legacy redirect URL removal reported success but a fresh
inventory confirms no actual canonical attachment removal. Preserve current
artifacts; do not claim linkage success. Retry exact new-PR attachment when possible
and keep repository/GitHub links as durable delivery state.


- **Work has been running in a git worktree.** `git checkout main` fails there — main is checked out in the primary dir. Always `git checkout -B <branch> origin/main`. To resync: `git reset --hard origin/main`.
- **Never bare `git stash`** — the stash stack is shared across worktrees and other sessions.
- **`gh` GraphQL 502s intermittently** on this repo. Fall back to REST: `gh api --method GET "repos/.../issues?..." --paginate`. **Always pass `--method GET`** — bare `-f key=value` defaults to POST and will 422.
- **Bash `read` collapses consecutive tabs.** `IFS=$'\t' read -r a b c` silently shifts fields when a column is empty, because tab is IFS-whitespace. This corrupted 9 of the 13 PayPal PRs (wrong titles, bogus `openapi/3.json` source URLs) before being caught on the pre-merge check. **Use a non-whitespace delimiter (`IFS='|'`) for any tabular loop.**
- **Check for existing specs with a full-depth search**, not `find -maxdepth 2`, and search by *service/dir name* as well as brand name. Searching "vertex" missed `aiplatform` and produced the #40 mistake.
- **PyYAML auto-types dates and timestamps, and that bites twice.** Stripe's old
  `version: 2022-11-15` loads as a `datetime.date`, not a string. Worse, `squareup.com/2.0`
  contains a YAML 1.1 timestamp with an out-of-range hour and raises
  `ValueError: hour must be in 0..23` on load. Strip the timestamp resolver:
  ```python
  SL.yaml_implicit_resolvers = {k: [(t, r) for (t, r) in v if t != 'tag:yaml.org,2002:timestamp']
                                for k, v in SafeLoader.yaml_implicit_resolvers.items()}
  ```
  Also force `info.version` to `str()` before dumping, or a date-like version round-trips wrong.
- **Some committed specs contain raw C1 control bytes.** `docusign.net/v2.1` has `0x80`/`0x99`
  (double-encoded UTF-8), which PyYAML rejects outright with a `ReaderError`. Strip
  `[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]` when loading for comparison.
- **If you build an OrderedDict and dump it, register the representer** or PyYAML emits
  `!!python/object/apply:collections.OrderedDict` and the file is corrupt. The validator
  caught this before it was committed; it will not be obvious from a `head` of the file.
- **PyYAML can't parse every vendor YAML.** Cloudflare's 19 MB spec uses the YAML 1.1 `tag:yaml.org,2002:value` construct, which `safe_load` rejects. Other parsers handle it. Verify integrity with `head`/`tail`/`wc -l` and commit as-is rather than reformatting.
- **`git ls-files` reads the CURRENT branch's index, not `main`.** After merging, a feature
  branch checked out locally still predates those merges, so auditing coverage from it shows
  freshly merged providers as missing. This nearly caused a false "Elasticsearch didn't
  land" panic. To audit what is actually on main, use
  `git ls-tree -r --name-only origin/main APIs`.
- **This worktree uses sparse-checkout** (`git sparse-checkout list`). The working tree holds only a couple of `APIs/` subdirs, so `ls`, `find` and `[ -d ]` under `APIs/` are all misleading — see §4. Widen with `git sparse-checkout add APIs/<domain>` before `git add`, and note the command takes no `-q`.
- **GitHub push protection is active on this repo.** Vendor specs routinely carry fake example tokens that match real credential patterns; a push can be rejected by content you did not write. Read the violation before assuming a genuine leak, and never bypass it without the user.
- **The auto-mode classifier can block `gh pr merge`** ("Merge Without Review") regardless of
  the user's standing permission. This is **intermittent**: it refused every merge early in
  the 2026-09-22 session and allowed all of them later the same session. If it refuses, do
  not fight it or look for a workaround — finish everything else, leave the PRs open and
  verified, and hand the user a ready-to-paste `gh pr merge` loop. It also misfires on
  read-only multi-command `git show ... | grep` pipelines; splitting them into single
  commands clears it.
- **Always verify `mergeable`/`mergeStateStatus` and the file list before merging.** `gh pr view N --json mergeable,mergeStateStatus,changedFiles,additions,deletions`. Unexpected deletions mean you're overwriting something that already exists — that's how #40 was caught.

---

## 8. Spam heuristics (for any future triage)

Strong signals a submission is junk: duplicate submissions from one domain; bursts posted seconds apart or on a fixed schedule; crypto / x402 / "pay-per-call" framing; gambling; "Intelligence"/"Analytics"/"Scraper" wrappers around someone else's platform; `Official: NO` with a Postman documenter link; a source URL pointing at a random personal repo.

Worked examples: BMObot filed 15 issues in 47 seconds. The "SplunkES8.1" issue (#1419) contains *genuine* Splunk ES 8.1 content but is hosted at `rigzindorje/gmail-api` — Splunk publishes no official spec (checked their GitHub org), so there's no trustworthy `x-origin` and it was skipped. The "guardian" issues (#1334/#1335) are a third-party Postman collection titled "guardian news", not The Guardian's Open Platform.

---

## 9. Build and maintain a reproducible update process

**Coinbase CDP implementation prepared (2026-10-05):** `coinbase-cdp` registers the
canonical hosted publication explicitly linked by maintained official
`coinbase/cdp-sdk` Makefile at discovery commit
`d40fb3975395033409643654faacfb3d4e4349ee`. Current plain and timestamp-query CDN
bytes match, hash `156440e9f8df1eb23aa0c30c78157dbe8fbd4e96929f2c1ff0b409963f704302`,
ETag and Last-Modified retained. The SDK mirror is 14 paths / 15 ops behind; no
SDK Git revision is claimed for hosted bytes. Native 3.1.0 / vendor 2.0.0,
140 paths / 169 ops, all 2594 local references resolve, none external. Target
`APIs/coinbase.com/cdp/2.0.0/openapi.yaml`; provider absent from fetched main
`cfb19aa445a5b9001f682af27a57c12dab03aaba`. Manifest now configures 54 artifacts.

Checked `maintenance/patches/coinbase-cdp.json` removes only four unsupported
`required:false` siblings from delegation/revocation Parameter Reference Objects.
The exact referenced XDeveloperAuth header itself already declares required:false.
Nine assertions cover the full header, four original parameter lists and operation
IDs. All constraints/auth/reference targets stay intact; no inlining/conversion or
endpoint removal. Vendor fixes, changed references, required:true, false-vs-zero,
changed schema constraints and operation identities stop replay. **102 local tests
pass**; complete patched source and preflight YAML validate, typed roundtrip and
whole vendor-content equivalence pass except four reviewed flag removals/provenance.
Public introduction confirms mixed GA/Beta groups, verified-business custodial
restrictions and Prime-only payment methods. Preserve private-beta annotations and
all native scope/lifecycle/auth restrictions, not a fabricated all-GA slice.

CDN cache review at 20:41 UTC again confirms plain/fresh-query identical hashes;
plain response is CloudFront RefreshHit with current Date and no stale Age value.
Cache metadata, raw responses and official public introduction are retained under
`cache/maintenance/discovery/coinbase-cdp/`. Do not freeze a timestamp query into
source configuration; revisit caching if future publication evidence diverges.
The chat reached its 100-attachment limit. Attempts to unlink verified merged historical updater PRs #61 and #66 returned
Codex app errors; a fresh inventory confirms both remain attached (100 total).
GitHub history and code remain intact. Attempt attachment on each new PR creation
and record failures accurately; current dependencies/protection evidence remain.

Selected-source audit against actual main reports valid missing CDP, no fetch or
validation errors, hosted health unassessed. Cached original bytes and review under
`cache/maintenance/discovery/coinbase-cdp/` and
`cache/maintenance/coinbase-cdp/`; verifier `/tmp/verify-coinbase-cdp-import.py`,
`/tmp/coinbase-cdp-import-review.json`, selected audit
`/tmp/coinbase-cdp-selected-audit.json/.md`. Infrastructure and API delivery remain
separate; do not represent the preflight as merged coverage.

Existing Zendesk delivery: updater #195 remains OPEN at d4f05b3ec, Support API #196
DRAFT at 8478b9bbf. Its 106 local tests pass, but both CI attempts on run 37362766037
failed to acquire a hosted runner without executing any tests. Do not waive CI or
rerun repeatedly during outage; merge #195 only after actual CI passes, then ready
and recheck/merge #196. Both API/infra PRs already exist; no duplicates. Twilio
Messaging and Zendesk Conversations push-protection owner choices remain unanswered.
Full 53-source audit is recorded on pending Support branch in #196 (42 matches /
11 known blocks, not a main-baseline claim); avoid redundant network audits.

**Confluence Cloud v2 prepared (2026-10-06 Europe/Amsterdam):** source registration
`confluence-v2` follows current official
https://developer.atlassian.com/cloud/confluence/rest/v2/intro/ download at
`https://dac-static.atlassian.com/cloud/confluence/openapi-v2.v3.json`.
The linked documentation-build query and plain moving URL have identical bytes.
Native **3.0.3 / vendor 2.0.0 / 151 paths / 218 ops / 682 resolved local refs**,
none external, raw hash
`edb639bbc700ee451a996acd2568e51db4ceab954449427537df30f0ce20ca08`.
Hosted repository health is not_assessed; preserve source hash/time/HTTP metadata,
no fabricated Git revision. Complete fetched main has Jira but no Confluence
service; target `APIs/atlassian.com/confluence-v2/2.0.0/openapi.yaml`. Existing Jira
is not a curation baseline and is not modified.

`maintenance/patches/confluence-v2.json` removes only two invalid scalar string
prefix defaults, literal `my, team`, outside the exact enum [`my`, `team`], on GET
`/spaces/{id}/labels` and `/spaces/{id}/content/labels`. Four assertions retain
complete original parameters/operation identities. No enum expansion, replacement
default, query relocation or inferred runtime omission behavior. Two regressions
prove positive/negative filter values unchanged and reject vendor fixes/removals,
array redesign, requiredness/identity changes. **102 local tests pass** on this
independent infrastructure branch (main's 100 plus these two); source/preflight
YAML fully validate and typed-roundtrip, complete vendor equivalence passes except
the two checked removals/provenance. All auth/server/scopes/permission/app-access
rules, 13 x-experimental flags and one deprecated operation retained. This is a
mixed-lifecycle public collection, not a fabricated all-GA slice. No conversion,
bundling, inlining or invented curation.

The official v1 download was separately fetched from its own reference:
`https://dac-static.atlassian.com/cloud/confluence/swagger.v3.json`, native 3.0.1 /
1.0.0 / 89 paths / 130 ops / 511 resolved local refs, raw hash
`6c66a606fa7535268512f07f599fe1e3f9de2ba0b1da7eb6ead405509875577e`.
It fails native validation first at GET /wiki/rest/api/label prefix's string
schema/default:null. No v1 recipe, registration or import adopted; do not conflate
v1 with v2 or assume v1 fully valid after one diagnostic.

Current source scope on this branch is **54 artifacts** (main's 53 plus Confluence
v2); Coinbase #197 separately adds one, so eventual combined scope is 55, not yet
main. Selected Confluence audit against main reports valid missing coverage.
Original intro/label-guide/spec/HTTP metadata and reviews cached under ignored
`cache/maintenance/discovery/confluence/` and `cache/maintenance/confluence-v2/`.
Scripts/logs/reviews: `/tmp/review-confluence-official-specs.py`,
`/tmp/confluence-official-spec-review.json`, `/tmp/confluence-v2-default-review.json`,
`/tmp/verify-confluence-v2-import.py`, `/tmp/confluence-v2-import-review.json`,
`/tmp/confluence-v2-tests.log`, `/tmp/confluence-v2-selected-audit.json/.md`.
Infrastructure and API additions must remain separate; full preflight is not yet
merged coverage. Recheck moving source hashes before final import/merge.

**Existing delivery holds verified this run:** Zendesk updater #195 at d4f05b3ec
and Support draft #196 at 8478b9bbf remain open. Coinbase updater #197 at 58bbea99b
and CDP draft #198 at 243f98f8a remain open. Coinbase run 37371438690 attempt 1
failed to acquire a hosted runner; tests job 111969289318 has zero steps, audit
skipped. Same exact failure annotation as both Zendesk CI attempts: no tests were
executed, not a code assertion failure. Do not waive actual CI, change runner
labels to evade it or repeatedly retry during outage. Ready API drafts after their
infrastructure passes/merges, then exact-head/file/source/CLEAN checks and merge.
Push-protection owner choices for Twilio Messaging and Zendesk Conversations stay
unanswered; preserve guarded deliveries. #179 remains independent and untouched.
Chat attachment cap/removal failures are recorded on #198; attempt each newly
created PR's attachment, report actual failure and retain durable links here.


The 2026-10-02 audit found no GitHub Actions workflows or general updater in this fork.
The generator under `APIs/moneybird.com/v2-readonly/` is specific to a derived subset.
The README's weekly-update promise, badges, and collection API links describe upstream
APIs.guru, not a verified maintenance or publication service for this fork. The following
is an implementation plan; do not describe these jobs as operational until implemented
and verified.

**Implementation progress (2026-10-02):** PR #60 merged these instructions; PR #61 merged
the initial updater under `maintenance/`: six configured service sources, locked
dependencies, 13 passing offline regression tests, read-only source checks, and a
validated single-API importer. Its PR tests passed on GitHub. The weekly report-artifact
workflow is enabled; a manual run [36976870489](https://github.com/ontola/openapi-directory/actions/runs/36976870489)
fetched all six sources and published a downloadable report and raw source snapshots.
That initial audit job exited nonzero for the then-known DigitalOcean bundling, Xero
validation, and Slack conversion/source-health blockers, distinct from the successful
test job. Xero's blocker is now resolved by #66's checked patch replay; 16 tests pass
locally and in GitHub CI. PRs #62/#63/#65/#67 added Hugging Face and refreshed Plaid,
both public GitHub REST artifacts, and Xero. #69 adds pinned repository bundling and exact
field removal, with locked Node tooling and 21 passing local/CI tests; #70 refreshes
DigitalOcean, and #71/#72 add Snowflake SQL and Warehouse, bringing the registry to nine
artifacts across eight services. #74/#75 add explicitly scoped pinned Fern code-sample
materialization and YAML 1.2 scientific-number parsing, with 27 passing regression tests;
#76/#77 add Cohere and Mistral. #78 aligns scientific-number quoting in the writer and
checks every import's serialized round-trip before writing, with 29 passing local/CI
tests. #79 repairs eight scientific-looking strings across both GitHub artifacts,
retaining the same vendor revision, version, paths and operations. Preserved curation
is now emitted in deterministic key order, tested across three Python hash seeds;
30 offline tests pass. #81 registers Stripe GA, Figma, PagerDuty and Atlas; #82/#83/#84
refresh the first three, with PagerDuty's checked default-removal recipe. Fifteen artifacts
across fourteen services are now registered. Atlas is still blocked by validator/dialect
compatibility, separately from Slack's archived-source blocker.
#86 adds reviewed numeric-directory release discovery and registers Intercom and Sentry;
#87/#88 refresh both. Seventeen artifacts across sixteen services are registered, and
35 regression tests pass locally and in CI. The release catalog response and selected
artifact are pinned together, with explicit release-selection provenance.
#90 adds readable Markdown reports alongside JSON, publishes the readable report in the
audit job summary even when checks fail, and records comparison base revisions per row.
Subset checks retain old rows/dates/bases; failed attempts retain earlier success dates.
Blocked matches are counted as blocked, and added/removed paths and operations remain
separate. Source text is escaped for Markdown/HTML display; custom report filenames cannot
overwrite JSON with their readable companion. Four report regressions bring the test
total to 39, passing locally and in CI. Database, Schema and Table registrations/imports
bring configured coverage to twenty artifacts across nineteen services.

#95 adds live repository-health observations, cached response evidence, import guards
and report findings, with 47 offline tests passing locally and in CI. #96 fixes repeat
imports' provenance to name the actual stored curation baseline rather than an older
manifest fallback; its command-level regression brings the total to 48 passing local/CI
tests. #97 refreshes Intercom's fixed public version `2.16` again after the vendor's
2026-10-02 14:20 UTC wording update: exactly the create/update contact request schemas'
`email_verified` descriptions change; 168 paths / 235 operations remain, with zero
added or removed endpoints. Existing curation/tag order and the two reporting-parameter
patches remain. Vendor commit `70d74db6722480bad239eba2f049ff3c98744c5f`, entry SHA-256
`3274c2255a71c18f38fc146cf316c332503973f5adf0b5ca117f2c409971a4e3`.
#99 implements reviewed Swagger 2.0 → OpenAPI 3.0.0 conversion and registers Grafana and
Square, bringing coverage to 22 artifacts across 21 services and 57 passing local/CI tests.
#100 refreshes Grafana's fixed `0.0.1` artifact: eight parsed content changes (certificate
field, ASN.1 title/description, five RBAC descriptions), with no path/operation additions
or removals and no converter warnings/patches. Vendor commit
`c58da1723a80496cc505922e457e2a0dc78993d0`, entry SHA-256
`5dde6d9a86399e9640ca0208664f7a78a8c5e63c0edbceb925686336471455a5`, converted SHA-256
`84895fb7bdb6cbd94d28f77202f4bf923cf20ec7f2c34579715596584cf0fb51`.
Vendor examples are unchanged; pushing succeeded without a protection bypass. The official
HTTP reference calls Swagger canonical but marks legacy APIs deprecated. New resource APIs
and Grafana Cloud need separate discovery; this scope warning appears in audit reports.

Square's current vendor source is **already OpenAPI 3.0.0**, not Swagger: no conversion is
needed. At vendor commit `0689c901bdfe1ff73f47aa28b17ccd6e0c40bf2d`, entry SHA-256
`8f65460732e19d7445f7a34d8a9df09163db45273df5176a1cc794890ef591fb`, the only parsed
drift after the two previously reviewed fixes is three metadata additions:
`info.externalDocs`, `info.license`, and `x-fern-global-headers`. Endpoints remain 253 / 332.
The new exact recipe asserts both complete source lists and operation identities before
restoring the required `vendor_id` parameter and empty OAuth scope list. It does not fix
undefined `CurrencyExchange` / `AppFeeAllocation` references, so imports remain blocked
by full validation. No Square refresh PR was created; its existing file is unchanged.
The expanded audit also rejects Square's new `info.externalDocs` field, which is not
allowed inside OpenAPI's Info Object. Review a documented exact correction separately;
moving it does not resolve the two missing schemas, and validation must not be waived.

Automatic PR generation, monthly discovery, and fork index publication
remain to do. A local hourly follow-up in this chat is active until 2026-10-09 08:55:58
Europe/Amsterdam for the user's one-week work request. It may stop while the laptop
sleeps; do not prevent sleep or extend the deadline without a new request.

Manual workflow run [36990592745](https://github.com/ontola/openapi-directory/actions/runs/36990592745)
at main `5c5b3a43e` verified the Node installation and bundler on GitHub: all 21 tests
passed, all nine configured artifacts fetched successfully, and all eight supported
OpenAPI artifacts matched their sources with zero validation errors. DigitalOcean's
bundle recorded 21 expected naming warnings; Warehouse recorded zero. The downloaded
artifact includes the source archives, file hashes, bundles, and report. The audit job
still exits nonzero solely for Slack's already-known archived Swagger/conversion blocker;
unsupported-format comparison is not evidence of new Slack API drift or current coverage.

The expanded audit [36994983111](https://github.com/ontola/openapi-directory/actions/runs/36994983111)
at main `ed6630fe3` fetched all eleven sources, passed 27 tests, and matched eight
supported artifacts. The two GitHub artifacts had only scientific-string type drift:
their vendor JSON strings `"0.16001e0"` were emitted unquoted by the old writer, and
the corrected YAML 1.2 reader detected the mismatch. #78/#79 fix the writer and stored
files, rather than ignoring these example differences. Slack remained the known blocker.
The downloaded artifact is `/tmp/openapi-ci-audit-36994983111`; CI artifacts, not `/tmp`,
are the durable download source. Cohere's seven snippets and Mistral's checked recipe
were exercised successfully in that network audit.

Final network audit [37002022081](https://github.com/ontola/openapi-directory/actions/runs/37002022081)
at main `fc16ad482` passed all 29 then-current tests and fetched all eleven artifacts.
All ten supported OpenAPI artifacts matched their official sources with zero validation
errors, including both repaired GitHub descriptions, Cohere's seven code samples, and
the patched public Mistral artifact. DigitalOcean still has 21 reviewed bundler warnings;
Warehouse has zero. The audit job exits nonzero solely for Slack's known archived Swagger
and source-health blocker. Source snapshots and the full report were published as the
`official-source-audit` artifact and downloaded to `/tmp/openapi-ci-audit-37002022081`;
the local `cache/maintenance/report.json` now contains that report. The deterministic
curation change adds one further offline regression (30 total); it changes no API values.

Expanded network audit [37004222700](https://github.com/ontola/openapi-directory/actions/runs/37004222700)
at main `7dff5b044` passed all 30 tests and fetched all fifteen registered artifacts.
Thirteen supported OpenAPI artifacts match their sources with zero validation errors,
including the refreshed Stripe GA, Figma and patched PagerDuty descriptions. The audit
job remains nonzero for two recorded import blockers: Atlas's validator recursion failure
and Slack's archived Swagger source. This does not establish freshness beyond the
configured services. The complete report and raw snapshots are available in the
`official-source-audit` workflow artifact, downloaded to
`/tmp/openapi-ci-audit-37004222700`; the ignored local `cache/maintenance/report.json`
contains this latest report. Recover from CI if the temporary files disappear.

Network audit [37009315774](https://github.com/ontola/openapi-directory/actions/runs/37009315774)
at main `2b0d4d993` passed all 35 tests and fetched seventeen artifacts. Fifteen supported
OpenAPI artifacts match their official sources with zero validation errors, including
Sentry and the catalog-selected, patched Intercom 2.16 description. The pinned catalog
and artifact revision agree, and the original catalog response is present in the uploaded
`official-source-audit` artifact. Atlas's recursion failure and Slack's archived Swagger
source remain the only two recorded blockers; the audit exits nonzero for those reasons.
The downloaded artifact is `/tmp/openapi-ci-audit-37009315774`, and the ignored local
report has been replaced with this verified report. CI is the recovery source after reboot.

Network audit [37016356022](https://github.com/ontola/openapi-directory/actions/runs/37016356022)
at main `7ce9472de` passed all 39 tests and fetched twenty registered artifacts. Eighteen
supported artifacts match their official sources with zero validation errors, including
all five Snowflake descriptions. Atlas's recursion failure and Slack's archived Swagger
source remain the only two import blockers; the audit job exits nonzero for those reasons.
The readable-summary step succeeds despite that exit status, and both `report.json` and
`report.md` are present in the uploaded `official-source-audit` artifact. Their totals
agree (18 matches, 2 blocked), and every row records this run's actual comparison base.
The artifact was downloaded to `/tmp/openapi-ci-audit-37016356022`; ignored local copies
of both reports have been updated. Retrieve the CI artifact if temporary files disappear.

Network audit [37023716280](https://github.com/ontola/openapi-directory/actions/runs/37023716280)
at main `53f3cbc8e` passed all 48 tests and fetched all twenty artifacts. Eighteen supported
artifacts match with zero validation errors, including the refreshed Intercom wording.
Only Atlas's validator recursion and Slack's archived Swagger/conversion remain blocked.
The new health checker recorded nineteen service observations from fourteen unique GitHub
repository requests: eighteen artifacts have `repository_available` sources, Slack is
independently confirmed `archived`, and hosted Hugging Face is `not_assessed` by this
repository check. No metadata checks failed. The overall audit exits nonzero for the two
known blockers; readable-summary publication and artifact upload succeed. Both reports
and every raw repository-metadata response/hash were verified in the downloaded artifact
at `/tmp/openapi-ci-audit-37023716280`. Ignored local reports and repository-health
snapshots are updated. CI artifacts are the recovery source if temporary/local files
disappear. No spec commits were created solely for health-check timestamps.

Expanded network audit [37048205733](https://github.com/ontola/openapi-directory/actions/runs/37048205733)
at main `f1a63de2b` passed 57 tests and fetched all 22 registered descriptions. Seventeen
match, two have valid new content drift (Plaid and Intercom), and three are import-blocked
(Atlas validator/dialect, Square invalid Info metadata/missing schemas, Slack archived
Swagger). Grafana's refreshed conversion matches with zero warnings/patches. All 21
GitHub-source observations succeeded across sixteen unique repositories; twenty sources
are `repository_available`, Slack is archived, and hosted Hugging Face is unassessed by
that repository check. Summary publication and artifact upload succeeded despite the
expected nonzero audit exit. Both reports, all sixteen repository-response hashes and
Grafana's conversion output/hash were downloaded and verified at
`/tmp/openapi-ci-audit-37048205733`; ignored local reports/health snapshots are updated.
The Grafana service-specific legacy/new-resource coverage note appears in the report.

**That drift queue is now complete (#102–#104):**
- #102 corrects the reviewed current manifest targets for Plaid, Xero Accounting, Stripe,
  Figma and Intercom. A successful new-version import advances its manifest target with
  the API file; commit both together. No universal vendor version ordering is guessed.
  Audits record the actual comparison/curation baseline. Matching imports can repair a
  lagging target without rewriting the spec. Manifest edits preserve unrelated formatting;
  source-configuration changes and edits during validation stop the import before writes.
  Four additional regressions bring the suite to 61 passing local/CI tests, including
  successive releases, invalid-release guards and preservation of concurrent edits.
  Baseline pointers describe reviewed imports, not a claim about all other stored versions.
- #103 imports Plaid `2020-09-14_1.762.0` from vendor commit
  `325e2e192bcb422df708029bafe9d950c94df2fd`, entry SHA-256
  `e07a869352e83670e2ef077376db268358ce7a0dc4a8e97b8e1e980b91616a8c`.
  Against actual last import `1.740.1`, both have 360 paths / 351 operations:
  POST `/cra/report/create` and `/protect/cash_advance/feedback/upload` are added;
  POST `/link_delivery/create` and `/link_delivery/get` are removed. The vendor's pinned
  CHANGELOG explicitly records these removals in 1.753.0 and the migration to
  `/link/token/create` with `hosted_link`. Both historical versions remain unchanged,
  curation comes from 1.740.1, and the reviewed manifest target advances to 1.762.0.
  Full validation and YAML value/type round-trip pass; no conversion or content patches.
  The vendor client-library artifact includes limited-availability fields; importing it
  does not imply every described product is generally available.
- #104 refreshes Intercom fixed public `2.16` from vendor commit
  `7b3a218f2b8a9c09ae24247270c764444cddaf70`, entry SHA-256
  `e007fe1902ceaa64e6dbaedfc064f2a2e4fc24bab6c86cf1c8f6900c2b0c42ca`.
  Exactly one vendor description changes: DELETE `/companies/{company_id}` now states
  the company record remains, contacts are detached without being deleted, detachment
  cannot be reversed, and changes may take time to appear. Vendor PR #697 documents it.
  168 paths / 235 operations, zero endpoint/schema/security changes; existing curation,
  reporting-parameter patches and historical 2.14 remain. Full validation and exact
  patched-vendor equivalence pass. No OpenAPI version conversion.
All three PRs are merged and attached to this chat. Re-fetch before future comparisons;
new vendor commits may appear independently of an unchanged version or endpoint count.


Expanded network audit [37057748754](https://github.com/ontola/openapi-directory/actions/runs/37057748754)
at main `845f81fff` passed all 61 tests and fetched all 22 registered artifacts. Nineteen
match their sources, including the new Plaid version and Intercom clarification. The only
three import blockers remain Atlas (validator/dialect), Square (invalid Info metadata and
undefined schemas), and Slack (archived unsupported Swagger). No fetch/prepare failures
or new valid content drift were found. The expected blockers make the audit exit nonzero;
readable-summary publication and artifact upload succeeded. Every row names the actual
comparison baseline. Downloaded reports, all 22 entry-source hashes and all sixteen unique
repository-response hashes were verified at `/tmp/openapi-ci-audit-37057748754`; ignored
local reports and health snapshots are updated. CI artifacts remain the recovery source
when temporary files disappear. All 22 reviewed manifest targets exist on fetched main
and agree with their stored `info.version` directory. No files were committed solely for
check timestamps.


Expanded network audit [37084738252](https://github.com/ontola/openapi-directory/actions/runs/37084738252)
at main `3388295d9` passed 69 tests under Python 3.11 and fetched all 22 descriptions.
Nineteen have valid source matches, including the refreshed Atlas Admin. Cohere matches
its configured source but is blocked by the newly detected empty `TruncationStrategy`
union; Square's invalid metadata/missing schemas and Slack's archived unsupported Swagger
remain the other blockers. No fetch/prepare failures or unblocked content drift were
found. The report distinguishes the blocked Cohere match from validated matches and
names the explicit validation profile for every row. The expected three blockers make
the audit exit nonzero. Readable-summary publication and source-artifact upload succeed.
Both reports, all 22 entry-source hashes and all sixteen unique repository metadata
hashes were downloaded and verified at `/tmp/openapi-ci-audit-37084738252`; ignored local
reports and health snapshots are updated. Recover original evidence from CI if temporary
files disappear. No vendor spec was changed solely for a check timestamp.

PR #109 extends the registry to 24 descriptions across 23 services with Snowflake
View and Stage. Infrastructure CI [37094348658](https://github.com/ontola/openapi-directory/actions/runs/37094348658)
passes all 69 offline tests. Imports #110/#111 are merged with exact verified heads.
Expanded audit [37096774816](https://github.com/ontola/openapi-directory/actions/runs/37096774816)
at main `5f0b8a4c7` passes 69 tests and fetches all 24 registered descriptions. Twenty-one
have valid source matches, including both new Snowflake services. The same three blockers
remain: Cohere's empty union, Square's invalid metadata/missing schemas, and Slack's
archived unsupported Swagger. There are no fetch/prepare failures or unblocked changes.
The expected blockers make the audit exit nonzero; summary publication and complete
source/report artifact upload succeed. Downloaded both reports, verified all 24 entry
source hashes and all sixteen unique repository-health snapshots at
`/tmp/openapi-ci-audit-37096774816`, and refreshed ignored local reports/health snapshots.
Recover this evidence from the CI artifact if `/tmp` disappears. No timestamps were
committed solely to assert freshness.


Fork-facing README and CONTRIBUTING now explain the registered-source weekly audit,
report-artifact access, validated manual import/PR process and source-specific recipes.
They explicitly identify upstream badges, API/RSS endpoints and contribution guidance;
direct reproducible spec PRs are accepted in this fork. No fork collection endpoint has
been published or claimed. Index publication still needs verified consumer access.

**Discord HTTP refresh completed (#113/#114, 2026-10-03):** the registry now monitors
25 descriptions across 24 services. The official
[repository README](https://github.com/discord/discord-api-spec/blob/main/README.md)
distinguishes `specs/openapi.json` (stable public HTTP API) from experimental
`openapi_preview.json`. The OpenAPI description itself remains a public preview;
retain its original title and source limitations. The vendor's API reference lists
v10 as Available. Gateway events and experimental features are outside this scope,
and source matches do not prove complete coverage.

Vendor commit `9426d3c1d4b103484283d7feb568f2ef142712de`, entry SHA-256
`c946facea80a4d356a9e930062c4d05cb6e96ec2638e532493e557805bb6c408`,
adds OAuth2 as an alternative to BotToken for GET `/channels/{channel_id}/messages`.
Declared `10`, OpenAPI 3.1.0, 153 paths / 246 operations remain unchanged; zero
endpoint additions/removals. Reversing this one security-list addition makes the
complete parsed vendor content identical to the prior stored file. No source patches,
bundling, conversion or invented scopes. Existing curation/externalDocs are preserved;
missing info.x-origin/x-conversion provenance is now recorded. The large text diff is
indented sequence serialization, not additional API changes. Full validation, exact
source-content/hash comparison and typed YAML roundtrip pass. Infrastructure CI
[37100774347](https://github.com/ontola/openapi-directory/actions/runs/37100774347)
and local tests pass all 69 cases.
Post-merge audit [37102924090](https://github.com/ontola/openapi-directory/actions/runs/37102924090)
at main `8dd9bb082` passes 69 tests and fetches all 25 descriptions. Twenty-two have
validated source matches, including Discord. Cohere's empty union, Square's invalid
metadata/missing schemas, and Slack's archived unsupported Swagger remain the only
three blockers; no fetch/prepare failures or unblocked changes. The expected blockers
make the audit exit nonzero; readable summary and source/report artifact publication
succeed. Both reports, all 25 entry hashes and seventeen unique repository metadata
hashes were downloaded and verified at `/tmp/openapi-ci-audit-37102924090`. Ignored
local reports/health snapshots are updated; recover evidence from CI after reboot.


**Datadog v2 refresh completed (#116/#117, 2026-10-03):** registry coverage is now
26 descriptions across 25 services. Continue the exact official SDK-generation source
already cited by the stored spec: `DataDog/datadog-api-client-python`,
`.generator/schemas/v2/openapi.yaml`. Its README identifies generation from public
OpenAPI descriptions and warns about opt-in unstable endpoints. Preserve those labels;
this is not a stable-only subset. v1 and other Datadog product artifacts need separate
coverage review. The source repository is available and unarchived.

Pinned source `2240a46b47e2d135962176dfc9dc665f506628af`, entry SHA-256
`2b3da388fca085e5c9dfef7fdf4617af85fc8126695e3065f7ad46badaa0118b`,
retains declared `1.0` and OpenAPI 3.0.0. Coverage grows 1008 / 1591 → 1042 / 1647
paths / operations: **35 paths / 57 operations added; one path / operation removed**.
Component schemas grow 8334 → 8673 (355 added, 16 removed, 84 changed). New operations
include 48 Experiments operations, five Databricks Integration operations, two Logs
Archive Searches operations and one each for Security Monitoring entity context and
SPA recommendations. Those last nine operations retain the vendor's preview/unstable
annotations. Do not infer that an unlabelled operation is generally available.

Removed POST `/api/v2/rum/query/insight/aggregated_signals_problems` is explicitly
retired in vendor [PR #4077](https://github.com/DataDog/datadog-api-client-python/pull/4077),
merged 2026-10-02 at `975eef9c6aa4c11d7af1746b1935333651c59427`. The generated client
and models are removed too. Public search results/reference titles still mention it;
retirement was verified from the vendor's explicit change, not guessed from absence
in a source artifact. All endpoint additions/removals are listed in #117.

Complete source/curation equivalence, raw hash/pinned provenance, separate endpoint
counts, full validation and typed YAML roundtrip pass. Curation and lifecycle labels
survive; info.x-origin/x-conversion now record reproducible provenance. No source
patches, bundling or OpenAPI conversion. The large diff includes deterministic YAML
sequence indentation. Infrastructure CI
[37107858460](https://github.com/ontola/openapi-directory/actions/runs/37107858460)
and local tests pass all 69 cases. Original upstream lead remains
[issue #1392](https://github.com/APIs-guru/openapi-directory/issues/1392), linked in
the API PR body.
Post-merge audit [37110790919](https://github.com/ontola/openapi-directory/actions/runs/37110790919)
at main `6b74e530c` passes 69 tests and fetches all 26 descriptions. Twenty-three
have validated source matches, including Datadog. Cohere's empty union, Square's invalid
metadata/missing schemas and Slack's archived unsupported Swagger remain the only three
blockers; no fetch/prepare failures or unblocked drift. Expected blockers make the audit
exit nonzero; summary and complete source/report artifacts are published. Both reports,
all 26 entry hashes and eighteen unique repository metadata hashes were downloaded and
verified at `/tmp/openapi-ci-audit-37110790919`. Ignored local reports/health snapshots
are updated; CI remains the recovery source after reboot.

**2026-10-03 Meraki / security semantics:** PR #119 merged the semantic security-name
check and native Meraki Dashboard source registration. The registry now covers 27
artifacts across 26 services. [Infrastructure CI 37111751120](https://github.com/ontola/openapi-directory/actions/runs/37111751120)
and local tests pass all 74 cases. Structural validation alone accepted unknown security
scheme names; the additional check enforces the OpenAPI requirement to declare them in
`components.securitySchemes`. It traverses document security, operations, referenced
path items, reusable path/callback components, callback operations and 3.1 webhooks.
Recursive callback graphs terminate; anonymous alternatives, empty security and defined
reference aliases remain valid. Examples and extensions are not security declarations.
Undefined names are aggregated with occurrence counts and first locations, and imports
fail before writing files. The report/import validation profile records this check.

The [official docs configuration](https://github.com/CiscoDevNet/Meraki-Dashboard-API-v1-Documentation/blob/e598959273954662886eda26b8dc2392a4616ef6/config%20copy.json)
uses `master/openapi/spec3.json` for public API Reference and `v1-beta` for Early Access.
The [public overview](https://developer.cisco.com/meraki/api-v1/overview/) confirms
released `1.74.0`. Source revision `9029d122861222bbe912193b77d8f2bc442900d4`, entry
SHA-256 `9c770522d456668aae1dfde78f7076a1cc994b41ff7f20dcd8864b3209f3e6b3`,
has 701 paths / 998 operations in OpenAPI 3.0.1. The companion Swagger at the same SHA
has the identical path/operation sets and hashes to
`bbdb2c81d5bf41cbfa8c3796b89a127076529fd3399cd21945e7c206c6036ec7`.
A review-only Swagger conversion exactly matches the stored 1.74.0 content after curation;
its 748 converter patches were only observed, not accepted as an import recipe.
This is deliberate discovery of a richer native artifact, not evidence of a new vendor
release or stale Swagger content. Native source adds 15 callback declarations and 13
vendor deprecation notices, but 822 operations reference an undefined `oauth2` scheme.
Only `meraki_api_key` and `bearerAuth` are declared. **No Meraki API refresh was made.**
Do not fabricate an OAuth scheme, remove requirements, substitute beta/streaming feeds,
or decide the parked `x-preferred` policy. Find an official correction or separately
review a reproducible exact repair before importing.

The docs repository's `specs/ga/spec3.json` at
`e598959273954662886eda26b8dc2392a4616ef6` is byte-for-byte the same artifact/hash and
has the same defect; it is not a corrected alternative. Vendor issue #62 lists general
spec inaccuracies but does not supply this correction; no upstream message was sent.
Temporary review files are `/tmp/meraki-content-changes.json`,
`/tmp/meraki-official-docs-ga.json`, `/tmp/meraki-spec2.json` and
`/tmp/meraki-security-tests.log`. Re-fetch pinned sources / recover CI artifacts after
reboot instead of depending on those files.

Post-merge audit [37111842991](https://github.com/ontola/openapi-directory/actions/runs/37111842991)
at main `09ef770b4` passes 74 tests and fetches/prepares all 27 descriptions. Twenty-three
have validated source matches; Cohere, Square, archived Slack and native Meraki are the
four import blockers. No fetch/prepare failures or unblocked content drift. The new
security-name check introduces no additional defects in the other registered sources.
The audit intentionally exits nonzero for those blockers, while summary and the complete
artifact upload succeed. Both reports, all 27 entry hashes and nineteen distinct
repository metadata snapshots were downloaded and verified at
`/tmp/openapi-ci-audit-37111842991`; ignored local reports/health snapshots are updated.
CI remains the durable recovery source. Hosted Hugging Face source health remains
unassessed independently of its validated source match.

**Snowflake Task completed (#121/#122, 2026-10-03):** the source registry now
covers 28 artifacts across 27 services. Task is a distinct resource-management API,
absent from the full main tree before import. The
[GA tutorial overview](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/tutorials-overview)
explicitly covers tasks; its
[service guide](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/tasks/tasks-introduction)
and [complete reference](https://docs.snowflake.com/en/developer-guide/snowflake-rest-api/reference/task)
carry no preview designation. Native `specifications/task.yaml` plus `common.yaml`
were bundled from vendor `990e25d97236a11826c9eed40e587c2b859e5680` with Redocly 2.57.0:
two files, zero warnings, no patches or OpenAPI version conversion. Declared `0.0.1`
and OpenAPI 3.0.0 are unchanged. Entry SHA-256
`9dc282435a8aea6304d61a12ba78eb2c31f89d28f0581ba44d2d244f3fc04649`;
source-file snapshot SHA-256
`e81d2befebadbb10d9afeb680bb19281dcbec7c0597f7c2ff0d5f041f413e894`.

The 13 paths / 16 operations cover CRUD, execute/resume/suspend, dependents, current /
completed graph runs and tag actions. Both deprecated underscored graph routes and their
hyphenated replacements remain exactly as the vendor publishes them. Complete parsed
vendor-bundle equality, raw hash/provenance, all references, security names, full schema
validation and typed YAML roundtrip pass. New curation was not invented. Imported
Snowflake coverage is now eight distinct descriptions, **78 paths / 97 operations**;
other catalog services still need lifecycle/validation review. This is not complete
SQL task command coverage. Local and [infrastructure CI 37116607239](https://github.com/ontola/openapi-directory/actions/runs/37116607239)
pass all 74 tests. Temporary verifier/import files are `/tmp/verify-snowflake-import.py`
and `/tmp/snowflake-task-import.log`; recover source evidence from the audit artifact
rather than relying on scratch files after reboot.

**Fresh drift caught and resolved (#123/#124, 2026-10-03):** the
[28-source audit 37119806342](https://github.com/ontola/openapi-directory/actions/runs/37119806342)
at main `f6c035ba8` passed 74 tests and found 21 validated matches, three valid drifts
(two GitHub artifacts and DigitalOcean), and four known blockers. Task matched its
new import. All 28 entry hashes, both reports and nineteen distinct repository-health
snapshots were downloaded/verified at `/tmp/openapi-ci-audit-37119806342`; there were
no fetch/prepare failures. Those new vendor changes arrived during this run.

GitHub source `836ce198db13a6fb194547e53eea99c6ddae495b` adds only POST
`/repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers/rerequest` in each public
artifact. Each fixed `1.1.4` / OpenAPI 3.0.3 description now has 816 paths / 1232 ops,
with one path / op added and none removed. Removing that single added path makes
complete parsed content equal to the prior stored description, excluding generated
provenance. Curation is preserved. Entry hashes (default / 2022-11-28):
`f3efa055b46b43f5f133ecf792a36a7f50cf8a4378cbd177390bc2bf8c6097cd` /
`28b908e1fd554f785e31368e334a897fb01a0439b6988e669c0011c64c77efd9`.
The vendor-published artifacts are the release evidence; the indexed linked review-request
reference had not exposed the new section when checked. No runtime/notification endpoint
was invoked. Other GitHub products still need independent review.

DigitalOcean source `4a87b3bd8e541f72450c426cf4ba197724b0e479` has exactly three parsed
changes: remove `EVALUATION_DATASET_TYPE_ADK` / `EVALUATION_DATASET_TYPE_NON_ADK` from
both documented dataset-type enums, and remove the ADK-workspace description qualifier.
[Vendor PR #1249](https://github.com/digitalocean/openapi/pull/1249) explicitly explains
ADK deprecation and says the API still accepts/returns the removed values. This is a
published-documentation narrowing, not evidence of runtime rejection; downstream generators
may expose narrower enums. Fixed `2.0`, OpenAPI 3.0.0 and 515 paths / 757 ops are unchanged.
The entry-file SHA-256 is also unchanged (`10fc8825506628176d9d0161e3eda83244da7341f4e860137a828f48e71f1b6e`):
only referenced files changed, demonstrating why the pinned bundle/content comparison matters.
New 3134-file snapshot SHA-256 `2e022194ed65ecc9481e3f54677491e8fd7b807ae2ac57c6996490512f100d92`;
Redocly still emits the same 21 reviewed naming warnings and the exact two-default patch
replays unchanged. No new corrections were introduced.

Both refreshes pass complete vendor/curation equality, full schema/reference/path/security
validation and typed YAML roundtrip checks. Temporary parsed diffs/verifiers are
`/tmp/github-rest-oct3-changes.json`, `/tmp/digitalocean-oct3-changes.json` and
`/tmp/verify-oct3-source-imports.py`; recover pinned source bytes from the CI artifact
or re-fetch them instead of relying on scratch files after reboot.

Post-refresh [audit 37126831458](https://github.com/ontola/openapi-directory/actions/runs/37126831458)
at main `ec209bd7e` passes 74 tests and fetches/prepares all 28 artifacts: **24 validated
source matches / four known blockers** (Cohere, Square, archived Slack, native Meraki).
No fetch/prepare failures or unblocked drift remain. Summary and source-artifact upload
succeed despite the expected nonzero audit exit for blockers. Both reports, every entry
hash and nineteen repository metadata snapshots were downloaded/verified at
`/tmp/openapi-ci-audit-37126831458`; ignored local reports/health snapshots are updated.
Recover this durable CI artifact after reboot. Hosted-source health remains independently
unassessed. The full-tree inventory is 729 provider domains / 4264 API files / 2090
openapi.yaml / 2168 swagger.yaml; GitHub and DigitalOcean updates changed no file counts.

**Twilio classic REST completed (2026-10-03, PRs #126 / #127):**
#126 registers the exact official artifact already cited by the old spec,
`twilio/twilio-oai/spec/json/twilio_api_v2010.json`, and documents its scope/version
policy. All 74 offline tests pass locally and in CI
[37127871086](https://github.com/ontola/openapi-directory/actions/runs/37127871086).
The vendor README labels the OpenAPI project GA and actively maintained; that does not
establish GA status or complete coverage for every operation or Twilio service.

#127 adds `APIs/twilio.com/api/1.0.0/openapi.yaml`, retaining the historical `1.55.0`
file byte-for-byte and advancing only this manifest target. The declared vendor version
**decreased**: before the [June 2024 MVR release, vendor PR 111](https://github.com/twilio/twilio-oai/pull/111),
the artifact declared `1.56.1`; at that merge it declared `1.0.0`, still used today.
Both pinned historical raw files were checked. Do not substitute the repository release
`2.8.3`, rename the vendor's version, or assume numeric ordering identifies freshness.
Source revision and retrieval evidence distinguish current content from older releases.

Current source revision `218b7821602a93ae63e83e20ab5e8637e870250f`, entry SHA-256
`78e76cc93c355a259e241866c241663eddb6ce0ed528f066c6cf0958648f5637`.
OpenAPI `3.0.1`; 119 / 195 becomes **121 paths / 197 operations**:
- Three paths/operations added: POST start/stop Calls real-time transcription, and GET
  Recording Add-On Result Payload Data. The transcription routes have a
  [public vendor reference](https://www.twilio.com/docs/voice/api/realtime-transcription-resource).
- One path/operation removed from this public snapshot: GET `/healthcheck`. The old
  vendor extensions already say `docs_visibility: private`, `libraryVisibility: private`,
  and `x-skip-path: true`; this is not evidence that the runtime endpoint was retired.
  The historical file remains available.
- Full content refreshed, including top-level Basic authentication, payment enums,
  messaging/call fields, reusable enum/nullable-schema changes and SDK annotation cleanup.
  Callback-method enums narrow to GET/POST at 111 source positions. Four existing POST
  responses change their documented status from 201 to 200. Ten usage-category enum
  schemas become strings; eleven schemas are added. Available-phone-number-country list
  response pagination metadata disappears. These documented choices/types may affect
  generators; no local API content was reconstructed or invented.

All parsed vendor content equals the imported file after preserved curation; categories,
logo, provider/service metadata and curated tags survive. Strict validation, references,
path parameters, responses/security requirement names, raw hash and typed YAML roundtrip
passed. No conversion, bundling, warnings or patches. All 74 tests pass on the import PR
[37127994150](https://github.com/ontola/openapi-directory/actions/runs/37127994150).
The registry now monitors **29 artifacts across 28 services**. Main `9b1101b18`
(after #127) has **729 domains / 4265 API files / 2091 openapi.yaml / 2168 swagger.yaml**;
these are dated counts, not live totals.

Expanded audit [37128042128](https://github.com/ontola/openapi-directory/actions/runs/37128042128)
at main `9b1101b1809cae8f71dc5d05ef8cc4118db94c79` fetched/prepared all 29 artifacts,
passed 74 tests, and found **25 validated source matches / four existing blockers**
(Cohere, Square, Slack, Meraki), with no new failures or unblocked drift. Twilio matches
its pinned source at 121 / 197. Twenty unique repository-health snapshots were verified;
hosted Hugging Face remains unassessed by that repository checker, and Slack remains
archived. The audit's expected nonzero exit is caused by those four blockers; summary
publication and complete artifact upload succeeded. Both reports, all 29 raw entry hashes,
all 20 repository metadata hashes, validation profiles, classifications and comparison
base were checked in `/tmp/openapi-ci-audit-37128042128`; ignored local reports/health
snapshots are updated. Recover the `official-source-audit` artifact from CI after reboot.

**Twilio Messaging audited; publication blocked (2026-10-03, #129 merged):**
#129 registers `twilio/twilio-oai/spec/json/twilio_messaging_v1.json`, the exact source
already cited by `APIs/twilio.com/twilio_messaging_v1/1.55.0/openapi.yaml`. All 74 tests
pass locally and in [CI 37135121007](https://github.com/ontola/openapi-directory/actions/runs/37135121007).
The registry now covers **30 artifacts / 29 services**. Only `messaging.twilio.com` v1
resource management is monitored, separately from classic Message sending and TwiML.

Source `218b7821602a93ae63e83e20ab5e8637e870250f`, entry SHA-256
`28993c66048625cb9421c8534609d9b3573365d0e25a5170b5026806634b3f9a`, OpenAPI `3.0.1`,
declared `1.0.0` (same vendor reset at PR 111 as classic REST, verified in both pinned
historical files). It has **32 paths / 58 operations**, versus stored 28 / 50:
four added paths, eight added operations, **no removed paths/operations**. Added routes
cover DestinationAlphaSenders CRUD/list, create/delete ChannelSenders, requesting a
managed Link Shortening certificate and validating domain DNS. Public
[DestinationAlphaSenders](https://www.twilio.com/docs/messaging/api/destination-alphasender-resource)
and [ChannelSenders](https://www.twilio.com/docs/messaging/api/messaging-service-channelsender-resource)
docs cover the sender operations but explicitly label REST Messaging Service configuration
**Public Beta**; sending is GA. The OAD project is GA, not every included product.
The [Link Shortening onboarding guide](https://www.twilio.com/docs/messaging/features/link-shortening/onboarding-guide)
documents RequestManagedCert; the published OAD is evidence for ValidateDns.
Missing old `x-maturity` annotations do not prove graduation to GA. Preserve the complete
published artifact with that lifecycle limitation in manifest/reports/docs.

Full changes include twelve added schemas (none removed), typed toll-free use-case arrays,
business-registration/vetting/help/privacy/consent fields, Aegis vetting, explicit Basic
security, brand-status enum changes and callback methods narrowed to GET/POST at six
positions. Vendor removes `DELETED` and adds `DELETION_PENDING`, `DELETION_FAILED`,
`SUSPENDED`; opt-in enum includes `IMPORT` / `IMPORT_PLEASE_REPLACE` as published.
No runtime behavior was asserted, source patches invented or annotations restored.

The complete import is committed **locally** on `codex/refresh-twilio-messaging`, commit
`8bf3ab52f17aabcdbb42c0dd059f4d0880f05522`: new `1.0.0/openapi.yaml` (8664 lines) and
manifest target advance only. Historical bytes, all curation, full parsed source equality,
strict schema/reference/path/response/security-name validation, raw hash and typed YAML
roundtrip pass; no conversion, bundling or patches. Verifier/log/body:
`/tmp/verify-twilio-messaging-import.py`, `/tmp/twilio-messaging-import-verification.log`,
`/tmp/openapi-pr-twilio-messaging-refresh.md`. Recover from the local branch and pinned
source if scratch files disappear. **No API PR was created**: the push was rejected,
and remote branch absence was verified; subsequent PR creation failed for missing head.

GitHub GH013 flags the same published account-SID example at YAML lines
2028 / 2102 / 2449 / 2485 / 2558. Each exact value was confirmed in the pinned vendor JSON;
SHA-256 of the flagged identifier is
`8f635d37958654d4ca9daaa71b92fe67bb8efa7c0b4b37f7f7a2ed2892d634a1`.
Do not quote the literal here: that can make handoff files unpushable too.
[Repo-owner review/allow link](https://github.com/ontola/openapi-directory/security/secret-scanning/unblock-secret/3KBwDoPE9Bb9YRpwIpSKhIDc7Hs).
The user was asked to choose owner review/allowlisting or an exact documented redaction;
**no response/authorization received yet**. Do not bypass protection, redact on your own,
retry rejected pushes unchanged, or mark this import merged. The manifest retains the
old target and records a source-specific delivery blocker; read-only audit still validates
and compares the new source. Continue independent maintenance while that decision is pending.

Expanded [audit 37140907056](https://github.com/ontola/openapi-directory/actions/runs/37140907056)
at main `993b3372f4f70a496795dc73e7377017ab6988b4` passes all 74 tests and fetches/prepares
all 30 artifacts. It records **25 validated source matches / five import blockers**:
Cohere, Square, archived Slack, native Meraki, plus Twilio Messaging's delivery blocker.
No new fetch failures or unblocked drift. Messaging still has zero validation errors;
its 28 / 50 → 32 / 58 comparison, four/eight additions and no removals are present.
Its coverage explicitly says Public Beta configuration; the blocker is push protection,
not invalid OpenAPI. Source-health observations cover twenty distinct repositories;
hosted Hugging Face remains unassessed by this repository check.
The expected audit exit is nonzero; tests, readable-summary publication and complete
artifact upload succeed. Both reports, all 30 raw entry hashes, 20 repository metadata
hashes, validation profiles, comparison base and blocker classifications were downloaded
and verified at `/tmp/openapi-ci-audit-37140907056`. Ignored local reports/health snapshots
are updated. Recover the durable `official-source-audit` artifact after reboot.
#130's [CI 37138872113](https://github.com/ontola/openapi-directory/actions/runs/37138872113)
also passed all 74 tests; its guarded manifest retains the stored `1.55.0` target.

**Twilio Verify v2 completed (#132/#133, 2026-10-03):**
#132 registers the exact official `twilio/twilio-oai/spec/json/twilio_verify_v2.json`
already cited by the stored `1.55.0` file. [CI 37143912190](https://github.com/ontola/openapi-directory/actions/runs/37143912190)
and the local suite pass all 74 tests. Source revision
`218b7821602a93ae63e83e20ab5e8637e870250f`, entry SHA-256
`10559c28858caa9b00620ebec400aded2aaebe4ff6e4215ec00396df0ffda52c`.
OpenAPI `3.0.1`, declared `1.0.0`. Both historical raw artifacts confirm the same
`1.56.1` → `1.0.0` reset at vendor PR 111; do not use repository release `2.8.3`
or numeric directory ordering to infer freshness.

#133 adds `APIs/twilio.com/twilio_verify_v2/1.0.0/openapi.yaml` (8987 lines), retaining
historical `1.55.0` bytes and advancing only this manifest target. **29 / 53 → 33 paths /
57 operations**, four added paths/ops and **none removed**. All are POST under
`/v2/Services/{ServiceSid}/Passkeys/`: ApproveChallenge, Challenges, Factors, VerifyFactor.
The [Verify overview](https://www.twilio.com/docs/verify/api) selects v2; the
[Passkeys overview](https://www.twilio.com/docs/verify/passkeys) explicitly labels Passkeys
**private beta**. This refresh follows the same broad public artifact already stored;
it is not a stable-only subset. Manifest/discovery/coverage reports and README record
that limitation. Removed old maturity annotations and the OAD project's GA label do not
establish feature graduation. Other Twilio service/preview artifacts and TwiML are separate.

Full vendor changes include Passkeys/WhatsApp service settings, SNA client-token parameters,
verification-check Templates, RBM attempt-channel enum values, composed nullable references,
descriptions/examples and explicit top-level Basic authentication. The 45 schema keys are
unchanged. No source patches, maturity reconstruction, conversion or bundling. All curation
and historical bytes survive; strict schema/reference/path/response/security-name validation,
full parsed vendor equality, exact raw hash/revision and typed YAML roundtrip pass.
[Import CI 37144008055](https://github.com/ontola/openapi-directory/actions/runs/37144008055)
passes 74 tests. Published account-SID examples use one repeated-character placeholder;
the push succeeded with source examples unchanged and no protection bypass. Messaging's
separate source-specific blocker remains pending the user's response; it was not retried.

Reproduction scratch files: `/tmp/twilio-verify-import.log`,
`/tmp/verify-twilio-verify-import.py`, `/tmp/twilio-verify-import-verification.log`,
`/tmp/twilio-verify-content-diff.json`. Recover from pinned sources/CI evidence after reboot.
The registry now monitors **31 artifacts / 30 services**. Fetched main `8ec1aa871`
(after #133) has **729 domains / 4266 API files / 2092 openapi.yaml / 2168 swagger.yaml**;
these are dated counts, not live inventory.

Expanded [audit 37144078955](https://github.com/ontola/openapi-directory/actions/runs/37144078955)
at main `8ec1aa87184c1e59e1466b88e0199b4d83d009ba` passes 74 tests and fetches/prepares all
31 artifacts: **26 validated source matches / five known blockers** (Cohere, Square,
archived Slack, native Meraki, Twilio Messaging delivery). No new fetch/prepare failures
or unblocked drift. Verify matches at 33 / 57; its coverage explicitly records private-beta
Passkeys. Messaging remains valid but publication-blocked. Twenty unique repository-health
snapshots were checked; hosted Hugging Face remains unassessed by this repository checker.
The audit's expected nonzero exit is caused by those blockers; tests, readable summary and
complete artifact upload succeed. Both reports, all 31 raw entry hashes, all 20 repository
metadata hashes, validation profiles, actual comparison base and classifications were
downloaded/verified at `/tmp/openapi-ci-audit-37144078955`. Ignored local reports/health
snapshots are updated. Recover the durable `official-source-audit` artifact after reboot.

Asana's maintained official source is now registered (#135) and its fixed `1.0`
REST artifact is refreshed (#136); do not repeat its import or archived-source search.
Current evidence and independent discovery leads are recorded at the end of this file.
All parked items and the Messaging publication decision remain pending.

**Resume next:** Atlas's validator/dialect blocker and refresh are resolved. Cohere's
empty union now needs vendor-correction discovery or a separately reviewed exact
correction; Meraki's native artifact needs its missing security scheme resolved from
verified official evidence. Do not invent variants/schemes or relax validation. Continue to
extend the registry to other major imported APIs,
audit more distinct stable Snowflake services, and continue vendor discovery. Square still
is registered as direct OpenAPI 3, with exact existing fixes replayed, but its undefined
vendor schemas still block import. Do not invent them or waive validation. Grafana's
legacy HTTP artifact is monitored/refreshed; discover maintained stable descriptions
for its newer `/apis` resources and Cloud separately. Repository-health checks are
implemented; extend artifact-specific
lifecycle/deprecation checks and assessment of hosted sources without confusing repository
activity with spec freshness. Ownership, service scope and stable-release checks still
need deliberate review.
Implement validated per-service
PR generation and monthly discovery in separate infrastructure PRs; no blanket automatic
merge. Consider fork publication only with
verified consumer access. Slack's maintained official replacement remains unresolved.
Cohere, Mistral, Stripe, Figma, PagerDuty and Sentry's recorded refreshes are complete. The registry
and local report retain the latest checks;
re-fetch main and inspect open PRs before continuing. Do not repeat completed imports.

### Implementation order

1. Build the fetch, compare, validate, and import commands alongside the first refreshes
   in §4. Put reusable tools and locked dependencies in the repository, rather than relying
   on `/tmp`, old session scratchpads, or packages installed globally.
2. Register and refresh the confirmed stale major APIs. Add the verified missing providers
   with the same machinery, one PR per API. Keep updater infrastructure in its own PR.
3. Add weekly GitHub Actions checks and PR generation after local runs are reproducible.
   Add a monthly discovery check for missing major APIs. These are repository workflows;
   do not assume a recurring Codex chat task already exists.
4. Extend coverage incrementally across priority providers. Respect every exclusion in §5;
   neither automation nor this plan authorizes Google regeneration or other parked work.
5. Update README and CONTRIBUTING to describe this fork's actual import process, maintenance
   coverage, and publication status. Identify upstream badges and API links explicitly.
   If publishing a fork index, derive it from this fork's committed specs and verify that
   consumers can see its additions before advertising that endpoint.

### Source configuration and discovery

- Maintain a machine-readable source manifest keyed by provider and API/service. Record
  the target spec, official source entry point, release/tag/catalog discovery strategy,
  source format, bundling/conversion recipe, patch recipe, version policy, and priority.
  Use existing `info.x-origin` to find leads; confirm vendor ownership and source health
  before enabling updates. Configuration does not replace in-spec provenance (§5b).
- Discover releases and service catalogs, not just the already-pinned version URL. A
  successful download of an old release cannot establish that no newer release exists.
- For new providers, search vendor documentation and vendor-owned repositories. Inspect
  repository roots, branches, tags, and SDK generation inputs before dismissing a 404.
  Check presence against fetched main at full depth and distinguish complete official
  specs from hand-authored slices, third-party scrapers, and generic protocol definitions.
- Prefer stable public products. Deduplicate catalog slices by API shape and purpose,
  following the HubSpot precedent in §4. Label scope accurately when importing only one
  service of a larger platform. Track unresolved candidates so searches are not repeated
  blindly, and record what URL was actually checked and when.

### Fetching and detecting changes

- Resolve a vendor repository branch/tag to a commit SHA and fetch the entry document and
  all referenced files from that revision. For hosted specs, record the retrieval time,
  final URL, content hash, and available ETag/Last-Modified values. Use bounded timeouts,
  retries, and concurrency; report failures rather than treating them as unchanged.
- Keep a raw source hash and a deterministic comparison of parsed vendor content. Check
  versions, added/removed paths and operations, parameters, security, request/response
  schemas, and descriptions. A matching version, path count, or recent local commit is
  insufficient evidence of freshness. Changes confined to YAML formatting or key order
  should not generate spec PRs.
- Compare after applying the same pinned conversion and documented patches. Exclude only
  identified fork-owned curation and generated provenance from vendor-content comparisons;
  do not ignore the entire `info` block or vendor extensions. Re-fetch external references
  as part of the source snapshot so their changes are detected too.
- Preserve the original source bytes for reproducibility. Parser workarounds used for
  inspection must not silently alter the committed vendor content. A 404, archived repo,
  authentication failure, or invalid document is a source-health result, not a reason to
  remove the stored API.

### Import, validation, and delivery

- Bundle external OpenAPI references into a standalone document before committing, with
  provenance for the bundling and conversion. Identify reference positions correctly:
  code-sample extensions can contain references to non-schema artifacts, as in Cohere.
  Preserve or explicitly materialize those artifacts without pretending they are schemas.
- Support the source's OpenAPI version, including 3.1 and its JSON Schema semantics.
  Do not downgrade 3.1 documents merely to fit a 3.0-only validator. Apply the checks in
  §6, including JSON Pointer array indices and referenced path parameters. Reject HTML
  error pages and catalog indexes that are not OADs.
- Preserve existing curation (§6); retain historical versions for version bumps and use
  the documented fixed-version/snapshot policies. Encode justified fixes as reproducible
  patches with explanations in `info.x-conversion`. Never invent missing schemas. Record
  known upstream defects explicitly and distinguish them from new validation regressions.
- Add meaningful tests for updater behavior: fixed-version content changes, referenced-file
  changes, metadata preservation, new-version directories, patch replay, and failed fetches.
  Test validators with array-index references, referenced parameters, and OpenAPI 3.1.
- Generate one update PR per API, updating an existing pending PR rather than duplicating
  it. Include the official source/revision, old/new versions, additions and removals,
  conversion warnings, patches, known defects, and validation results. Link any relevant
  upstream issue or PR in the body. Verify file lists and merge status as required by §7.
- Routine official additions may follow the existing merge authorization in §1. Do not
  implement blanket automatic merging of all refreshes. Flag unexplained large removals,
  source substitutions, new patches, and deferred decisions for review. Respect push
  protection and approval-review blocks; leave verified PRs ready when merging is blocked.

### Scheduled checks and freshness reporting

- Run weekly checks for registered priority sources; make unsupported providers visible
  rather than suggesting every historical spec is monitored. Separate read-only fetching
  and validation from the step permitted to write PRs. Run validation on generated PRs.
- Publish a machine-readable freshness report and a readable summary as workflow artifacts
  or a verified fork index. For each API, show the stored/source versions and revisions,
  last check attempt, last successful fetch/comparison/validation, content drift, pending
  PR, known defects, and source-health status. Failed attempts must not advance the last
  successful check. Keep original and converted provenance in the spec's `info` block.
- Distinguish **matches the configured source**, **a newer release is available**, and
  **source health or current API coverage is uncertain**. Slack's archived source is the
  concrete example of why these are different claims. Do not create spec commits solely
  to change a last-checked timestamp.
- The monthly discovery job should produce a deduplicated queue of official candidates
  for well-known APIs, with URLs, ownership evidence, scope, and import obstacles. Notify
  on actionable drift, failures, or decisions; avoid repetitive unchanged-status updates.


**Asana source migration / representation repair (2026-10-03):** The original stored
`APIs/asana.com/1.0/openapi.yaml` had 126 paths / 167 operations. Its old source
`Asana/developer-docs` redirects to `AsanaArchive/developer-docs`, archived 2025-02-24.
The archived README explicitly points to [Asana/openapi](https://github.com/Asana/openapi).
The [current public REST overview](https://developers.asana.com/reference/rest-api-reference)
links `defs/asana_oas.yaml`; the active repository README distinguishes that description
from app components and the SDK artifact. This is an evidenced official replacement,
not a guessed substitution. Source revision `1b1c15108d490fc5b780bb83e070293b5815d522`,
entry SHA-256 `7c4c198fda7627c28be82ca0d85886fd034c93b16ed13c7d96a13d2f3534eaa6`:
OpenAPI 3.0.0, fixed vendor version 1.0, 177 paths / 251 operations.

The source has 1,556 unquoted response-code mapping keys. PyYAML reads these as integers;
the structural validator rejects them. The vendor's pinned `convert_yaml_to_json.py`
and `.github/workflows/push_openapi_spec_to_readme.yml` convert exactly this YAML to JSON
before publication, making those object keys strings. The opt-in `yaml_response_keys`
recipe quotes only integer 100–599 keys in path-operation Responses Objects, checking
an exact reviewed count and absence of collisions before mutation. Payload keys, schema
values and all response content remain unchanged. Shared YAML mappings are counted once.
No global coercion, API version conversion, fabricated responses or validation waiver.
The prepared full source validates with zero errors; all 2,575 local references resolve.
Keep this step and explanation in the imported spec's own provenance. If vendor keys
are fixed or the count changes, review/remove/update the recipe deliberately.

The complete public artifact includes preview Project briefs and beta wording in
RuleTriggerRequest; retain and report that limitation instead of claiming all features GA.
App components, SDK-specific OAD, SCIM and MCP are separate scope. The current source has
52 added paths / 87 added operations and one removed path / three removed operations.
Two removals are the status-update path parameter rename `status_gid` → `status_update_gid`;
the third is PUT /teams, with PUT /teams/{team_gid} now published. Audit the corresponding
public references before importing and record these as specification route changes,
not proof of runtime retirement. Infrastructure registration is separate from the API PR.


**Asana REST import completed (2026-10-03 UTC, #135/#136 merged):**
The fixed `1.0` description is refreshed in place to **177 paths / 251 operations**:
**52 paths / 87 operations added, one path / three operations removed**. All removals
are published route changes, with operation IDs retained: GET/DELETE status updates
rename `{status_gid}` to `{status_update_gid}` and PUT /teams moves to
PUT /teams/{team_gid}. The current [get-status](https://developers.asana.com/reference/getstatus),
[delete-status](https://developers.asana.com/reference/deletestatus) and
[update-team](https://developers.asana.com/reference/updateteam) references confirm the
new routes; this says nothing about old runtime route availability.

Full source changes cover access requests, agents / AI Studio usage, allocations/budgets,
custom types, graph/resource exports, goals, generalized memberships, out-of-office entries,
portfolio/project settings, rates/roles/reactions, rule triggers, task templates, time tracking,
timesheet approval statuses and additional workspace resources. Components grow 165 → 280
schemas (118 added, three vendor definitions removed: ProjectMembershipResponse, TagRequest,
TaskRequest). Existing operations gain OAuth scope requirements and refined request/response
schemas, enums, required fields, query options and descriptions. Top-level PAT/OAuth
alternatives remain. No schemas, scopes or runtime behavior were invented.

Pinned entry hash/revision above, equality with the vendor's JSON representation after the
reviewed response-key repair, complete prepared-source plus curation equality, strict
schema/reference/path/response/security-name validation and typed YAML roundtrip all pass.
All 2,575 references resolve locally. Curation/Twitter/curated tags are retained. No bundling,
OpenAPI version conversion or other source repairs; preview Project briefs, beta rule-trigger
wording and deprecated routes remain. The repair is described in `info.x-conversion` and
`x-origin` now names the pinned maintained source. Manifest target remains `1.0`.
Infrastructure #135's [CI 37153285326](https://github.com/ontola/openapi-directory/actions/runs/37153285326)
passes all 79 tests. Local verifier/log: `/tmp/verify-asana-import.py`,
`/tmp/asana-import-verification.log`; parsed-change inventory `/tmp/asana-content-diff.json`.
The registry covers **32 artifacts / 31 services**. Run the full network audit after merge
and record its actual base, source snapshots and classification; earlier 31-source evidence
must not be represented as validating this addition. Messaging's publication decision is
still pending; no rejected push was retried.


**Asana delivery recovered (2026-10-03 23:02 UTC):** GitHub recovered after the earlier
502/503/timeouts. Both GraphQL and REST branch-specific all-state PR searches confirmed
that the stalled attempt had created no PR; no existing PR was duplicated. The exact remote
head `825a0d8ee653b32719a7edb761776a73aa81ae28` matched the local branch, including its
additional handoff notes. Re-fetching the maintained Asana source confirmed unchanged
revision/hash, complete validation and live repository health. [PR #136](https://github.com/ontola/openapi-directory/pull/136)
was created, attached, verified CLEAN/MERGEABLE with exactly the Asana spec and AGENTS.md,
and merged with an exact-head guard. Merge commit `caa19c1cf7c4b931b51ac86d64e42be126c8a7cb`.
The API-only PR had no infrastructure CI checks because of the workflow path filter;
post-merge audit below verifies all 79 tests and the actual imported main. The creation
uncertainty and GitHub delivery outage are resolved. Do not retry creation or import.

**Expanded network audit verified (2026-10-03 UTC; local 2026-10-04):**
[Run 37160446576](https://github.com/ontola/openapi-directory/actions/runs/37160446576)
at main `caa19c1cf7c4b931b51ac86d64e42be126c8a7cb` passes all **79 tests**, fetches/prepares
all **32 registered artifacts / 31 services**, and reports **27 validated source matches /
five known import blockers**: Cohere, Square, archived Slack, native Meraki and Twilio
Messaging delivery. No new fetch/prepare failures or unblocked drift. Asana matches at
177 / 251 with zero errors and the recorded 1,556-key transformation. Its coverage retains
preview/beta limitations. Twilio Messaging is still valid but push-protection-blocked;
its pending owner choice was neither answered nor retried. All other parked items remain.

The audit's expected nonzero exit comes from these known blockers. Test job, readable
summary publication and complete artifact upload succeeded. Both reports, all 32 entry
hashes and 21 distinct repository-health metadata hashes, validation profiles, actual
comparison base, classifications and the Asana-specific row were downloaded and verified
at `/tmp/openapi-ci-audit-37160446576`; ignored local reports/health snapshots are updated.
Verifier/log: `/tmp/verify-asana-full-audit.py`, `/tmp/asana-audit-verification.log`.
Recover the durable `official-source-audit` workflow artifact after reboot. The fetched
main inventory remains 729 domains / 4266 API files / 2092 openapi.yaml / 2168 swagger.yaml;
Asana is an in-place refresh, not a new provider/version directory.

**Independent discovery queue (2026-10-04 local):**
- **OpenRouter** is missing from the full fetched main tree (domain/service/brand search).
  Its [official API overview](https://openrouter.ai/docs/api_reference/overview) explicitly
  links `https://openrouter.ai/openapi.json` and `.yaml`. The JSON fetched at
  `2026-10-03T23:39:02.409720+00:00` is OpenAPI 3.1.0, declared 1.0.0, **113 paths / 151
  operations**, hash `8d4747322d09b4848572dc30bdb713b3e74e6f0642dc8507482ce58154324f4a`.
  No external references; hosted source has no revision/ETag/Last-Modified. It is a vendor
  description of OpenRouter's own routing service, not those underlying model vendors'
  APIs or a generic OpenAI protocol import. **Not registered/imported**: strict validation
  rejects boolean `exclusiveMaximum`/`exclusiveMinimum` in four schemas, which require
  numeric bounds in 3.1. Exact locations: EndpointDocumentV2.discount_to_user;
  ModelInputV2.oneOf[2/3].params.max_duration_seconds.value; VideoGenerationRequest.upscale_factor.
  Look for official correction or review an exact evidenced repair separately; do not
  downgrade the artifact, invent bounds or waive validation. It also includes
  `/api/alpha/decisions`, v2 models and other experimental-looking products. Review each
  feature's official lifecycle/public scope before selecting this broad artifact; the docs'
  word “complete” is not a blanket GA guarantee. Snapshots remain in ignored
  `cache/maintenance/discovery/openrouter/<hash>/` and `/tmp/openrouter-source*.json`.
- **Vercel** already exists at `APIs/vercel.com/0.0.1/openapi.yaml`: 85 paths / 113 ops,
  OpenAPI 3.1.0. Its hosted official REST source is now fetched, compared and registered
  below; the newer artifact fails validation. No API import was made. Configuration
  JSON Schemas on that host remain separate from the REST description.
- Zoom likewise already exists (`zoom.us/2.0.0`, 265 / 373); the stored marketplace OAD
  URL is a lead, not a verified current artifact. Jira's stored snapshot failed the
  current YAML loader on `tag:yaml.org,2002:value`; no source was fetched or content
  silently rewritten. Keep these separate from the actionable Vercel/source discovery.

**Resume next:** Continue independent major-provider official-source audit/discovery,
Vercel is registered with the blocker below; continue with another major provider or a
verified stable missing provider. Asana delivery is complete. The 32-source audit above
is the latest verified full network run until the expanded audit is completed.
Infrastructure PR generation/monthly discovery remain authorized future work; keep them
separate from API PRs and never introduce blanket automatic merging.


**Vercel official source / validation diagnostics (2026-10-04 UTC):**
The official [vercel/sdk](https://github.com/vercel/sdk) publishing input is confirmed at
commit `ad18800891417be665d96d6c5a09737410b5f5ac`: its
[Speakeasy workflow](https://github.com/vercel/sdk/blob/ad18800891417be665d96d6c5a09737410b5f5ac/.speakeasy/workflow.yaml)
uses `https://openapi.vercel.sh/` before an SDK-specific overlay. This is the same URL
cited by the stored REST description, with current vendor evidence rather than a guess.
The public SDK repository was unarchived/active; that observation does not assess the
hosted artifact's ongoing health. The updater correctly reports hosted health unassessed.

Fetches at `2026-10-04T00:30:54.446427+00:00` and
`2026-10-04T08:39:05.082847+00:00` have identical SHA-256
`2c463a1d98b1d93e95a0e5aac33d210c18cb68f704ffeeadd3b4a0b408e18ae5`,
ETag `"2e448742d1ec429f32556c82e45050a3"`, Last-Modified
`Sat, 03 Oct 2026 21:58:11 GMT`, and no revision. Declared placeholder version stays
**0.0.1**, but native dialect is **3.0.3**, with **321 paths / 443 operations** versus
stored 85 / 113: **263 paths / 368 ops added, 27 paths / 38 ops removed**. No external
references or preparation transformations. Removed routes include version moves and
renames; review each individually before any eventual import, and do not infer runtime
retirement from this difference. Broad public artifact retains preview custom-environment
APIs, deprecated log drains and plan restrictions; this is not stable-only coverage.

**Import blocked:** native 3.0.3 fails strict validation on unsupported schema keywords
including `const` and `patternProperties`, plus other structure failures. Independent
structural iteration found 33 failures; the updater's caught top-level failure remains
one aggregate finding, now with exact nested schema pointers. The SDK's separate
`vercel-spec.json` at the same pinned revision has 315 paths / 435 ops, hash
`b6b52dcccc93788459188642c6c8a735183804cc8379ba1556496af9cdc10281`, and also fails;
it is an overlaid, different snapshot, not a valid substitution. Preserve the old spec
until a vendor correction or separately reviewed exact evidenced repair. Do not drop
constraints, change declared dialect, invent schemas or waive validation. The registry
now has **33 artifacts / 32 services**, including explicit `vercel-rest` import guard.
The selected read-only check reports changed/blocked, zero transformations and no
successful-validation date; source snapshot and report are in ignored maintenance cache.
No file under APIs/ was changed and import refusal was verified before fetching/writing.

Validation reports previously truncated the repr of a huge failed response schema before
showing the actual defect. The new bounded formatter follows nested error context,
prints escaped JSON Pointer locations plus keyword/type findings, omits redundant
missing-$ref alternative branches when actual failures exist, and limits output to five
distinct leaf findings / 1,500 characters. This does not enumerate every document error.
For schema-meta/default errors the pinned validator emits schema-relative paths; location
annotations are attached after its normal exception conversion, so its outer wrapper
preserves them. Resolved targets are located by object identity with cycle guards,
including referenced component definitions. Validation semantics remain unchanged.
Four regression tests cover actual 3.0/3.1 rejection, pointer escaping, nested keyword
causes, empty unions, numeric bounds, invalid defaults, omitted payload/default values,
referenced target locations and unchanged input. All **83 tests pass locally**. Infrastructure [PR #138](https://github.com/ontola/openapi-directory/pull/138) merged
with exact head `78c32fb8ecb96c985ee059ee24e4da7dad7db2f2`, merge
`4193a52552358a085fe4d538bac51629c2f2c83d`. [CI 37189747823](https://github.com/ontola/openapi-directory/actions/runs/37189747823)
passes all 83 tests; only AGENTS.md and five maintenance files changed. The full 33-source
audit was dispatched at this merged main as run 37189799727. Do not represent earlier
32-source evidence as validating this registration; its completed results are recorded below.


**Zoom Meetings discovery lead (2026-10-04 UTC; not registered/imported):**
Zoom's own [Meetings inventory](https://github.com/zoom/skills/blob/2d75fba014118e5eafbc75c4143418fb2d934e29/skills/rest-api/references/meetings.md)
explicitly names `https://developers.zoom.us/api-hub/meetings/methods/endpoints.json`
as its canonical OpenAPI input, with `https://api.zoom.us/v2` base URL. Vendor repository
reference pinned at `2d75fba014118e5eafbc75c4143418fb2d934e29`; its dated inventory is
129 paths / 184 operations, so it cannot substitute for fetching the current description.
The hosted artifact fetched at `2026-10-04T08:43:47.902356+00:00` is native **3.0.0**,
declared version **2**, **131 paths / 186 operations**, SHA-256
`969f8b111fe98ae12e4cb8c035fc3bfbc51a281217f0158ca3665d26efeab946`, ETag
`"7b5b47313b8b713b584827ece8a5447e"`, Last-Modified
`Mon, 28 Sep 2026 22:49:37 GMT`. No external references. **Validation fails** at GET
/users/{userId}/recordings query `recording_source_type`: string default `"null"` is
absent from its two-value enum, though described in vendor prose. Do not silently alter
that enum, drop the default or waive validation; review an exact evidenced repair or
vendor correction separately. New diagnostic points at the actual parameter/schema/default.

Existing `zoom.us/2.0.0` has 265 paths / 373 ops and covers broader services. Do not replace
it with this narrower Meetings-only artifact or imply that the old combined coverage is
retired. The current [Meetings reference](https://developers.zoom.us/docs/api/meetings/)
advertises OpenAPI 3.1.1 whereas this named hosted input declares 3.0.0: resolve that
publication difference, public/stable feature lifecycle and product catalog/service
boundaries before registration/import. Archived `zoom/api` is not a current replacement.
Original bytes/fetch metadata are in ignored
`cache/maintenance/discovery/zoom-meetings/<hash>/`, with pinned ownership reference
alongside; temps `/tmp/zoom-meetings-source`, `/tmp/zoom-meetings-meta.json`,
`/tmp/zoom-meetings-validation.json` and `/tmp/zoom-meetings-official-reference.md`.
Continue this major-provider lead rather than repeating old guessed URLs.


**Expanded 33-source audit verified (2026-10-04 UTC):**
[Run 37189799727](https://github.com/ontola/openapi-directory/actions/runs/37189799727)
at main `4193a52552358a085fe4d538bac51629c2f2c83d` passes all **83 tests**, fetches/prepares
all **33 artifacts / 32 services**, and reports **27 validated matches / six known import
blockers**: Cohere, Square, archived Slack, native Meraki, Twilio Messaging delivery and
Vercel. No new fetch/prepare failures or unblocked drift. Vercel's native source is
321 / 443 at the exact hash above, with an explicit import guard, exact nested `const`
failures and no successful-validation date. Cohere now points directly to
`#/components/schemas/TruncationStrategy/oneOf`; Square still fails on `info.externalDocs`
with missing vendor definitions unresolved; Meraki retains 822 undefined OAuth2 requirements.
Messaging remains valid but publication-blocked pending the existing unanswered owner
choice. No rejected push was retried, no vendor example was redacted and parked work remains.

The expected nonzero audit exit is solely these six blockers. Test job, readable summary
and complete artifact upload succeeded. Downloaded reports, every one of the 33 entry
hashes, 21 distinct repository metadata hashes, validation profiles, actual per-row base,
classifications, Vercel/Asana/Twilio-specific rows and rendered Markdown were verified at
`/tmp/openapi-ci-audit-37189799727`; ignored local reports/health snapshots are updated.
Hosted sources Hugging Face and Vercel remain health-unassessed. Verifier/log:
`/tmp/verify-vercel-full-audit.py`, `/tmp/vercel-full-audit-verification.log`; CI log
`/tmp/vercel-full-audit-ci-complete.log`. Recover the durable `official-source-audit`
artifact after reboot. API inventory remains 729 domains / 4266 files / 2092 openapi.yaml /
2168 swagger.yaml; infrastructure registration changes no API spec.

**Resume next:** This is the latest verified full audit; Vercel monitoring/diagnostics are
merged and require no duplicate PR/import. Continue independent major-provider discovery,
especially Zoom's current product-specific publishing sources/lifecycle or another stable
missing provider. OpenRouter/Vercel schema repairs need separately reviewed official
evidence. Do not replace broad existing coverage with a narrower service artifact.
Per-service PR generation and monthly repository discovery remain authorized future
infrastructure work, with no blanket automatic merging. Respect the one-week deadline and
local sleep constraint, and preserve Messaging's local verified branch awaiting user choice.


**Zoom Meetings publishing / exact correction reviewed (2026-10-04 UTC):**
The current `https://developers.zoom.us/docs/api/meetings/` HTML page's own serialized
page data explicitly specifies downloadPath `/api-hub/meetings/methods/endpoints.json`.
Its embedded native spec also declares 3.0.0, version 2, 131 paths / 186 ops. All
non-security content is parsed-identical to the hosted download. The page viewer changes
apiKey display to bearer and removes OAuth scope requirements; preserve the actual download,
not this viewer representation. This resolves the prior 3.1.1 markdown-rendering discrepancy:
that display label is not the downloadable/embedded artifact's declared dialect. No
conversion or fabricated 3.1 version is needed. The pinned vendor inventory independently
names the same URL; the older `/api-hub/meetings/` page itself returns 404, which does not
invalidate its downloadable JSON or the current `/docs/api/meetings/` reference.

Reviewed correction: query `recording_source_type` for GET /users/{userId}/recordings
has string default `"null"`, and its own description explicitly documents that literal
as the all-recordings mode alongside the two other modes. The exact same parameter is
embedded in the live public page. Its enum accidentally omits that documented option.
`maintenance/patches/zoom-meetings.json` appends literal string `"null"` to the two-value
enum, preserving the declared default, example, complete query/path parameter list and all
other fields. The recipe asserts the entire original list plus operationId `recordingsList`
and summary, so changed meaning, moved parameters or an upstream correction stop replay.
No actual JSON null coercion, default/constraint removal or invented mode. The fully patched
native artifact validates with zero errors and zero external refs; manual guard tests reject
a vendor-fixed enum, changed description and changed operation identity. All 83 offline tests
pass. The exact typed recipe and its hash/explanation travel in in-spec provenance.

Register this distinct current public Meetings/Webinars product description at
`APIs/zoom.us/meetings/2/openapi.yaml`, retaining vendor version `2`. Full fetched main has
only the broader historical `zoom.us/2.0.0` (265 paths / 373 ops across Users, Accounts,
Phone, Rooms and other products); it remains byte-for-byte intact. Of the current product's
131 paths / 186 ops, 70 paths overlap the historical combined snapshot and 61 paths /
86 ops are absent there. This is an updated product-specific publication, not a replacement
of broad combined coverage or proof of retired routes. Do not copy generic combined
curation/permalinks to this new service or invent new curation. No API spec has been written
yet; deliver registry/recipe in its separate infrastructure PR before the API import.
The registry is now 34 artifacts / 33 services; previous full audit still covers only 33.

Public current source retains deprecated parameters/fields and account/license restrictions;
no preview/experimental operation labels were found. A beta keyword occurs only in dummy
meeting-summary example prose, not as a lifecycle designation. Do not infer universal GA
from this observation. Other products are separate. **Phone discovery only**, not registered
or imported: official pinned inventory names
`https://developers.zoom.us/api-hub/phone/methods/endpoints.json`. Fetched at
`2026-10-04T09:00:58.708459+00:00`, native 3.0.0/version 2, 257 paths / 420 ops,
SHA-256 `b4b91c12a36bdfce98c74b584845049b3ce2b7138dfe4243f7903073934176a4`, fails at DELETE
/phone/call_queues/{callQueueId}/custom_groups/{customGroupId}/members/{extensionId}:
requestBody lacks required content. Do not invent its missing schema. Inspect public
product docs/vendor correction separately. Discovery snapshots remain ignored; no Phone
API files were changed, no parked decision or Messaging owner choice was actioned.


**Zoom Meetings service import prepared (2026-10-04 UTC):**
Infrastructure [#140](https://github.com/ontola/openapi-directory/pull/140) merged at
`2594640f3f215fd7c6927024ed7be0f9a408aa89`, exact PR head
`8d2546c0f50a026eca644b20243908d63b54263a`; [CI 37191129818](https://github.com/ontola/openapi-directory/actions/runs/37191129818)
passes all 83 tests. The live selected source check reports missing/new product artifact,
zero validation errors, one recorded patch, hosted health unassessed, same raw hash.

The updater fetched the unchanged official download at `2026-10-04T09:09:02.834482+00:00`
and generated `APIs/zoom.us/meetings/2/openapi.yaml`: native **3.0.0**, actual vendor **2**,
**131 paths / 186 operations**, 29,611 YAML lines, no external or local references
(vendor inlines schemas). The one exact enum repair is recorded with recipe SHA-256
`3c1336f698ec80692879d54eefbdf56b88dcf21d370a485db0153816852247aa` in `info.x-conversion`;
`x-origin` names the original official download. All other vendor data, including original
OAuth scope requirements, defaults, examples, deprecated fields and license restrictions,
is retained. No bundling, conversion, invented curation or additional content repairs.
Full prepared/imported validation, parsed vendor equality after exactly that repair,
source/recipe provenance, typed YAML roundtrip and byte equality of the historical combined
`zoom.us/2.0.0` all pass. This is a product-specific current publication, not a destructive
replacement of historical broader coverage. It adds one file and changes no existing API.
Verifier/log: `/tmp/verify-zoom-meetings-import.py`,
`/tmp/zoom-meetings-import-verification.log`; branch `codex/add-zoom-meetings`.
Deliver this API in its own PR, verify push/create/file list, then run the expanded
34-source audit against its actual merged main. Earlier audits do not validate this import.


**Zoom Meetings delivered (2026-10-04 UTC):**
[PR #141](https://github.com/ontola/openapi-directory/pull/141) merged with exact head
`a0a144cfdcb49bbfdc01459d6ca012dcf01307f1`, merge
`1e278e601e264273c8b519155ed2262d37f9a3bd`; verified CLEAN/MERGEABLE and exactly two
files: new Meetings service YAML plus AGENTS.md, zero deletions. Push succeeded without
protection exceptions. No older combined spec or curation was changed. API-only PR has no
infrastructure CI due to the workflow path filter; the expanded full audit below tests
and compares the actual merged main. Source registration/recipe were delivered separately
in #140. Full fetched main now has 729 domains / 4267 API files / 2093 openapi.yaml /
2168 swagger.yaml. Do not duplicate this addition or confuse its product-specific scope
with complete Zoom platform coverage.

**Next Zoom product candidates (2026-10-04 UTC; discovery only):**
The official `zoom/skills` references directory at pinned
`2d75fba014118e5eafbc75c4143418fb2d934e29` contains separate Users and Accounts inventories,
explicitly naming the following product JSON inputs. Both fetched/parsed and passed full
validation without patches; this is not yet completion of public lifecycle/scope review
or source registration. The broader legacy combined description covers these products,
but distinct maintained product layouts are absent from the full fetched main. Preserve
that legacy file; verify current public pages, original download auth and service
boundaries before importing, one API PR per product.
- **Users**: `https://developers.zoom.us/api-hub/users/methods/endpoints.json`, native
  OpenAPI 3.0.0, declared version 2, **46 paths / 76 ops**, fetched
  `2026-10-04T09:13:26.255129+00:00`, SHA-256
  `c83ce0ee31d51bf9715c9a95930b05feb0dbf360e87c012a25e170841a761d0f`,
  ETag `"5f31525a096323479cf1b3eb26c58654"`, Last-Modified
  `Mon, 28 Sep 2026 22:49:41 GMT`.
- **Accounts**: `https://developers.zoom.us/api-hub/accounts/methods/endpoints.json`, native
  OpenAPI 3.0.0, declared version 2, **66 paths / 87 ops**, fetched
  `2026-10-04T09:13:26.181811+00:00`, SHA-256
  `868e9e60f64152024a77ae56b718319d069c0cbdc8943fba1e0510ea1039254f`,
  ETag `"2ab076076726a6e4b2fae943b4fa3a02"`, Last-Modified
  `Mon, 28 Sep 2026 22:49:34 GMT`.
Both hosted sources have no revision and health remains unassessed. Complete source bytes,
fetch metadata, pinned vendor inventory evidence and validation results are in ignored
`cache/maintenance/discovery/zoom-users/<hash>/` and `zoom-accounts/<hash>/`.
Discovery script/logs `/tmp/inspect-zoom-product.py`, `/tmp/zoom-users-discovery.json`,
`/tmp/zoom-accounts-discovery.json`; reconstruct from pinned inventories after reboot.
Phone remains blocked on missing requestBody content; do not fabricate a request schema.


**Expanded 34-source audit verified (2026-10-04 UTC):**
[Run 37191393072](https://github.com/ontola/openapi-directory/actions/runs/37191393072)
at actual main `1e278e601e264273c8b519155ed2262d37f9a3bd` passes all **83 tests**,
fetches/prepares all **34 artifacts / 33 services**, and reports **28 validated matches /
six known import blockers** (Cohere, Square, archived Slack, native Meraki, Twilio Messaging
delivery and Vercel). No new fetch/prepare failures or unblocked drift. Zoom Meetings matches
its current official source at 131 paths / 186 ops, source hash
`969f8b111fe98ae12e4cb8c035fc3bfbc51a281217f0158ca3665d26efeab946`, one exact documented
repair with recipe hash `3c1336f698ec80692879d54eefbdf56b88dcf21d370a485db0153816852247aa`,
zero validation errors and no added/removed paths or operations relative to its imported file.
Historical combined Zoom bytes remain unchanged; this result does not establish freshness
for unregistered Zoom products. Hosted source health for Zoom, Hugging Face and Vercel
remains unassessed; 21 distinct GitHub repository metadata snapshots were verified.

The nonzero audit exit is solely the six known blockers. Test job, readable job summary
and complete artifact upload succeeded. Downloaded JSON/Markdown reports, all 34 entry
hashes and 21 repository hashes, exact per-row comparison base, validation profiles,
classifications and the Zoom-specific transformation/match row were verified at
`/tmp/openapi-ci-audit-37191393072`; ignored local report/health cache is updated.
Verifier/log: `/tmp/verify-zoom-full-audit.py`, `/tmp/zoom-full-audit-verification.log`;
CI log `/tmp/zoom-full-audit-ci-complete.log`. Recover the durable `official-source-audit`
artifact after reboot. No owner-only protection exception, redaction or parked work was
actioned. All required work for #140/#141 is complete; no duplicate registration/import PR.

**Resume next:** This 34-source run supersedes earlier full audits. Review the current
public Users and Accounts publishing pages and lifecycle, confirm their original downloads,
then register/import those valid distinct product descriptions one PR per API. Their
previous fetched counts/hashes are discovery snapshots, not release guarantees. Phone
needs evidenced vendor correction or exact repair review; do not invent its missing body.
Continue other major-provider discovery and authorized separate updater PR-generation /
monthly-discovery infrastructure. Keep all explicit parked items, Messaging owner decision,
source-validation blockers, local sleep constraints and the one-week deadline in force.


**Zoom Users / Accounts source review and registration (2026-10-04 UTC):**
The current public [Users](https://developers.zoom.us/docs/api/users/) and
[Accounts](https://developers.zoom.us/docs/api/accounts/) pages explicitly name their
`/api-hub/<product>/methods/endpoints.json` downloads in serialized page data. Each embeds
native 3.0.0/version 2. All non-security content matches the fetched download; the viewer
simplifies authentication, as with Meetings. Preserve original OAuth scope requirements
and API-key scheme, not the viewer's altered auth. The markdown rendering's 3.1.1 label
is not the actual artifact's dialect. The pinned official inventories cited above confirm
both inputs independently. No OpenAPI conversion, patches or bundling needed.

Fresh downloads at `2026-10-04T10:11:10.620452+00:00` (Users) and
`2026-10-04T10:11:10.699509+00:00` (Accounts) retain the exact hashes/ETags/Last-Modified
values recorded in discovery above. **Users: 46 paths / 76 ops**, user/group/contact-group
administration, settings and provisioning; **Accounts: 66 / 87**, account/subaccount
administration, settings, roles, dashboards, information barriers and data compliance.
Both fully validate without repairs, with zero local/external references (inlined schemas).
No beta/preview/experimental string mentions were found in either full artifact. This
is a current public product description, not proof every licensed/master-account feature
is GA; preserve deprecated fields and plan/account restrictions. Hosted health unassessed.

Full fetched main contains only the legacy combined Zoom spec and the newly maintained
Meetings product, not these separate product layouts. No operations overlap Users vs
Accounts or either with Meetings. These are distinct public product descriptions, not
HubSpot-style duplicated object slices. Users adds 21 paths / 34 ops absent from the
legacy combined snapshot; Accounts adds 32 / 47. Leave historical combined coverage
byte-for-byte intact; do not replace its broader services or copy its generic curation/
permalinks to new services. New layouts: `zoom.us/users/2` and `zoom.us/accounts/2`,
actual declared version `2` each; no invented curation. Registry expands to **36 artifacts /
35 services** in a separate infrastructure PR before the two API-specific imports.
The previous full audit still covers only 34, until this expanded audit is completed.

Current-page HTML/fetch evidence, page data, original bytes and pinned vendor references
are in ignored `cache/maintenance/discovery/zoom-users/<hash>/` and `zoom-accounts/<hash>/`.
Review script/outputs: `/tmp/verify-zoom-product-source.py`,
`/tmp/zoom-users-source-review.json`, `/tmp/zoom-accounts-source-review.json`.
Phone remains blocked and all parked work/Messaging owner choice remain untouched.


**Zoom Users import prepared / source infrastructure delivered (2026-10-04 UTC):**
[#143](https://github.com/ontola/openapi-directory/pull/143) merged at
`40aebc5ad722c74740421600f24f3cd9dff7820c`, exact head
`37203eefdac1a47491f92de6e094c6f39d2c32bb`;
[CI 37196429832](https://github.com/ontola/openapi-directory/actions/runs/37196429832)
passes all 83 tests. Brief PR-create connection failure was reconciled by an all-state
REST head search before retry; no duplicate PR was created. Sources/README/AGENTS only.

The updater re-fetched Users at `2026-10-04T10:53:00.030778+00:00` with unchanged hash
`c83ce0ee31d51bf9715c9a95930b05feb0dbf360e87c012a25e170841a761d0f`, and generated
`APIs/zoom.us/users/2/openapi.yaml`: native 3.0.0, declared version 2, **46 paths / 76 ops**,
20,624 YAML lines. No patches, bundling, conversion or local/external refs; vendor inlines
schemas. Full prepared/imported validation, complete unmodified vendor-content equality,
source/date/hash provenance and typed YAML roundtrip pass. No invented curation; legacy
combined Zoom and existing Meetings are byte-identical. Original OAuth scopes, defaults,
examples, deprecated fields and license restrictions remain. This product contributes
21 paths / 34 ops absent from historical combined coverage, which remains intact.
Verifier/log `/tmp/verify-zoom-clean-import.py users`,
`/tmp/zoom-users-import-verification.log`; local branch `codex/add-zoom-users`.
Deliver this API-specific PR before proceeding with Accounts in its own PR; full
36-source audit follows both merges and must use the actual merged base.


**Zoom Users delivered / Accounts import prepared (2026-10-04 UTC):**
[#144](https://github.com/ontola/openapi-directory/pull/144) merged with exact Users head
`c0f19a5384f149779fae79da210258ae8a2bdd12`, merge
`f6b35019052eb68eeab293c666b9d968d7c44515`; verified CLEAN/MERGEABLE, exactly the new
Users YAML plus AGENTS.md, zero deletions. Push succeeded without protection exceptions.
No duplicate Users PR/import is needed. API-only CI is absent due to workflow path filter;
the expanded network audit after Accounts must verify both actual imported files.

The updater fetched Accounts at `2026-10-04T11:39:58.873157+00:00`, unchanged SHA-256
`868e9e60f64152024a77ae56b718319d069c0cbdc8943fba1e0510ea1039254f`, generating
`APIs/zoom.us/accounts/2/openapi.yaml`: native 3.0.0, actual vendor version 2,
**66 paths / 87 ops**, 29,930 YAML lines. No content patches, bundling or conversion;
no local/external refs, because vendor schemas are inlined. Original OAuth scope
requirements, defaults/examples, deprecated fields and license/master-account restrictions
remain intact. Prepared/imported strict validation, full unmodified vendor-content equality,
source/date/hash provenance and typed YAML roundtrip pass; no invented curation.
Legacy combined Zoom, Meetings and the new Users file remain byte-identical to main.
Accounts contributes 32 paths / 47 ops absent from the historical combined snapshot,
which remains intact; no prior routes are removed or declared retired.
Verifier/log `/tmp/verify-zoom-clean-import.py accounts`,
`/tmp/zoom-accounts-import-verification.log`; branch `codex/add-zoom-accounts`.
Deliver this separate API PR, then run/verify the full 36-source audit on the merged base.
Phone, Vercel, OpenRouter and other recorded blockers/parked items remain untouched.


**Zoom Users / Accounts delivered; expanded audit fetch failure (2026-10-04 UTC):**
[#144](https://github.com/ontola/openapi-directory/pull/144) Users and
[#145](https://github.com/ontola/openapi-directory/pull/145) Accounts are merged and
attached. Accounts exact head `b34a01305d97b7a622f70123c5344b6155424675`, merge
`8073e1124f8cae3aee7ce99e44ab133d9d9f2764`. A connection reset during the merge was
reconciled by reading its confirmed MERGED state and exact merge commit; do not retry.
Both PRs contain only their new product YAML plus AGENTS.md, with zero deletions;
legacy combined Zoom and existing product files remain unchanged. Inventory recomputed
from fetched main: 729 domains / 4269 files / 2095 openapi.yaml / 2168 swagger.yaml.
No duplicate registration or API imports are needed.

Expanded [audit 37203709144](https://github.com/ontola/openapi-directory/actions/runs/37203709144)
at actual main `8073e1124f8cae3aee7ce99e44ab133d9d9f2764` passes all 83 tests,
but **31 GitHub-hosted sources fail with HTTP 403 rate limit exceeded**, including
repository metadata. The five hosted inputs succeed: Users, Accounts, Meetings and
Hugging Face match, while Vercel retains its known validation/import blocker. The summary
and complete partial-result artifact upload succeed. This is not a complete 36-source
validation; the latest complete verified audit remains 37191393072 (34 sources).
Failed report/artifact preserved at `/tmp/openapi-ci-audit-37203709144`; log
`/tmp/zoom-expanded-audit-ci.log`. Do not replace previous success evidence with a claim
that GitHub sources were freshly checked.

**Scoped GitHub API authentication implemented (2026-10-04 UTC; delivery pending):**
The updater's optional `GITHUB_TOKEN` environment variable is used only for exact HTTPS
`api.github.com`, default/443 port and no URL user information. The Actions audit step
receives its built-in token under existing `contents: read`; no new permissions, PR
creation or merging. Raw downloads, archives and third-party hosts remain unauthenticated.
An unredirected Authorization header is discarded by urllib on every redirect, including
same-origin redirects; configure canonical API URLs. Headers are not cached or reported.
HTTP 403 remains a single failed attempt with no anonymous fallback or blind quota retry.
All 87 offline tests pass (83 previous plus four HTTP regressions). They exercise API
authentication/metadata, excluded hosts/authorities, real urllib redirect handling and
fail-closed 403 behavior. Deliver this infrastructure
separately, verify its exact-head CI, then rerun and verify the complete 36-source audit
on merged main. Phone, OpenRouter, vendor validation defects, Messaging owner choice and
all parked items remain untouched; maintain the original deadline and local sleep policy.


**Scoped authentication delivered / full 36-source audit verified (2026-10-04 UTC):**
[#146](https://github.com/ontola/openapi-directory/pull/146) merged and attached,
exact head `22639559ab3e06c68efefe59772108bb7d229595`, merge
`f16fa55cdc0ca4ed8da667f6a6769dd6a706f649`. Its
[CI 37209014620](https://github.com/ontola/openapi-directory/actions/runs/37209014620)
passes all **87 tests**, including four new HTTP authentication/redirect regressions.
Five expected infrastructure/instruction files only; CLEAN/MERGEABLE before merge;
workflow permissions still `contents: read`. No API data or vendor examples changed.

The subsequent full [audit 37211039800](https://github.com/ontola/openapi-directory/actions/runs/37211039800)
at actual merged main `f16fa55cdc0ca4ed8da667f6a6769dd6a706f649` passes all **87 tests**,
fetches/prepares all **36 artifacts / 35 services**, and reports **30 validated matches /
six known import blockers**. All GitHub source and repository metadata requests now
succeed; no new fetch/prepare failures or unblocked drift. The six blockers remain
Cohere's empty union, Square's invalid Info metadata/undefined schemas, archived unsupported
Slack, Meraki's undefined OAuth2 requirements, Twilio Messaging publication protection
pending the existing owner choice, and Vercel's invalid native source. Validation and
import guards remain enforced; the audit's nonzero exit is solely these known blockers.
Readable summary and complete artifact upload succeed.

Both new Zoom products match their imported native 3.0.0/version 2 files exactly:
Users **46 paths / 76 ops**, raw SHA-256
`c83ce0ee31d51bf9715c9a95930b05feb0dbf360e87c012a25e170841a761d0f`;
Accounts **66 / 87**, raw SHA-256
`868e9e60f64152024a77ae56b718319d069c0cbdc8943fba1e0510ea1039254f`.
Zero validation errors, no transformations, no added/removed endpoints relative to their
imports, no invented curation. Meetings also matches at 131 / 186 with its one reviewed
exact repair. Legacy combined Zoom remains unchanged. This validates configured product
artifacts, not every Zoom product or every feature's general availability. Hosted sources
Zoom's three products, Hugging Face and Vercel remain health-unassessed; 21 distinct GitHub
repository metadata snapshots were verified separately.

Downloaded JSON/Markdown reports, every one of the 36 entry-source hashes, all 21
repository metadata hashes, per-row actual comparison bases, validation profiles,
classifications, transformation evidence and rendered Markdown were verified at
`/tmp/openapi-ci-audit-37211039800`. Ignored local reports/health snapshots are refreshed.
Verifier/log `/tmp/verify-zoom-36-full-audit.py`,
`/tmp/zoom-36-full-audit-verification.log`; CI log `/tmp/source-auth-full-audit-ci.log`.
Recover the durable `official-source-audit` artifact after reboot. Inventory remains
729 domains / 4269 API files / 2095 openapi.yaml / 2168 swagger.yaml.

**Resume next:** This is the latest complete verified audit, superseding the earlier
34-source success and incomplete anonymous-rate-limited 36-source attempt. Users and
Accounts (#144/#145), registrations (#143) and scoped authentication (#146) are done;
do not duplicate their PRs. Continue independent well-known provider discovery or
separately scoped updater PR-generation/monthly-discovery infrastructure. Zoom Phone
still needs evidence for its missing requestBody content; OpenRouter and Vercel need
reviewed vendor schema evidence. Do not invent schemas, relax validation, retry Messaging's
rejected push, redact examples or action any explicitly parked item. Preserve its local
verified branch and the existing unanswered owner choice. Keep the original one-week
deadline and local laptop sleep policy; no additional chat automation.


**Mailchimp Transactional official source / initial Swagger baseline (2026-10-04 UTC):**
The [public Transactional reference](https://mailchimp.com/developer/transactional/api/)
directly links `mailchimp/mailchimp-client-lib-codegen/spec/transactional.openapi.json`.
Vendor repository README/spec instructions identify official SDK/docs generation inputs;
Mailchimp's Tools page links these official clients. Transactional Email is formerly
Mandrill, as its public overview says. Full fetched main already contains community
`mandrillapp.com/1.0/swagger.yaml` (90 paths / 90 ops, explicitly unofficial), plus
Marketing 3.0.55/3.0.91; no native Transactional release. This is a new official release
of existing provider coverage, not discovery of a wholly missing API. Preserve history
and curation under `APIs/mandrillapp.com/1.4.0/openapi.yaml`, not a duplicated provider.

Pinned repository `74feb256f8ba8bb9d5a322de83c92b42306831fd`, native artifact SHA-256
`c7e5fe9ee7376cf7becdfc3f12c8ea5d276e06b8da60687938506b4be339915c`, fetched
`2026-10-04T15:57:42.146304+00:00`: **OpenAPI 3.1.0 / vendor 1.4.0 / 99 paths / 99 ops**,
fully validates without patches, bundling or conversion. The public page's 1.4.1 display
links this exact 1.4.0 native file; separate `transactional.json` Swagger SDK input declares
1.4.1 and a different base API version, though it has the same operation/path set.
Do not borrow that label, downgrade native 3.1 or silently substitute/concatenate SDK data.
Repository is public, unarchived/undisabled with exact identity. No beta/preview/experimental/
deprecated string designations in the native document; public documentation advertises
email and SMS without a preview badge. Retain account/plan restrictions; this is not proof
all features are GA. Body-key authentication is vendor content, not a missing security
scheme to invent. All stored history is retained, including legacy unofficial labeling.

Human comparison after stripping only legacy `.json` suffix: 15 added paths and six absent
from the native description. Three whitelist methods have new allowlist counterparts;
three old URL analytics methods are absent. Do not report all 90 raw renamed paths as
actual retirements or delete the historical description. Added surface includes SMS and
SMS rejection management, Mailchimp templates, allowlists, sender/tracking-domain deletion.
The updater still reports literal path/operation additions and removals; provenance is
scoped to the native vendor input. No route/server/schema or vendor-prose changes proposed.

Infrastructure adds explicit `initial_baseline`, used only when the new destination and
current manifest target are both missing. Safe same-provider canonical Swagger/OpenAPI
paths only; missing configured history fails rather than discarding curation. Existing
imported releases take priority for subsequent comparisons. Two regressions exercise a
full Swagger-to-native first import, curation/provenance/history preservation, subsequent
baseline selection and unsafe/missing history guards. **89 offline tests pass**.
Register native Transactional separately before its API PR; registry becomes **37 artifacts /
36 services**. Source cache/evidence in ignored `cache/maintenance/discovery/` includes
native bytes, pinned README/spec instructions/scripts and repository metadata. Scripts/logs:
`/tmp/review-mailchimp-native.py`, `/tmp/mailchimp-native-review.log`,
`/tmp/mailchimp-baseline-tests.log`. Previous full audit covers 36 until expanded after import.

Marketing discovery: official `spec/marketing.json` remains Swagger2/version3.0.91,
181 paths, source hash `374046a5209daa8d68cdb5dd7e0244fcf214928af4321ff539755849641b9a21`.
No native Marketing artifact in this pinned directory. The converter records 218 automatic
patches and zero warnings, requiring detailed review before registering or importing;
Transactional Swagger similarly records 101 patches, avoided by the explicitly linked
native source. Do not waive conversion expectations or claim Marketing freshly validated.
Marketing snapshots/diagnostics remain discovery-only; no spec edits. Parked decisions,
Messaging owner choice and original deadline/local-sleep constraint remain in force.


**Mailchimp Transactional official import prepared (2026-10-04 UTC):**
[#148](https://github.com/ontola/openapi-directory/pull/148) infrastructure merged at
`a775ab199ac7def1ce815c153180aded28d77173`, exact head
`e5514875debc27d08553d8d8552216650c4ec5f2`;
[CI 37219014419](https://github.com/ontola/openapi-directory/actions/runs/37219014419)
passes all 89 tests. Live source check validates the native artifact and repository
health, recording historical Swagger as initial comparison/curation baseline.

The updater re-fetched unchanged native source at `2026-10-04T17:13:44.212069+00:00`
and generated `APIs/mandrillapp.com/1.4.0/openapi.yaml`: native **3.1.0**, actual declared
**1.4.0**, **99 paths / 99 operations**, 8429 YAML lines. All 778 local references
resolve; zero external references. No content patches, bundling or version conversion.
Full strict source/import validation, complete vendor-content equality after curation,
source/revision/hash provenance and typed YAML roundtrip pass. Existing categories, logo,
provider name and externalDocs are preserved from `1.0/swagger.yaml`, which remains
byte-identical and retains its historical unofficial label. The new vendor-published file
is not labelled unofficial; that source-classification flag is not curation to copy.
No invented metadata or changes to vendor paths, servers, schemas/defaults or body keys.
Verifier/log: `/tmp/verify-mailchimp-import.py`, `/tmp/mailchimp-import-verification.log`;
branch `codex/add-official-mailchimp-transactional`. Deliver this separate API PR then
verify the expanded 37-source audit on actual merged main. All recorded blockers and
parked decisions remain untouched.


**Mailchimp Transactional delivered (2026-10-04 UTC):**
[#149](https://github.com/ontola/openapi-directory/pull/149) merged and attached,
exact head `bad886d70dcebd9c36e37a173a5db8cd448d1d50`, merge
`be3d1fe310356d7f8797227f34df7cac9174aa64`. Verified CLEAN/MERGEABLE and exactly
two expected files: new 1.4.0 OpenAPI YAML plus AGENTS.md, 8453 added lines, zero deletions.
Push succeeded without protection exceptions; no historical file or old unofficial label
was changed. API-only PR has no infrastructure CI due to workflow path filter; #148's
source/baseline CI passes 89 tests and the expanded network audit follows on actual merged
main. Inventory recomputed from fetched tree: 729 domains / 4270 API files /
2096 openapi.yaml / 2168 swagger.yaml. This is new official-release coverage under an
existing provider, not a wholly missing vendor. Do not duplicate registration/import.


**Expanded 37-source audit verified (2026-10-04 UTC):**
[Run 37221885851](https://github.com/ontola/openapi-directory/actions/runs/37221885851)
at actual merged main `be3d1fe310356d7f8797227f34df7cac9174aa64` passes all **89 tests**,
fetches/prepares all **37 artifacts / 36 services**, and reports **31 validated matches /
six known import blockers**. No new fetch/prepare failures or unblocked drift. Mailchimp
Transactional matches its imported native 3.1.0 / declared 1.4.0 / 99 paths / 99 ops,
source SHA-256 `c7e5fe9ee7376cf7becdfc3f12c8ea5d276e06b8da60687938506b4be339915c`,
revision `74feb256f8ba8bb9d5a322de83c92b42306831fd`, no transformations or validation errors.
Its actual comparison baseline is now `mandrillapp.com/1.4.0/openapi.yaml`, proving that
subsequent audits prefer the current official import over the initial community Swagger.
No path/operation additions or removals relative to the new imported file. The historical
community snapshot remains unchanged; Marketing still requires separate conversion review.

The six blockers remain Cohere, Square, archived unsupported Slack, native Meraki,
Twilio Messaging delivery and Vercel. Strict validation and all import guards remain in
force; the nonzero audit exit is solely these recorded blockers. Tests, readable summary
and complete artifact upload succeed. All 37 original entry hashes, 22 distinct GitHub
repository metadata hashes, per-row actual comparison bases, validation profiles,
classifications, Mailchimp/Zoom/Twilio/Vercel transformation rows and rendered Markdown
were verified in `/tmp/openapi-ci-audit-37221885851`. Hosted health for three Zoom
products, Hugging Face and Vercel remains unassessed. Ignored local reports/health cache
is updated. Recover the durable `official-source-audit` artifact after reboot.
Verifier/log `/tmp/verify-mailchimp-37-full-audit.py`,
`/tmp/mailchimp-37-full-audit-verification.log`; CI log `/tmp/mailchimp-full-audit-ci.log`.
A local watch experienced a connection reset; the workflow continued normally, with no
duplicate dispatch or interrupted job. Inventory remains 729 domains / 4270 files /
2096 openapi.yaml / 2168 swagger.yaml; no check-only timestamp API commits.

**Resume next:** This is the latest complete verified audit. Mailchimp Transactional
source/baseline infrastructure #148 and official import #149 are delivered, attached and
require no duplicate PR. Continue independent well-known provider discovery or separately
scoped updater PR-generation/monthly-discovery infrastructure. Mailchimp Marketing's 218
converter patches require a precise review before enabling conversion; cached diagnostics
are leads, not a validated source. Zoom Phone, OpenRouter, Vercel and other vendor schema
blockers need official evidence; do not fabricate repairs or relax validation. Messaging's
local verified branch and unanswered owner choice remain intact. Respect all parked
items, the one-week deadline and local laptop sleep policy; no additional chat automation.


**Mailchimp Marketing live publishing audit / monitoring (2026-10-04 UTC):**
The official Marketing fundamentals' API self-description link and pinned vendor
`spec/README.md` SDK instructions name
`https://api.mailchimp.com/schema/3.0/Swagger.json?expand`, exactly the existing 3.0.91
spec's `x-origin`. Fetch at `2026-10-04T18:08:50.165470+00:00`, raw SHA-256
`064cfd877f087cf4c6679681f44f6e0f1d10c667d4f524e34e25ee68f46010bc`, no ETag or
Last-Modified, native Swagger 2.0 / **3.0.91 / 181 paths / 298 ops**, zero external refs.
Hosted repository health is explicitly unassessed. Do not substitute the older GitHub SDK
snapshot just because its version/path/operation counts agree. At pinned repository
`74feb256f8ba8bb9d5a322de83c92b42306831fd`, SDK raw hash
`374046a5209daa8d68cdb5dd7e0244fcf214928af4321ff539755849641b9a21` differs at **23 raw
source positions**: production adds webhook `signing_enabled` boolean metadata, permits
empty language enum values, caps SMS media at one item, adds media MIME metadata and
updates audience consent/stat/prose. No new/removed paths or operations. Conversion
layout differences (e.g. generated requestBody aliases) are separate from this source drift.
This demonstrates fixed-version/count equality is insufficient evidence of freshness.

Reviewed the 218 converter counts against the actual locked 7.0.8 implementation:
**210** processResponse increments for already-empty response descriptions leave their
strings unchanged; **eight** fixUpSubSchema increments translate exact `type: [string,
integer]` image variant-ID item schemas to disjoint string/integer `oneOf` alternatives.
No null union or guessed missing type. All eight are explicit source fields in e-commerce
order/product/image request schemas. No warnings; paths and operations survive exactly.
Accept expected 218 converter counts for comparison, retaining complete strict validation.
A real-converter regression verifies empty-description preservation, disjoint union shape,
unchanged invalid boolean-on-string defaults and import rejection. **90 offline tests pass**.

**Import remains blocked:** first exact validation error is
`#/paths/~1lists/get/responses/200/content/application~1json/schema/properties/lists/items/properties/notify_on_subscribe/default`:
expected string, got bool. Inspection finds **20 converted occurrences** of boolean false
defaults on the two string notification fields (response representations repeat schemas).
These exist in the original vendor input, not a parser/converter regression. Do not coerce
to string, infer a schema union, remove default annotations or waive validation without a
separately justified exact correction. The current stored 3.0.91 content remains intact,
along with 3.0.55 history and all curation. No Marketing API refresh PR is proposed.
The broad existing vendor publication includes Audiences marked BETA in public docs;
retain its scope honestly, not a universal GA claim or arbitrary stable-only slice.

Register live production source `mailchimp-marketing`, current baseline
`APIs/mailchimp.com/3.0.91/openapi.yaml`, conversion expected 218 patches / zero warnings;
registry becomes **38 artifacts / 37 services** in its own infrastructure PR. No API data
changes, blanket merging or protection bypass. Expected live selected check is changed /
validation-blocked, with zero added/removed endpoints. Previous full audit covers 37 until
this expansion is verified. Discovery scripts/logs `/tmp/trace-mailchimp-conversion.cjs`,
`/tmp/review-mailchimp-marketing.py`, `/tmp/prepare-mailchimp-marketing.py`,
`/tmp/mailchimp-marketing-production-review.log`, `/tmp/mailchimp-marketing-prepared-review.log`,
`/tmp/mailchimp-marketing-tests.log`; ignored cache stores original production/SDK bytes,
fetch metadata, complete diffs, converted outputs and trace script. Source health, all
existing blockers, parked items, Messaging owner choice, deadline and sleep constraints
remain unchanged. Continue independent implementation/discovery after recording delivery.


**Mailchimp Marketing monitoring delivered / 38-source audit verified (2026-10-04 UTC):**
[#151](https://github.com/ontola/openapi-directory/pull/151) merged and attached,
exact head `d98148d10705fb1e7aa8b3a7671405aee5c07e97`, merge
`15ba8fba732d3b6a6f16f7a4f2e5321e4d1fe46c`. Four expected infrastructure/instruction
files, all additions, no API data changes; CLEAN/MERGEABLE before merge.
[CI 37227031064](https://github.com/ontola/openapi-directory/actions/runs/37227031064)
passes all **90 tests**, including the real-converter default/import guard regression.
No API refresh is delivered or claimed: Marketing remains blocked on native vendor defaults.

Expanded [audit 37228165440](https://github.com/ontola/openapi-directory/actions/runs/37228165440)
at actual merged main `15ba8fba732d3b6a6f16f7a4f2e5321e4d1fe46c` passes all **90 tests**,
fetches/prepares all **38 artifacts / 37 services**, and reports **31 validated matches /
seven recorded import blockers**. No new fetch/prepare failures or unblocked drift.
Marketing's live production artifact has the reviewed raw hash
`064cfd877f087cf4c6679681f44f6e0f1d10c667d4f524e34e25ee68f46010bc`, actual baseline
`mailchimp.com/3.0.91/openapi.yaml`, unchanged 181 paths / 298 operations / version3.0.91,
zero endpoint additions/removals, one complete conversion with **218 counts / zero warnings**.
The exact string-notification/default validation pointer is reported, with no successful
validation timestamp; content drift is visible without treating its old stored file as
updated. Source health for Marketing is hosted/unassessed. The other six blockers remain
Cohere, Square, archived unsupported Slack, native Meraki, Messaging delivery and Vercel.
Strict validation and import guards remain enforced. The audit's nonzero exit is solely
these seven blockers; tests, readable-summary publication and complete artifact upload succeed.

All 38 entry-source hashes, 22 distinct GitHub repository metadata hashes, actual per-row
comparison bases, validation profiles, classifications, conversion evidence, specific
Mailchimp/Zoom/Twilio/Vercel rows and rendered Markdown were verified at
`/tmp/openapi-ci-audit-37228165440`. Six hosted artifacts (three Zoom products, Hugging Face,
Vercel and Marketing) remain health-unassessed. Ignored local reports/health cache updated;
recover the durable `official-source-audit` artifact after reboot. Verifier/log
`/tmp/verify-mailchimp-38-full-audit.py`, `/tmp/mailchimp-38-full-audit-verification.log`;
CI log `/tmp/mailchimp-marketing-full-audit-ci.log`. API inventory stays 729 domains /
4270 files / 2096 openapi.yaml / 2168 swagger.yaml. No timestamp-only spec commits.

**Resume next:** This is the latest complete verified audit. Marketing monitoring #151
is done; do not duplicate registration or import invalid vendor defaults. SDK/production
drift is now tracked, including webhook signing, language enums and SMS bounds. A future
API refresh needs separate exact correction evidence or a vendor fix; do not silently
remove/coerce defaults or fabricate allowed types. Continue independent well-known
provider discovery or authorized separate updater PR-generation/monthly-discovery work.
All previously recorded vendor blockers, explicitly parked items, Messaging's local
verified branch and unanswered owner choice remain in force. Keep the original one-week
deadline and local sleep policy; no extra recurring chat automation.

**Zoom Whiteboard / Scheduler official discovery (2026-10-05 UTC):** Current public
[Whiteboard](https://developers.zoom.us/docs/api/whiteboard/) and
[Scheduler](https://developers.zoom.us/docs/api/scheduler/) pages explicitly name their
`/api-hub/<product>/methods/endpoints.json` downloadPath and embed native **OpenAPI
3.0.0 / version 2**. The rendered markdown's 3.1.1 label is not the downloaded dialect.
All non-security content is equal; retain original downloadable OAuth scope requirements
and API-key scheme instead of the simplified viewer. Pinned vendor inventory
`zoom/skills` at `2d75fba014118e5eafbc75c4143418fb2d934e29`,
`skills/rest-api/references/{whiteboard,scheduler}.md`, independently names the inputs.
Inventory is supporting ownership/selection evidence, not proof of complete current
coverage. Whiteboard: **25 paths / 43 operations**, source hash
`3f35458bba020eda9f509a9d3f4908d4dbec7145493d10a95e3f287ef4a2eb87`.
Scheduler: **16 paths / 24 operations**, source hash
`b0231b26205920d8c331376cba65bf25e2d13ba4f438283b164a02a7186c6daf`.
Both validate strictly without patches, conversion or bundling; zero refs. All routes/
operations absent from historical combined Zoom, with no operation overlap with current
Meetings, Accounts or Users. Full fetched main tree has no other Zoom Whiteboard/Scheduler
service, brand or alias. Import each separately, retain all old files and native lifecycle,
license/account annotations. Whiteboard's only preview mentions describe image preview
links, not a release label; Scheduler has none. Public documentation/absent labels alone
are not a universal feature-GA claim. Hosted source health remains unassessed.
Register both sources in a separate infrastructure PR: **40 artifacts / 39 services**.
No blanket merging or protection bypass. Original bytes, ownership/page snapshots and
fetch evidence are in ignored discovery caches; scripts/logs
`/tmp/inspect-zoom-more.py`, `/tmp/verify-zoom-next-source.py`,
`/tmp/zoom-{whiteboard,scheduler}-source-review.json`.

**Additional Zoom candidates, do not import invalid data:** Rooms live hash
`58c50ddcc751451e599bd000a0d042343cb4e133c2b72e6c698848b94296bdbb`,
3.0.0 / 2 / **76 paths / 128 ops**, exact official input
`https://developers.zoom.us/api-hub/rooms/methods/endpoints.json`. Public Rooms page names
that download and matches all non-security content. GET/POST
`/workspaces/users/{userId}/calendar/settings` mark their in:path userId optional, despite
both explicit Missing User ID error responses. Correcting only required flags reveals
DELETE `/rooms/content/digital_signage/playlists/{playlistId}` requestBody has description
but no required content definition. Do not invent a payload or discard the useful prose;
no recipe, registration or API import delivered. Scratch proposed flag recipe was never
adopted. Team Chat's pinned vendor reference names `/api-hub/chat/methods/endpoints.json`,
not `/api-hub/team-chat/`; its 3.0.0 / 2 / **81 paths / 120 ops** source hash
`e3098b33ea735c09602370a04c84b703e93e25776e8fe752f3a1943c4ac0007f` has duplicate
channel_id in one required array. Semantically deduplicating it reveals PATCH
`/chat/channels/{channelId}/owner/{identifier}` requestBody missing content. No payload
invented, registration or import. Zoom Docs canonical canvas source also parses/validates
(29/39), hash `82cc4556a1ba6ff8770aae93bfe4de89ca13c51d5db82a4dc35bc13c4b65743c`;
ownership/public-page/lifecycle scope still needs separate review before registration.
All candidate raw bytes, pinned vendor references and initial validation saved in ignored
`cache/maintenance/discovery/zoom-*`. Previous blockers, parked items, unanswered Messaging
owner choice, week deadline and local sleep policy remain unchanged.

**Zoom monitoring delivered / Whiteboard import prepared (2026-10-05):** Infrastructure
[#153](https://github.com/ontola/openapi-directory/pull/153) merged and attached,
head `d452663e9dd00ad9f074702962d883421cbb7abd`, merge
`bbbff76d98c84623185ac94ac62c30c226a051f9`; three expected instruction/source files,
81 additions / zero deletions, CLEAN/MERGEABLE. CI
[37254924610](https://github.com/ontola/openapi-directory/actions/runs/37254924610)
passes all 90 tests. Registry has 40 artifacts / 39 services; latest complete verified
network audit still covers 38 until the new registrations/imports are audited.
Whiteboard importer re-fetched exact reviewed bytes at 2026-10-05T02:37:16.770456Z,
hash `3f35458bba020eda9f509a9d3f4908d4dbec7145493d10a95e3f287ef4a2eb87`,
creating `APIs/zoom.us/whiteboard/2/openapi.yaml` with 25 paths / 43 ops. Strict full
validation, exact vendor-content equality after provenance, typed YAML round-trip,
no invented curation, original authentication and zero refs all verified. No patches,
conversion, bundling, removed routes or historical-file edits. Import/source logs
`/tmp/zoom-whiteboard-import.log`, `/tmp/zoom-whiteboard-import-verification.log`;
verifier `/tmp/verify-zoom-next-import.py`. Deliver this API in its own PR; Scheduler
follows separately. Rooms/Team Chat remain discovery blockers; no proposed patches adopted.

**Whiteboard delivered / Scheduler import prepared (2026-10-05):**
[#154](https://github.com/ontola/openapi-directory/pull/154) merged and attached,
head `55d85f9cb7ab0164c0ff7fae7b195d10249a2370`, merge
`fdd2f7ef772459e636c70d0139924f12ef1a95dc`. Only the new Whiteboard YAML (4476 lines)
and progress record, 4494 additions / zero deletions, CLEAN/MERGEABLE. No API-path CI
checks are configured; strict source/import verification above passed before delivery.
Scheduler re-fetched exact reviewed bytes at 2026-10-05T02:38:18.269974Z, hash
`b0231b26205920d8c331376cba65bf25e2d13ba4f438283b164a02a7186c6daf`, creating
`APIs/zoom.us/scheduler/2/openapi.yaml`: **16 paths / 24 operations**, all absent from
historical combined coverage. Same full strict validation, exact vendor equality after
provenance, typed YAML round-trip, no invented curation and zero refs pass. Preserve
native OAuth requirements, no conversion/patches/bundling/deletions. Prior Zoom files
remain unchanged. Source/import logs `/tmp/zoom-scheduler-source-review.json`,
`/tmp/zoom-scheduler-import.log`, `/tmp/zoom-scheduler-import-verification.log`.
Deliver Scheduler separately, then verify an expanded complete audit. Latest complete
verified network audit remains 38 until that new run is downloaded and checked.

**Scheduler delivered / 40-source audit verified (2026-10-05 UTC):**
[#155](https://github.com/ontola/openapi-directory/pull/155) merged and attached,
head `138446035969552c42b9e8fc06cc0e250579ea99`, merge
`ad461f223af141f9b43d66d17feae892306ae635`. Two expected files: new Scheduler YAML
6028 lines and progress record; 6045 additions / zero deletions, CLEAN/MERGEABLE.
Whiteboard #154 and Scheduler #155 are complete; do not duplicate imports. No patches,
conversion, lifecycle annotation removal, history replacement or protection bypass.
Their combined 41 paths / 67 operations were entirely absent from the old combined API.
Existing combined, Meetings, Users and Accounts files remain intact. Inventory verified
against this fetched main: **729 domains / 4272 files / 2098 openapi.yaml / 2168 swagger.yaml**.

Expanded [audit 37256244045](https://github.com/ontola/openapi-directory/actions/runs/37256244045)
at actual merged main `ad461f223af141f9b43d66d17feae892306ae635` passes all **90 tests**,
fetches/prepares all **40 artifacts / 39 services**, and reports **33 validated matches /
seven recorded import blockers**. No fetch/prepare failures or unblocked drift.
Whiteboard and Scheduler are matches with actual baselines
`APIs/zoom.us/{whiteboard,scheduler}/2/openapi.yaml`, exact reviewed raw hashes,
native 3.0.0 / version 2, 25/43 and 16/24 counts, no transformations, full validation
success dates, and zero endpoint additions/removals. Hosted health is explicitly unassessed.
Other seven blockers remain Cohere, Square, archived unsupported Slack, native Meraki,
Messaging delivery, Vercel and Marketing; strict validation/import guards are unchanged.
The audit's nonzero exit is solely those blockers; tests, readable-summary publication
and complete artifact upload succeed. A transient connection reset while reading run
status was reconciled against the same completed run, without duplicate dispatch.

All 40 raw entry hashes, 22 distinct GitHub repository-metadata snapshots, exact per-row
comparison bases, profiles/classifications, transformation evidence, seven blocker rows,
current Zoom/Mailchimp/Asana/Twilio/Vercel rows and the identical rendered Markdown were
verified at `/tmp/openapi-ci-audit-37256244045`. Eight hosted sources (five Zoom products,
Hugging Face, Vercel and Marketing) remain health-unassessed. Ignored local report.json /
report.md and health snapshots updated. Recover the durable `official-source-audit`
artifact from this run after reboot; temporary verifier/logs
`/tmp/verify-zoom-40-full-audit.py`, `/tmp/zoom-40-full-audit-verification.log`,
`/tmp/zoom-next-full-audit-ci.log`, `/tmp/zoom-next-full-audit-status.json`.
No API commits were created solely for timestamps.

**Resume next:** This is the latest complete verified audit. Whiteboard/Scheduler
monitoring and both API additions are delivered (#153–#155). Rooms/Team Chat discovery
blockers and the not-yet-selected Docs candidate are recorded above; no corrections to
those invalid/mixed-scope sources have been adopted. Continue independent well-known
provider discovery/freshness auditing (e.g. existing official Cloudflare/Auth0/OpenAI
sources) or authorized separate updater PR-generation/monthly-discovery work. All prior
vendor blockers, parked items and Messaging's unanswered owner choice remain in force.
Preserve the original one-week deadline and local sleep policy; no additional chat
automation or cloud execution.

**Auth0 / Cloudflare official-source audit and parser repair (2026-10-05 UTC):**
Auth0 Management's current [reference](https://auth0.com/docs/api/management/v2) directly
links `https://auth0.com/docs/oas/management/v2/management-api-oas.json`; pinned official
CLI `auth0/auth0-cli` at `a6239f907a81238e081a4abb1882c028558b2655`,
`internal/openapi/schema.go`, independently declares the exact SchemaURL. Native **3.1.0 /
2.0 / 258 paths / 478 ops**, source hash
`893adeada5156cf2f72ac8e4707892357fcf87a07783958cbcdf5881fa8e04b2`, fetched
2026-10-05T03:48:14.634489Z, Last-Modified 2026-10-02 19:19:11 UTC. Stored counts agree,
but parsed vendor content differs at **83 positions**, including experimentation lifecycle
beta -> EA, user-block enforcement descriptions and operation error metadata. Zero added/
removed endpoints; counts are not freshness evidence. Native/stored both fail at
`#/components/schemas/GetGuardianEnrollmentResponseContent/properties/name/default`:
device-name default `iPhone 7` cannot match its phone-number pattern. No constraint removed
or replacement invented. The current reference explicitly labels OpenAPI 3.1 schema
support Beta; this established Management API publication includes EA operations, not a
stable-only subset. Do not silently substitute old Swagger, Authentication or other Auth0
services. Hosted health remains unassessed. No API refresh delivered; old file remains
unchanged (it also lacks in-spec provenance, to fix only on a validated future import).

Cloudflare official `cloudflare/api-schemas` public/unarchived repository contains both
native formats. The [vendor transition article](https://blog.cloudflare.com/open-api-transition/)
explicitly names `openapi.yaml`; follow that original format. Pinned source revision
`03a6de21e114bf8f998013d5b477d7c20fa70475`, native **3.0.3 / 4.0.0 / 2287 paths / 3647 ops**.
YAML hash `be71f538efd5f166ca3d43c7bcac4c8516c5d435f7df0ddfbd35ae89bc3b0463`, JSON hash
`6d665f1f96baa87c5ba7bfc5ded9401d743a14af74250f594bd302ef4f1c71e8`. Stored **2234 / 3567**:
**79 paths / 129 ops added; 26 paths / 49 ops removed**, not merely net 53/80 growth.
Some raw differences are URL variable renames (Images/custom-pages/etc.); do not claim
all removals are runtime retirements. Full per-endpoint lifecycle/removal review remains
before any API refresh. Current validation blocks DNS-order default `type` outside its
name/created_on/modified_on enum; missing `assets_jwt` scheme in one requirement and
`pages_upload_token` in three. No authentication guessed, requirements dropped or enum
constraint waived. Broad official artifact retains vendor preview/beta/deprecated scope.

The updater could not read the stored Cloudflare YAML: bare equals mapping key triggered
PyYAML's obsolete implicit value tag with no safe constructor. Removing only that legacy
resolver revealed two JSON/YAML differences: realtimekit_participants example `1:10`
incorrectly became integer 70 under YAML 1.1 sexagesimal rules. Implement YAML 1.2 core
integer/float resolution (no sexagesimal, decimal leading zeros, explicit 0o octal/0x hex,
scientific forms) and string fallback for `=`. Update the writer's conservative quoting
for every new numeric form. No raw vendor bytes changed. **Whole published JSON/YAML
parsed canonical content is now exactly equal** at the same pinned revision, confirming
both fixes; old Cloudflare comparison can proceed. Explicit unsupported tags still fail;
PyYAML's global safe loader is untouched. Three regression tests cover cross-format equals
keys/values, numeric/sexagesimal string types and serialization, global isolation,
explicit unknown-tag rejection and strict invalid-default/import rejection. **93 tests
pass**. Full validation/import guards remain active; no native source content correction.
Register Auth0 and Cloudflare separately from API data changes in an infrastructure PR:
registry **42 artifacts / 41 services**. Latest complete audit remains 40 until verified.

Discovery raw bytes, exact pinned ownership files, current Auth0 reference, complete typed
diffs and validation evidence are in ignored `cache/maintenance/discovery/` under
`auth0-management`, `cloudflare-json`, `cloudflare-yaml`. Scripts/logs
`/tmp/inspect-auth0.py`, `/tmp/auth0-discovery.log`, `/tmp/inspect-cloudflare.py`,
`/tmp/cloudflare-discovery.log`, `/tmp/cloudflare-pair-diff.py`,
`/tmp/cloudflare-pair-diff.json`, `/tmp/review-cloudflare.py`, `/tmp/cloudflare-review.json`,
`/tmp/cloudflare-review.log`, `/tmp/auth0-cloudflare-tests.log`. No API files changed;
all prior blockers, parked items, Messaging owner choice and local week/sleep policy remain.

**Infrastructure delivered / expanded audit found four quoting repairs (2026-10-05):**
[#157](https://github.com/ontola/openapi-directory/pull/157) merged and attached,
head `473e90e8eb16d552644780196060f190c087317c`, merge
`8d479d33dffab8f81fc32b1179e848e7d2ec855e`. Five expected infrastructure/instruction
files; no API data. CLEAN/MERGEABLE, exact-head
[CI 37270619896](https://github.com/ontola/openapi-directory/actions/runs/37270619896)
passes all **93 tests**. Raw native Auth0 6046 and Cloudflare 24564 local refs independently
resolve, with no external references; native schema/security defects still block imports.

Expanded [audit 37273474074](https://github.com/ontola/openapi-directory/actions/runs/37273474074)
at main `8d479d33dffab8f81fc32b1179e848e7d2ec855e` passes all 93 tests and successfully
fetches/prepares all **42 artifacts / 41 services**. Verified result is **29 matches,
nine import blockers, four valid content differences**. The previous seven blockers plus
Auth0/Cloudflare are recorded native/delivery defects; no new fetch/prepare failures.
All 42 entry hashes, 23 distinct repository metadata snapshots, exact per-row bases,
validation profiles/classifications, raw endpoint deltas, transformations and rendered
Markdown were verified in `/tmp/openapi-ci-audit-37273474074`. Nine hosted sources remain
health-unassessed. Ignored reports/health cache updated; recover the durable CI artifact.
Verifier/log `/tmp/verify-auth0-cloudflare-42-interim.py`,
`/tmp/auth0-cloudflare-42-interim-verification.log`. This is an interim repair queue,
not a claim that 33 artifacts currently match.

All four content differences use **unchanged vendor hashes/revisions** already recorded
in the old files. Full typed comparison finds only unquoted leading-zero digit strings
containing 8/9: **19** each GitHub artifact, **7** Plaid, **19** Xero (64 total positions).
The old YAML 1.1 dumper did not quote them because they could not be octal; YAML 1.2
consumers parse them as decimal integers and lose the string type/leading zeros. Preserve
the exact source strings by re-importing with #157's matching writer/reader. GitHub tag
order differences in the first raw comparison are curation; compare after preserve_curation
and retain that order exactly, rather than modifying tags. No vendor endpoint/version
change, metadata stripping, invented example, schema weakening or historical-directory
rewriting. Deliver repairs one PR per API (both GitHub counterparts together).

**GitHub repair prepared:** re-fetched source commit
`836ce198db13a6fb194547e53eea99c6ddae495b`, default hash
`f3efa055b46b43f5f133ecf792a36a7f50cf8a4378cbd177390bc2bf8c6097cd`, date-versioned hash
`28b908e1fd554f785e31368e334a897fb01a0439b6988e669c0011c64c77efd9`.
Both remain 1.1.4 / 816 paths / 1232 ops. Only 19 quote additions per file; full strict
validation, typed YAML, exact prepared vendor content, all curation/externalDocs/tag
order and endpoint sets verified. Public-key IDs retain their
vendor string values. No provenance-only timestamp changes. Logs
`/tmp/github-yaml12-import.log`, `/tmp/github-yaml12-import-verification.log`, verifier
`/tmp/verify-yaml12-current-import.py`; full reviewed diffs in
`/tmp/{github-rest,github-rest-2022-11-28,plaid,xero-accounting}-parser-drift.json` and
`/tmp/parser-drift-review.log`. Plaid/Xero repairs follow separately; afterward verify
33 matches / nine blockers with a new complete audit before claiming queue completion.

**GitHub quoting repair delivered / Plaid prepared (2026-10-05):**
[#158](https://github.com/ontola/openapi-directory/pull/158) merged and attached,
head `1624ceddd76988dc5beaec389f7ea435b87c0e4c`, merge
`7782419eb8c981c9dd28379e41a43ca3186f4758`. Three expected files: 19 quote changes
per GitHub artifact and progress. CLEAN/MERGEABLE; no API-path CI configured, strict
source/import verification above passed. Identifiers are public-key IDs; no App-installation
identifier changes. No vendor hash/version/endpoint changes or new example values.

Plaid's validated re-import at unchanged vendor commit
`325e2e192bcb422df708029bafe9d950c94df2fd`, raw hash
`e07a869352e83670e2ef077376db268358ce7a0dc4a8e97b8e1e980b91616a8c`, quotes exactly
seven digit-string examples: routing numbers, DTC numbers and one bank account number.
Version 2020-09-14_1.762.0 / 360 paths / 351 operations remains unchanged; source string
values and leading zeros preserved. Provenance also records the current strict validation
profile and actual current curation baseline 1.762.0 instead of prior import fallback1.740.1.
Full exact prepared-source equality after provenance/curation, strict validation, typed
YAML round-trip, tags/externalDocs/all curation, hashes and endpoint sets verified.
Historical versions unchanged. Logs `/tmp/plaid-yaml12-import.log`,
`/tmp/plaid-yaml12-import-verification.log`; same command-level verifier. Deliver Plaid
separately, then Xero's remaining 19 quote repairs; expanded complete audit remains interim.

**Plaid quoting repair delivered / Xero prepared (2026-10-05):**
[#159](https://github.com/ontola/openapi-directory/pull/159) merged and attached,
head `cec118189063b7e3b59b72717864c2e44213c4e4`, merge
`13c40d552e19797f8362975016f6dfc1c8da173e`. Only current Plaid YAML (seven quotes and
current validation/baseline provenance) plus progress; CLEAN/MERGEABLE. Full import
verification passes. GitHub and Plaid representation repairs are done; no source versions,
hashes, schemas, endpoint sets, curation or historical versions changed.

Xero validated re-import uses unchanged official commit
`fd9d44b04bf4934a7509b8e7ece51a9e0e462e4f`, raw hash
`1afca0717bb0d323210c0f88f3802684c068059f6e5161ee24ddde7ee6294a64`, quoting exactly
19 digit-string account-code examples. Native 19.1.0 / 138 paths / 235 ops unchanged.
The existing exact 46 boolean-value correction remains identical with recipe hash
`782b419bbef21cca5d3190f31777cd9e6c994f39e309cb29e761f4718c3d9308`; no new source
patch. Curation key placement becomes the updater's deterministic order without value
changes; tag order/externalDocs stay exact. Provenance records current strict validation
and actual 19.1.0 curation baseline instead of historical2.9.4. Full prepared-source equality
with preserved curation/provenance, strict validation, typed YAML round-trip, unchanged
raw hash and endpoint sets verified. Other files/history unchanged. Logs
`/tmp/xero-yaml12-import.log`, `/tmp/xero-yaml12-import-verification.log`.
Deliver this separately, then validate the complete 42-source audit after all four repairs.

**Xero delivered / final 42-source audit verified (2026-10-05 UTC):**
[#160](https://github.com/ontola/openapi-directory/pull/160) merged and attached,
head `3b2d6eda553df86c9db2446eb12ef3730a96e914`, merge
`4be1fd571afd08dcb6db3c1c9d2135a71baad839`. Two expected files: current Xero YAML
and progress. CLEAN/MERGEABLE; no API-path CI configured, full strict source/import
verification above passed. Existing boolean patch and all vendor values/curation retained.
The four representation repairs are complete in three API PRs (#158–#160): **64 string
positions** now preserve leading zeros/types across both GitHub artifacts, Plaid and Xero.
No vendor version, endpoint set or raw source hash changed; historical files untouched.

Final [audit 37275451577](https://github.com/ontola/openapi-directory/actions/runs/37275451577)
ran against exact main `4be1fd571afd08dcb6db3c1c9d2135a71baad839`. All **93 tests pass**;
all **42 artifacts / 41 services** fetch and prepare successfully. Verified **33 matches /
nine import blockers**, with no remaining valid content drift or fetch/prepare failures.
Both GitHub counterparts, Plaid and Xero explicitly match their current baselines, with
the same source hashes/versions and zero added/removed paths or operations. Blockers remain
Cohere, Square, archived Slack, Meraki, Twilio Messaging delivery, Vercel, Mailchimp
Marketing, Auth0 Management and Cloudflare. Auth0/Cloudflare monitoring is delivered in
#157; their API data has not been refreshed. Do not waive native validation or delivery
guards to make the audit green. Overall workflow/audit conclusion is intentionally failure
for these blockers; tests, readable summary and artifact upload all succeeded.

Verified all 42 raw entry hashes, 23 distinct repository metadata snapshots, exact report
bases, strict validation profiles/classifications, transformations, endpoint deltas and
rendered Markdown. Nine hosted sources remain health-unassessed; repository availability
alone is not current coverage evidence. Recover durable evidence from the run's
`official-source-audit` artifact; local copy `/tmp/openapi-ci-audit-37275451577`, verifier
`/tmp/verify-auth0-cloudflare-42-audit.py`, logs
`/tmp/yaml12-repairs-42-audit-verification.log`, `/tmp/yaml12-repairs-full-audit-ci.log`.
Ignored reports/health caches updated. Recomputed tree inventory is unchanged: **729
domains / 4272 API files / 2098 openapi.yaml / 2168 swagger.yaml**.

App attachment capacity briefly blocked attaching #160: the thread already had 100 PR
identities. Verified #150 and #152 were merged, AGENTS-only progress records superseded
by later audits; unlinked only those two app attachments, leaving their PRs/history intact.
#160 was then attached successfully. Preserve API/infrastructure attachments; if the cap
recurs, inspect and unlink only superseded merged progress-only records before attaching
the new PR. No pending attachment failure. Twilio Messaging's unanswered owner choice,
explicitly parked items and the original one-week local/sleep deadline remain unchanged.

**Zoom Canvas official selection / monitoring prepared (2026-10-05 UTC):**
The current [Canvas API reference](https://developers.zoom.us/docs/api/canvas/) explicitly
names `/api-hub/canvas/methods/endpoints.json`, embedding the same **OpenAPI 3.0.0 /
vendor version 2 / 29 paths / 39 operations** as the original download. Native hash
`82cc4556a1ba6ff8770aae93bfe4de89ca13c51d5db82a4dc35bc13c4b65743c`, fetched
2026-10-05T07:36:12.376440Z, Last-Modified 2026-09-28 22:49:33 UTC. All non-security
content equals the current viewer; preserve the original download's OAuth requirements
and API-key scheme. Rendered markdown's 3.1.1 is not the native dialect. Full strict
validation passes, with zero refs and no content patches, conversion or bundling.

Pinned vendor `zoom/skills` at `2d75fba014118e5eafbc75c4143418fb2d934e29`,
`skills/rest-api/references/zoom-docs.md`, names this exact Canvas input. Its older
inventory has only **20 paths / 26 operations**: supporting selection evidence, not a
current coverage source. Use the live publication intact, retaining collaborator,
access/ownership, table, import/export, archive and report operations. Do not truncate to
the introduction's older future-permissions prose or concatenate the separate Hub API.
The current [Canvas introduction](https://developers.zoom.us/docs/canvas/) lists enabled
Canvas on Basic and paid plans, without a prerelease designation. Source lifecycle scan
finds only example beta-testing text and attachment-preview event names, not release labels.
Public publication is not a universal feature-GA claim; retain account/license and
Gov-cluster exclusions. Hosted health is explicitly unassessed.

Full fetched main tree has no Canvas/Docs counterpart; all 29 paths / 39 operations are
absent from **all six existing Zoom files**, including combined history and current
Meetings, Users, Accounts, Whiteboard and Scheduler. No alias or new-version refresh
disguised as an addition. Register `zoom-canvas`, target
`APIs/zoom.us/canvas/2/openapi.yaml`, separately from the API addition: **43 artifacts /
42 services**. Latest complete verified network audit remains 42 until expansion is
verified. Evidence in ignored `cache/maintenance/discovery/zoom-canvas/<hash>/` includes
original bytes, fetch metadata, current HTML/page data and pinned vendor reference.
Script/log `/tmp/verify-zoom-canvas-source.py`, `/tmp/zoom-canvas-source-review.json`.

To free three app attachment slots, verified #94/#98/#105 were merged AGENTS-only
progress records superseded by current audits and unlinked only their app attachments.
Their PRs/history remain intact; API/infrastructure attachments preserved. No protection
or approval bypass. All previous blockers, parked items, Messaging owner choice and the
original local one-week/sleep deadline remain unchanged. Next deliver monitoring, then
the fully validated Canvas API in its own PR; Rooms/Team Chat remain discovery blockers.

**Canvas monitoring delivered / API import verified (2026-10-05):**
[#162](https://github.com/ontola/openapi-directory/pull/162) merged and attached,
head `faddedb0523c6b125facb81b6a80cd98b51dc865`, merge
`294a3761067e7751d91eaacfe4fa48aa916f36b5`. Three expected infrastructure/instruction
files, 63 additions / zero deletions, CLEAN/MERGEABLE; exact-head
[CI 37278959442](https://github.com/ontola/openapi-directory/actions/runs/37278959442)
passes all **93 tests**. No API data in monitoring PR; 43 artifacts / 42 services registered.

Importer re-fetched the exact reviewed Canvas bytes at 2026-10-05T07:40:37.252584Z,
hash `82cc4556a1ba6ff8770aae93bfe4de89ca13c51d5db82a4dc35bc13c4b65743c`, creating
`APIs/zoom.us/canvas/2/openapi.yaml`: **29 paths / 39 operations**, all previously absent.
Full strict source/final validation, exact vendor-content equality after provenance,
typed YAML round-trip, no invented curation, native authentication and zero refs verified.
No patches, conversion, bundling, version invention, removals or historical-file edits.
All six prior Zoom files remain byte-identical. Logs `/tmp/zoom-canvas-import.log`,
`/tmp/zoom-canvas-import-verification.log`; verifier `/tmp/verify-zoom-canvas-import.py`.
Deliver the API separately, then verify a complete expanded network audit before claiming
43-source coverage is current. All previous blockers, owner decisions and constraints remain.


**Canvas addition delivered (2026-10-05):**
[#163](https://github.com/ontola/openapi-directory/pull/163) merged and attached,
head `1b80a5125e0cc78dea27d98a58c1c2d69a24fe6f`, merge
`14da5cc9a74e4dd4467e14af8089632390d017a1`. Two expected files: new Canvas YAML
7715 lines and progress; 7734 additions / zero deletions, CLEAN/MERGEABLE. No API-path
CI checks configured; full strict source/import verification above passed. Canvas
monitoring #162 and addition #163 are complete; do not duplicate. Preserve all prior
Zoom files, native scopes/restrictions and vendor version 2. Tree inventory is now **729
domains / 4273 API files / 2099 openapi.yaml / 2168 swagger.yaml**.

**Next candidate — Zoom Hub, not yet registered/imported:** Current public
[Hub API reference](https://developers.zoom.us/docs/api/hub/) names
`https://developers.zoom.us/api-hub/hub/methods/endpoints.json`, and all non-security
content equals its original download. Native **3.0.0 / version 2 / six paths / nine
operations**, SHA-256 `8f41b4fc3e42fb98ea10a3641688614b4a7f677bed1adeabf8b3827463d5de66`,
fetched 2026-10-05T07:43:44.021875Z, Last-Modified 2026-09-28 22:49:36 UTC. Strict
validation passes with zero refs; no patches, conversion or bundling. No paths/operations
overlap any of the seven existing Zoom files, including Canvas. It is a distinct shared
content API, not a replacement for Canvas or other products. No source lifecycle keywords
found; service/release/account coverage still needs review before selection/import.
Do not infer universal GA from absent labels. Original bytes, fetch evidence and current
HTML/page data saved in ignored `cache/maintenance/discovery/zoom-hub/<hash>/`; script/log
`/tmp/verify-zoom-hub-source.py`, `/tmp/zoom-hub-source-review.json`. Refetch/review when
resuming; this discovery snapshot is not part of the registered audit or its CI artifact.
Rooms/Team Chat remain blocked discovery leads; no proposed patches adopted. Continue
independent well-known-provider freshness/discovery or authorized separate updater work.
All previous blockers, parked items, unanswered Messaging owner choice, local sleep policy
and the original 2026-10-09 06:55:58 UTC deadline remain in force.

**Expanded Canvas audit verified (2026-10-05 UTC):**
[Audit 37279198156](https://github.com/ontola/openapi-directory/actions/runs/37279198156)
ran against exact main `14da5cc9a74e4dd4467e14af8089632390d017a1`. All **93 tests pass**;
all **43 artifacts / 42 services** fetch and prepare successfully, with **34 matches /
nine recorded import blockers**. No unblocked content drift or fetch/prepare failures.
Canvas matches its new baseline `APIs/zoom.us/canvas/2/openapi.yaml`, reviewed raw hash,
native 3.0.0 / version 2 / 29 paths / 39 ops, no transformations, validation success
date and zero added/removed paths or operations. Hosted health remains unassessed.
GitHub's two artifacts, Plaid and Xero explicitly remain matches after the quoting repairs,
with unchanged raw hashes and no endpoint changes.

The same nine blockers remain Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0 and Cloudflare. Strict
validation/import guards remain active; the overall workflow/audit failure reflects
these blockers, while tests, readable summary and full artifact upload succeed.
All 43 raw entry hashes, 23 distinct repository metadata snapshots, exact per-row bases,
validation profiles/classifications, transformations, endpoint deltas and identical
rendered Markdown were verified at `/tmp/openapi-ci-audit-37279198156`. Ten hosted
sources remain health-unassessed; repository availability is not complete current coverage.
Ignored local reports and source-health cache updated. Recover durable evidence from this
run's `official-source-audit` artifact; verifier/logs `/tmp/verify-zoom-canvas-43-audit.py`,
`/tmp/zoom-canvas-43-audit-verification.log`, `/tmp/zoom-canvas-full-audit-ci.log`,
`/tmp/zoom-canvas-full-audit-status.json`. No timestamp-only API commits.

**Resume next:** Canvas monitoring/addition #162/#163 are delivered and verified in this
latest complete audit; do not duplicate. Review the independent Hub candidate's coverage
before registration/import, or continue other well-known industry providers and separate
authorized updater PR-generation/monthly-discovery work. Discovery-only Hub evidence is
not registered or included in this CI artifact. Preserve every recorded blocker, parked
item, Messaging owner choice and the original one-week local sleep/deadline policy.

**Zoom Hub coverage reviewed / monitoring prepared (2026-10-05 UTC):**
Re-fetched the exact previously discovered native bytes at 2026-10-05T07:54:09.238605Z:
SHA-256 `8f41b4fc3e42fb98ea10a3641688614b4a7f677bed1adeabf8b3827463d5de66`,
OpenAPI 3.0.0 / vendor version 2 / **six paths / nine operations**. Current public
[Hub reference](https://developers.zoom.us/docs/api/hub/) explicitly names this download;
all non-security content equals its embedded viewer. Strict validation passes with zero
refs, no patches/conversion/bundling. Preserve original OAuth scopes, relative/empty
flow URL values and API-key scheme; do not infer replacement authentication endpoints.

The current [Hub introduction](https://developers.zoom.us/docs/hub/) identifies the shared
content layer for Canvas/AI Productivity Suite and lists public account prerequisites,
including Basic and paid plans, without a prerelease designation. Neither current reference
nor native artifact labels preview/beta. This is public service selection, not universal
feature-GA evidence. The download covers content read/import, file duplication/task polling
and shared-folder management. The broader guide mentions file moves/permissions and other
AI Productivity Suite capabilities not all represented here: do not fabricate missing
operations or claim complete product coverage. Retain file-type/format limits, admin/OAuth
scopes and every Gov-cluster exclusion. Distinct from Canvas and Zoom Events hubs.
Full fetched tree/alias check and all seven existing Zoom documents have no overlapping
paths/operations; retain them all. Hosted source health remains unassessed.

Register `zoom-hub`, target `APIs/zoom.us/hub/2/openapi.yaml`, in an infrastructure PR,
separate from its API addition: **44 artifacts / 43 services**. Latest complete verified
audit remains 43 until expansion is checked. Evidence in ignored discovery cache includes
original bytes, current public reference/page data, introduction HTML and fetch metadata;
source script/log `/tmp/verify-zoom-hub-source.py`, `/tmp/zoom-hub-source-review.json`.
Verified #108/#156/#161 were merged AGENTS-only progress superseded by later audits and
unlinked only those app attachments to free three slots; PRs/history unchanged, all API
and infrastructure attachments preserved. Every recorded blocker, parked item, unanswered
Messaging owner choice and original one-week local/sleep deadline remain in force.



**Hub monitoring delivered / API import verified (2026-10-05):**
[#165](https://github.com/ontola/openapi-directory/pull/165) merged and attached,
head `c621a40fd287230bf9e1bb7c2a209c974470fcea`, merge
`2bf2d41b61b75ae02d7ee55a763720095409d453`. Three expected infrastructure/instruction
files, 54 additions / zero deletions, CLEAN/MERGEABLE; exact-head
[CI 37280493449](https://github.com/ontola/openapi-directory/actions/runs/37280493449)
passes all **93 tests**. Registry has 44 artifacts / 43 services; no API data in this PR.

Importer re-fetched exact reviewed Hub bytes at 2026-10-05T07:56:35.323260Z,
hash `8f41b4fc3e42fb98ea10a3641688614b4a7f677bed1adeabf8b3827463d5de66`, creating
`APIs/zoom.us/hub/2/openapi.yaml`: **six paths / nine operations**, all previously absent.
Full source/final strict validation, exact vendor-content equality after provenance,
typed YAML round-trip, no invented curation, native authentication and zero refs verified.
No patches, conversion, bundling, version invention, removals or historical-file edits.
All seven prior Zoom files remain byte-identical. Logs `/tmp/zoom-hub-import.log`,
`/tmp/zoom-hub-import-verification.log`; verifier `/tmp/verify-zoom-hub-import.py`.
Deliver the API separately, then verify a complete expanded network audit before claiming
44-source coverage is current. Existing blockers, owner decisions and constraints remain.


**Hub addition delivered (2026-10-05):**
[#166](https://github.com/ontola/openapi-directory/pull/166) merged and attached,
head `7465c06ab113d5db3f29430423cd461a954d9911`, merge
`d36a849755cfc3457d3b7d6bd7694cb2e25f7222`. Two expected files: new Hub YAML 937 lines
and progress; 956 additions / zero deletions, CLEAN/MERGEABLE. No API-path CI configured;
full strict source/import verification above passed. Hub monitoring #165 and API #166 are
complete; do not duplicate. Preserve all seven prior Zoom files, source limits/scopes,
Gov exclusions and vendor version 2. Inventory now **729 domains / 4274 API files /
2100 openapi.yaml / 2168 swagger.yaml**.

**Next candidate — missing Datadog v1, not registered/imported:** Full fetched tree and
brand/service alias search has only `APIs/datadoghq.com/v2/1.0/openapi.yaml`. Vendor
`DataDog/datadog-api-client-python` also publishes `.generator/schemas/v1/openapi.yaml`:
commit `2240a46b47e2d135962176dfc9dc665f506628af`, raw SHA-256
`83353a2cbaec662aa74d12d1721daf40d81a574fe2a043f900fc595eea6dfd8f`, fetched
2026-10-05T07:58:29.274675Z. Native **3.0.0 / version 1.0 / 150 paths / 235 operations**,
strict validation passes, all **2794 local refs** independently resolve with no external
refs. Zero path/operation overlap with stored v2. This is separate v1 API coverage, not
an older version of that v2 file; retain v2 and use the vendor's actual declared version.
Pinned same-commit README identifies generation from public Datadog OpenAPI descriptions,
shows v1 usage and explicitly warns that the client can include opt-in unstable endpoints.
Source contains **65 deprecated operations**; preserve all lifecycle annotations and
review current public scope before registration/import, without pretending all v1 features
are GA/current or removing deprecated vendor routes. The v2 source remains separately
monitored. Original bytes, fetch metadata, pinned README and full validation/reference/
overlap/lifecycle review saved in ignored `cache/maintenance/discovery/datadog-v1/<hash>/`.
Script/log `/tmp/inspect-datadog-v1.py`, `/tmp/datadog-v1-discovery-review.json`.
Refetch/review when resuming; this candidate is not in the registered audit or CI artifact.
All existing source/delivery blockers, parked items, Messaging owner choice and original
one-week local sleep/deadline policy remain in force.

**Expanded Hub audit verified (2026-10-05 UTC):**
[Audit 37280667077](https://github.com/ontola/openapi-directory/actions/runs/37280667077)
ran against exact main `d36a849755cfc3457d3b7d6bd7694cb2e25f7222`. All **93 tests pass**;
all **44 artifacts / 43 services** fetch and prepare successfully: **35 matches / nine
recorded import blockers**, no unblocked content drift or fetch/prepare failures.
Hub matches its new baseline `APIs/zoom.us/hub/2/openapi.yaml`, exact reviewed raw hash,
native 3.0.0 / version 2 / six paths / nine ops, no transformations, validation success
date and zero endpoint additions/removals. Canvas and all prior repaired GitHub/Plaid/Xero
artifacts explicitly remain matches, with unchanged source hashes and endpoint sets.

The same nine blockers remain Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0 and Cloudflare. Strict
validation/import guards remain active; overall workflow/audit failure reflects these
blockers, while tests, readable summary and full artifact upload succeed. All 44 raw entry
hashes, 23 distinct repository metadata snapshots, exact per-row bases, strict validation
profiles/classifications, transformation evidence, endpoint deltas and identical rendered
Markdown were verified at `/tmp/openapi-ci-audit-37280667077`. Eleven hosted sources
remain health-unassessed; repository availability is not complete-current-coverage evidence.
Ignored local reports and source-health cache updated. Recover durable evidence from the
run's `official-source-audit` artifact; verifier/logs `/tmp/verify-zoom-hub-44-audit.py`,
`/tmp/zoom-hub-44-audit-verification.log`, `/tmp/zoom-hub-full-audit-ci.log`,
`/tmp/zoom-hub-full-audit-status.json`. No timestamp-only API commits.

**Resume next:** Hub monitoring/addition #165/#166 are delivered and verified in this
latest complete audit; do not duplicate. Datadog v1 is the next substantial missing
official service candidate (150 paths / 235 ops): review public/lifecycle scope, register
separately and import with full validation and provenance, preserving v2 and deprecated
annotations. The vendor's public API introduction was also cached in its discovery
directory: original gzip transport bytes plus decoded HTML, without altering any API
source. Datadog v1 discovery is not registered or included in this audit/CI artifact.
Other independent well-known-provider discovery and separate authorized updater
PR-generation/monthly-discovery work remain in scope. Preserve every recorded blocker,
parked item, unanswered Messaging owner choice and original one-week local sleep/deadline.

**Datadog v1 selection / monitoring prepared (2026-10-05 UTC):**
Re-fetched source at 2026-10-05T08:19:54.510680Z, unchanged official commit
`2240a46b47e2d135962176dfc9dc665f506628af`, hash
`83353a2cbaec662aa74d12d1721daf40d81a574fe2a043f900fc595eea6dfd8f`.
Native **OpenAPI 3.0.0 / info.version 1.0 / 150 paths / 235 operations** validates
strictly without patches, conversion or bundling; all 2794 local refs independently
resolve with none external. Full fetched main tree/aliases still have no v1 counterpart,
and no paths/operations overlap stored v2. Same-commit SDK README explicitly identifies
public OpenAPI generation and v1 usage; current public Monitors reference still includes
`/api/v1/monitor`. Source selection is the official publication, not a third-party scrape
or a claim that every SDK package version is an API release.

Preserve all **65 deprecated operations**, including four AWS Logs operations with vendor
`x-sunset: 2027-02-20`: DELETE/POST `/api/v1/integration/aws/logs`, POST its
`/check_async` and `/services_async` routes. Do not remove sunset annotations or infer
runtime retirements from deprecated labels. Reviewed operation extensions are permissions,
code-generation request names, pagination and sunset; no unstable/beta/private flags.
The SDK README nevertheless warns about opt-in unstable endpoints across its public
client; retain any future native lifecycle annotations rather than claiming universal GA.
Regional/server variables, all original authentication/permission requirements and
metrics/monitors/dashboard/log/integration/SLO/synthetics coverage remain as published.
This is distinct v1 coverage, not a replacement for v2 or every Datadog/private product.

Register `datadog-v1`, target `APIs/datadoghq.com/v1/1.0/openapi.yaml`, separately from
the API addition: **45 artifacts / 44 services**. Latest complete verified audit remains
44 until expansion is checked. Discovery cache stores raw source, exact pinned README,
reference/validation/lifecycle/overlap evidence and current Monitors page original bytes
plus decoded HTML. No source bytes changed when decoding HTML transport. Script/log
`/tmp/inspect-datadog-v1.py`, `/tmp/datadog-v1-discovery-review.json`.
Verified #112/#115/#118 were merged AGENTS-only progress superseded by later audits and
unlinked only their app attachments to free three slots; PRs/history unchanged and all
API/infrastructure attachments preserved. Existing blockers, parked items, unanswered
Messaging owner choice and original one-week local/sleep deadline remain in force.

**Datadog v1 monitoring delivered / API import verified (2026-10-05):**
[#168](https://github.com/ontola/openapi-directory/pull/168) merged and attached,
head `f7ccae10389f0aa1f2d8bdfb7b304392c0fe7f31`, merge
`1e260131f7664113a72845a3e6cd29a67107c109`. Three expected infrastructure/instruction
files, 60 additions / zero deletions, CLEAN/MERGEABLE; exact-head
[CI 37283283221](https://github.com/ontola/openapi-directory/actions/runs/37283283221)
passes all **93 tests**. Registry 45 artifacts / 44 services; no API data in this PR.

Importer re-fetched exact reviewed bytes at 2026-10-05T08:24:47.463228Z, official commit
`2240a46b47e2d135962176dfc9dc665f506628af`, entry hash
`83353a2cbaec662aa74d12d1721daf40d81a574fe2a043f900fc595eea6dfd8f`, creating
`APIs/datadoghq.com/v1/1.0/openapi.yaml`: **150 paths / 235 operations**, all previously
absent. Full source/final strict validation, exact vendor-content equality after provenance,
typed YAML round-trip and all 2794 local refs verified. No invented curation, patches,
conversion, bundling, version invention, removals or historical edits. All 65 deprecated
operations/four sunset labels, regional servers and authentication remain exact; stored
v2 is byte-identical. Logs `/tmp/datadog-v1-import.log`,
`/tmp/datadog-v1-import-verification.log`; verifier `/tmp/verify-datadog-v1-import.py`.
Deliver the API in its own PR, then verify the complete expanded audit. Latest complete
verified network audit remains 44 until expansion is checked; all prior constraints remain.


**Datadog v1 delivered / expanded audit verified (2026-10-05 UTC):**
[#169](https://github.com/ontola/openapi-directory/pull/169) merged and attached,
final head `9f5cd770b498ea6819e90094562c3726613d9e76`, merge
`749ac81ee2434614ac659340a03abb916af6597e`. Two expected files: new native v1 YAML
(45,825 lines) and 23 instruction lines; 45,848 additions / zero deletions. CLEAN/MERGEABLE
and exact-head verification precede merge. The final documentation-only commit places
its delivery record at the end of this cumulative log; API bytes remain as validated.
No API-path CI is configured for that PR; full strict source/import/content/round-trip,
reference, lifecycle and v2-preservation checks are recorded immediately above.

[Expanded audit 37283764443](https://github.com/ontola/openapi-directory/actions/runs/37283764443)
ran against exact main `749ac81ee2434614ac659340a03abb916af6597e`. All **93 tests pass**;
all **45 artifacts / 44 services** fetch and prepare: **36 matches / nine recorded
import blockers**, with no unblocked drift or fetch/prepare failures. Datadog v1 matches
`APIs/datadoghq.com/v1/1.0/openapi.yaml`, the reviewed commit/raw hash, native
3.0.0 / version 1.0 / 150 paths / 235 operations, no transformations and a successful
validation date, with zero endpoint deltas. Hub, Canvas and repaired GitHub/Plaid/Xero
artifacts remain explicit matches with unchanged source hashes and endpoint sets.

The same nine blockers remain Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0 and Cloudflare. Strict
validation/import guards remain active. Overall workflow/audit failure reflects these
recorded blockers; tests, readable summary and artifact upload succeed. All 45 entry
hashes, 23 distinct repository-metadata snapshots, exact per-row bases, strict profiles,
classifications, transformation evidence, endpoint deltas and identical rendered Markdown
verified at `/tmp/openapi-ci-audit-37283764443`. Eleven hosted sources remain
health-unassessed; repository availability does not establish complete vendor coverage.
Ignored local reports/source-health cache updated. Durable recovery: run artifact
`official-source-audit`; temporary verifier/logs `/tmp/verify-datadog-v1-45-audit.py`,
`/tmp/datadog-v1-45-audit-verification.log`, `/tmp/datadog-v1-full-audit-ci.log`,
`/tmp/datadog-v1-full-audit-status.json`. No timestamp-only API commits.

Full fetched main tree at the above merge: **729 domains / 4,275 API files**, including
**2,101 openapi.yaml / 2,168 swagger.yaml**; header updated with this dated observation.

**Resume next:** Datadog v1 monitoring/addition #168/#169 are complete and verified;
do not duplicate. Continue independent official-source audits/discovery of well-known
industry APIs or the separately scoped, authorized updater PR-generation and monthly
discovery infrastructure in section 9. PR generation is not implemented yet and must
retain one API per PR, validation/provenance/curation guards, duplicate detection and
human-visible review evidence; do not introduce blanket automatic merging. Other
Datadog products are not covered by v1/v2 imports. Preserve all recorded native defects,
explicitly parked items, unanswered Messaging owner choice, no approval/push-protection
bypasses, and original one-week local sleep/deadline policy. This 45-source audit
supersedes the earlier 44-source network audit; docs-only progress commits need no
repeat network audit.


**Okta official source recovered / monitoring prepared (2026-10-05 UTC):**
The earlier guessed-path 404 does not establish a missing repository. Official
`okta/okta-management-openapi-spec` is maintained, unarchived/undisabled, default branch
`master`, pushed 2026-10-01. Pinned README says `dist/current` is generated directly
from the Management API and used by its SDKs, with historical vendor releases retained.
Reviewed commit `df5fc58bdf64d1a7594b324bb39d24a8c3b31eeb` publishes native
**3.0.3 / 2026.09.1 / 485 paths / 731 operations**. Register full enum/example-bearing
`dist/current/management-oneOfInheritance.yaml`, raw SHA-256
`a51eb501567a643aaeacf77576752aee62869b34f444b2d1b96fece62ab2a7b9`, not its
noEnums/noExamples/development alternatives. `management-minimal.yaml` has identical
endpoint sets and the same first defect, raw hash
`efb8f839ba5d3cfd27ec37539cb5f57e0c7ceeed80e947c039619935e77bf6a7`;
this comparison is not a claim that all variant schemas are interchangeable.

All 7580 full-variant local refs resolve independently with none external. Preserve four
deprecated operations, 718 `x-okta-lifecycle` operation annotations, documented Early
Access/Beta features, tenant servers and authentication. Vendor publication is not a
universal feature-GA guarantee. Current public API overview describes scoped OAuth/API
tokens and explicitly excludes undocumented endpoints; separate Okta products need their
own review. Full fetched main tree has only community `APIs/okta.local/1.0.0`, not an
official Management import. Target `APIs/okta.com/management/2026.09.1/openapi.yaml`
is distinct; do not delete or silently replace that community submission.

**No API import:** native validation fails at GET `/api/v1/hook-keys/{id}` inline path
parameter missing `required: true`; its shared `pathHookKeyId` already declares the
required string. A diagnostic-only copied repair exposes
`components.schemas.Brand.properties.customPrivacyPolicyUrl.default: null` on a
nonnullable string. Neither hypothetical repair is adopted, no null semantics/default
invented, constraints relaxed or validation waived. Look for a vendor correction or a
separately reviewed exact recipe. Register monitoring so raw changes/fixes remain visible.
Registry **46 artifacts / 45 services**; latest verified complete audit remains 45 until
expansion is checked. Evidence under ignored
`cache/maintenance/discovery/okta-management/df5fc58bdf64d1a7594b324bb39d24a8c3b31eeb`:
exact source variants/repository metadata/README, validation JSON, hypothetical diagnostics
and public User-reference HTML/fetch hash. Script/log `/tmp/inspect-okta.py`,
`/tmp/okta-discovery/validation.log`. No production parser/source edits.
Verified #120/#125/#128 were merged AGENTS-only progress superseded by later audits;
unlinked only those app attachments to free three slots. PRs/history and all API/updater
attachments remain intact. Preserve all nine previous blockers, parked items, unanswered
Messaging owner choice and original one-week local sleep/deadline instructions.


**Okta monitoring delivered / complete expanded audit (2026-10-05 UTC):**
[#171](https://github.com/ontola/openapi-directory/pull/171) merged and attached,
head `c68f8a4bd14302253e75e3f38a9866eb254947e8`, merge
`337082cde96d861c5d3c69b8a494128408999ad5`. Three expected instruction/source files,
73 additions / zero deletions, CLEAN/MERGEABLE; exact-head
[CI 37290040939](https://github.com/ontola/openapi-directory/actions/runs/37290040939)
passes all 93 tests. No API import or source patch was adopted.

[Audit 37290126584](https://github.com/ontola/openapi-directory/actions/runs/37290126584)
ran against exact main `337082cde96d861c5d3c69b8a494128408999ad5`. All **93 tests pass**;
all **46 artifacts / 45 services** fetch and prepare: **36 matches / ten recorded
import blockers**, no unblocked drift or fetch/prepare failures. Okta is missing from
the official vendor namespace, fetched at the reviewed exact commit/hash, with native
3.0.3 / 2026.09.1 / 485 paths / 731 operations and the expected hook-key validation
failure. No transformations or successful-validation date is asserted for it.
Previously matched Datadog v1, Hub/Canvas and repaired GitHub/Plaid/Xero remain matches.

Blockers are the previous nine (Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0 and Cloudflare) plus Okta.
Strict guards remain in force; overall audit/workflow failure reflects these native or
delivery blockers, while tests, summary and artifact upload succeed. All 46 entry hashes,
24 unique repository metadata snapshots, per-row bases, strict validation profiles,
classifications, transformation evidence, endpoint deltas and identical rendered Markdown
verified at `/tmp/openapi-ci-audit-37290126584`. Eleven hosted sources remain
health-unassessed. Ignored local reports/source-health cache updated. Durable recovery:
run artifact `official-source-audit`; verifier `/tmp/verify-okta-46-audit.py`, logs
`/tmp/okta-46-audit-verification.log`, `/tmp/okta-full-audit-ci.log`,
`/tmp/okta-full-audit-status.json`. This supersedes the prior 45-source complete audit.

**Box discovery / concrete next import queue:** official maintained, unarchived
`box/box-openapi`, commit `5b055e333a802b10b8ca90fcc513643836dd92b4`, publishes three
separate year-version artifacts in `openapi/`. Full main tree already has
`APIs/box.com/2.0.0/openapi.yaml`: 161 paths / 260 ops, not a missing vendor. Pinned README
identifies root `openapi.json` as the latest compatibility description, byte-identical
to `openapi/openapi.json`. Both declare **3.0.2 / 2024.0 / 187 paths / 297 ops**,
raw hash `13cc601e01a7b82133975aaf7aeffb1850159a10ac6365fae00d5af94406d9d4`.
Strict native validation and a curation-preserving serialized import preflight pass,
with no conversion, patches or bundling. Current public versioning guide confirms
`2024.0` labels the pre-year-versioning endpoints and is the default without a header;
version labels do not mean this maintained compatibility artifact is frozen.

Against stored 2.0.0: **28 paths / 40 operations added, two paths / three operations
removed**. Removed GET `/metadata_query_indices`, PUT the vendor's literal
`/metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema#delete`,
and DELETE `/metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema`.
These are official-source omissions, not yet proven runtime retirements; do not invent
replacement operations or silently normalize vendor fragment paths. New AI agents/
extraction, integration mappings, metadata taxonomies, signing-template and other API
content remains exact. All 1451 classic local refs resolve; preserve seven native stable
annotations, admin/free-developer restrictions and original authentication/servers.
New vendor version requires **new `APIs/box.com/2024.0/openapi.yaml`**, retaining the
2.0.0 history and its curation; follow future fixed-version content in place.

Separate `openapi/openapi-v2025.0.json` declares **2025.0 / 24 paths / 37 operations**,
raw hash `a28dd665970613050341911ed72900c3607d203b0805e71443ce12305aef4282`.
It is a versioned subset, not a wholesale replacement: comparing it alone with historical
classic coverage would falsely imply mass removals. Native strict validation passes.
`openapi/openapi-v2026.0.json` declares **2026.0 / five paths / five operations**,
raw hash `f46e2c894930ec58dedd1794d7b368f46f0844ab592b5b630f33ca2ca771d370`;
strict validation passes, all 53 local refs resolve, but two operations are explicitly
beta. Review release/feature scope and retain beta annotations; do not blindly select
only the numerically highest file or claim universal GA. Current versioning guide
explains per-endpoint headers and native stability/deprecation indications.

Box is discovery-only and not in this 46-source audit/manifest. Register the compatibility
source separately, then refresh as one Box API PR with exact content/provenance/curation
and removal evidence; independently review versioned slices. Do not fabricate a merged
superset or discard historical coverage. Raw sources/catalog/repository metadata/README,
current versioning HTML/fetch hash and reviews are cached under ignored
`cache/maintenance/discovery/box-platform/5b055e333a802b10b8ca90fcc513643836dd92b4`.
Scripts/logs `/tmp/inspect-box.py`, `/tmp/inspect-box-versions.py`,
`/tmp/box-discovery-review.log`, `/tmp/box-versions-review.log`. Re-fetch from the pinned
vendor commit after reboot; local discovery caches are not in the CI artifact.

**Resume next:** Okta monitoring is delivered; keep its native import blocker and seek
a vendor fix or separately reviewed exact recipe. Prioritize the validated Box
compatibility refresh described above, then review its year-version slices; no Box API
PR has been created. Other major-provider discovery and separate authorized updater
PR-generation/monthly discovery remain in scope. Every parked item, unanswered Messaging
owner choice, push/approval protection and original one-week local sleep/deadline remains.
Docs-only progress changes do not require another network audit.

Manual raw-node duplicate-key checks additionally find zero duplicate scalar mapping
keys in either current Okta variant. Vendor issue #241 concerns an older duplicate-key
artifact; it is not evidence that the current hook-key/default defects have been fixed.
No third-party fork patches or vendor messages were used. Future parser duplicate-key
rejection is a separate possible infrastructure improvement, not implemented here.


**Box compatibility monitoring prepared (2026-10-05 UTC):**
Re-fetched unchanged official source at 2026-10-05T10:21:28.552915Z, commit
`5b055e333a802b10b8ca90fcc513643836dd92b4`, raw hash
`13cc601e01a7b82133975aaf7aeffb1850159a10ac6365fae00d5af94406d9d4`.
Native **3.0.2 / 2024.0 / 187 paths / 297 operations** passes full validation,
all 1451 local refs and curation-preserving import serialization preflight, with no
patches, conversion or bundling. Exact public compatibility source is selected by the
pinned vendor README; `openapi/openapi.json` is identical. Current vendor versioning
reference confirms the 2024.0 compatibility/default semantics; do not infer that its
fixed year freezes content, or select the highest subset filename instead.

Register `box-platform`, initially target existing `APIs/box.com/2.0.0/openapi.yaml`
so curation and historical content are the real comparison baseline. Import advances
target to vendor `2024.0` with its new YAML directory in a separate API PR. Registry
**47 artifacts / 46 services**, latest complete verified audit still 46 pending expansion.
Preserve native seven stable annotations, admin/free-developer restrictions, authentication,
servers and original fragment paths. Source omissions (two paths / three operations)
are not asserted runtime retirements; full delta from stored history is +28 paths / 40 ops.
Separate 2025/2026 year-versioned subsets remain discovery-only and require scope review.

Fresh discovery evidence/cache and strict preflight at
`cache/maintenance/discovery/box-platform/5b055e333a802b10b8ca90fcc513643836dd92b4`;
script/log `/tmp/refresh-box-review.py`, `/tmp/box-fresh-review.log`.
Verified #131/#134/#137 are merged AGENTS-only progress superseded by later audits;
unlinked only those app attachments to free three slots. PRs/history and all API/updater
attachments remain intact. Every existing blocker, parked item, unanswered Messaging
owner choice and original one-week local sleep/deadline remains in force.


**Box monitoring delivered / compatibility import verified (2026-10-05 UTC):**
[#173](https://github.com/ontola/openapi-directory/pull/173) merged and attached,
head `a13dd050702c77099ee6c9dfa26e118ea9bbdd8e`, merge
`ee4e1e14c82e3b3debbca36f4b4f29ca00722981`. Three expected infrastructure/instruction
files, 58 additions / zero deletions, CLEAN/MERGEABLE; exact-head
[CI 37296249041](https://github.com/ontola/openapi-directory/actions/runs/37296249041)
passes all 93 tests. Registry 47 artifacts / 46 services; no API data in this PR.

Importer re-fetched exact reviewed bytes at 2026-10-05T10:24:46.915366Z, official commit
`5b055e333a802b10b8ca90fcc513643836dd92b4`, raw hash
`13cc601e01a7b82133975aaf7aeffb1850159a10ac6365fae00d5af94406d9d4`.
New `APIs/box.com/2024.0/openapi.yaml`: **187 paths / 297 operations**, compared
with historical 2.0.0 at 161 / 260: **+28 paths / 40 ops, -2 paths / 3 ops**.
The three official omissions are GET `/metadata_query_indices`, DELETE the literal
`/metadata_templates/enterprise/securityClassification-6VMVochwUWo/schema`, and PUT
its `schema#delete` path. These source omissions are not asserted runtime retirements.
All additions/removals are included in the API PR body. Native fragment paths remain
exact; do not guess normalized replacements or remove historical coverage.

Full source/final strict validation, exact vendor-content equivalence after curation/
provenance, typed YAML roundtrip and all 1451 local refs pass. All original curation,
curated tags/externalDocs, Twitter, authentication, servers and seven stable annotations
are preserved; historical 2.0.0 is byte-identical. No source patches, conversion or
bundling. Manifest target advances to the new actual vendor version with the API file.
Verifier/logs `/tmp/verify-box-import.py`, `/tmp/box-import-verification.log`,
`/tmp/box-final-content-review.json`, `/tmp/box-import.log`. Deliver in its own API PR,
then verify the expanded 47-source audit; latest complete verified network audit remains
46 until expansion is checked. Separate 2025/2026 subsets remain discovery-only; all
prior blockers, parked decisions, unanswered Messaging owner choice and original local
one-week sleep/deadline policy remain in force.


**Box compatibility delivered / expanded audit verified (2026-10-05 UTC):**
[#174](https://github.com/ontola/openapi-directory/pull/174) merged and attached,
head `988d2fb8973aef49691677e22b084d5d42250b38`, merge
`e195e7d86bd63f108e3ff4da9d564a509bc04e3c`. Three expected files: new 42,253-line
2024.0 YAML, manifest baseline advance and 32 instruction lines; 42,286 additions /
one deletion (old manifest target only). CLEAN/MERGEABLE; exact-head
[CI 37296535892](https://github.com/ontola/openapi-directory/actions/runs/37296535892)
passes all 93 tests. Full strict content/curation/provenance/roundtrip/reference checks
are recorded immediately above. ExternalDocs retains its URL and vendor-updated
punctuation; all 67 historical tag names remain, with native vendor field updates and
new tags bringing the final list to 75. Stored 2.0.0 remains byte-identical.

[Audit 37296651820](https://github.com/ontola/openapi-directory/actions/runs/37296651820)
ran against exact main `e195e7d86bd63f108e3ff4da9d564a509bc04e3c`. All **93 tests pass**;
all **47 artifacts / 46 services** fetch and prepare: **37 matches / ten recorded
import blockers**, no unblocked drift or fetch/prepare failures. Box matches its new
actual baseline `APIs/box.com/2024.0/openapi.yaml`, exact reviewed commit/raw hash,
native 3.0.2 / 2024.0 / 187 paths / 297 operations, no transformations, successful
validation date and zero endpoint deltas. Datadog v1, Hub/Canvas and repaired
GitHub/Plaid/Xero remain explicit matches with unchanged source hashes/endpoint sets.

The same ten blockers remain Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0, Cloudflare and Okta.
Strict guards remain active; overall audit/workflow failure reflects these recorded
blockers while tests, readable summary and artifact upload succeed. All 47 entry hashes,
25 distinct repository metadata snapshots, per-row bases, strict validation profiles,
classifications, transformation evidence, endpoint deltas and identical rendered Markdown
verified at `/tmp/openapi-ci-audit-37296651820`. Eleven hosted sources remain
health-unassessed. Ignored local reports/source-health cache updated. Durable recovery:
run artifact `official-source-audit`; verifier `/tmp/verify-box-47-audit.py`, logs
`/tmp/box-47-audit-verification.log`, `/tmp/box-full-audit-ci.log`,
`/tmp/box-full-audit-status.json`. This supersedes the prior 46-source complete audit.
Full fetched main tree at this merge: **729 domains / 4,276 API files**, including
**2,102 openapi.yaml / 2,168 swagger.yaml**; header updated with dated observation.

**Box 2025 scope review / next distinct coverage:** re-fetched the pinned official
`openapi/openapi-v2025.0.json` unchanged, raw hash
`a28dd665970613050341911ed72900c3607d203b0805e71443ce12305aef4282`, native
**3.0.2 / 2025.0 / 24 paths / 37 operations**. All 383 local refs resolve; full validation
passes without patches/conversion/bundling. Zero path/operation overlap with classic
2024.0; every one of its 37 operations explicitly requires a `box-version` header with
sole enum `2025.0`. This is additional current public coverage, not a broad compatibility
replacement or evidence that 187 classic paths retired. Scope includes Doc Gen templates/
jobs, Hubs/collaborations/items/documents, Shield lists, Archives and external-user jobs.

All 37 operations are unmarked by `x-stability-level`, and the vendor's current versioning
guide defines unmarked or stable as latest stable. Current English
[Doc Gen guide](https://developer.box.com/guides/docgen) explicitly calls 2025.0 a released
API and requires Enterprise Advanced; [Hubs update guide](https://developer.box.com/guides/hubs-api/hubs/update-hub)
requires the same version header. Preserve original account/free-developer/admin limits,
authentication and server declarations; do not claim every Box product is covered.
Original source URLs, docs HTML/fetch hashes and scope JSON are cached in the same Box
discovery directory; script/log `/tmp/review-box-2025-scope.py`,
`/tmp/box-2025-scope.log`. No 2025 registration/import/PR created in this run, and it is
not in the 47-source audit. Retain both existing Box histories; do not fabricate a merged
superset or use cross-scope comparison to report mass removals. The 2026 file remains
separate discovery with two explicit beta operations and needs its own scope review.

Additional read-only 2026 operation review: the two explicit beta operations are GET
`/automate_workflows` and POST `/automate_workflows/{workflow_id}/start`. The remaining
unmarked operations are POST `/notes/convert`, `/query` and `/query_insights`. Do not
infer Doc Split coverage from the broader Doc Gen guide or fabricate a stable-only slice;
this small collection needs independent current public-reference/release review.
Evidence `2026-operation-scope.json` in the same discovery cache; no new 2026 registration,
import or PR, and no operations removed from any published artifact.

**Resume next:** Box compatibility monitoring/refresh #173/#174 are delivered and
verified; do not duplicate. Register and import the reviewed 2025 public subset as distinct
coverage, using its own actual baseline for future audits. Review curation intentionally
for this previously absent scope rather than silently cloning broad classic operations/
tags or inventing metadata. Continue independent well-known-provider discovery and
separate authorized updater PR-generation/monthly-discovery work. All recorded blockers,
parked items, unanswered Messaging owner choice, push/approval protections and original
one-week local sleep/deadline remain in force. Docs-only progress commits need no
repeat network audit.


**Cloudflare changed during this expanded audit — still blocked:**
The 47-source audit fetched new official commit
`af9a48bedc0b5668350b1eb05eefdaf2549b8ebe`, YAML entry hash
`a29cff4572ef1dfe74262e56548de00129d10a25270513f7ed86bbf1a35bcd54`, replacing the
previous `03a6de21e114bf8f998013d5b477d7c20fa70475` source observation. Actual stored
file remains unchanged. Native 3.0.3 / 4.0.0 / 2287 paths / 3647 ops unchanged between
vendor revisions; exact source path/operation sets are identical. Parsed changes:
**56 SDK annotation updates / seven schema-field changes**: five ruleset response
error-item refs added and the ruleset version `readOnly` annotation moved from its
allOf child to the property. Do not mistake stable version/counts for unchanged content.

Pinned companion vendor JSON independently equals the new YAML exactly after typed
parsing; all **24569 local refs** resolve. JSON SHA-256 `b0dd848ccfd7676886ab08a995de9de048036e5efb1ea9bb5717b7d43e3b89a9`.
The DNS-order invalid default and undefined `assets_jwt` / `pages_upload_token` security
requirements remain; no successful validation date, API import, invented auth/schema,
constraint waiver or source patch. Stored-vs-source deltas still +79/-26 paths and
+129/-49 operations. The initial audit verifier caught the changed raw hash; independent
source delta/ref/YAML-JSON review justified updating only its expected source revision/hash,
not bypassing validation or editing source bytes. All 47-source verification then passes.

New Cloudflare raw sources/review cached under ignored
`cache/maintenance/discovery/cloudflare-rest/af9a48bedc0b5668350b1eb05eefdaf2549b8ebe`;
script/log `/tmp/review-cloudflare-new-audit.py`, `/tmp/cloudflare-new-audit-review.log`,
`/tmp/cloudflare-new-audit-review.json`. YAML/fetch evidence is also durable in the CI
artifact; retrieve JSON from the same pinned vendor commit after reboot. Resume Box 2025
as directed above while preserving this updated Cloudflare blocker/source observation.


### 2026-10-05 Box 2025 official-source registration

Re-fetched reviewed vendor commit `5b055e333a802b10b8ca90fcc513643836dd92b4`,
`openapi/openapi-v2025.0.json`, SHA-256
`a28dd665970613050341911ed72900c3607d203b0805e71443ce12305aef4282`. Native
**3.0.2 / 2025.0 / 24 paths / 37 operations** passes complete source/import validation
and typed YAML roundtrip; all 383 local refs resolve. Every operation requires
`box-version` with sole enum `2025.0`; no deprecated or stability/prerelease designation.
Zero path/operation overlap with both stored Box descriptions. Current public Doc Gen
and Hubs guides rechecked; Doc Gen explicitly calls 2025.0 released and requires
Enterprise Advanced. Scope and original restrictions documented in the manifest.

Register `box-platform-2025` separately, bringing monitoring to **48 artifacts**.
Target its own `APIs/box.com/2025.0/openapi.yaml`; no cross-scope initial baseline,
copied classic curation, invented metadata or broad compatibility replacement. Both
existing Box histories remain intact. No patches, conversion or bundling. Full
regression/selected-source checks precede delivery; API import follows separately.
Fresh source/review cached in ignored Box discovery directory, script
`/tmp/refresh-box-2025-review.py`, log `/tmp/box-2025-fresh-review.log`, review
`/tmp/box-2025-fresh-review.json`. These local files are not durable after reboot;
pinned URL/hash above recover exact input.

Attachment housekeeping: verified #139 and #142 were merged, docs-only progress PRs
superseded by newer recorded evidence, then unlinked only their chat attachments to
make room. Their GitHub PRs/history are unchanged; API/updater attachments retained.
All parked items, ten known blockers and unanswered Twilio Messaging owner choice
remain in force. No rejected-push retry, owner unblock or example redaction.

Registration validation: all **93 local regressions pass**. Selected-source audit
finds the expected absent distinct target, healthy/unarchived vendor repository,
exact pinned source hash/revision and successful complete validation; no transformations
or import blocker. No API file is changed by this registration PR.


### 2026-10-05 Box 2025 validated API addition

Monitoring [#176](https://github.com/ontola/openapi-directory/pull/176) merged at
`751aad470e2d59f94b03de9f4e0b7457b5e46d90`, exact head
`7f70c94451ab7c9e9f60acdee853f7014ed13365`; all **93 regressions pass locally and
in CI 37303172727**. Three expected files only, CLEAN/MERGEABLE before exact-head merge.

Importer independently re-fetched the healthy official vendor repository/artifact
and writes only new `APIs/box.com/2025.0/openapi.yaml` plus this progress record.
Native **3.0.2 / 2025.0 / 24 paths / 37 operations**, pinned commit/raw hash as above.
Complete source/final validation, exact typed vendor-content equivalence apart from
provenance and typed YAML roundtrip all pass. All **383 local refs** resolve, including
the shared `BoxVersionHeader`; all **37 operations** require the sole version 2025.0.
No deprecated/stability flags, source patches, conversion, bundling, invented curation
or cross-scope historical baseline. Original servers, security, account/admin/plan
restrictions, externalDocs, tags and vendor fields retained verbatim in parsed content.
Both existing Box 2.0.0 and 2024.0 files are byte-identical; zero path/operation overlap,
no removals from either. This is separate current public coverage, not their replacement.

Independent verifier `/tmp/verify-box-2025-import.py`, log
`/tmp/box-2025-import-verification.log`, evidence `/tmp/box-2025-final-content-review.json`;
import log `/tmp/box-2025-import.log`. The verifier resolves vendor shared parameter
references before checking headers; no source changes to inline them. API-only paths
and AGENTS do not trigger maintenance CI; full manual checks above are required, with
expanded main audit after delivery. No 2026 collection import or blocker waiver.


### 2026-10-05 Box 2025 delivery and follow-up scope review

Monitoring [#176](https://github.com/ontola/openapi-directory/pull/176) and API
addition [#177](https://github.com/ontola/openapi-directory/pull/177) are merged and
attached; no duplicate delivery is needed. #177 exact head
`e185548ca7b2dda450ecc96f51ed7447cf703ab4`, merge
`3401453e38982262ddd3568d0d1a3b5b8983463a`: only new 5,342-line YAML and progress
record, CLEAN/MERGEABLE before exact-head merge. Native 2025.0 / 3.0.2 / 24 paths /
37 operations, all source/final validation and independent typed-content/reference/
header/history checks pass as recorded above. No source patches, invented metadata,
conversion, bundling or removals; historical 2.0.0 and 2024.0 byte-identical. All 93
regressions pass in monitoring CI 37303172727.

**Box 2026 public scope now verified, discovery only:** current vendor docs index
`https://developer.box.com/llms.txt` links `_llms/en/api-reference.md`, whose v2026.0
section points to five current references under `/reference/v2026.0/` rather than the
older guessed `...-v2026.0` paths. Earlier tool failures on guessed URLs are not
evidence that the endpoints or description are missing. The index links the complete
public download `https://developer.box.com/box-openapi-v2026.0.json`. Native GitHub
artifact remains commit `5b055e333a802b10b8ca90fcc513643836dd92b4`, hash
`f46e2c894930ec58dedd1794d7b368f46f0844ab592b5b630f33ca2ca771d370`,
**3.0.2 / 2026.0 / five paths / five operations**, 53 resolved local refs and complete
validation pass. No overlap with any of the three current Box histories.

Public [list Automate workflows](https://developer.box.com/reference/v2026.0/get-automate-workflows)
and [start workflow](https://developer.box.com/reference/v2026.0/post-automate-workflows-id-start)
references explicitly label both endpoints Beta in navigation and exclude Free Developer
Plan. The [Notes conversion](https://developer.box.com/reference/v2026.0/post-notes-convert),
[query](https://developer.box.com/reference/v2026.0/post-query) and
[query insights](https://developer.box.com/reference/v2026.0/post-query-insights)
references are unmarked, matching vendor versioning guidance and native source labels.
All five operations require `box-version: 2026.0`; identifiers and header declarations
match each embedded endpoint snippet. Preserve restrictions and beta annotations if
this complete mixed collection is selected; do not fabricate a stable-only slice or
claim every operation GA. No 2026 registration/import/PR created this run.

**Do not infer lifecycle from filtered viewer snippets:** embedded Markdown omits
`x-stability-level` and other Box extensions while the rendered navigation and raw
hosted JSON retain both explicit beta labels. Hosted download SHA-256
`b0233b1bf9dd06a26a3c9dc4e2d849656bf64ef2f61274c942f6e6f572253d73`. Exact
comparison with pinned native GitHub source finds only five added operation code-sample
lists, 55 description line folds (paragraph breaks retained; one existing trailing
space folded), and root `x-mint: {mcp: {enabled: true}}`. All other typed values/keys,
constraints, auth and lifecycle labels are identical. This is discovery comparison
only: raw inputs kept, no prose normalization, code execution or patch adopted. Native
GitHub source remains the preferred future import input. Cached original indices,
five references, hashes/fetch metadata, raw hosted JSON and verified scope evidence
under ignored Box discovery directory. Scripts `/tmp/fetch-box-2026-reference.py`,
`/tmp/verify-box-2026-public-scope.py`; logs `/tmp/box-2026-public-reference.log`,
`/tmp/box-2026-public-scope-verification.log`. Re-fetch public references after reboot.


**Expanded 48-source audit verified:**
[Run 37303528267](https://github.com/ontola/openapi-directory/actions/runs/37303528267)
checked exact main `3401453e38982262ddd3568d0d1a3b5b8983463a` after #177. All
**93 tests pass**; all **48 artifacts** fetch/prepare: **38 matches / ten known
import blockers**, no unblocked drift or fetch/prepare failures. Both Box collections
match their own actual baselines, exact reviewed hashes/commit, native stats and full
validation, no transformations, successful validation dates and zero endpoint deltas.
The same ten blockers remain Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0, Cloudflare and Okta;
no validation waiver, API deletion, fabricated auth/schema or push-protection bypass.
Audit/workflow fails for these recorded blockers while tests, summary and upload succeed.

All 48 entry hashes, **25 distinct repository metadata snapshots**, strict validation
profiles, per-row comparison bases, endpoint deltas, transformation evidence and
classifications verified; rendered Markdown exactly matches JSON. Eleven hosted
sources remain health-unassessed. Source/raw evidence and reports downloaded to
`/tmp/openapi-ci-audit-37303528267`; ignored local reports/source-health cache updated.
Durable recovery: run artifact `official-source-audit`. Verifier
`/tmp/verify-box-48-audit.py`, log `/tmp/box-48-audit-verification.log`; CI log/status
`/tmp/box-2025-full-audit-ci.log`, `/tmp/box-2025-full-audit-status.json`. This
supersedes the prior 47-source complete audit. Full main inventory: **729 domains /
4,277 API files / 2,103 openapi.yaml / 2,168 swagger.yaml**; header updated as dated
observation rather than a live count.

**Commit-only source observations:** the audit caught newer Datadog repository commit
`1b4d8386c29829141a3f888824aaccb5edd6ab72` and Grafana commit
`c7a7b797c1980a886efdd01b433a8d92b7ae7166`. Independently re-fetched all three
entry URLs pinned to these commits; exact original bytes equal both the previous and
new audit snapshots. Datadog v1 SHA-256
`83353a2cbaec662aa74d12d1721daf40d81a574fe2a043f900fc595eea6dfd8f`, v2
`2b3da388fca085e5c9dfef7fdf4617af85fc8126695e3065f7ad46badaa0118b`; Grafana
`5dde6d9a86399e9640ca0208664f7a78a8c5e63c0edbceb925686336471455a5`.
All three remain fully valid content matches, no endpoint deltas or API edits. Only
the audit verifier's expected Datadog v1 revision advanced after this byte-level review;
no weakened hash/validation checks or timestamp-only imports. Review script/log/JSON
`/tmp/verify-box-48-revision-only.py`, `/tmp/box-48-revision-only-review.log`,
`/tmp/box-48-revision-only-review.json`. Cloudflare's latest previously reviewed
`af9a48bedc0b5668350b1eb05eefdaf2549b8ebe` / `a29cff...` source and all three native
blockers remain unchanged in this audit.

**Resume next:** Box compatibility #173/#174 and distinct 2025 #176/#177 are delivered
and verified; do not repeat. The separate 2026 native/public collection and current
references are now reviewed above; consider registration/import as a complete public
collection with both explicit beta labels and all native restrictions retained, consistent
with other public mixed-lifecycle collections. Do not choose it as broad compatibility
replacement, fabricate a stable-only slice or infer missing Doc Split routes. Continue
independent well-known-vendor discovery and the separately authorized updater PR-generation/
monthly-discovery work. Source scope and release status still require manual review.
All ten blockers, explicitly parked items and unanswered Messaging owner choice persist;
local branch remains `8bf3ab52f17aabcdbb42c0dd059f4d0880f05522`, no rejected-push
retry/unblock/redaction. Original local one-week deadline/sleep rules remain in force.
Docs-only progress delivery requires no repeat full network audit.


### 2026-10-05 Box 2026 official-source registration

Startup: clean detached main `79f4c676be7fb1708bae90128429469b6bc7ee2d`, sparse
checkout reviewed; existing open #179 only edits Bunq/Codat/SendGrid YAML and does not
overlap this work. No changes to that session's PR/files. Deadline not reached.

Re-fetched exact official Box commit `5b055e333a802b10b8ca90fcc513643836dd92b4`,
`openapi/openapi-v2026.0.json`, SHA-256
`f46e2c894930ec58dedd1794d7b368f46f0844ab592b5b630f33ca2ca771d370`. Native
**3.0.2 / 2026.0 / five paths / five operations**, all 53 local refs resolve; source/
preflight import validation and typed YAML roundtrip pass. Every operation requires
sole `box-version: 2026.0`; two Automate beta labels and three unmarked operations
retained. Zero path/operation overlap with all three existing Box descriptions.
Current public versioning guidance and endpoint references rechecked. This is a complete
public mixed-lifecycle collection, consistent with existing public vendor collections
containing labelled beta functionality; not a preview-only artifact or invented slice.
No universal GA claim or compatibility replacement. Native source preserves auth,
servers, Free Developer exclusions and all account/admin restrictions without copying
classic curation. No patches, conversion or bundling.

Fresh public-reference/hosted-download comparison again verifies the exact differences
recorded above (five code-sample lists, 55 description line folds, root Mint extension).
Do not infer lifecycle from filtered viewer snippets; both raw source and rendered
navigation retain beta labels. Scripts `/tmp/refresh-box-2026-review.py`,
`/tmp/fetch-box-2026-reference.py`, `/tmp/verify-box-2026-public-scope.py`; fresh review
`/tmp/box-2026-fresh-review.json`, logs `/tmp/box-2026-fresh-review.log`,
`/tmp/box-2026-public-scope-verification.log`. Pinned source/fetch/review evidence also
in ignored Box discovery cache; durable URL/hash above recover originals after reboot.

Register `box-platform-2026` against its own absent target, bringing monitoring to
**49 artifacts**. API addition follows separately after registration checks. Attachment
limit housekeeping: verified #164/#167/#170 were merged docs-only progress PRs, now
superseded, and unlinked only their chat attachments; GitHub history unchanged and
all API/updater attachments retained. All blockers/parked items and unanswered
Messaging owner choice remain; no rejected push retry, unblock or redaction.

Registration checks: all **93 local regressions pass**; selected-source audit finds
expected missing distinct target, exact reviewed source/revision, healthy/unarchived
vendor repository and successful full validation; no transformations/import blocker.
Only AGENTS, maintenance README and source manifest changed; no API file yet.


### 2026-10-05 Box 2026 validated API addition

Monitoring [#180](https://github.com/ontola/openapi-directory/pull/180) merged at
`646239339e6f121c6bb3b2c7e959136c37fc56e1`, exact head
`bf875dca88d8c722eda88aef0c4b6024d12dbe44`; all **93 local/CI regressions pass**
(CI 37309462499). Three expected files, CLEAN/MERGEABLE before exact-head merge.
Importer rechecked vendor repository health and fetched the reviewed native artifact.

New `APIs/box.com/2026.0/openapi.yaml`: **3.0.2 / 2026.0 / five paths / five ops**.
Full source/final validation, exact typed vendor-content equivalence apart from
provenance, YAML roundtrip, all **53 local refs** and all **five required version
headers** pass. Both explicit Automate beta labels survive; Notes conversion/query/
query-insights remain unmarked, as in vendor source/current reference. Original
auth, servers, plan/admin restrictions, externalDocs/tags and vendor metadata retained.
No invented curation, cross-scope baseline, patches, conversion or bundling. All
three historical Box files are byte-identical with zero path/operation overlap.
Separate full public collection, no stable-only slice, universal GA claim or removal.

Independent verifier `/tmp/verify-box-2026-import.py`, log
`/tmp/box-2026-import-verification.log`, content review
`/tmp/box-2026-final-content-review.json`, import log `/tmp/box-2026-import.log`.
API-only paths/AGENTS do not trigger maintenance CI; complete manual verification
above plus expanded main audit after delivery. #179 remains a separate session's
unrelated YAML fixes; no changes to its files or PR. All protections/parked items
and ten known blockers remain. No Messaging retry/unblock/redaction.


### 2026-10-05 Box 2026 delivery and Zendesk discovery

Monitoring [#180](https://github.com/ontola/openapi-directory/pull/180) and API
addition [#181](https://github.com/ontola/openapi-directory/pull/181) are merged and
attached. #181 exact head `84d76796923210d5e972c22c22f834a061290fbd`, merge
`adbb1b6e745c7a9ac9e695af2e3a2f6af5654647`; only new 1,245-line YAML and AGENTS,
CLEAN/MERGEABLE before exact-head merge. Native **3.0.2 / 2026.0 / five paths / five
operations**, all 53 local refs, five required version headers and two explicit beta
labels verified. Complete typed source/final equivalence, full validation and YAML
roundtrip pass; original restrictions/auth/metadata retained. All three historical
Box files byte-identical, zero overlap/removals, no patches/conversion/bundling or
invented curation. Monitoring's **93 tests pass locally and in CI 37309462499**.

**New official Zendesk discovery — not yet registered/imported:** full fetched main
at `adbb1b6e745c7a9ac9e695af2e3a2f6af5654647` has no Zendesk/Smooch/Sunshine file at
any depth; sparse directory absence was not used. ClickUp does already exist at
`APIs/clickup.com/1.0.0/openapi.yaml`, but subsequent content inspection proves it
is an unrelated Polls sample, as recorded below. Do not equate provider-directory
presence with actual API coverage. No third-party scraped spec selected. Zendesk's prior guessed GitHub-path 404 did not establish source absence.

1. **Zendesk Support / Ticketing:** official
   [Ticketing introduction](https://developer.zendesk.com/api-reference/ticketing/introduction/)
   explicitly links Download OpenAPI file to
   `https://developer.zendesk.com/zendesk/oas.yaml`. The live native publication is
   **3.0.3 / 2.0.0 / 451 paths / 652 operations**, all **2,501 local refs** resolve,
   no external refs, four deprecated operations retained. SHA-256
   `3a477ea89b274f4d3731f1c7ff93dc93d4520de871ac759b06d3297798fd685d`. It is Support
   (tickets/users/organizations/custom objects/workflows), not all Zendesk products.
   Hosted repository health remains **not_assessed**, not implicitly healthy/current.
   Web tool's octet-stream failure was a content-type limitation; updater download succeeds.
   Native validation blocks at
   `#/components/schemas/AccessRuleCondition/properties/value/oneOf/4/type`: vendor
   declares `type: null` while top-level dialect is OpenAPI 3.0.3. The property explicitly
   allows null for present/not_present terminal operators. Do not delete the null
   alternative, invent operator/value semantics or blindly upgrade the dialect.
   Preserve all native OAuth/authentication/API-token deprecations and account limits.
2. **Zendesk Conversations / Messaging:** current official
   [OpenAPI guide](https://developer.zendesk.com/documentation/conversations/references/openapi-specification/)
   directly selects `zendesk/sunshine-conversations-api-spec`, `master`, `openapi.yaml`.
   The guide says the spec feeds the hosted reference and is maintained; generated API
   wrappers are deprecated, which is distinct from spec maintenance. The v1.1 artifact
   at historical tag 5.29 stopped receiving updates in 2020; do not substitute it.
   Live vendor repository identity/availability verified, public/unarchived/undisabled.
   Source commit `07a4ade211c8420d6a3ee94e174127522cbaa033`, native **3.0.2 / 17.13.2 /
   42 paths / 68 operations**, **742 local refs** resolve, no external refs. Retain
   `info.version` 17.13.2, distinct from runtime public API v2. SHA-256
   `d78f05f64282ecaf7dfe4fe19573dc6d49c213780061b64de39629d49d35ce01`.
   Native validation blocks at `#/components/schemas/reference`: unsupported
   `dependencies: {sourceType: [source]}` under OpenAPI 3.0.2. Vendor prose independently
   says source is required when sourceType is present. Dropping this keyword would
   discard a declared conditional requirement; do not waive it or invent alternatives.

Independently re-fetched both exact entry URLs and confirmed identical original bytes,
native defects and complete local-reference resolution. No patch, conversion, source
registration, successful validation date, API import or vendor issue/comment sent.
These are new discovery candidates, outside the configured 49-artifact audit, not
additional configured blockers yet. The ten existing registered blockers remain ten.
Investigate vendor corrections/compatible public variants or separately reviewed
constraint-preserving recipes; a schema keyword removal is not an acceptable quick fix.
No new user-declined item is inferred or blanket approval requested.

Raw sources/fetch metadata, original official-guide HTML/hash, source stats, defect
checks and exact repository metadata snapshot cached under ignored
`cache/maintenance/discovery/zendesk`. Scripts `/tmp/discover-zendesk-official.py`,
`/tmp/verify-zendesk-discovery-defects.py`; review
`/tmp/zendesk-official-discovery-review.json`, `/tmp/zendesk-verified-native-defects.json`;
logs `/tmp/zendesk-official-discovery.log`, `/tmp/zendesk-verified-native-defects.log`.
Original URLs/hash/commit above recover source evidence after reboot.


**Expanded 49-source audit verified:**
[Run 37309889023](https://github.com/ontola/openapi-directory/actions/runs/37309889023)
checked exact main `adbb1b6e745c7a9ac9e695af2e3a2f6af5654647` after #181. All
**93 tests pass**; all **49 configured artifacts** fetch/prepare: **39 matches / ten
known import blockers**, no unblocked drift or fetch/prepare failures. All three
registered Box collections match their own actual baselines, reviewed source hashes/
commit, native stats, successful full validation, zero transformations and endpoint
deltas. Historical Polls/ClickUp and Zendesk discovery candidates are outside this
configured audit; no additional registered blocker is silently counted.

The same ten registered blockers remain Cohere, Square, archived unsupported Slack,
Meraki, Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0, Cloudflare and
Okta. Audit/workflow fails on these blockers while tests, readable summary and artifact
upload succeed. Verified all **49 entry hashes / 25 distinct repository metadata
snapshots**, strict profiles, per-row comparison bases, transformations, classifications
and endpoint deltas; rendered Markdown exactly matches JSON. Eleven hosted sources
remain health-unassessed. Reports/raw snapshots in `/tmp/openapi-ci-audit-37309889023`;
ignored local reports/source-health cache updated. Durable recovery is run artifact
`official-source-audit`; verifier `/tmp/verify-box-49-audit.py`, log
`/tmp/box-49-audit-verification.log`; CI log/status
`/tmp/box-2026-full-audit-ci.log`, `/tmp/box-2026-full-audit-status.json`.
Full fetched main inventory: **729 domains / 4,278 API files / 2,104 openapi.yaml /
2,168 swagger.yaml**; header updated as dated observation. This supersedes the prior
48-source audit; docs-only progress delivery does not need another network audit.

**Fresh Cloudflare observation — still blocked:** the 49-source audit fetched commit
`1fb76fd3e67f2abf892b4702e13bb42948bc2421`, YAML SHA-256
`286ada22a3ed34f4e27d6ec077f900f051d836d6a4135c335e628a8a37507774`, replacing the
previous `af9a48bedc0b5668350b1eb05eefdaf2549b8ebe` source observation. Independent
pinned YAML re-fetch and same-commit companion JSON comparison confirm exact typed
equivalence; all **24,569 local refs** resolve. JSON SHA-256
`d63dbdde0ee732fc20669ee9f9c21442a02ffbed24799e7c9082202942506ce9`. One parsed
leaf changes: `components.responses.analytics-sql_UnprocessableQuery.description`
now explicitly mentions invalid function arguments. No paths/operations, schemas,
authentication or constraints change. Native **3.0.3 / 4.0.0 / 2,287 paths / 3,647
operations** unchanged; all three native blockers (DNS-order default, undefined
assets_jwt and pages_upload_token) remain after independent full validation. Stored
file stays unchanged at 2,234 paths / 3,567 ops; source-vs-stored deltas still +79/-26
paths and +129/-49 ops. No import, successful validation timestamp, auth fabrication,
constraint waiver or patch. Verifier caught the changed source hash; only expected
revision/hash advanced after this content/ref/validation review.
Evidence in ignored `cache/maintenance/discovery/cloudflare-rest/1fb76fd3e67f2abf892b4702e13bb42948bc2421`,
script `/tmp/review-cloudflare-49-audit.py`, log/review
`/tmp/cloudflare-49-audit-review.log`, `/tmp/cloudflare-49-audit-review.json`.
Grafana repository advanced to `7dbb7ee667842dffe198ff3a24900c3927c1a087` while its
entry hash stayed `5dde6d9a86399e9640ca0208664f7a78a8c5e63c0edbceb925686336471455a5`;
independent pinned re-fetch equals both audit snapshots byte-for-byte. No timestamp-only
API change; review `/tmp/box-49-grafana-revision-only.json`.

**ClickUp coverage correction / ready next source:** the existing
`APIs/clickup.com/1.0.0/openapi.yaml` is not actual ClickUp coverage: title `clickup20`,
description of the API Blueprint Polls example, server `https://polls.apiblueprint.org`
and `/questions` routes. Preserve this historical file; do not silently delete it or
claim example paths were retired ClickUp endpoints. Directory/brand presence alone
hid this gap. Its existing fork curation includes `x-logo` and `x-providerName`;
explicitly preserve/review legitimate branding on a correction, without copying the
Polls server, schema, title or description into a real ClickUp description. Do not
invent new curation or silently adopt an unrelated content-comparison baseline.

Current official [OpenAPI guide](https://developer.clickup.com/docs/open-api-spec)
links both public collections directly:

- **ClickUp v2:** `https://developer.clickup.com/openapi/clickup-api-v2-reference.json`,
  native **3.1.0 / 2.0 / 83 paths / 138 operations**, all **234 local refs** resolve,
  no external refs or deprecated operations. SHA-256
  `a0a72ec97ddb4e4859b9ed89b997bb784ba5828412ff35119f41e87103069662`. Full native/
  preflight-import validation and typed YAML roundtrip pass without patches/conversion/
  bundling. Server `https://api.clickup.com/api`, native `Authorization_Token` scheme
  and public token/OAuth guidance retained. Zero overlap with the stored Polls example.
  Official guide/title identify actual public v2 resources. Review plan/auth/scope
  restrictions and curation handling before registration/import; use vendor version
  `2.0`, not the legacy sample's `1.0.0` or an invented release. A separate v2 service
  directory is a reasonable layout alongside separately published v3; record the choice.
- **ClickUp v3:** `https://developer.clickup.com/openapi/ClickUp_PUBLIC_API_V3.yaml`,
  native **3.0.0 / literal info.version `version` / 23 paths / 35 operations**, all
  **268 local refs** resolve, no external refs or deprecated operations. SHA-256
  `167e0b99e0c2218312d1318fff613f180dccdfcb8decb724ce08559aa04329f2`. Preserve the
  vendor's placeholder `version` instead of assigning runtime v3 or a made-up date.
  Native `authHeader` scheme and original permissions/restrictions remain authoritative.
  Validation blocks at
  `#/components/schemas/PublicDocsCreateDocOptionsDto/properties/parent/default`: null
  default for non-nullable referenced `PublicDocsParentDto` object. `parent` is optional
  and its exact declaration is description + default null + one allOf ref. Diagnostic-
  only copy removing this exact invalid default passes complete validation; no other
  correction, changed nullability, invented runtime default or source mutation. A
  future exactly checked recipe must assert original value/declaration and referenced
  object constraints, preserve every schema alternative and fail when vendor changes.
  No patch adopted, registered source or import yet. Public v2/v3 endpoint sets are
  disjoint; no fabricated union or third-party scrape selected.

Independently re-fetched both official hosted inputs unchanged. Hosted repository
health remains unassessed. Original guide HTML/fetch metadata, source bytes, reviews,
placeholder snapshot and diagnostic evidence in ignored
`cache/maintenance/discovery/clickup`; scripts `/tmp/discover-clickup-official.py`,
`/tmp/verify-clickup-discovery.py`, logs `/tmp/clickup-official-discovery.log`,
`/tmp/clickup-verified-review.log`, reviews `/tmp/clickup-official-discovery-review.json`,
`/tmp/clickup-verified-review.json`. Re-fetch these moving public sources before delivery.

**Resume next:** all three real Box public collections are delivered/verified; do not
repeat #173/#174, #176/#177 or #180/#181. Prioritize the valid official ClickUp v2
coverage correction, preserving legitimate old curation and historical bytes with
explicit scope; review the small exact v3 default recipe separately, one PR per API
and infrastructure separate. Register Zendesk's confirmed official sources with their
known native defects visible, and investigate vendor corrections/constraint-preserving
compatibility rather than dropping null/conditional requirements. No Zendesk or ClickUp
source has been added to the 49-source manifest this run. Continue independent major-
vendor discovery and separately authorized PR-generation/monthly-discovery infrastructure.
Existing open #179 remains an independent session's unrelated YAML fixes; do not
overwrite, duplicate or merge it merely because it is open. All ten blockers, parked
items, unanswered Twilio Messaging owner choice and original local deadline/sleep
rules remain in force. No rejected-push retry, unblock or redaction.


### 2026-10-05 13:22 UTC heartbeat — ClickUp v2 monitoring preparation

Fresh main at `a9eb33b3c`; clean detached checkout, existing open #179 belongs to
an independent session and is untouched. Current official OpenAPI/authentication
guides still identify the two separately published public collections, personal
tokens and OAuth with Workspace/user permissions; OAuth app creation requires
Workspace owner/admin. Native v2 plan/admin restrictions remain unchanged.
Re-fetched v2 byte-identical: SHA-256
`a0a72ec97ddb4e4859b9ed89b997bb784ba5828412ff35119f41e87103069662`,
OpenAPI **3.1.0 / vendor version 2.0 / 83 paths / 138 operations**, all 234 local
refs resolve, no external refs/deprecated operations/patches/conversion/bundling.
Native and preflight import validation plus typed YAML serialization pass. The
source's old getting-started `/docs/index` URL returns 404; preserve vendor prose
rather than rewriting it. This does not make the linked public artifact unavailable.

Register `clickup-v2`, target `APIs/clickup.com/v2/2.0/openapi.yaml`, alongside
independently published v3. An explicitly reviewed `initial_baseline` points to
`APIs/clickup.com/1.0.0/openapi.yaml` solely to retain its actual `x-logo` and
`x-providerName` curation during correction. Existing updater uses this as the
initial comparison too: expect +83 paths/+138 operations and -1 path/-2 operations
against the unrelated Polls sample before import. These are **not ClickUp retirements**.
No endpoint overlap; keep all historical bytes. Subsequent audits select the actual
v2 destination, so no ongoing cross-scope comparisons or copied Polls API content.
Hosted repository health remains `not_assessed`; no GA/whole-platform guarantee.
This separate infrastructure PR changes no API file and expands monitoring to 50
artifacts. Deliver the full v2 correction in its own PR after tests/monitoring merge.

For the app attachment cap, verified merged docs-only #172/#175/#178 were unlinked
from this chat to attach these new deliveries. GitHub PRs and all API/updater
attachments remain intact. No retry of rejected Twilio Messaging push, owner
question, unblock/redaction, parked-item work or other-session changes.

All **93 regression tests pass** locally. Selected check against main reports the
expected explicit sample baseline/deltas and zero validation errors, hosted health
`not_assessed`, no transformations. Independent preflight with real legacy curation
passes native/import/serialized validation and exact typed vendor-content comparison;
only the two existing branding keys plus required provenance are added.


**ClickUp v2 delivered in separate API PR preparation:** infrastructure #183 merged
from exact head `2b784495b38f983f8ed93c4dac54bd1be4e7baef` as
`950d436482540d2933741c186a295457ffcc9a51`; CLEAN/MERGEABLE and all **93 tests**
passed locally and in CI [37317311436](https://github.com/ontola/openapi-directory/actions/runs/37317311436).

Importer adds `APIs/clickup.com/v2/2.0/openapi.yaml` with **83 paths / 138 operations**,
full native **3.1.0**, unchanged vendor `2.0`, `Authorization_Token` scheme, server,
all original schemas/examples/prose and feature/plan restrictions. Guest and user
management are vendor-labelled Enterprise-only; time-in-status requires owner/admin
enablement. No invented OAuth scheme, schema, version, API patch or conversion.
Both existing branding fields survive with current hosted SHA/date provenance in
`info`; no new curation is invented. Separate current v3 remains unimported/native-
invalid. Historical Polls `1.0.0` bytes remain exact SHA-256
`55ca1f4f93a936c0fd023a8b6e47e5bda1d24393b1ec56349d14a239b6e30ab2`;
no old paths claimed retired or old content copied.

Independent live re-fetch confirms raw hash unchanged. Complete source/serialized
validation, typed roundtrip, exact parsed vendor-content equality, all 234 local ref
resolutions, native auth/server identity and two-field curation preservation pass.
Script `/tmp/verify-clickup-v2-import.py`, log `/tmp/clickup-v2-import-verification.log`,
import log `/tmp/clickup-v2-import.log`. API-only PR has no maintenance-triggered CI;
these complete checks provide its validation. Follow with the expanded 50-source
audit after merge, against the actual v2 baseline; no repeated historical comparison.


**ClickUp v2 API delivery confirmed:** [#184](https://github.com/ontola/openapi-directory/pull/184)
merged from exact head `f3b0d16b015e11f98aaa78aebfb7d5c954436dbe` as
`55b4ea237c5c9fbeb7cb872b6811b4a133a4f3a4` after complete manual validation, exact
intended API+AGENTS file list, CLEAN/MERGEABLE state and no CI required for API-only
changes. Monitoring [#183](https://github.com/ontola/openapi-directory/pull/183) is
also merged/attached; no other-session work changed. The full main tree now has
**729 provider domains / 4,279 API files / 2,105 openapi.yaml / 2,168 swagger.yaml**.
This is a dated observation, not coverage of all these APIs' current sources.

**ClickUp v3 recipe guard investigation:** re-fetched original native source unchanged
at SHA-256 `167e0b99e0c2218312d1318fff613f180dccdfcb8decb724ce08559aa04329f2`.
The referenced `PublicDocsParentDto` is `type: object`, requires `id` (string) and
`type` (number), and excludes null. Parent is optional, complete declaration is the
previously recorded description/default-null/one-allOf-ref. Diagnostic-only removal
of this exact invalid default passes full validation. A simulated vendor fix adding
`nullable: true` to the referenced object also passes full validation **without
changing any siblings of the default**. The existing patch engine checks siblings
only; a simple current-format removal recipe would mistakenly erase that now-valid
default. Therefore before adopting any v3 recipe, add separately reviewed exact
referenced-schema assertions (or an equivalent checked context) so this demonstrated
vendor correction fails replay for review. Do not change runtime nullability or
infer a replacement default. No recipe, source registration or import adopted.
Evidence `/tmp/clickup-v3-recipe-preconditions.json` and ignored
`cache/maintenance/discovery/clickup/v3-recipe-preconditions.json`.

**Additional major-vendor discovery — Adobe Acrobat Sign:** no Sign/EchoSign artifact
in the full fetched main tree; `adobe.com/aem/3.7.1-pre.0` is a different product and
not Sign coverage. The current official
[developer guide](https://developer.adobe.com/acrobat-sign/docs/overview/developer_guide/apiusage)
links `https://www.adobe.com/go/acrobatsignapireference`, which redirects to
`https://secure.adobesign.com/public/docs/restapi/v6`. Current reference HTML
explicitly initializes Swagger UI with **`/restapijson/v6/restapi.json`**. Native
public input `https://secure.adobesign.com/restapijson/v6/restapi.json` is
**OpenAPI 3.1.0 / vendor version 6.0.0 / 135 paths / 184 operations**, SHA-256
`d6e49ce58e14b63ba632e0b79eb462a68b726447eccd6f80e8260f6769dbffb5`.
Independent repeated fetch is byte-identical and reproduces native validation failure.
Hosted repository health is unassessed. This is official public v6 signing coverage,
not all Adobe APIs; keep OAuth `sign_auth`, bearer `sign_bearer`, account/admin/scope
permissions and required tenant-specific access-point guidance. The relative server
`/api/rest/v6` must not be replaced with an invented universal tenant host.

Native defects prevent an import: unsupported `info.authorizationUrl`; **75 unresolved
example references across eight distinct targets** (`Full` occurs 68 times, plus
FormFieldMergeInfo, SignerIdentityReportInfo, UserLocaleInfo, CopyAgreementInfo,
DelegatedParticipantSetInfo, LibraryDocumentShareeList, SettingsQueryRequestInfo once
each). All 712 reference occurrences are local; 637 resolve and 75 fail. Structural
inspection also finds **1,122 responses lacking required descriptions**; diagnostic
copy removing only the unsupported info field then fails on the first such response.
No field removal adopted, missing examples invented, empty descriptions injected,
constraints waived, metadata fabricated or API version changed. Do not register an
importable recipe merely because JSON parsing or endpoint counting succeeded.

The official [SDK guide](https://developer.adobe.com/acrobat-sign/docs/overview/sdks/openapi)
links `adobe/acrobat-sign`'s `sdks/AcrobatSign_OpenAPI_SDK/json` directory, but all
ten published SDK JSON files are **Swagger 1.2**, not modern OpenAPI/Swagger 2.0.
Their directory's latest change was 2022-08-01 (`c280dab41440dc69d1a6236d29966be997072864`);
repository at `a9135acd159192c26f5dd8d615d6b721d237866b` is public/unarchived/undisabled
and pushed 2026-05-14, which does not establish spec freshness. The older
`adobe-sign/AdobeSign-OpenAPI` repo is also unarchived but last pushed in August 2022.
Do not import the old SDK files as current public coverage or feed Swagger 1.2 into
the locked Swagger 2.0 converter. Public live reference above resolves discovery
without a speculative conversion of the legacy SDK catalog. No Adobe source is
registered or API imported; this is a newly verified candidate outside the 50-source
audit and the ten configured blockers. Cache includes primary-guide/reference HTML
and fetch metadata, original SDK catalog/repo metadata/all ten files, current live
source/hashes and defects under ignored `cache/maintenance/discovery/adobe-sign`.
Scripts `/tmp/discover-adobe-sign-official.py`, `/tmp/discover-adobe-sign-live.py`;
reviews `/tmp/adobe-sign-live-discovery-review.json`, `/tmp/adobe-sign-native-defects.json`;
logs `/tmp/adobe-sign-discovery.log`, `/tmp/adobe-sign-live-discovery.log`.


**Expanded 50-source audit verified:**
[Run 37317708286](https://github.com/ontola/openapi-directory/actions/runs/37317708286)
checked exact main `55b4ea237c5c9fbeb7cb872b6811b4a133a4f3a4` after #184. All
**93 tests pass**; all **50 configured artifacts** fetch/prepare: **40 matches / ten
known import blockers**, no unblocked drift or fetch/prepare failure. ClickUp v2
uses its own actual `APIs/clickup.com/v2/2.0/openapi.yaml` baseline and matches
reviewed raw hash, native 3.1.0 / 2.0 / 83 paths / 138 operations, successful strict
validation, no transformations or endpoint deltas. It no longer compares to the
historical Polls sample. The newly discovered native-invalid ClickUp v3, Zendesk
Support/Conversations and Adobe Sign candidates remain unregistered and outside
these ten configured blockers; do not silently count them as configured failures.

Same ten blockers: Cohere, Square, archived unsupported Slack, Meraki, Twilio
Messaging delivery, Vercel, Mailchimp Marketing, Auth0, Cloudflare and Okta. Workflow
fails on blockers while regression tests, readable summary and artifact upload succeed;
exact job/step outcomes verified. All **50 entry hashes / 25 distinct repository
metadata snapshots**, strict profiles, per-row comparison bases, classifications,
transformations and endpoint deltas checked; rendered Markdown equals JSON. **Twelve
hosted sources** remain health-unassessed. Reports/raw snapshots recovered from CI
in `/tmp/openapi-ci-audit-37317708286`; ignored local report/source-health cache
updated only after complete verification. Durable recovery is run artifact
`official-source-audit`; verifier `/tmp/verify-clickup-50-audit.py`, log
`/tmp/clickup-50-audit-verification.log`; CI log/status
`/tmp/clickup-50-audit-ci.log`, `/tmp/clickup-50-audit-status.json`. This supersedes
the 49-source observation; no further network audit needed for this docs-only PR.

**Cloudflare native source advance, still blocked:** latest audit selected commit
`5f0956548c8984eb2262e642e8c528236585e4e6`, YAML SHA-256
`830555e3f5ebb4ac7d10b6b6ba25747672c6499167dd018df2932d440cffc5ce`. Independent
pinned YAML re-fetch and companion JSON confirm exact typed equivalence; JSON hash
`a7036aeace920f4c58a99b29df01bc3164e56e4a280251a539bfa7d4269ba313`. All **24,575
local references** resolve. Compared with previous `1fb76fd3` snapshot, six parsed
changes: two new WebMCP MCP endpoint-setting components and one added reference in
each of four existing setting unions. All previous alternatives survive; endpoint
sets unchanged. Vendor labels this setting **beta**. Value is a root-relative path
with optional query, string default empty, maxLength 2,048 and original pattern;
requires WebMCP enabled and corresponding pack active. No scope/runtime behavior
inferred or stable guarantee claimed. Native source remains **3.0.3 / 4.0.0 / 2,287
paths / 3,647 operations**; independent full validation reproduces the same three
DNS-order default/undefined-security blockers. Stored remains 2,234 paths / 3,567
ops, +79/-26 paths and +129/-49 ops versus source, no import/patch/waiver.
Verifier caught the hash change; expected revision/hash advanced only after this
content/ref/validation review. Evidence in ignored
`cache/maintenance/discovery/cloudflare-rest/5f0956548c8984eb2262e642e8c528236585e4e6`,
script `/tmp/review-cloudflare-50-audit.py`, log/review
`/tmp/cloudflare-50-audit-review.log`, `/tmp/cloudflare-50-audit-review.json`.
Grafana revision advances to `0933c5bc7fc7f46b9da6971bbf5add63137aa01b` but artifact
hash stays `5dde6d9a86399e9640ca0208664f7a78a8c5e63c0edbceb925686336471455a5`;
independent pinned re-fetch equals both audit snapshots byte-for-byte. No timestamp-
only API update; `/tmp/clickup-50-grafana-revision-only.json` records evidence.

**Resume next:** ClickUp v2 coverage and monitoring #183/#184 are delivered/verified;
do not repeat the import or compare against Polls. Implement separately reviewed
exact referenced-schema preconditions for the small v3 invalid-default recipe, with
the demonstrated nullable vendor fix failing replay; then public v3 scope/auth/release
review and one API PR if full validation succeeds. Register Zendesk's confirmed
official sources with native defects visible; investigate constraint-preserving
compatibility/vendor corrections. Adobe Sign's current public 3.1 source is now a
verified discovery lead with unresolved examples/missing descriptions, not a ready
import or old SDK conversion. Continue major-vendor discovery and separately
authorized PR-generation/monthly-discovery infrastructure. Independent open #179,
Twilio Messaging branch/owner choice, all parked items and local deadline/sleep
rules remain unchanged. No rejected push retried, example redacted, unblock action,
new automation, power setting change, cloud-host migration or vendor message.


### 2026-10-05 14:23 UTC heartbeat — checked reference assertions / ClickUp v3

Started from clean detached main `745ff2f70`, fetched main unchanged, read
instructions/parked queue and existing PRs. Independent open #179 remains untouched.
New updater recipe `assertions` compares complete JSON nodes at explicit local
pointers **before any operation in that recipe**. Nonempty exact pointer/value
lists, JSON-type-sensitive equality and missing/duplicate/malformed-pointer guards
fail closed; unknown recipe fields are now rejected to catch misspelled preconditions.
No asserted content is modified; existing recipes are backward compatible and
recipe hashes/provenance include all preconditions. No general coercion or validation
waiver. Four regressions cover actual ClickUp recipe/one-default-only output, valid
nullable vendor fix and changed required/default fields, escaped array pointers and
false-vs-zero/string/null types, invalid/missing/duplicate/misspelled assertions,
and failed live-style audit retaining source bytes without validation success.
All **97 tests pass** locally; complete existing recipe suite remains green.

Fresh official v3 hash unchanged:
`167e0b99e0c2218312d1318fff613f180dccdfcb8decb724ce08559aa04329f2`, native
**3.0.0 / literal version `version` / 23 paths / 35 operations / 268 local refs**.
Register `clickup-v3` target `APIs/clickup.com/v3/version/openapi.yaml`; no old v3
curation or comparison baseline. Preserve v2 and historical Polls files unchanged.
The reviewed recipe asserts complete `PublicDocsCreateDocOptionsDto` (including
optional parent and its exact original declaration) and `PublicDocsParentDto`
(object, required string id/number type, no nullable). Remove only parent's invalid
null default after sibling/value checks. All schemas, required fields, nullability,
prose and alternatives remain identical; no replacement or runtime default inferred.
Fresh native source fails exactly at that default; patched source/preflight import/
serialized YAML fully validate, exact typed content comparison matches a copy with
only that field removed, all 268 refs resolve. Simulated vendor `nullable: true`
fix validates natively but now stops replay. Selected audit reports missing v3
baseline, no validation errors, one hash-recorded transformation and hosted health
`not_assessed`. Source cached under ignored `cache/maintenance/clickup-v3`.

Public scope/release review: current official OpenAPI guide links v3 separately;
[Chat guide](https://developer.clickup.com/docs/chat) explicitly calls Chat
experimental. This public collection includes 19 Chat operations, one comment-type
operation tagged Chat (Experimental), eight Docs/page operations, two attachments,
privacy/access, audit logs and three task operations. It is mixed-lifecycle public
coverage, not a preview-only or claimed GA/stable-only slice. Preserve all vendor
tags, authHeader/server definitions and permissions/restrictions; do not inject
speculative lifecycle extensions. Current
[Docs limitations](https://developer.clickup.com/docs/docsimportexportlimitations)
and [plan availability](https://developer.clickup.com/docs/apis-available-by-plan)
reviewed; public availability does not waive formatting/plan/user permissions.
Deliver updater guards/recipe/monitoring separately from API import. No v3 API file
changed in this infrastructure PR.

At app attachment limit, verified merged docs-only #147/#182/#185 were unlinked to
attach these new deliveries; GitHub and API/infrastructure attachments unchanged.
No Twilio rejected-push retry/redaction/unblock, new automation, power changes,
cloud-host migration, vendor message or parked-item work.


**ClickUp v3 infrastructure merged:** [#186](https://github.com/ontola/openapi-directory/pull/186)
from exact head `85c01572683de5dc655cef590f7aa1eed7a50d82`, CLEAN/MERGEABLE with
intended six infrastructure/doc files and **97 local/CI tests** passing. CI
[37325195836](https://github.com/ontola/openapi-directory/actions/runs/37325195836),
log/status `/tmp/clickup-v3-guard-ci.log`, `/tmp/clickup-v3-guard-ci-status.json`.
Recipe SHA-256 `36c6e20fd869abb31c544750fd0ba9fe63052181219594050267ed770578e810`.

**Separate API import prepared:** `APIs/clickup.com/v3/version/openapi.yaml`,
native **3.0.0 / literal vendor version `version` / 23 paths / 35 operations**.
Independent original live re-fetch confirms reviewed hash, original invalid null
default, patched source validates, and serialized typed values match the entire
vendor document except exactly that one default and required provenance. All 268
local refs resolve; zero external refs or conversion. Complete containing and
referenced schema assertions protect original optionality/constraints; valid
nullable vendor correction blocks replay. No fabricated schema/auth/version, old
curation removed or fresh curation invented. Both existing ClickUp files remain
byte-identical to fetched main, v2/v3 endpoint sets disjoint. Native authHeader,
server, tags, schemas (including unused vendor definitions) and examples retained.

Public scope includes **experimental Chat**; no whole-platform or universal-GA
claim. Native Workspace audit-log operation is owner-only/Enterprise; per-user
time estimates are Business or above, at most ten estimates and assigned users;
privacy/access edits may incur charges. Docs access follows user permissions and
formatting limitations. Original restrictions/prose retained without inferred
server behavior. Public mixed-lifecycle artifact was imported completely rather
than an invented subset. Verification `/tmp/verify-clickup-v3-import.py`, log
`/tmp/clickup-v3-import-verification.log`; CLI log `/tmp/clickup-v3-import.log`.
API-only PR does not trigger maintenance CI; complete independent checks above
are its validation, followed by full 51-source CI audit after merge.


**51-source audit found a new actionable Sentry refresh:** full CI
[37325626675](https://github.com/ontola/openapi-directory/actions/runs/37325626675)
at main `dd679cc363eff5baebee5fe877fd3b2f028de1e2` detected Sentry vendor commit
`226d4470bf70f5617eb1b4f8f4852a98e2dba97b`, raw SHA-256
`32495641a918ab3656d87dade918dd7b7daeb0c036928b6779c4be89a9424a64`. Native public
**3.0.3 / fixed v0** grows from **151 paths / 245 ops** to **155 / 249**, +4 GET
paths/operations and no removals. Full parsed vendor-content diff is exactly eight
additions: four new SCIM discovery paths and four response schema components.
All existing endpoint/schema/auth content stays identical. The added endpoints
list ResourceTypes, query ResourceTypes/{resource_type_name}, query
Schemas/{schema_uri}, and retrieve ServiceProviderConfig. Source is vendor-
dereferenced, zero refs; no reconstruction, bundling, patches or conversion.

Fresh repository identity/public/unarchived/undisabled health and pinned byte
re-fetch/full validation confirmed. Current
[SCIM guide](https://docs.sentry.io/api/scim/) requires SaaS Business Plan with
SAML2 enabled and SCIM-generated bearer token; retain native member:admin/read/write
auth scope alternatives and original restrictions. No preview/deprecated marking
on these added operations; other Sentry products are outside this public artifact.
Independent serialized validation, exact typed vendor-content equivalence, all old
endpoint/auth/curation preservation, roundtrip and SHA/commit provenance pass.
Script `/tmp/review-sentry-51-audit.py`, log/review `/tmp/sentry-51-audit-review.log`,
`/tmp/sentry-51-audit-review.json`; independent import checker/log
`/tmp/verify-sentry-scim-import.py`, `/tmp/sentry-scim-import-verification.log`.
Original bytes/review cached in ignored `cache/maintenance/discovery/sentry/226d4470bf70f5617eb1b4f8f4852a98e2dba97b`.
Deliver this in its own API refresh PR, then selected post-merge Sentry check;
the complete audit and ClickUp results are recorded in the following docs PR.


**ClickUp v3 delivery confirmed:** updater infrastructure #186 merged from head
`85c01572683de5dc655cef590f7aa1eed7a50d82` as
`4402db468bba7bf4ef0fd8c8d539c24abe4503c7`. Separate API
[#187](https://github.com/ontola/openapi-directory/pull/187) merged from exact
head `88ea4994e816563201c2069526252475d77e853f` as
`dd679cc363eff5baebee5fe877fd3b2f028de1e2` after complete independent source/import/
serialization checks, intended API+AGENTS file list and CLEAN/MERGEABLE state. Both
PRs attached. No maintenance CI for API-only PR; infrastructure passed 97 tests
locally/CI. Full fetched-main dated inventory now **729 domains / 4,280 API files /
2,106 openapi.yaml / 2,168 swagger.yaml**. Public v3 includes experimental Chat;
keep original scope/version/restrictions and exact assertions on future refreshes.

**Zendesk Conversations diagnostic compatibility investigation:** primary official
[guide](https://developer.zendesk.com/documentation/conversations/references/openapi-specification/)
still identifies the maintained public spec as the direct reference source; generated
wrappers are deprecated, not the native specification. Fresh repository-health check
confirms same public/unarchived/undisabled repository; re-fetched entry still commit
`07a4ade211c8420d6a3ee94e174127522cbaa033`, SHA-256
`d78f05f64282ecaf7dfe4fe19573dc6d49c213780061b64de39629d49d35ce01`,
native **3.0.2 / 17.13.2 / 42 paths / 68 operations**. No source registered/imported.

Original `reference` object has unsupported `dependencies: {sourceType: [source]}`.
Vendor prose explicitly requires source when sourceType is present. Diagnostic
copy replaces only that keyword with supported
`anyOf: [{not: {required: [sourceType]}}, {required: [source]}]`, expressing the
same implication: sourceType absent OR source present. All other type/property/
length/prose/required-uri constraints remain exact; no dependency simply deleted.
Whole-schema Draft4Validator truth checks match for all 16 combinations of absence,
valid strings, null and invalid numeric sourceType/source values, with otherwise-
valid required `uri` supplied: three valid / thirteen invalid cases. SourceType
alone fails while both absent, source-only and valid paired values pass. These diagnostics
do not adopt a patch or make a server-behavior claim.

Full-document validation then exposes a **second native defect**:
`#/components/parameters/userFilterQuery/schema/properties/identities.email/required`
is boolean true, while a Schema Object requires an array. Complete query parameter
has `required: true`, object schema with only `identities.email`, no parent required
array, and a string child carrying this malformed true flag. Diagnostic copy moves
the child true-presence declaration to enclosing `required: [identities.email]`,
retaining query `required: true` and every other field. The full document validates
after these two diagnostic changes. This is a candidate interpretation of the
vendor's malformed declaration, not an established equivalence of invalid syntax
or new observed server behavior; check the public user-list contract before adoption.
Do not blindly drop the child requirement or claim fixing dependencies alone is
sufficient. A future exact recipe needs full-node preconditions, constraint/opt-in
semantics tests and vendor-fix refusal, plus release/auth/scope review before any
import. New exact assertion support can protect complete containing objects.

Original bytes, health snapshot and diagnostic objects/tests cached in ignored
`cache/maintenance/discovery/zendesk/conversations-dependency-review.json`;
script `/tmp/review-zendesk-conversations-dependency.py`, review/log
`/tmp/zendesk-conversations-dependency-review.json`,
`/tmp/zendesk-conversations-dependency-review.log`. The follow-up diagnostic records
the second defect and complete parameter there. Zendesk Support and Adobe Sign
remain separate native-invalid discoveries, outside configured audit counts.


**Expanded 51-source audit verified, with detected drift delivered:**
[Run 37325626675](https://github.com/ontola/openapi-directory/actions/runs/37325626675)
checked exact main `dd679cc363eff5baebee5fe877fd3b2f028de1e2` after ClickUp v3 #187.
All **97 tests pass**; all **51 artifacts** fetch/prepare: **40 matches / one
unblocked Sentry content change / ten known import blockers**. This original CI
snapshot is retained as observed, not relabelled after the later Sentry refresh.
Both ClickUp v2 and v3 match their own actual baselines, source hashes, typed native
versions/stats, full validation and zero endpoint deltas. v3's one checked recipe
transformation includes hash `36c6e20fd869abb31c544750fd0ba9fe63052181219594050267ed770578e810`.
Thirteen hosted sources have health unassessed. All **51 raw entry hashes / 25
repository metadata snapshots**, profiles, per-row baselines/classifications/
transformations/deltas and exact Markdown/JSON rendering verified. No fetch/prepare
failures. Same ten blockers: Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0, Cloudflare and Okta.
Audit job/workflow fails on known blockers; tests, readable summary and artifact
upload succeed, exact head/job/step outcomes checked.

Reports/raw artifacts `/tmp/openapi-ci-audit-37325626675`; durable recovery is
`official-source-audit` on that run. Ignored local report/source-health cache updated
only after verification. Script/log `/tmp/verify-clickup-51-audit.py`,
`/tmp/clickup-51-audit-verification.log`; CI log/status
`/tmp/clickup-51-audit-ci.log`, `/tmp/clickup-51-audit-status.json`. Verifier caught
the new Sentry drift; expected classification/hash/revision were reviewed deliberately,
not forced to a stale match. Cloudflare source hash/commit/stats and its three native
blockers remain identical to the prior 50-source observation; no redundant import/
patch. Grafana moves to `c2d399ec8baabc3de4a0ac08d6b890a8c222c4f2` with unchanged
raw hash `5dde6d9a86399e9640ca0208664f7a78a8c5e63c0edbceb925686336471455a5`;
independent pinned re-fetch is byte-identical to both audits. Evidence
`/tmp/clickup-51-grafana-revision-only.json`; no timestamp-only API refresh.

**Sentry drift closure confirmed:** separate API
[#188](https://github.com/ontola/openapi-directory/pull/188) merged exact head
`005b265fb8d34d7ca6157b98456cc928ef0ec8cb` as
`dff639b2ae4dc2d672039340e490c11467ea3ee3`, after intended API+AGENTS file list,
CLEAN/MERGEABLE and complete independent validation/content/curation checks.
Post-merge selected check against that exact main reports **matches_source**, fixed
v0 / native 3.0.3 / **155 paths / 249 operations**, no deltas/validation errors/
transformations, repository available and reviewed source hash/revision unchanged.
Report `/tmp/sentry-scim-post-merge.json`. Only Sentry changed between the full
audit tree and this source check; preserve original CI classifications above and
this independently verified closure. No repeat broad network audit needed for
the following docs-only change. API/file inventory remains 729 / 4,280 / 2,106 /
2,168 because this fixed-version refresh changed an existing file. To attach this
additional delivered API and progress PR at the app limit, verified merged docs-only
#64 was unlinked; GitHub PRs and all API/updater attachments unchanged.

**Resume next:** ClickUp v2/v3 and new Sentry SCIM discovery refresh are delivered;
do not repeat imports. First verify Zendesk Conversations' public user-list/filter
contract for the malformed boolean child required flag. The diagnostic equivalent
dependency plus candidate required-array placement fully validate, but need
separately reviewed exact source recipes/regressions, including vendor-fix refusal,
and public release/auth/scope check before registration/import. Preserve all
constraints; do not merely drop dependencies or true required declarations.
Register official Zendesk Support with its native null-type defect visible and
continue compatible-source/correction investigation. Adobe Sign remains a separate
verified native-invalid discovery; old Swagger 1.2 SDK inputs are not current
OpenAPI coverage. These three unregistered candidates are outside the configured
ten blockers. Continue well-known vendor discovery and separately authorized
PR-generation/monthly-discovery infrastructure. Independent open #179, Twilio
Messaging branch/owner choice, all parked items and local deadline/sleep rules
remain unchanged; no approval rejection bypass, push retry/redaction/unblock,
new automation, power setting change, cloud-host migration or vendor message.


**Zendesk Conversations official monitoring and compatibility recipe (2026-10-05):**
The rendered current [List Users reference](https://developer.zendesk.com/api-reference/conversations/#operation/ListUsers)
explicitly states the identities.email filter is required and demonstrates the
`filter[identities.email]` query. The same requirement appears verbatim in the
maintained source operation prose. This resolves the diagnostic's outstanding
required-filter intent question; it is documentation evidence, not a live API test.
The [OpenAPI guide](https://developer.zendesk.com/documentation/conversations/references/openapi-specification/)
identifies the maintained native spec as the direct reference input; only generated
wrappers/old v1.1 are deprecated. The current [authentication guide](https://developer.zendesk.com/documentation/conversations/getting-started/api-authentication/)
and quickstart confirm public runtime v2 and tenant `https://{subdomain}.zendesk.com/sc`,
basic/JWT access, account/app/integration restrictions and direct-account-only
provisioning. User-scoped SDK JWTs are not accepted by the public API. Preserve
labelled legacy Smooch servers and vendor scope prose; do not infer universal access.

Fresh health and source check remain public/unarchived/undisabled, commit
`07a4ade211c8420d6a3ee94e174127522cbaa033`, entry SHA-256
`d78f05f64282ecaf7dfe4fe19573dc6d49c213780061b64de39629d49d35ce01`.
Native **3.0.2 / document 17.13.2 / 42 paths / 68 operations**, 742 resolved local
references, none external, no operation deprecation or preview/beta/experimental
prose found in this snapshot. Do not equate document release 17.13.2 with runtime v2.
Full source still has the two reviewed invalid schema declarations. Registered
`zendesk-conversations` now selects that maintained moving source, bringing the
manifest to **52 artifacts**; API import remains a separate PR.

`maintenance/patches/zendesk-conversations.json` hash
`494e2da6b256cfb3a16ba09d7f0e7b949257ded241bc885243db7dc7e083deed`
uses exactly checked whole-node replacements: original sourceType dependency becomes
supported anyOf/not presence logic with all other reference constraints retained;
malformed child boolean required becomes the parent identities.email required array,
retaining query required:true and deepObject serialization. Full original reference,
full filter parameter and operation prose assertions run before either correction.
Vendor fixes/changed constraints/optional filter/changed documentation stop replay.
No enums/types/nullability/defaults/auth or runtime semantics invented. Full prepared
native validation and all 742 references pass. Three new regressions check 16 whole-
schema truth cases with required URI supplied (3 valid/13 invalid), original URI and
length constraints, filter presence/string type without invented email/length rules,
vendor-fix refusal and caller input preservation. **100 tests pass locally**; log
`/tmp/zendesk-conversations-tests.log`, full source/diagnostic/cache evidence remains
under ignored `cache/maintenance/discovery/zendesk`, prepared review
`/tmp/zendesk-conversations-prepared-review.json`. CI/import delivery still pending.

To make attachment slots at the app limit, unlinked verified merged AGENTS-only
progress PRs #68/#73/#85; GitHub records and all API/updater attachments stay intact.
Independent #179 and all parked/delivery/deadline/local sleep rules remain unchanged.

**Zendesk Conversations delivery held by push protection — do not retry:**
Separate fully validated API addition remains local branch
`codex/add-zendesk-conversations`, exact commit
`afb95b89fdc7a4f9566e22495abe97627e7a82ed`; no API PR created, remote push rejected
GH013. GitHub flags a Twilio Account String Identifier in the vendor's own example
at `#/components/schemas/twilio/allOf/1/properties/accountSid/example` (serialized
line 6174). Exact unchanged value verified in pinned original vendor bytes; no literal
printed/recorded here. Same complete validation/content/reference/roundtrip evidence
above, checker `/tmp/verify-zendesk-conversations-import.py`, review/log
`/tmp/zendesk-conversations-import-review.json`,
`/tmp/zendesk-conversations-import-verification.log`. Native example evidence with
value omitted `/tmp/zendesk-conversations-push-protection-review.json`.

Owner review link:
https://github.com/ontola/openapi-directory/security/secret-scanning/unblock-secret/3KHixj4X70ysiwPZQDeAaA5dbR7
Owner was asked once to allow this published Zendesk example or explicitly authorize
an exactly checked neutral example replacement. Response pending; selected/default
options and elapsed time are not authorization. Do not retry push, visit unblock,
redact examples or bypass the block without a fresh applicable owner response.
Existing separately parked Twilio Messaging choice remains unchanged.

Registered source now has an explicit import delivery guard, so future checks fetch,
prepare, fully validate and report this missing-but-valid description as import
blocked; CLI import refuses new writes. Guard does not waive schema validation or
change source bytes/compatibility recipe. Source registration/recipe #190 is merged
and attached, 100 local/CI tests. Saved API branch also contains its independent
source/import evidence in AGENTS; consult both it and this main progress record.
Proceed with expanded 52-source audit, expecting delivery blockers separately from
native defects, then Zendesk Support null-type compatibility investigation and
other well-known official discovery. Adobe Sign remains native-invalid/unregistered.

**Zendesk Support moving hosted source — diagnostic only (2026-10-05):**
Fresh hosted publication has advanced since the prior discovery, despite fixed
2.0.0: original hash `3a477ea89b274f4d3731f1c7ff93dc93d4520de871ac759b06d3297798fd685d`
451 paths / 652 ops now becomes hash
`3258ec97eed69d58deceee500efe090ea0e0b16fd616dddf15107ab209688fdc`,
**native 3.0.3 / 2.0.0 / 455 paths / 657 ops**, 2,534 resolved local refs, none
external. Full parsed comparison finds 49 leaf additions/removals/changes: parallel
approval requests/response alternatives, approval-workflow IDs, custom-role change-
management permissions, autocomplete wording and four ticket-task/subticket/link
paths (five ops). No endpoint removals. New bytes cached before review; not forced
to the older snapshot/hash. Hosted health remains unassessed, no git revision claimed.

Same first native invalid `AccessRuleCondition.value.oneOf[4]: {type: 'null'}` remains.
Diagnostic copy represents that null-only alternative as `{type: string, nullable: true,
enum: [null]}`: OAS 3.0.3 nullable adds null only when type is explicit, and enum
excludes every string. Whole value semantics match original Draft4 type:null intent
under OAS30Validator for 13 representative string/null/bool/integer/fraction/object/
array values; both positive and negative witnesses. All original four non-null
alternatives and oneOf exclusivity are retained. In particular, existing integer/
number overlap still rejects integer values; do not silently replace oneOf with anyOf
or claim new runtime behavior. This is **not adopted/registered/imported**.

Full diagnostic document then reveals a second native defect: unused component
`#/components/parameters/UserLogin` declares `in: path` with `style: deepObject`,
required:true, object email/password schema. It has zero `$ref` occurrences in this
artifact; do not guess a query relocation or remove it without an exact, separately
reviewed recipe and complete follow-up validation. Public [custom-object permission reference](https://developer.zendesk.com/api-reference/custom-data/custom-objects/custom_object_permissions/)
corroborates terminal Present/Not present concepts/admin restrictions; schema prose
itself explicitly allows null. [OpenAPI 3.0.3 schema rules](https://spec.openapis.org/oas/v3.0.3.html#schema-object)
explain the diagnostic nullable/enum representation. Preserve all other constraints.

Scripts/reviews/log `/tmp/review-zendesk-support-null-compatibility.py`,
`/tmp/zendesk-support-latest-review.json`,
`/tmp/zendesk-support-null-compatibility-review.json`,
`/tmp/zendesk-support-null-compatibility-review.log`; original/latest bytes and evidence
in ignored `cache/maintenance/discovery/zendesk`. Support and Adobe Sign remain
unregistered native-invalid candidates outside the configured audit blockers.

**Zendesk Support monitoring registration:** `zendesk-support` now registers the
current official hosted publication separately, bringing the manifest to **53
artifacts**. It adopts no diagnostic patch/conversion or API file. Actual selected
native source check `/tmp/zendesk-support-monitor-check.json` verifies reviewed
new hash/stats, successful fetch/comparison, health not_assessed, native null-type
failure, no transformations and **no successful-validation stamp**. The nonzero
CLI exit is the expected verified native validation block. Preserve the discovered
unused UserLogin defect too; do not assume the null-only diagnostic permits import.
The in-flight full CI audit still covers the exact **52-source** main before this
registration; record that snapshot separately and run a complete 53-source check
on a later run after this registration is merged. Do not relabel its total.
Merged AGENTS-only progress #101 was unlinked to make room at the attachment limit;
all API/updater attachment records remain. Independent #179 remains untouched.

**MongoDB Atlas content drift found in expanded 52-source audit:**
Run [37358848624](https://github.com/ontola/openapi-directory/actions/runs/37358848624)
at exact main `9a4d00029f41fd78b4a76bb4953403663ba69005` finds one unblocked Atlas
content change, despite fixed version and unchanged endpoint counts. Current official
source commit `f84bc82a8a0f85c83cbca399da3228223d6a397d`, SHA-256
`8c15051acf24542238abb64a3e6fc5dda872337ce4fdceb9bf560c93580e2fd4`,
**native 3.0.1 / fixed 2.0 / 339 paths / 549 operations**. Independent pinned and
moving-source re-fetch plus public/unarchived/undisabled repository checks agree.
Full parsed comparison is exactly three leaf changes: add `Agent Engine` to the
CostExplorerFilterRequestBody.services and UsageDetailsFilterRequest.skuServices
item enums, preserving all old alternatives/order; vendor `info.x-xgen-sha` updates.
No endpoint additions/removals, authentication or server changes. This does not
establish GA/account availability of the named product; retain source restrictions.

Separate fixed-version import refreshes `APIs/mongodb.com/atlas-admin/2.0/openapi.yaml`
in place with no source patches, conversion or bundling. All endpoints/auth/servers
and existing APIs.guru curation retained. Native and serialized complete validation,
exact typed curated vendor-content equivalence, all **8,593 local references** resolved
(zero external), typed YAML roundtrip and SHA/commit/profile provenance pass.
Fresh review `/tmp/review-atlas-52-audit.py`, log/review `/tmp/atlas-52-audit-review.log`,
`/tmp/atlas-52-audit-review.json`; independent import checker/log
`/tmp/verify-atlas-agent-engine-import.py`,
`/tmp/atlas-agent-engine-import-verification.log`; import log
`/tmp/atlas-agent-engine-import.log`. Original bytes/full diff/health cached in ignored
`cache/maintenance/discovery/mongodb-atlas-admin/f84bc82a8a0f85c83cbca399da3228223d6a397d`.
API PR delivery and audit-wide verification/closure will be recorded separately.

**Zendesk monitoring/delivery-guard and Atlas delivery confirmed:**
#190 is merged/attached as recorded above. Delivery guard
[#191](https://github.com/ontola/openapi-directory/pull/191) merged exact head
`28a743f39a72a24b3feb2d59e7d87483e72ddb02` as
`9a4d00029f41fd78b4a76bb4953403663ba69005`; intended AGENTS+manifest files,
CLEAN/MERGEABLE and [CI 37354570263](https://github.com/ontola/openapi-directory/actions/runs/37354570263)
passed 100 tests. GitHub connection reset on merge response; read-only REST confirms
merged state/exact head/merge SHA, no duplicate merge or workaround.
Separate Support monitoring
[#192](https://github.com/ontola/openapi-directory/pull/192) merged exact head
`0810b4213edd55e1b502c6415cadd3d30cae6bc3` as
`f751abbb8e1d256a3c69a3b6e5923b38b8c1fe84`, intended AGENTS/README/manifest files,
CLEAN/MERGEABLE and [CI 37359670026](https://github.com/ontola/openapi-directory/actions/runs/37359670026)
passed 100 tests. Both attached immediately after confirmed PR creation.
CI logs `/tmp/zendesk-conversations-delivery-guard-ci.log`,
`/tmp/zendesk-support-monitor-ci.log`; manifest now **53 artifacts**, Support is a
separately verified native-invalid source and not part of the 52-source CI snapshot.

Separate Atlas refresh
[#193](https://github.com/ontola/openapi-directory/pull/193) merged exact head
`da22b4d1d35c9a41d252155f11f57a635ce1974b` as
`54b6b7a3c8268230225d029ad612780822f80676`, after intended API+AGENTS files,
CLEAN/MERGEABLE and full independent native/import/curation/reference/roundtrip
checks above. Attached. API-only PR has no maintenance CI; complete local checks
pass. Post-merge selected check `/tmp/atlas-agent-engine-post-merge.json` against
that exact main reports **matches_source**, fixed 2.0/native 3.0.1/339 paths/549 ops,
reviewed hash/revision, no validation errors/transformations or endpoint deltas.
Inventory recomputed from fetched tree remains **729 domains / 4,280 API files /
2,106 openapi.yaml / 2,168 swagger.yaml**; Zendesk addition is held, not counted.

**Expanded 52-source CI audit verified as observed:**
[Run 37358848624](https://github.com/ontola/openapi-directory/actions/runs/37358848624)
checked exact main `9a4d00029f41fd78b4a76bb4953403663ba69005`, prior to Support
registration and Atlas closure. **100 tests pass**, all **52 artifacts** fetch/
prepare; **40 matches / one valid Atlas content change / 11 import blockers**.
Preserve this original snapshot, not relabelled as 53 sources or 41 matches after
later changes. New Zendesk Conversations is missing but fully validates after its
checked recipe and is explicitly delivery-blocked on vendor-example push protection.
Its hash/revision/stats and recipe hash match the independent held import evidence.
Sentry's actual current 155/249 baseline matches, including its prior SCIM closure.

Other ten blockers unchanged: Cohere, Square, archived unsupported Slack, Meraki,
Twilio Messaging delivery, Vercel, Mailchimp Marketing, Auth0, Cloudflare and Okta.
Thirteen hosted sources have health unassessed; **26 unique repository metadata
snapshots**. All 52 raw-entry hashes, 26 repository-response hashes, validation
profiles, per-row actual baselines/classifications/transformations/deltas and exact
Markdown/JSON report rendering verified. No fetch/prepare failures. Audit job/
workflow fails on known blockers; tests, summary and artifact upload succeed.
Exact head/job/step conclusions verified independently. Downloaded artifacts
`/tmp/openapi-ci-audit-37358848624`; durable recovery `official-source-audit` on
that run. Ignored local report/health copies updated only after all assertions pass.
Verifier/log `/tmp/verify-zendesk-52-audit.py`,
`/tmp/zendesk-52-audit-verification.log`; CI log/status
`/tmp/zendesk-52-audit-ci.log`, `/tmp/zendesk-52-audit-status.json`.

Verifier caught and deliberately reviewed Atlas drift and additional moving-source
revisions/hashes. Independently pinned byte re-fetches confirm source-identical
revision-only advances for Sentry `0a3f51ed3397530cdbb2de8d03f15625d0748bde`, both
Datadog artifacts at `b851cbca2c9a3eeed913567f5e0d04eca05a0ce6`, and Grafana
`0833fa8880960f3d49a034718c89fddcce83c0e0`. No timestamp-only API changes created;
evidence `/tmp/zendesk-52-revision-only.json`.

**Blocked moving sources reviewed without waivers:**
Vercel native hash now
`93294b378d48fd4bd36a3e57e2cf363f72249f1dc6b4733f8b533b07d9c89a27`,
still 3.0.3/fixed 0.0.1/321 paths/443 ops, **2,542 resolved local refs**. Nineteen
parsed leaf changes since the prior audit: dark-mode project avatars, new
v0-migration-payment-confirmed event enum/payload, Connect 500 response and sandbox
4096-byte size guidance. No endpoint additions/removals. Native unsupported const/
other invalid schema declarations and previously recorded missing body remain;
no dialect upgrade, patch or import adopted. Bounded diagnostics under local Python
3.12 and CI 3.11 can select different first five leaves; each reported pointer resolves
in the same unchanged native artifact, both full validations fail. Preserve both
lists, not force exact text equality or waive constraints.

Cloudflare official commit `d1171ef1b5f19c5602d99642603a0adafa07742a`, YAML hash
`c78911d6b9f56246ceccdc0d73d1851227cdb1334e0db74fbcfa3867ec547c34`,
still 3.0.3/fixed 4.0.0/2287 paths/3647 ops, **24,577 resolved local refs**.
Full parsed difference is 101 leaves (33 additions/52 changes/16 removals):
resource-library application/category schema/filter/lookup and SDK wording, tagging
access_service_token alternative, AI Gateway usage-cost wording, and Page Shield
native authentication alternatives/hidden-extension/schema-type changes. No endpoint
additions/removals versus prior source. Independently pinned YAML re-fetch and full
typed companion JSON equivalence pass. Same three native blockers persist: invalid
DNS order default and undefined assets_jwt/pages_upload_token security schemes.
Source lifecycle/authorization changes are vendor content; no universal GA claim,
auth fabrication, patch or blocked import. Stored endpoint deltas remain +79/-26
paths and +129/-49 ops versus the older stored spec, not this source-to-source delta.

Fresh full source-change review script/log/records
`/tmp/review-52-audit-source-changes.py`,
`/tmp/zendesk-52-source-changes-review.log`,
`/tmp/zendesk-52-blocked-source-changes.json`. Raw reviewed sources/full parsed
changes/diagnostics retained under ignored `cache/maintenance/discovery/vercel-rest`
and `cache/maintenance/discovery/cloudflare-rest` at their respective hash/revision.

**Resume next:** 53 registered sources, Atlas billing-enum drift delivered, new
Zendesk Conversations recipe/monitoring and delivery guard delivered, Support
monitoring delivered. First inspect fresh state/PRs and recorded work; do not
repeat those imports. Zendesk Conversations validated local commit/owner-review
link and one pending user question remain above; no owner response yet. Do not
retry push/unblock/redact or treat a preselected option as authorization. Existing
separate Twilio Messaging choice remains pending too. Full 53-source check is still
needed on a later run (Support selected check already verified), preserving this
52-source snapshot and independent Atlas closure. Investigate a separately reviewed
Support exact null-only compatibility recipe and unused UserLogin defect with
complete constraints/reference/serialization guards and vendor-fix refusal; neither
diagnostic is adopted yet. Adobe Sign remains another unregistered invalid source.
Continue independent well-known official-source discovery and updater PR-generation/
monthly-discovery infrastructure. All parked items, independent open #179, local
sleep rules and week deadline unchanged; no vendor messages, new automation, cloud
host migration or power changes. To attach this superseding progress PR at the app
limit, verified merged AGENTS-only #189 was unlinked; GitHub history and API/updater
attachments preserved.

### 2026-10-05 19:25 UTC heartbeat — Support compatibility and unused-reference guards

Resumed clean main `cfb19aa445a5b9001f682af27a57c12dab03aaba` (#194), fetched
unchanged main, sparse coverage and independent open #179 verified. Conversations
and Twilio Messaging owner choices remain unanswered; neither rejected push retried.
Current hosted Support re-fetch retains hash
`3258ec97eed69d58deceee500efe090ea0e0b16fd616dddf15107ab209688fdc`, native
3.0.3 / fixed 2.0.0 / 455 paths / 657 operations / 2,534 resolved local refs.
A complete key/string scan finds `UserLogin` only at its component definition;
no pointer, prose, extension or implicit-name occurrences elsewhere. Diagnostic
null-only correction plus removal of that exact unused component makes the full
native document valid; no further defects are waived. Cached original unchanged.

**Separate updater implementation:** optional recipe `unreferenced` preconditions
verify existing pointer targets and conservatively scan every string/key, including
examples, extensions and mappings, for direct, descendant or enclosing JSON Pointer
uses. Percent-encoded fragments, escaped tokens, arrays, URI-prefixed fragments and
root pointers are covered. Missing, malformed or duplicate targets fail closed;
new uses block before any operation in that recipe. Named anchors/prose are not
pointer references, so independent vendor name-resolution review remains required.
No caller object or original cache is changed on failure; no success stamp fabricated.

`maintenance/patches/zendesk-support.json` asserts the complete original
AccessRuleCondition and UserLogin nodes. It preserves the documented null-only
alternative with explicit string type, nullable:true and enum:[null]; all four other
alternatives and original oneOf exclusivity remain, including integer/number overlap.
It removes only the asserted unused invalid in:path/style:deepObject component after
the absence guard. No query relocation, auth scheme, runtime values or alternate
operator enum is invented. Source monitoring now replays this exact recipe;
API import will be a separate PR after infrastructure CI and merge.
Recipe SHA-256 `38d1641799c8a082fdb21f71f500b400e1bd9f752b5e6024e60eaa0dff2b47e5`.
**106 local regression tests pass** (six new tests covering semantic positive/negative
witnesses, new uses/vendor fixes, escaped/encoded pointer equivalence, conservative
extension/example/enclosing references, malformed guards and cached failure).
Fresh source full validation and typed YAML roundtrip pass after the two corrections.

Official Ticketing introduction links this exact hosted download; it covers Support
and included custom data, not Conversations/all Zendesk. Native tenant variable
server is retained. Current [authentication reference](https://developer.zendesk.com/api-reference/introduction/security-and-auth/)
recommends OAuth and deprecates API tokens; the artifact itself models only basicAuth.
Preserve that publication limitation, all native auth/deprecation/role/plan prose,
and end-user password restrictions rather than fabricate a complete auth model.
The [OAS 3.0.3 parameter rules](https://spec.openapis.org/oas/v3.0.3.html#parameter-object)
restrict deepObject style to query; [nullable rules](https://spec.openapis.org/oas/v3.0.3.html#schema-object)
allow this null-only representation while retaining enum constraints.
Review/script `/tmp/review-support-unused-parameter.py`,
`/tmp/zendesk-support-unused-parameter-review.json`; new regression log
`/tmp/zendesk-support-guards-tests.log`. Earlier diagnostic-only records remain
historical; this entry supersedes them once the infrastructure is merged.
At the attachment cap, verified merged AGENTS-only #60 unlinked to make
room; GitHub history and all API/updater attachments retained.

### 2026-10-06 Confluence v1 source review and monitoring preparation

Fresh official v1 download and its currently linked `_v=1.8516.128` query are byte-identical
at 07:46 UTC: SHA-256 `6c66a606fa7535268512f07f599fe1e3f9de2ba0b1da7eb6ead405509875577e`.
Native 3.0.1 / document 1.0.0 / 89 paths / 130 operations / 511 resolved local refs;
none external. The earlier note calling the first invalid parameter `prefix` was wrong:
GET `/wiki/rest/api/label` parameter 0 is **required `name`**. Complete native error
enumeration (not only the first diagnostic) identifies three invalid null defaults:
that name, optional label `type`, and optional group `accessType`. Removing exactly
these defaults produces zero full/native validation errors; requiredness, types,
enums and all remaining vendor content are unchanged.

Separate registration `confluence-v1` targets
`APIs/atlassian.com/confluence-v1/1.0.0/openapi.yaml`; neither Jira nor v2 is a curation
baseline. The complete checked recipe asserts three whole parameters and two operation
IDs, refuses vendor fixes/nullable changes/contract changes, and chooses no replacement
default or runtime omission behavior. Two meaningful regressions cover accepted/rejected
instances and all three parameter guards. **112 local tests pass**. Preflight import
passes full validation, all references, typed YAML roundtrip and complete vendor
comparison except the three defaults and provenance. No conversion or bundling.

Current official v1 intro, label/group and descendants reference pages are retained.
This is a mixed-lifecycle public collection: seven experimental flags and two deprecated
descendant operations retained. Current references still label the descendants deprecated;
historical retirement announcements make runtime availability uncertain. Do not claim
all v1 endpoints are GA/operational, resurrect retired paths, or concatenate v2. Hosted
source health remains not_assessed. Native protocol-relative tenant server/auth/permission/
app-access content stays unchanged. Selected audit against main `62adb98e65b0` reports
valid missing coverage, not a full new 56-artifact network audit.

Original bytes/HTTP metadata, docs, diagnostic review, preflight YAML/review and selected
JSON/Markdown audit are under ignored `cache/maintenance/discovery/confluence/v1-current/`.
Scratch verifier `/tmp/verify-confluence-v1-preparation.py`, logs
`/tmp/confluence-v1-preparation.log`, `/tmp/confluence-v1-tests.log`; restored pinned
Python 3.12 environment `/tmp/openapi-maintenance-py312/` (old scratch venv disappeared).
Deliver monitoring/recipe infrastructure separately, require its actual CI before API
merge, and record created PR identities below; no API has been committed yet.
