# Public Spec Alignment with Current Codebase

## Codebase Reviewed
- `C:\Users\archm\code\TP`

## What Already Exists
1. FastAPI service with SQLite/SQLModel persistence.
2. User registration/login and signed session token flow.
3. User fingerprint generation for identity traceability.
4. Idea submission with signatures.
5. Idea update and merge operations.
6. Voting (up/down) and score aggregation.
7. Comment threads with signatures.
8. Static web UI with authentication and idea workflow.
9. In-app rendering of `segment_000.md` spec.
10. Status lifecycle (`submitted`, `acknowledged`, `in_progress`, `resolved`).
11. Reporting summary endpoint plus admin CSV export.
12. Admin audit-event access.

## What Partially Exists
1. Requirement prioritization
- Exists via votes, scoring, and sorting.
- Missing a more advanced weighted prioritization model.

2. Governance controls
- Admin access exists for status, export, and audit endpoints.
- Missing richer multi-role partner/governance scopes.

## What Is Missing (vs public roadmap)
1. Local boards and geo filtering.
2. Partner integration hooks.
3. Advanced recommendation features.
4. Stronger compliance-specific governance surfaces.

## Practical Conclusion
The `TP` repo already contains a credible MVP foundation. Public positioning can truthfully claim an operational prototype with signed submissions, discussion, merge, status lifecycle, reporting, export, and audit behaviors.
