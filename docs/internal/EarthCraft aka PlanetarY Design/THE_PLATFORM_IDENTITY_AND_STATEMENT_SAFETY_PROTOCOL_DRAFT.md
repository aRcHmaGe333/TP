# The Platform Identity and Statement Safety Protocol (Draft v0.1)

## Status
Working operations draft. Intended to reduce participant risk and project hijack risk while preserving transparent accountability.

## Objective
Enable identity-tied accountability without exposing participants to unnecessary personal harm or legal ambiguity.

## Operating Principle
Accountability requires attributable actions; safety requires controlled disclosure.

## Identity Model
1. Internal Verified Identity
- Real person or legal entity verified in private.

2. Public Persona
- Stable pseudonymous display identity tied to internal verification.
- Public profile does not expose private identity attributes by default.

3. Role Credentials
- Time-bounded credentials for steward/auditor/implementer functions.

## Statement Classes
1. `S0` General feedback/request
- Standard posting path.

2. `S1` Product/service claim
- Requires clear scope and expected outcome.

3. `S2` Process challenge/dispute
- Requires references to prior events and explicit remedy request.

4. `S3` High-risk allegation or conflict statement
- Requires evidence bundle and enhanced review path before broad amplification.

## Minimum Statement Requirements
1. What is being claimed/asked.
2. Who is making it (public persona + signed identity token).
3. When it was asserted.
4. Where it applies (local/region/global scope).
5. Basis/evidence for the statement.
6. Requested response or resolution path.

## Safety Guardrails
1. No doxxing or release of private identity data.
2. No threats, incitement, or celebration of violence.
3. No unverifiable criminal allegations presented as fact.
4. No hidden safety actions: all safety actions become signed events.
5. High-risk statements require documented review and reasoned disposition.

## High-Risk Review Path (`S3`)
1. Intake: classify and lock original claim payload.
2. Triage: assign rotating reviewers with conflict-of-interest checks.
3. Evidence quality check: verify provenance and relevance.
4. Temporary visibility controls while review is active.
5. Outcome event: accept, reject, or request more evidence, with reasons.
6. Appeal window with a separate reviewer set.

## Anti-Hijack Operational Rules
1. No permanent admin accounts.
2. Privileged actions require dual authorization.
3. Operating-rule changes require public comment period and supermajority decision.
4. All ruleset versions are immutable and diffable.
5. Emergency actions auto-expire and trigger mandatory public postmortem.

## Public Positioning Layer (External Narrative)
Public framing should emphasize:
1. Requirement intelligence
2. Transparent product feedback infrastructure
3. Local issue prioritization and response latency reduction
4. Auditable collaboration between users and providers

Internal systems language can remain explicit, but public-facing material should avoid inflammatory framing and remain operational/legal.

## Implementation Tasks
1. Add statement-class field and validator in API schema.
2. Add high-risk routing workflow and reviewer assignment logic.
3. Add safety-action and appeals event types.
4. Add privacy filters by identity layer and statement class.
5. Add automated detection for doxxing/threat patterns.
6. Add ruleset version registry and diff endpoint.

## Documents Needed Next
1. Threat Model and Abuse Case Library
2. Appeals and Due Process SOP
3. Data Retention and Legal Hold Policy
4. Public Communications Style Guide (safe phrasing rules)
