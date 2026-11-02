# Further native GraphQL coverage — 2026-11-02

## Approved batch delivered

All nine previously approved PRs **#471–#479 are merged**. Every reconciled head
passed its actual hosted native-snapshot checks and required gate before an
exact-head merge. The shared report also passed the maintenance suite. Index
reconciliation preserved each previously merged artifact and candidate update;
it did not overwrite another API's entry. The machine report includes the exact
PR heads, merge commits and observed check outcomes. This supersedes the earlier
report's historical pending-delivery status.

## Five more prepared API surfaces

| Surface | Native publication | Types | Fields | Scope |
| --- | --- | ---: | ---: | --- |
| Apollo Platform / GraphOS | Official Rover CLI SDL | 524 | 1,594 | GraphOS control-plane API, not every customer's application graph. |
| commercetools Composable Commerce | Official documentation-linked SDL | 2,323 | 8,951 | Core commerce API; region, project endpoint and account permissions remain deployment-specific. |
| Fly.io control plane | Official flyctl SDL | 493 | 2,150 | CLI GraphQL source snapshot; not the separate Machines REST API or verified runtime parity. |
| OpenCTI | Official Relay-client SDL | 1,235 | 12,714 | Client/server contract as shipped; deployment, edition and module differences remain unassessed. |
| Sourcegraph | Public schema introspection | 842 | 3,454 | Supported metadata surface of the public endpoint, with unavailable modern annotations recorded as unknown. |

All five pass the unchanged `graphql-core 3.3.1` native validation profile. Vendor
bytes, hashes, provenance, source scope and full validation outcomes are retained.
GitHub sources additionally have immutable revisions, independently verified Git
blob identities and artifact-specific commit dates. No inferred release version
or universal runtime freshness is claimed.

The commercetools documentation directly links `api-specs/graphql/schema.sdl`.
The nonstandard filename suffix was followed from that authoritative link rather
than declaring an API absent after a narrower filename search. The retained
`schema.graphql` filename changes no source bytes.

OpenCTI's pinned Relay configuration names the retained full schema and explicitly
excludes separate LSP-only directive files. Those directives and individual operation
documents were not fabricated into a server schema. Self-managed endpoints remain
unknown instead of being replaced with an arbitrary demo installation.

## Sourcegraph introspection capabilities

The initial modern standard introspection query failed because this provider rejects
schema descriptions, repeatable-directive metadata, and input-value/argument deprecation
metadata. A compatible standard query retained all supported type/field metadata,
descriptions, field/enum deprecations and scalar specified-by URLs. The same strict
native validator still passes; no validation rule or profile was disabled.

The exact credential-free request and original response are retained. Missing modern
annotations are explicitly unknown, not proof that a scalar/directive/input value
lacks an annotation. Standard introspection still cannot preserve applied SDL
directives. Only schema metadata was selected; no customer/application records were
queried and no mutation was executed.

## Fresh obstacles, not invented coverage

- **Shopify Admin 2026-10:** its official SDK's production configuration identified
  the public schema-proxy URL. It returns a full schema with 3,708 types / 12,780 fields,
  but the pinned native profile reports six interface/deprecation violations. This
  supersedes the earlier source-not-located observation; no fixture was imported.
- **Shopify Storefront 2026-10:** the official public proxy independently reproduces
  the SDK snapshot's `MediaPresentation.id` interface/deprecation violation.
- **Railway:** the official CLI's full introspection schema has 616 types / 2,705
  fields, but `Team.id` violates the pinned profile's interface/deprecation rule.
- **Atlassian:** anonymous metadata retrieval succeeds (32,256 types / 109,661 fields),
  but the native profile reports interface/deprecation violations. The response is
  retained in the ignored research cache; it is not advertised as native-valid.
- **GitHub / Octokit:** an alternative official SDK publication was checked. SDL has
  duplicate `EnterpriseOwnerInfo` fields; JSON also fails native validation. The
  original GitHub pilot is neither replaced nor relabeled valid.
- **Grafbase:** its CLI SDL validates, but last changed **2025-09-05**. A read-only
  schema request to the endpoint configured by the current CLI returned HTTP 404.
  This is held for freshness/lifecycle investigation rather than counted as a current
  API addition. The 404 alone does not prove the vendor has no API elsewhere.
- **Hashnode:** the public schema endpoint redirects to the vendor's paid-access
  announcement. No credential or paid-access bypass was attempted.

These native-profile failures do not establish that the providers' services are
unusable. Profile/specification compatibility and upstream schema correction are
separate review work; no rule was waived to make an import pass.

Other bounded repository scans found operation files, fixtures, application-specific
schemas or no matching publication. Truncated trees and guessed-path 404s were never
treated as whole-vendor absence. Tenant-defined content/database schemas remain
explicitly scoped gaps rather than universal API schemas reconstructed from models.

The [machine report](graphql-second-expansion-2026-11-02.json) preserves source URLs,
revisions, hashes, exact errors, the prior merge receipts and prepared artifact paths.
The new additions are delivered separately for review. Their preparation and local
validation do not establish hosted CI success or merge; verify those exact heads.

## Prepared PRs

The five new API PRs remain separate from the approved-and-merged first batch.
They are prepared for review, not merge receipts:

- [Apollo GraphOS Platform — #480](https://github.com/ontola/openapi-directory/pull/480)
- [commercetools Composable Commerce — #481](https://github.com/ontola/openapi-directory/pull/481)
- [Fly.io control plane — #482](https://github.com/ontola/openapi-directory/pull/482)
- [OpenCTI — #483](https://github.com/ontola/openapi-directory/pull/483)
- [Sourcegraph — #484](https://github.com/ontola/openapi-directory/pull/484)
