# EarthCraft Implementation Roadmap

## Delivery Strategy
Build in phases with operating rules and architecture locked before feature scaling.

## Phase 0: Alignment and Constraints (Week 1-2)
### Tasks
1. Freeze canonical vision and scope from current variants.
2. Resolve safety-handling model conflict (record-keeper vs hybrid).
3. Resolve monetization rule conflict (ads vs no-ads).
4. Define identity/privacy baseline by jurisdiction.
5. Approve MVP feature list and non-goals.
6. Create a scope-filter rule for mixed corpora (`segment_000.md` in-scope vs out-of-scope ranges).

### Exit Criteria
- Signed canonical brief
- Signed operating-rule decisions for safety handling, identity, and monetization
- Approved source-hygiene note for mixed documents

## Phase 1: Architecture and Foundations (Week 3-5)
### Tasks
1. Select cloud and runtime architecture.
2. Define domain model (users, identities, posts, signatures, merges, votes, reports).
3. Define append-only event model and revision strategy.
4. Publish API contract (OpenAPI) for MVP endpoints.
5. Establish CI/CD, static analysis, security scanning, and test framework.
6. Produce stakeholder-power map and opposition-risk model for launch strategy.

### Exit Criteria
- Architecture spec approved
- API v0 contract approved
- Deployment pipeline passing

## Phase 2: Trust, Identity, and Security Core (Week 6-8)
### Tasks
1. Integrate one identity provider (BankID-like or equivalent).
2. Implement signed post creation and verification flow.
3. Implement pseudonymous display layer tied to verified identity.
4. Add anti-abuse controls (rate limits, sybil checks, anomaly detection baseline).
5. Build immutable audit log and export endpoint.

### Exit Criteria
- End-to-end signed posting works
- Identity and pseudonym model operational
- Audit trail available and verifiable

## Phase 3: Core Product MVP (Week 9-12)
### Tasks
1. Build posting, browsing, tagging, search, and filter experience.
2. Build commenting, support, merge/link workflows.
3. Implement status lifecycle and prioritization queue.
4. Implement reporting and legal escalation case flow.
5. Build admin console for rules and incident operations.
6. Implement local issue boards with geographical filters and local prioritization.

### Exit Criteria
- Pilot-ready MVP with core workflows complete
- All P0 acceptance tests green

## Phase 4: Pilot and Validation (Week 13-16)
### Tasks
1. Launch closed pilot with defined participant mix.
2. Monitor reliability, abuse patterns, and resolution performance.
3. Run weekly operations/protocol review loops.
4. Triage and ship pilot-critical fixes.
5. Publish pilot metrics and lessons learned.
6. Track economic opportunity signals (fulfilled demands, new providers, local job/contract matches).

### Exit Criteria
- Pilot KPIs hit minimum thresholds
- Go/no-go decision for expanded rollout

## Phase 5: Expansion (Post-Pilot)
### Tasks
1. Add multilingual and accessibility hardening.
2. Add integrations (external org workflows, partner APIs).
3. Add recommendation/ranking improvements with auditability.
4. Expand legal and compliance coverage by region.
5. Add resilience mode and crisis-response operating playbooks.

## Immediate Backlog to Commence Development (First 10 Work Items)
1. Create mono-repo and baseline service scaffolding.
2. Create ADR-001 safety handling and accountability model.
3. Create ADR-002 identity and pseudonym rules.
4. Create ADR-003 immutable ledger and revision model.
5. Create ADR-004 ethical monetization rules (ads, subscriptions, partnerships, data-use boundaries).
6. Define OpenAPI v0 endpoints for auth, posts, merges, votes, reports.
7. Implement signed post schema and verification library.
8. Implement minimal React frontend shell for auth and feed.
9. Implement PostgreSQL schema + event table + audit export.
10. Implement CI pipeline: lint, test, SAST, dependency scan.

## Critical Risks and Mitigations
1. Legal exposure from harmful content
- Mitigation: clear liability rules, escalation workflow, jurisdiction matrix.

2. Identity friction hurting adoption
- Mitigation: phased identity assurance levels and strong onboarding UX.

3. Trust erosion from opaque ranking
- Mitigation: transparent ranking factors and audit logs.

4. Scope creep before MVP validation
- Mitigation: strict phase gates and change control.
