# OpenAPI directory handover to Claude — 2026-10-08

The user asked Codex to wrap up and hand this maintenance work to Claude. **Codex has
stopped**, and its existing hourly automation
`maintain-openapi-directory-for-one-week` is **PAUSED** (saved state verified).
Do not restart it from historical heartbeat/deadline instructions. No extra automation,
power-setting change or execution-host move was made.

Read this first, then [AGENTS.md](AGENTS.md) for the standing conventions, full delivery
ledger and detailed source reviews. The newest dated entries supersede older
"prepared", "pending" and one-week-deadline notes; verify actual GitHub state before
acting. [maintenance/README.md](maintenance/README.md) documents the tools and recipes.

## Repository and verified state

- Repository: **ontola/openapi-directory**, a fork of APIs-guru. The old
  `localthought/openapi-directory` origin redirects; the moved-repository push notice
  is harmless.
- Maintenance checkout: `/Users/michieldejong/.codex/worktrees/6edc/openapi-directory`.
  The primary checkout is `/Users/michieldejong/gh/ontola/openapi-directory`; it and
  other worktrees belong to other sessions. This handover is delivered through main;
  fetch it in the checkout Claude will use rather than overwriting another session.
- Main immediately before this documentation: **`b4c28a81c3fe14b67b8c9c3764b09ae28b2f2ad9`**,
  the confirmed merge of [#234](https://github.com/ontola/openapi-directory/pull/234).
- Only unrelated [#179](https://github.com/ontola/openapi-directory/pull/179),
  "Make the bunq, codat and sendgrid API descriptions parse as YAML", remained open
  after #234. Its head was `38ad4f98167c2fb9def09097abef83fc18d7a6e4`. Preserve it.
- Full fetched-tree inventory: **733 provider domains / 4,294 API files**, including
  **2,120 openapi.yaml / 2,168 swagger.yaml**. Monitoring covers **65 artifacts / 64
  services**, not the whole directory. Recompute these dated observations when resuming.
- The checkout is sparse. Missing files/directories on disk do not establish missing
  APIs. Use `git ls-tree -r origin/main`, including service names and historical versions.

## Completed work; do not repeat

The original priorities are delivered: Plaid #63, Xero Accounting #67, DigitalOcean
#70, and multiple GitHub REST refreshes; official Hugging Face Endpoints #62, Snowflake
SQL/Warehouse #71/#72, Cohere #76 and Mistral #77 are imported. Cohere now has a known
native-source validation block despite its earlier import. Snowflake coverage has grown
to **12 separate descriptions** (116 paths / 148 operations), and all **five individually
reviewed HCP services** linked by the overview are delivered (115 / 156). These are
service scopes, not whole-platform coverage. Other additions/refreshes, including
Confluence, Coinbase CDP, Zendesk Support, Box and ClickUp, are in the AGENTS ledger.

Recent completed infrastructure/API deliveries:

| Delivery | Confirmed result |
| --- | --- |
| [#216](https://github.com/ontola/openapi-directory/pull/216) | Create-only guarded draft generator and exact generated-head read-only CI. |
| [#218–#219](https://github.com/ontola/openapi-directory/pull/219) | Snowflake Compute Pool registration and separate API-only addition. |
| [#221–#222](https://github.com/ontola/openapi-directory/pull/222), [#224–#228](https://github.com/ontola/openapi-directory/pull/228) | Original hosted HCP Swagger extraction/conversion recipes and five separate API-only additions; no SDK reconstruction. |
| [#231](https://github.com/ontola/openapi-directory/pull/231) | Read-only pending-draft reviewer; 188 local and actual CI tests. |
| [#232](https://github.com/ontola/openapi-directory/pull/232) | GitHub fixed-version companion refresh; merge `3f6cbeebce0b3281a7779a9368e3d710cb46ea38`. Actual generated-head CI passed; read-only reviewer also exercised on the real still-draft PR before merge. |
| [#234](https://github.com/ontola/openapi-directory/pull/234) | Explicit guarded pending-head updater; **206 local and actual CI tests**, including 18 new real-Git cases. Head `648db85cef1bea5d4b3888b0973ac5e4ab483d9e`, merge `b4c28a81c3fe14b67b8c9c3764b09ae28b2f2ad9`. |

Another session delivered Airtable read-only Web API in #230. It was preserved;
do not duplicate it or attribute it to this maintenance run.

The last fresh checks fetched **only three artifacts at 11:08 UTC on October 8**:
both GitHub public REST companions match pinned vendor
`2eba8c3ba02f022011539cf01efc43e0251502f8` (native 3.0.3 / vendor 1.1.4 /
816 paths / 1,232 operations each); HF Endpoints matches native 3.1.0 / vendor 2.0.0 /
40 paths / 46 operations. Full raw/health hashes, native/stored validation, independent
vendor-plus-curation equality, typed YAML and 20,872 OpenAPI reference objects pass.
HF hosted repository health remains `not_assessed`; no Git revision is invented.
These are selected observations, **not a full 65-artifact or post-merge network audit**.
No production draft was created/updated by #234's writer; the selected PRs were absent.
Its write path is exercised by real local Git repositories and mocked read-only GitHub
responses. Actual new-production-head CI and its new Actions summary await a genuine
eligible update; no synthetic GitHub test PR was manufactured.

## Tooling available

- `maintenance/update.py`: reproducible source check/import, preservation of curation,
  pinned bundling/conversion/snippets, checked patch replay, full native validation,
  typed YAML, JSON/Markdown reports and exact provenance.
- `maintenance/sources.json`: current reviewed source recipes, targets, coverage and
  explicit publication groups. A version/count match alone does not establish freshness.
- `maintenance/discovery.py` and `discovery.json`: bounded official-source discovery.
- `maintenance/draft_pr.py`: default dry run; explicit `--publish` creates one new draft
  API/group. Existing PRs **and branches** are held. It uses a private index, preserves
  historical versions/local staging, and retains publication guards and receipts.
- `maintenance/pending_pr.py`: fresh read-only comparison with a generated pending
  draft, requiring successful original creation/update receipts and complete Git trees.
  It never authorizes publication or changes a PR.
- `maintenance/refresh_pr.py`: default read-only review; explicit `--publish` updates
  only an untouched protocol-2 draft at the same original/current/advertised base and
  fixed vendor version. It holds removals, auth/server/callback changes, reviewed/manual
  work, legacy bodies, missing evidence and any main advance. Exact previous-head Git
  leases protect concurrent commits. PR title/body remain an initial submission snapshot;
  current provenance/stats/deltas appear in exact-head CI JSON and summary.
- Weekly maintenance and monthly discovery repository workflows remain `contents: read`.
  The Codex hourly chat automation is separately paused. **Scheduled publication and
  automatic merging are not enabled.**

The updater saves immutable success history back to original creation. Rejected or
uncertain publication retains `blocked.json`; interruptions retain `publishing.lock`.
If post-push success/failure receipts cannot be saved, the lock remains. PR metadata and
Git refs cannot be checked atomically: a racing body/ready/review change is caught after
push and held for deliberate outcome review. Human edits are never undone blindly.
Do not delete guards, retry rejected pushes, manufacture receipts or restore old heads.

## Claude VPS run — 2026-10-08 (newest; supersedes counts above)

- Baseline at `528504bfe813`: 206 tests pass; full 65-artifact audit = 42 matches / 13 valid
  drifts / 11 recorded blocks / 0 fetch failures. Inventory 733 / 4,298 / 2,121 / 2,168.
- Infrastructure merged: #237 (register 8 Xero In Release services + YNAB, 74 artifacts),
  #238 (design: merged generated branches), #239 (design: scheduled publication). Designs
  only; nothing enabled, no permission changes.
- API merged (exact-head validation + tests passed, CLEAN, matching-head merge): YNAB 1.87.0
  #240; Xero 19.1.0 Assets #241, Bank Feeds #242, Files #243, Identity #244, Payroll AU #245,
  Projects #246, Payroll UK #247, Payroll NZ #248.
- **Open, verified, awaiting a human merge** (the auto-mode classifier refused further
  merges as "Merge Without Review"; per §7 they are left open): #249 Asana, #250
  DigitalOcean, #251 Figma 0.44.0, #252 Atlas, #253 Sentry, #254 Intercom, #255 Datadog v2,
  #256 Discord, #257 Grafana, #258 Zendesk Support, #259 Coinbase CDP, #260 Twilio Verify,
  #261 Twilio REST. All drafts on base `cda412cc`, actual exact-head validation passed, zero
  endpoint removals, one API file each (Figma also advances its manifest target).
- Generated drafts use the tool-required `codex/official-update-*` prefix; VPS creation
  receipts live under `cache/maintenance/claude-drafts/` on the VPS (never delete).
- Twilio Messaging / Zendesk Conversations (Q-102), the eleven blocks and §5 parked scope
  were not touched.

## Claude VPS run, round 2 — 2026-10-08 (newest)

- **Merged infrastructure:** #264 (generation-suffixed drafts after verified merged
  branches, the #238 design); #265 (scheduled-publication groundwork: shared eligibility,
  append-only `maintenance-state` store library, read-only plan / explicit operator
  publish runner, read-only `workflow_dispatch` validation; no schedule, no write
  permissions, store branch not created); #267 (Moneybird source with the new
  `stable_directory` version policy and an exact invalid-default recipe). Suite: 226 tests.
- **Merged API:** #268 Moneybird v2 in place (+3 ops); first real `--g2` generations
  #269 Sentry, #270 Datadog v2 (+8 ops), #271 Asana. All 29 earlier generated branches
  verify as merged outcomes, so their APIs can be republished as `--g2`.
- **Open proposal:** #266, a path-aware `PR gate / gate` check that can be required
  without blocking docs-only PRs. Not merged and not required; owner decision.
- **Held:**
  - Q-102 redaction (Twilio Messaging, Zendesk Conversations). The auto-mode classifier
    refused generating the redaction recipes ("Security Weaken"). The authorization
    reached Claude only through the coordinator. Not attempted again, nothing pushed;
    needs Michiel's direct confirmation or a permission rule.
  - Microsoft Graph v1.0 (official msgraph-metadata, 3.0.4, 11,558 paths / 17,885 ops,
    validates). It would copy curation `x-preferred: true` into a second Graph version,
    which touches the parked `x-preferred` policy; about 45 MB. Evidence:
    VPS `cache/maintenance/discovery/claude-msgraph/`.
  - `APIs/moneybird.com/v2-readonly` (another session's generated subset) should be
    regenerated by its owner after #268.

## Claude VPS run, round 3 — 2026-10-08 (newest)

- **Coordinator additions:**
  - #273 regenerated `moneybird.com/v2-readonly` from refreshed v2. The new
    `contacts/doubles` is classified a lookup helper (generator rule plus test), so there is
    no duplicate collection; the two new report endpoints are classified as reports.
  - #179 (another session's bunq/codat/sendgrid parse fixes) was reviewed, given §5b
    `x-conversion` provenance, verified with serde_yaml 0.9.34 (main fails, PR passes) and
    merged. None of these is monitored, so no recipe is needed.
- **Discovery, registered (#278) and delivered:** Klaviyo stable 2026-07-15 (#282, new
  provider), OpenAI 2.3.0 in place (#284), Jira Cloud platform v3 in place with
  `stable_directory` (#285). Each has an exact invalid-default recipe. Reported removals
  are source omissions: OpenAI eval-run cancel moved to `/cancel`; Jira legacy workflow
  APIs were superseded.
- **Drift delivered:** HF Endpoints #274, Atlas #275, Sentry #276, Intercom #277,
  Datadog v2 #280, Moneybird #281 (later found to be example-only churn, so #286 adds an
  opt-in `volatile_examples` for Moneybird only), DigitalOcean #283 after #279 accepted
  its reviewed 22nd bundler naming warning.
- **Held:** Coinbase CDP drops `GET /v2/coinbase-accounts/balances` without public
  evidence found, so it is not delivered. The eleven blocks are re-validated and still
  blocked (AGENTS). Q-102, Q-110, Q-111 and Q-112 await owner answers.
- **Next leads:** Netlify 2.60.0 and Bitbucket (Swagger 2.0, need conversion review);
  Twilio services still at 1.55.0 (run the SID pre-scan first).

## Claude VPS run, round 4 — 2026-10-09 (newest)

- **Infrastructure:** #288 (Netlify registered with three guarded `x-nullable` translations;
  the nullable location guard now counts only `true`; Bitbucket registered for monitoring
  with an explicit `import_blocker`), #290 (13 current Twilio services), #293 (Resend,
  Pipedrive v1 and v2, Render).
- **API delivered (generated, exact-head validation passed):** Netlify 2.60.0 #289 (+61 ops);
  Twilio 1.0.0 Conversations #291, Voice #292, Video #294, Lookup v2 #295, Studio v2 #296,
  Serverless #297, TaskRouter #298, Sync #299, Trunking #300, Intelligence v2 #301,
  Event Streams #302, Trust Hub #303, Flex #304 (no push-protection rejections; 1.55.0
  history retained); new providers Resend #305, Pipedrive v1 #306, Pipedrive v2 #307,
  Render #308; drift Sentry #309 (`--g4`), OpenAI #310 (`--g2`).
- **Held:**
  - Bitbucket refresh: 5 cross-workspace route removals lack vendor evidence.
  - Twilio Numbers v2, Content v1 and Insights v1: they add realistic Account-SID
    examples (push-protection class, Q-102).
  - Coinbase `coinbase-accounts/balances` removal: still no public notice (rechecked).
  - Adyen Checkout v72 / Legal Entity v4: `x-preferred` curation (Q-111 class); the
    stored v71 also fails the YAML 1.2 loader.
  - Mollie and Supabase: native defects.
- Drift re-check at 00:32 UTC across 85 unblocked sources: 82 matched, 3 changed.

## Claude VPS run, round 5 — 2026-10-09 (newest)

- **Mollie:** registered (#312) with an exact recipe removing only 35 sibling `schema`s from
  parameter Reference Objects (OpenAPI 3.1: SHALL be ignored); delivered #313 (new provider).
- **Supabase Management:** not registered. Three `propertyNames` constraints have no
  OpenAPI 3.0 equivalent, so no constraint-preserving recipe exists; no dialect upgrade.
- **Bitbucket:** hold lifted (#314) after tracing all 28 removed paths / 47 operations to
  vendor announcements (Issue Tracker and addon linkers in the changelog; the cross-workspace
  API end of life, CHANGE-2770; the `/pullrequests/{selected_user}` staff notice). The
  path-surviving `GET /snippets` removal belongs to the same cross-workspace class. Delivered #315.
- **PayPal:** the six natively valid stored artifacts are now monitored (#316); the Orders
  2.32 content refresh is delivered (#317). Seven invalid PayPal artifacts are recorded, not
  registered.
- **CircleCI v2:** registered (#316) and delivered (#318), missing beside v1 until now.
- **Still held:** Coinbase balances removal (rechecked 00:58, no notice). Trello's official
  spec (enum-default defect, path layout change) is a lead.
- Drift: last full re-check 00:32 UTC; next due in a few hours.

## Recommended next work

1. **Deliberate handling of already merged generated branches**, in separate infrastructure.
   The original GitHub generated branch/receipt from #232 remains. Current create-only
   publication correctly holds such branches, and the refresh command only handles open
   untouched drafts. Design future branch naming/reuse around verified closed/merged
   outcomes and retained evidence; do not delete a branch merely to force publication.
2. **Scheduled publication**, separately from read-only audits and explicit updating.
   Keep per-API review, durable cross-run locks/receipts, source/native validation,
   genuine exact-head CI, and publication protection. GitHub Actions token-trigger
   behavior and the retained local evidence need a reviewed design before enabling writes.
   Do not broaden permissions or add blanket auto-merge to make it work.
3. **Broader freshness and official-source discovery** for well-known industry APIs.
   Prioritize useful gaps/real content drift over niche additions or repeating delivered
   HCP/Snowflake work. Registered hosted sources need separate health/coverage assessment;
   repository availability alone is not proof of vendor lifecycle or complete coverage.
4. Exercise the new writer on a **genuine eligible draft** when vendor content changes,
   retain its success evidence, and verify actual updated-head CI before ready/merge.
   Main advances and legacy/manual drafts require deliberate reconciliation, not rebasing
   or changing descriptions automatically.

The task has a substantial continuing backlog; it does not need new niche API tasks.
Do not resume Codex's paused automation while Claude is working.

## Eleven existing blocks and parked scope

These are recorded blocks, not fresh October 8 observations. Exact source snapshots,
locations and semantic reviews are in AGENTS and retained reports. Preserve stored APIs.

| Source | Recorded blocker |
| --- | --- |
| Cohere | `TruncationStrategy.oneOf: []`, invalid empty union. Do not invent variants. |
| Square | Undefined CurrencyExchange/AppFeeAllocation plus invalid metadata. |
| Slack Web | Archived Swagger repository; current coverage uncertain, no registered conversion. |
| Meraki | Undefined `oauth2` security scheme in operation requirements. |
| Vercel | Declares 3.0.3 but uses unsupported schema keywords/other native defects. |
| Mailchimp Marketing | Native boolean default where the schema requires a string. |
| Auth0 Management | Native default conflicts with its pattern constraint. |
| Cloudflare REST | Native enum/default and security-name defects; preserve latest exact review. |
| Okta Management | Invalid path parameter declaration; review current vendor variants separately. |
| Twilio Messaging | Valid prepared refresh held by push protection on a vendor Account SID example. |
| Zendesk Conversations | Valid prepared 17.13.2 addition held by the same vendor example protection. |

The last two need a repository-owner decision: allowlisting/review or explicit
authorization for an exact documented redaction. There is **no answer yet**. Local
branches `codex/refresh-twilio-messaging` and `codex/add-zendesk-conversations` are retained.
Do not retry, unblock or redact on your own; do not bypass approval-review rejection.

Explicitly parked: Google regeneration (including Vertex/DisplayVideo), Linode
discriminator work, Greenpeace removal, `x-preferred` policy, php-openapi README,
HubSpot's 34 per-object CRM slices/residual native-defect work, and fully deprecated
standalone Snowflake Grant. Fresh user authorization is needed to change parked scope.
Do not contact vendors, open upstream issues or send messages without authorization.

## Reproducing work locally

Use Python 3.11+ (CI: 3.11), Node 24+ and the locked dependencies. The existing clean
local environment is `/tmp/openapi-maintenance-py312/bin/python` (Python 3.12);
`maintenance/node_modules` is installed. `/tmp` helpers/environments are disposable;
recreate from `requirements.txt` and `package-lock.json` when needed. `gh` is already
configured on this laptop. Supply `GITHUB_TOKEN` privately if needed for authenticated
source fetches; never store or print credentials.

```sh
git status --short
git fetch origin main
git sparse-checkout list
git ls-tree -r --name-only origin/main APIs
gh api --method GET 'repos/ontola/openapi-directory/pulls?state=open&per_page=100'

# From an appropriate clean checkout, install if needed and run the maintenance suite:
python -m pip install -r maintenance/requirements.txt
npm ci --prefix maintenance --ignore-scripts --no-audit --no-fund
python -m unittest discover -s maintenance -v

# Example selected read-only audit; retain a new report/cache per run:
python maintenance/update.py check --source digitalocean --source plaid \
  --source xero-accounting --base origin/main \
  --cache cache/maintenance/reports/claude-selected/sources \
  --report cache/maintenance/reports/claude-selected/report.json

# One API/group dry run (selecting github-rest also includes the dated companion):
python maintenance/draft_pr.py --source github-rest --base origin/main \
  --cache cache/maintenance/claude-drafts

# Read-only review of a real pending draft from its ORIGINAL creation-cache root:
python maintenance/refresh_pr.py --source github-rest --base origin/main \
  --prior-cache cache/maintenance/drafts \
  --cache cache/maintenance/reports/claude-pending-review
```

Source/reviewer/generator code must match the committed comparison tree. Do not run
publication from uncommitted infrastructure or work around that guard. Use a new
`codex/` branch from fetched main after checking status; preserve other sessions'
changes. Do not use shared bare stashes or destructive resets to get a clean checkout.
For manual sparse API changes, widen the cone before staging. New versions use new
directories; fixed vendor versions can refresh in place. Preserve existing curation,
YAML types/layout, native constraints and `info.x-origin`/`info.x-conversion`.

Separate infrastructure delivery from API-only PRs; one PR per API/explicit group.
Verify actual CI execution, exact head/base/full file list, ready state and
CLEAN/MERGEABLE before matching-head merge. Never substitute a queued/skipped job for
actual validation. Intermittent `gh` GraphQL 502s can use read-only REST fallback;
unknown publication outcomes require inspection, not automatic retries.

## Evidence that is local, not in Git

**Do not archive/delete this worktree or its ignored cache during transfer.** A new
checkout does not contain the evidence below. Preserve/copy it deliberately if moving
machines; missing successful creation receipts/Git objects cause correct holds.

- `cache/maintenance/reports/guarded-pending-draft-updates/`: #234 candidates, local
  tests, exact actual CI run `37768566573` / job `113282140755`, PR/merge receipts,
  independent live/refs verifiers, selected raw/health snapshots and automation-pause receipt.
- `cache/maintenance/reports/pending-api-refresh-review/`: #231/#232 original source
  diffs, full import/ref checks, actual CI receipts and the real read-only draft observation.
- `cache/maintenance/drafts/`: **original successful generated-draft receipts**, including
  #232. Keep this as the original cache for its PR; do not point a reviewer at an empty
  new cache or overwrite it with fresh sources. Future creations must retain their own
  actual original cache root.
- `cache/maintenance/discovery/`: prior vendor/publication/native/conversion/control
  evidence (HCP, Snowflake, Coinbase, Confluence and other reviews). AGENTS names the
  specific per-delivery paths. Some historical `/tmp` helpers may disappear.
- Generic `cache/maintenance/report.json` is a **52-artifact October 5 audit**, base
  `9a4d00029f41fd78b4a76bb4953403663ba69005`; it is not a current 65-artifact audit.
  Prefer explicitly dated per-run reports and distinguish cached reconciliation from
  new network observations.

The Codex app hit its 100-attachment cap. Required PR attachment attempts failed for
recent deliveries, including #234. Actual GitHub PRs/merges are intact; do not claim app
linkage or remove history to make room. This limitation does not block repo work.
