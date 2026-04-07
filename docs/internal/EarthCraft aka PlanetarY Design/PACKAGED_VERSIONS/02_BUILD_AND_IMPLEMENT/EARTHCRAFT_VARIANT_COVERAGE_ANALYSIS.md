# EarthCraft Variant Coverage Analysis

## Scope Reviewed
- `formatted-conversation.md`
- `medium-article-formatted.md`
- `medium-article-formatted (1).md`
- `medium-article-enhanced.md`
- `segment_000.md`

## High-Level Finding
The five files describe the same core concept, but `segment_000.md` is a mixed corpus: it includes valuable EarthCraft expansions and a large unrelated tail. The best path is to define one canonical source, absorb only EarthCraft-relevant additions, and explicitly quarantine off-topic material.

## What Each Version Adds (Unique or Distinct)
### `formatted-conversation.md`
- Full origin context and intent behind the concept.
- Benefit expansion flow (27 -> 32 benefits), including de-duplication logic.
- Impact categorization into groups (transformative, user-centric, operational, etc.).
- Strong local-impact framing (small local problems with high daily-life impact).
- User statement on skipping advertising influence.
- Conversational implementation ordering and MVP-first framing.

### `medium-article-formatted.md`
- Most complete long-form article version.
- Most complete technical requirements bundle.
- Identity and authentication detail set (real ID, pseudonymous mode, hierarchy).
- Reputation and anti-abuse baseline (fraud, sybil, rate limit / proof-of-work).
- Explicit "record-keeper, not moderator" section.

### `medium-article-formatted (1).md`
- Almost identical to `medium-article-formatted.md`.
- Unique value: explicit IP rights language in opening premise:
  - Prior Art
  - Patents
  - Copyright
  - Licensing rights

### `medium-article-enhanced.md`
- Most concise and publication-friendly narrative.
- Better readability for non-technical audiences.
- Editorial packaging (visual sections, CTA tone).
- Adds "external accountability" and "community-driven content management" in compact form.

### `segment_000.md`
- Adds explicit "what it is" framing as a buildable web app with staffing model and effort estimate.
- Adds a concrete timeline draft:
  - Planning and design: 1-2 months
  - Development: 6-12 months
  - Testing and QA: 2-3 months
  - Deployment and maintenance: ongoing
- Adds job-creation and economic-opportunity framing:
  - Entrepreneurial ventures
  - Freelance and contract work
  - Supply-chain and manufacturing response
  - Skill matching and training pathways
- Adds expanded risk framing around "powerful interests":
  - Corporate incumbents
  - Advertising/marketing systems
  - Regulatory friction and operating-rule resistance
  - IP disputes and stakeholder conflict
- Adds mitigation framing (stakeholder engagement, legal counsel, transparency, advocacy).
- Adds an expanded value taxonomy (up to 20 values), including:
  - Digital inclusion
  - Regulatory compliance and service operations
  - Data privacy and security
  - Ethical business practices
  - Crisis response and resilience
- Adds monetization ethics language:
  - Opt-in data sharing
  - Data anonymization
  - Explicit value exchange
  - Preference for subscriptions/premium/partnerships over data-sales dependency

## What Is Missing by Version
### `formatted-conversation.md` leaves out
- Clean final article structure.
- Explicitly finalized product scope boundaries.
- Formal architecture, domain model, API, and delivery plan.

### `medium-article-formatted.md` leaves out
- Why/intent context from the conversation.
- Benefit impact ranking rationale.
- Explicit anti-advertising motivation from the user context.

### `medium-article-formatted (1).md` leaves out
- Same gaps as `medium-article-formatted.md` (except stronger IP wording).

### `medium-article-enhanced.md` leaves out
- Most deep technical detail.
- Identity architecture specifics and anti-abuse mechanisms.
- Implementation depth required for immediate engineering execution.

### `segment_000.md` leaves out
- Tight scope boundaries: the file mixes EarthCraft content with unrelated conversations.
- A clear canonical extraction boundary for what should be considered product truth.
- Consolidated non-duplicated architecture and implementation plan (many repeated list expansions).

## Out-of-Scope Content Detected in `segment_000.md`
- The file appears to contain merged material from unrelated threads.
- Example unrelated starts around `segment_000.md:1460` (`Affirmative action explained`) and continues with non-EarthCraft political/systemic analysis well beyond the product concept.
- Recommendation: treat `segment_000.md:1-1459` as primary EarthCraft candidate corpus and process everything after as out-of-scope unless manually re-tagged.

## Conflicts to Resolve Before Build
1. Safety-handling strategy conflict
- File claims both:
  - "Safety tools" as a technical need
  - "Moderation is impossible; platform is a record-keeper"
- Required decision: choose legal-accountability model vs active safety-handling model (or explicit hybrid).

2. Advertising conflict
- Conversation includes anti-advertising motivation.
- Technical section lists ads as possible monetization.
- Required decision: ads banned, limited, or allowed with strict constraints.

3. Identity/privacy tension
- Strong real-identity model is proposed.
- Pseudonymous posting is also proposed.
- Required decision: what is public vs private identity data, and by jurisdiction.

4. Immutable content vs correction needs
- Signed immutable posts are proposed.
- Real systems need updates/corrections.
- Required decision: immutable append-only ledger with versioned amendments.

## Recommended Canonical Baseline
Use `medium-article-formatted.md` as base, then import:
- From `medium-article-formatted (1).md`: explicit IP rights opening sentence.
- From `formatted-conversation.md`: anti-advertising rationale, local-impact framing, benefit impact tiers.
- From `medium-article-enhanced.md`: concise public-facing narrative structure.
- From `segment_000.md`: team/effort estimates, job-creation framing, power-map risk model, and monetization ethics principles.

## Decision Set Needed to Start Engineering
1. Operating entity model: public utility, nonprofit, coop, or commercial hybrid.
2. Safety/legal model: record-keeper only vs hybrid trust-and-safety.
3. Identity model: mandatory legal identity + pseudonym layer rules.
4. Data model: append-only signed ledger with revision events.
5. Monetization rules: no ads / limited ads / alternative funding.
6. MVP scope: what is in v0.1 and what is deferred.
7. Corpus hygiene rule: how mixed-source files (like `segment_000.md`) are filtered into canonical product knowledge.
