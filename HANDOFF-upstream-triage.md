# Handoff: upstream triage & port workflow

**Repo**: `ontola/openapi-directory` (fork of `APIs-guru/openapi-directory`).
Note the git remote resolves via an old org rename — `localthought/openapi-directory` redirects to `ontola`. Pushes print a "This repository moved" notice; harmless.

**Last updated**: 2026-09-22. Main branch at PR #43 merged; PRs #44-#48 open and awaiting merge.

---

## 1. The standing task

Work through the upstream `APIs-guru/openapi-directory` backlog (PRs and issues) and port anything worth having into our fork.

**Filter criterion the user set, which governs everything:**
> "you can skip additions of niche APIs, I'm more interested in additions or corrections of well-known industry APIs."

**Delivery pattern:** one PR per API, against our own `main`, upstream issue/PR link in the **PR body, not the title**. Merge when clean.

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

**#44–#48 are open, verified clean, but NOT merged** — merging was blocked by the
Claude Code auto-mode classifier ("Merge Without Review"), a harness restriction, not a
change of mind by the user. Each is one file, `+N / −0`, `MERGEABLE`/`CLEAN`:

| PR | API | Paths / ops | Note |
|---|---|---|---|
| #44 | Stripe `2026-08-26.dahlia` | 419 / 594 | refresh; curated metadata preserved |
| #45 | Figma `0.42.0` | 47 / 54 | new; source already YAML |
| #46 | Sentry `v0` | 147 / 234 | new; upstream artifact is deref'd, so no `$ref`s at all |
| #47 | PagerDuty `2.0.0` | 273 / 465 | new |
| #48 | MongoDB Atlas Admin `2.0` | 333 / 541 | new; filed under `mongodb.com/atlas-admin/` |

**Grafana is converted and committed locally on `add-grafana-api` but could not be
pushed** — see §4.

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
| Grafana | `.../grafana/grafana/main/public/api-merged.json` | **BLOCKED — see below.** Confirmed **Swagger 2.0**; converts cleanly (0 warnings). |
| ~~Square~~ | — | **NOT new — we already have `squareup.com/2.0`.** Refresh only; compare versions before doing anything. |
| ~~DocuSign~~ | — | **NOT new — we already have `docusign.net/v2.1`.** Refresh only. |

#### Grafana: blocked by GitHub push protection

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

It was left unresolved on purpose. Two ways forward, both the user's call:
1. **Allow it** via the unblock URL in the push error (repo owner only) — keeps the vendor spec byte-for-byte as published.
2. **Redact the example** — but that means editing vendor content, which cuts against how every other spec here was added.

Do not bypass push protection unilaterally.

### Missing, official spec not yet located
Shopify, Intercom, HubSpot, Zendesk, Airtable, Heroku, Snowflake, Elastic, HashiCorp, Coinbase, Dropbox, New Relic, Anthropic, Hugging Face, NVIDIA.

Corrections to this list from the index audit:
- **Notion** — we already have `notion.com/1.0.0` **and** `notion.com/2026-03-11`. Current; drop it from the list.
- **Okta** / **Salesforce** — `okta.local/1.0.0` and `salesforce.local/einstein/2.0.1` exist, but the `.local` domains mark these as community submissions, *not* the vendors' official APIs. Real Okta and Salesforce specs are still genuinely missing; don't let the grep hit fool you.
- **Heroku** — the `*.herokuapp.com` hits are unrelated third-party apps hosted on Heroku, not Heroku's own API.

(Guessed URLs that 404'd, don't retry as-is: `okta/okta-management-openapi-spec`, `intercom/Intercom-OpenAPI` 2.11 and 2.13, `api.hubspot.com/api-catalog-public/v1/apis`, `api.heroku.com/schema`.)

---

## 5. Parked — do NOT action without a fresh go-ahead

Each of these was either explicitly declined or deliberately deferred.

- **Google spec regeneration** (#611 OAuth `Oauth2c` malformed security, #1189 Gmail path structure, #1300 DisplayVideo `kpiType` enum, #2393 general staleness, #1356 Vertex AI). User said **"don't do the DisplayVideo regeneration."** This is a systemic ~457-file problem, not per-file typos.
  - **PR #40 was closed for exactly this reason.** Vertex AI was proposed as a new addition; it was actually a *regeneration* — `APIs/googleapis.com/aiplatform/v1/` already exists (the search used "vertex"; the dir is `aiplatform`). It would also have stripped curated metadata. The conversion itself worked (214 paths / 271 ops / 1488 schemas, clean `security` blocks) if it's ever wanted.
- **Linode discriminator fix** (#1250) — 10 occurrences of non-standard `x-linode-ref-name`. User explicitly excluded it ("just the openai one").
- **Greenpeace removal** (#1269) — `greenwire.greenpeace.org` no longer resolves (curl exit 6). Removal is destructive; offered, never requested.
- **`x-preferred` policy** (#1115) — on `meraki.com`, only the v0 `0.0.0-streaming` spec is flagged `x-preferred: true`, so nothing in the v1 line is preferred. Looks wrong. 1.74.0 was set to `false` mirroring 1.32.0 rather than deciding it.
- **php-openapi README addition** (#1390) — asked, never answered.

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
- **PyYAML can't parse every vendor YAML.** Cloudflare's 19 MB spec uses the YAML 1.1 `tag:yaml.org,2002:value` construct, which `safe_load` rejects. Other parsers handle it. Verify integrity with `head`/`tail`/`wc -l` and commit as-is rather than reformatting.
- **This worktree uses sparse-checkout** (`git sparse-checkout list`). The working tree holds only a couple of `APIs/` subdirs, so `ls`, `find` and `[ -d ]` under `APIs/` are all misleading — see §4. Widen with `git sparse-checkout add APIs/<domain>` before `git add`, and note the command takes no `-q`.
- **GitHub push protection is active on this repo.** Vendor specs routinely carry fake example tokens that match real credential patterns; a push can be rejected by content you did not write. Read the violation before assuming a genuine leak, and never bypass it without the user.
- **The auto-mode classifier blocks `gh pr merge`** ("Merge Without Review") regardless of the user's standing permission to merge. It also intermittently misfires on read-only multi-command `git show ... | grep` pipelines; splitting them into single commands clears it.
- **Always verify `mergeable`/`mergeStateStatus` and the file list before merging.** `gh pr view N --json mergeable,mergeStateStatus,changedFiles,additions,deletions`. Unexpected deletions mean you're overwriting something that already exists — that's how #40 was caught.

---

## 8. Spam heuristics (for any future triage)

Strong signals a submission is junk: duplicate submissions from one domain; bursts posted seconds apart or on a fixed schedule; crypto / x402 / "pay-per-call" framing; gambling; "Intelligence"/"Analytics"/"Scraper" wrappers around someone else's platform; `Official: NO` with a Postman documenter link; a source URL pointing at a random personal repo.

Worked examples: BMObot filed 15 issues in 47 seconds. The "SplunkES8.1" issue (#1419) contains *genuine* Splunk ES 8.1 content but is hosted at `rigzindorje/gmail-api` — Splunk publishes no official spec (checked their GitHub org), so there's no trustworthy `x-origin` and it was skipped. The "guardian" issues (#1334/#1335) are a third-party Postman collection titled "guardian news", not The Guardian's Open Platform.
