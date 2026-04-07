# The Platform Transparent Recording Architecture (Draft v0.1)

## Status
Working draft. This is intentionally not final and should be refined through implementation feedback.

## Design Target
Build a system that is destroyable at the infrastructure level but hard to corrupt silently at the operations and record level.

## Reality Check
No system can be mathematically guaranteed "uncorruptible." The practical target is:
1. Corruption becomes expensive.
2. Corruption becomes visible.
3. Recovery from sabotage is fast and verifiable.

## Core Invariants
1. Every meaningful coordination action is an event.
2. Every event is signed by an accountable actor identity.
3. No silent edits and no hard deletes of coordination events.
4. Every event records who, what, when, and where (scope).
5. Public views must be reproducible from the raw event log.
6. Data export and independent verification are always available.

## Event Model (Who-Wants-What-When-Where)
Minimum event fields:
1. `event_id` (UUID)
2. `event_type` (request, claim, response, vote, challenge, resolution, safety_action)
3. `actor_id` (internal verified identity)
4. `public_persona_id` (external display identity)
5. `subject_ref` (what this event is about)
6. `statement` (the explicit ask/claim/decision)
7. `location_scope` (local, region, global, or geo-tag)
8. `created_at_utc` (when asserted)
9. `effective_window` (when it is expected/relevant)
10. `evidence_refs` (links/files/hash pointers)
11. `privacy_class` (public, limited, restricted)
12. `previous_event_hash` (chain continuity)
13. `event_hash` (content hash)
14. `signature` (actor signature over canonical payload)

## Reference Architecture
1. Identity and Credential Service
- Verifies real-world identity privately.
- Issues signing credentials tied to platform accounts.

2. Event Ingest API
- Accepts only signed events with schema validation.
- Rejects malformed or unsigned coordination actions.

3. Append-Only Event Store
- Immutable event table with sequence index.
- History preserved; corrections are additive events.

4. Evidence Store
- Content-addressed object storage for attachments.
- Hash-locked references in event payloads.

5. Rules Engine
- Applies transparent operating rules to classify, queue, or escalate events.
- Never rewrites event history.

6. Materialized Views
- Feed, local board, unresolved requests, response latency dashboards.
- Views are derived from events, not hand-edited truth.

7. Audit and Export API
- Public snapshots, hash manifests, and replay endpoints.
- Third parties can independently rebuild state.

## Anti-Capture Controls
1. Rotating steward privileges with expiry.
2. Dual control for high-impact actions (2-of-3 signatures).
3. External signed checkpoints (daily/weekly hash publication).
4. Tamper-evident safety-action trail (no hidden safety actions).
5. Public operations rulebook versioning (rule changes are events too).

## Destroyable But Recoverable Pattern
1. Primary system can fail or be taken down.
2. Independent mirrors keep signed snapshots and hash manifests.
3. Any mirror can restore service with replay verification.
4. Divergence creates visible fork evidence, not silent replacement.

## MVP Build Tasks
1. Define canonical event schema (`jsonschema` + versioning rules).
2. Build signing and signature-verification libraries.
3. Implement append-only event table and hash-chain checks.
4. Build replay tool that reconstructs state from events.
5. Add public export endpoint (events + hashes + schema version).
6. Implement first materialized views: local board and unresolved queue.
7. Add checkpoint publishing job and verification CLI.

## Open Decisions
1. Which signature standard for user keys and rotation rules?
2. Which events must be always public vs privacy-limited?
3. What legal retention/deletion requirements must overlay immutability?
4. What fork resolution rule is acceptable when mirrors disagree?
