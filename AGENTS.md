# AGENTS.md — working on this OpenAPI directory fork

Instructions for an agent picking up work in this repo. Read this first.

**Repo**: `ontola/openapi-directory` (fork of `APIs-guru/openapi-directory`).
Note the git remote resolves via an old org rename — `localthought/openapi-directory` redirects to `ontola`. Pushes print a "This repository moved" notice; harmless.

**Last updated**: 2026-09-22. `main` at PR #59 merged; no open PRs; 725 provider domains tracked.

---

## 1. The standing task

Work through the upstream `APIs-guru/openapi-directory` backlog (PRs and issues) and port anything worth having into our fork.

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
   `info.version` and path counts.

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
Check `git sparse-checkout list` first, and audit against the git index:

```bash
git ls-files APIs | cut -d/ -f2 | sort -u > /tmp/have_domains.txt
for v in stripe square figma sentry pagerduty docusign mongodb grafana shopify okta \
         intercom hubspot salesforce zendesk notion airtable heroku snowflake elastic \
         hashicorp coinbase dropbox newrelic anthropic huggingface nvidia; do
  printf "%-14s " "$v"; m=$(grep -i "$v" /tmp/have_domains.txt | tr '\n' ' ')
  [ -n "$m" ] && echo "HAVE: $m" || echo "missing"
done
```

717 distinct provider domains, 4179 tracked files under `APIs/`.
To add a new spec you must first widen the cone: `git sparse-checkout add APIs/<domain>`,
otherwise `git add` refuses with "paths ... outside of your sparse-checkout definition".

### Verified live official specs (HTTP 200 confirmed 2026-09-22)

| Vendor | Source | Status |
|---|---|---|
| **Stripe** | `.../stripe/openapi/master/openapi/spec3.yaml` | **DONE, PR #44.** Use the **`.yaml`**, not the `.json` — the `.yaml` is what the existing spec's `x-origin` already cites, so no conversion is needed. |
| Figma | `.../figma/rest-api-spec/main/openapi/openapi.yaml` | **DONE, PR #45.** OpenAPI 3.1.0, already YAML. |
| Sentry | `.../getsentry/sentry-api-schema/main/openapi-derefed.json` | **DONE, PR #46.** Deref'd artifact: no `$ref`s, no `components.schemas`, everything inlined. That is upstream's doing, not a conversion fault. |
| PagerDuty | `.../PagerDuty/api-schema/main/reference/REST/openapiv3.json` | **DONE, PR #47.** |
| MongoDB Atlas | `.../mongodb/openapi/main/openapi/v2.json` | **DONE, PR #48**, as `mongodb.com/atlas-admin/2.0`. |
| Grafana | `.../grafana/grafana/main/public/api-merged.json` | **DONE, PR #50.** Swagger 2.0; converts cleanly (0 warnings). Version dir is `0.0.1` because that is literally Grafana's declared `info.version` — a placeholder they never bump. See the push-protection note below. |
| Square | `.../square/connect-api-specification/master/api.json` | **DONE, PR #51** — a *refresh*, we already had `squareup.com/2.0`. |
| DocuSign | `.../docusign/OpenAPI-Specifications/master/esignature.rest.swagger-v2.1.json` | **DONE, PR #52** — a *refresh*, we already had `docusign.net/v2.1`. Swagger 2.0. |
| Intercom | `.../intercom/Intercom-OpenAPI/main/descriptions/2.14/api.intercom.io.yaml` | **DONE, PR #54.** See the 404 warning further down before writing this vendor off again. |

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

- **Refresh audit across the rest of `APIs/`.** 725 provider domains; only a dozen or so have
  been checked. This has been the **higher-yield half of the work by a wide margin** — Stripe
  was ~4 years stale and Square was 94 paths behind, while the entire upstream issue backlog
  yielded almost nothing (§3). Walk `APIs/` against vendor sources comparing `info.version`
  and path counts.
- **Locate specs for the vendors below**, minding the 404 warning.
- **Decide whether to take HubSpot's 34 per-object CRM slices.** Currently skipped by
  deliberate choice, not oversight.

### Missing, official spec not yet located

Shopify, Zendesk, Airtable, Heroku, Snowflake, HashiCorp, Coinbase, Dropbox, New Relic,
Anthropic, Hugging Face, NVIDIA.

**Probed and 404'd on 2026-09-22** — these exact URLs, not the vendors themselves:
`snowflakedb/snowflake-rest-api-specs` (`main`, `releases/8.40/...`),
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

- **Everything is `.yaml`.** 1982 `openapi.yaml` files, 0 `openapi.json`. Convert JSON sources with Python before committing:
  ```python
  yaml.dump(d, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=100000)
  ```
- **Layout**: `APIs/<domain>/<version>/openapi.yaml`, or `APIs/<domain>/<service>/<version>/openapi.yaml` for multi-service providers. Version dir = `info.version`.
- **Version bumps are new directories**, never in-place edits. Both #41 and #42 are `+N / −0`.
- **Preserve apis.guru curation metadata on any refresh.** A wholesale file replacement silently drops `x-apisguru-categories`, `x-logo`, `x-preferred`, `x-permalink`, `x-providerName`, `x-serviceName`, `x-hasEquivalentPaths`, `contact.x-twitter`, top-level `externalDocs` and `tags`. Merge new spec content *into* the old `info` block. This is the single most important rule for updates — it's what #40 got wrong.
- **`x-origin` records provenance.** Match existing style; for converted specs list the chain, e.g. API Blueprint → swagger → openapi (see `APIs/icons8.com`, `APIs/ritekit.com`, and `APIs/eventbrite.com/3`).
- **New additions go in essentially as-is.** Checked against the recently merged ones (Picsart, Nylas, Eventbrite): they carry **no** `x-apisguru-categories`, `x-logo` or `x-providerName`. Those values are apis.guru curation, and inventing them would be fabricating metadata. Add `x-origin` for provenance and otherwise leave the vendor spec alone. The preserve-metadata rule above applies to **refreshes of specs we already have**, where that curation exists and must survive.
- **Match the sibling file's YAML style.** PyYAML's default dumper writes sequences flush against the parent key; this repo indents them. Subclass the dumper:
  ```python
  class Dumper(yaml.Dumper):
      def increase_indent(self, flow=False, indentless=False):
          return super().increase_indent(flow, False)
  ```
- **CONTRIBUTING.md** says the canonical route is a web form feeding apis.guru's own curation pipeline, and discourages direct PRs amending spec files. We add vendor specs largely as-is anyway, matching already-merged manual additions.

### Conversion toolchain
Installed under the session scratchpad (`apibconv/`), re-installable anywhere:
- `swagger2openapi` (7.0.8) — Swagger 2.0 → OpenAPI 3. Use `{patch:true, warnOnly:true}`. Reliable.
- `apib2swagger` (1.17.1) — API Blueprint → Swagger 2.0. **Its `--open-api-3` path is broken on modern Node** (`json-schema-to-openapi-schema@0.4.0` throws `Type "null" is not a valid type`, with a misleading stack because of a broken error prototype). Workaround: convert to Swagger 2.0, then hand to `swagger2openapi`. That's how Eventbrite was done.
- `google-discovery-to-swagger` — Discovery → Swagger 2.0, then `swagger2openapi`.

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
