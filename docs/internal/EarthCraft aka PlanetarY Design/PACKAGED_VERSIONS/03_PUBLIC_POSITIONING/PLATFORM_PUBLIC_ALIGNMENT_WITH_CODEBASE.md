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

## What Partially Exists
1. Requirement prioritization
- Exists via votes and sorting.
- Missing explicit weighted prioritization model.

2. Accountability trail
- Signatures and timestamps exist.
- Missing explicit append-only audit ledger/export surface.

## What Is Missing (vs public roadmap)
1. Formal status lifecycle (`submitted`, `acknowledged`, `in_progress`, `resolved`).
2. Reporting/export API for partner consumption.
3. Role-based governance controls (partner/admin scopes).
4. Advanced anti-abuse modules beyond baseline constraints.
5. Local boards and geo filtering.
6. Partner integration hooks.

## Practical Conclusion
The `TP` repo is already a credible MVP foundation. Public positioning can truthfully claim an operational prototype with signed submissions, discussion, merge, and prioritization behaviors.

