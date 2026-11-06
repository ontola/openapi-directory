# Native GraphQL artifacts

This directory retains native SDL and provenance independently of `APIs/`.
An OpenAPI document exposing a `/graphql` route is not a complete GraphQL schema.
See [issue #465](https://github.com/ontola/openapi-directory/issues/465) and the
[baseline inventory](../maintenance/reports/graphql-inventory-2026-11-02.json).

The [latest coverage report](../maintenance/reports/graphql-second-expansion-2026-11-02.md)
records the merged first expansion (#471–#479), five further prepared API surfaces,
and fresh source/validation findings. It supersedes earlier pending-delivery notes.

`index.json` records retained artifacts and a bounded discovery queue. Unknown
endpoints, formats, source revisions and hashes remain null; a playground or saved
query is not substituted for an authoritative schema. The public directory used
for discovery is a secondary lead, not evidence of vendor ownership or freshness.

## GitHub pilot

The public Free/Pro/Team SDL is copied byte-for-byte from GitHub's documentation
repository at `ab7258a0374c0666a71f27493b655975d304a8e5`. GitHub's
`src/graphql/README.md` describes synchronization from its API. The retained file
has 1,829 non-introspection types, 8,426 fields, eight directives, Query and Mutation
roots, and no Subscription root. The adjacent provenance records the original URL,
SHA-256, retrieval time, source revision, scope and exact validation outcome.
The source repository's licenses remain applicable; its license reference is in
provenance. No invented vendor version or live-account claim is supplied.

**The pilot is validation-blocked, not verified-current or advertised as usable.**
The pinned `graphql-core 3.3.1` profile reports eight interface/deprecation
violations in GitHub's SDL. No directives, constraints, descriptions or deprecations
were removed to obtain a passing result. See provenance for every error.
The source builds, including its type references, but fails full native validation.
Schema-profile compatibility and upstream correction need separate investigation.

The baseline committed tree contains no native `.graphql`/`.gql` artifacts or
introspection candidates within the documented scan. It has 57 OpenAPI text
mentions, including five documents with GraphQL routes. These do not establish
native coverage. The candidate queue records GitLab, Shopify Admin/Storefront,
monday.com, Braintree, Buildkite and Contentful as missing native artifacts within
that baseline, with upstream discovery links and explicitly unassessed freshness.
Contentful's schema depends on a space/content model; a demo schema cannot stand
for all accounts. These were the initial leads; additions and updated status are
recorded below and in the index.

## Expanded coverage

The [coverage expansion report](../maintenance/reports/graphql-expansion-2026-11-02.md)
adds native-valid snapshots for Linear, Buildkite, public GitLab.com, monday.com,
Shopify Customer Account 2026-10, Saleor, Dagster OSS and Dagster Plus. Source
snapshots are distinct from verified runtime freshness. Self-managed and
tenant-specific endpoints remain explicit limitations rather than guessed URLs.
Linear's two official formats are retained with their 12 semantic differences;
equal counts are not treated as proof of equivalence.

GitLab was retrieved through a one-off, credential-free standard introspection
query selecting schema metadata only. Its request is retained with the original
response and provenance. No application-data query or mutation was executed.

## Validation and comparison

From the repository root, with the pinned maintenance dependencies installed:

```sh
python maintenance/graphql_inventory.py --base origin/main --output cache/maintenance/graphql-inventory.json
python maintenance/graphql_schema.py --verify-index GraphQL/index.json
python maintenance/graphql_schema.py path/to/schema.graphql
python maintenance/graphql_schema.py path/to/schema.graphql --upstream path/to/fresh-schema.graphql
python maintenance/graphql_schema.py path/to/introspection.json --format introspection
```

Native validation returns nonzero for invalid artifacts. Index verification checks
hashes and reproduces the recorded counts, roots, validation profile and errors.
It can succeed for a retained invalid source only when that source stays explicitly
blocked and all observed errors match provenance. Such success means snapshot
integrity, not native validity, live freshness, runtime availability or task completion.
The read-only GraphQL workflow runs regression and snapshot-integrity checks; it
does not fetch schemas, publish artifacts, change credentials or introspect endpoints.

Comparison includes complete schema introspection with descriptions, fields,
arguments/defaults, scalars and specified-by URLs, enums, interfaces/unions, operation
roots, directives and deprecations. SDL-to-SDL comparison additionally compares the
complete parsed AST, preserving applied directives and extension information.
AST ordering differences conservatively request review; they are not automatically
classified as breaking changes. Standard introspection cannot prove full SDL or
applied-directive equality, so cross-format comparison explicitly reports incomplete
coverage. Executable saved queries and partial/error introspection responses are
rejected. Validation failures block semantic equivalence claims.

## Deliberate refresh procedure

1. Use the existing isolated checkout; do not create a worktree unless requested.
   Fetch current main through the existing authenticated HTTPS route. Resolve the
   official source repository/ref to an immutable commit and retain the raw source
   and retrieval metadata. Successful repository access is not artifact freshness.
2. Fetch the published schema at that exact revision with TLS verification enabled.
   Recheck vendor ownership, product/API version, source synchronization and scope.
   Published SDL is preferred when introspection is disabled or requires account
   permissions. Do not run introspection queries against customer data or request
   credentials when public artifacts suffice.
3. Validate the entire native artifact. Compare it with the previous retained
   schema and record additions/removals and changed semantic content. Counts and
   a recent commit date alone cannot establish completeness or freshness.
4. Add a new immutable revision directory with unchanged vendor bytes and adjacent
   provenance. Update the index and review report, preserve old revisions and all
   validation failures, and rerun the tests and integrity check. Do not patch vendor
   schema semantics or label a blocked snapshot verified-current.
5. Downstream overlays, proxies and Syncables should pin the artifact path, commit
   and hash. A saved operation's projection is separate from the full schema.
   Runtime permissions, collection ordering, pagination and sync/archive semantics
   need the separate work linked from #465 (atomic-plugins #679–#682); this snapshot
   neither implements those components nor authorizes provider requests.

No scheduled writer, automatic endpoint introspection, API deployment or OpenAPI publication
change is introduced. The remaining vendor-schema retrievals, GitHub profile issue
and account-specific limitations keep #465 open.
