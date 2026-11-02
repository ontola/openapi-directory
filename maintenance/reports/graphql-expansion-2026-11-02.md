# Native GraphQL coverage expansion — 2026-11-02

Eight additional API surfaces have native-valid source snapshots. These are complete
vendor-published SDL or full schema introspection responses, not saved-query response
projections, OpenAPI wrappers, or schemas reverse-engineered from SDK model classes.

| Provider / surface | Publication | Non-introspection types | Fields | Scope |
| --- | --- | ---: | ---: | --- |
| Linear | Official SDK SDL and companion introspection | 1,361 | 9,678 | Production API schema publication; the two formats differ at 12 semantic locations. |
| Buildkite | Official documentation SDL | 536 | 2,188 | Public GraphQL API publication. |
| GitLab.com | Anonymous, read-only standard introspection | 4,639 | 20,059 | Public GitLab.com endpoint, not every self-managed release or edition. |
| monday.com | Official public `/v2/get_schema` export | 1,456 | 4,908 | Platform schema; the export does not identify its effective default dated API version. |
| Shopify Customer Account | Official Hydrogen introspection | 509 | 1,714 | API version **2026-10**, independently identified by the pinned source constants and codegen configuration. Not Admin or Storefront. |
| Saleor | Official core server SDL | 1,475 | 6,400 | Source-revision snapshot, not a claim about a deployed tenant, stable release or custom extensions. |
| Dagster OSS | Official UI SDL | 615 | 2,181 | OSS API surface at the pinned source revision. |
| Dagster Plus | Official CLI SDL | 1,021 | 3,201 | Plus surface documented by adjacent `GRAPHQL_SCHEMA.md`; file last changed 2026-08-25, so current runtime parity is not established. |

Each artifact has original bytes, SHA-256, retrieval time, endpoint or explicit
deployment limitation, native format, full validation result and source scope in
adjacent provenance. GitHub publications also record immutable revision, Git blob
identity and the most recent artifact-specific commit, independently of repository
activity. No vendor release number is inferred from a repository head.

The eight surfaces use nine native artifacts because Linear's two original formats
are both retained. Its SDL and JSON have equal type/field counts but differ in
descriptions and standard directive definitions. The complete comparison is retained
in `GraphQL/linear.app/consistency.json`. Neither original was rewritten to hide the
differences. Cross-format introspection cannot recover applied SDL directives.

The GitLab request selected only standard `__schema`/`__type` introspection metadata.
It sent no credential, selected no application/account data and invoked no mutation.
The exact query is retained as `request.json`. Schema mutation definitions appearing
inside a schema response do not mean those mutations were executed. Other additions
were fetched from published files/exports, without runtime data requests.

## Remaining limitations and leads

- **Braintree:** official SDL retrieved at a pinned revision, but three native
  interface/deprecation errors remain under the current validation profile.
- **Shopify Storefront 2026-10:** official Hydrogen SDL and JSON both fail the same
  native interface/deprecation rule (`MediaPresentation.id`). Its generation context
  also explicitly distinguishes tokenless from token-scoped Storefront schemas.
  No token was requested and no substitute scope was invented.
- **Shopify Admin:** the discovered codegen test fixture was not accepted as an
  authoritative Admin schema. Publication discovery remains open.
- **Contentful, Hasura and Strapi:** content models, database metadata or installed
  application configuration determine the schema. A demo/fixture cannot stand for
  every tenant. These need explicitly scoped application schema snapshots.
- **Dagger:** schema publications were discovered, but engine/module composition,
  version and public service scope were not reviewed sufficiently for import.
- The earlier GitHub pilot remains explicitly validation-blocked. No source was
  patched, no validator rule was disabled, and no lower validation profile was
  substituted to turn an error into a passing result.

The [machine report](graphql-expansion-2026-11-02.json) records the retained paths,
Linear comparison, exact blocked-source errors and unresolved leads. Endpoint
availability, account permissions and application-data operations are separate from
schema validity. This expansion advances #465 without claiming a universal GraphQL
catalog or completing its remaining gaps and downstream integration work.

Validation: all **284 maintenance tests pass** locally, and the existing index
integrity verifier reproduces each retained artifact's hash, counts, roots and
native validation outcome. Each provider is delivered separately, following the
repository's one-API-per-PR convention. Actual hosted check results and merge state
must be verified per PR; local checks alone do not establish those outcomes.

## Prepared delivery

These eight PRs are prepared separately and remain unmerged. Automatic approval
review rejected repeated default-branch merges without explicit batch approval;
no merge or default-branch write was performed. They independently edit the shared
index, so approved entries must be reconciled and exact-head checks rerun as merges
proceed. PR preparation and current check results are not merge receipts.

- [Linear — #471](https://github.com/ontola/openapi-directory/pull/471)
- [Buildkite — #472](https://github.com/ontola/openapi-directory/pull/472)
- [GitLab.com — #473](https://github.com/ontola/openapi-directory/pull/473)
- [monday.com — #474](https://github.com/ontola/openapi-directory/pull/474)
- [Shopify Customer Account 2026-10 — #475](https://github.com/ontola/openapi-directory/pull/475)
- [Saleor core — #476](https://github.com/ontola/openapi-directory/pull/476)
- [Dagster OSS — #477](https://github.com/ontola/openapi-directory/pull/477)
- [Dagster Plus — #478](https://github.com/ontola/openapi-directory/pull/478)
