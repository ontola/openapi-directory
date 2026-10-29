# Google API description refresh — 2026-10-29

This is a refresh from Google's maintained
[Discovery mirror](https://github.com/googleapis/discovery-artifact-manager/tree/1f1d01578507ceded42f7453bbef1bb0f637faee/discoveries),
at exact revision `1f1d01578507ceded42f7453bbef1bb0f637faee`.
It describes public API contracts, not a live account or runtime endpoint test.

| Result | Service/version descriptions |
| --- | ---: |
| Existing files refreshed | 411 |
| Previously missing versions/services added | 118 |
| Keep already newer; retained | 1 |
| Historical descriptions absent from mirror; retained unchanged | 87 |
| Conversion/validation blockers | 0 |

The 529 changed files contain 25,863 operations, 18,282 paths, 52,961 schemas
and 295,611 resolved local references. Together with the separately refreshed
Keep OAD, all 530 available native mirror descriptions are accounted for.
The Google directory grows from 499 to 617 files without deleting historical
versions. Vendor versions are preserved rather than invented or renamed.

The [machine report](google-discovery-2026-10-29.json) records every source
revision/hash, exact baseline/candidate hash, actual native method/schema/
reference counts, compatibility correction, unavailable historical target
and removed method/schema name. There are 142 old operation IDs absent from
the current native descriptions; these removals are explicit and independently
checked against the complete native method inventories. They are not methods
lost through template collisions. No absence establishes runtime retirement.

The official directory index also lists six entries with no JSON artifact
in this mirror snapshot: area120tables v1alpha1, contentwarehouse v1,
datalabeling v1beta1, mybusinessqanda v1, poly v1 and rapidmigrationassessment
v1. Those source gaps and their canonical Discovery URLs are recorded rather
than fabricated or silently removed. Live Google downloads are blocked in
this worker; hosted web retrieval also could not obtain these six sources.

The conversion uses Google's concrete `flatPath` routes, preserving original
whole-resource templates, patterns and bindings in explicit extensions.
It preserves every native method and schema, fixes OAuth alternatives,
retains exact numeric and query constraints, and carries protocol-specific
metadata without inventing an implementation. All candidates pass full OAS
validation, independent native schema/method/body/scope/reference comparisons
and typed YAML roundtrip checks. Existing APIs.guru curation is preserved;
new files receive no invented curation. See the
[conversion profile and limitations](../GOOGLE_DISCOVERY.md).

Two exact-node compatibility corrections are reported: Reports' impossible
empty `orgUnitID` defaults remain as annotations while value constraints stay
unchanged; PageSpeed's RE2 inline-case pattern becomes an equivalent portable
expression with Unicode folding and non-LF dot behavior retained. Native RE2,
ECMA-262, positive/negative and full Unicode case-fold witnesses pass.

The read-only exact-head CI reconstructs each changed artifact from its
immutable official source and base curation. Its actual PR result and report
establish hosted validation; local checks alone do not claim that CI ran.
Existing downstream catalogs/overlays keep their immutable OAD pins. The
separate Keep catalog update is unchanged; this batch makes no deployments,
provider-data requests, or provider writes.
