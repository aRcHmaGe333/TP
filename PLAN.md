# The Transparency Platform (TTP) Pilot Readiness Plan (Free-Only, EU Region)

## Summary
1. Keep internal documentation alignment in `TP/docs/internal` concise and current, including adjacent initiatives such as `PatentMake` and `ValueFlow`.
2. Prepare `TP` for pilot launch on a zero-cost managed stack: `Render Free Web Service` + `Neon Free Postgres`, both in EU region.
3. Close pilot-critical product gaps in `TP`: security hardening, verified identity enforcement, auditability, privacy hygiene, and test coverage.
4. Keep app-level billing out of scope; “billing” is treated strictly as infrastructure cost control with free-tier guardrails.

## Immediate Tasks From Repo Review
1. Keep private and local files out of git via a root `.gitignore`.
2. Enforce verified identity for account creation: no verified person, no account.
3. Enforce one account per verified identity subject.
4. Support Bank ID / government ID integration via a verified-identity bridge token model and a dev-safe verification flow.
5. Rename human-facing project references to `The Transparency Platform (TTP)`.
6. Remove client-controlled IP spoofing from rate-limit and audit attribution logic.

## Extracted Tasks: Installation and Deployment
1. Correct the local install and run instructions to match the root-based TTP repo, not the old `feedback_platform` package path.
2. Keep a PowerShell-safe install sequence that does not depend on `Activate.ps1`.
3. Keep a Python 3.10-compatible local setup path:
   1. `python -m venv .venv`
   2. `.\.venv\Scripts\python.exe -m pip install --upgrade pip`
   3. `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`
   4. `.\.venv\Scripts\python.exe -m uvicorn main:app --reload`
4. Keep deployment steps aligned with free Neon Postgres in EU region plus Render free web service in Frankfurt.
5. Keep backup and restore commands documented and runnable.
6. Keep admin bootstrap instructions documented for the configured admin identity.

## Extracted Tasks: GitHub / ToS Boundaries
1. Keep GitHub account creation user-initiated: do not create GitHub accounts for users.
2. Keep repositories user-owned: if submissions are published to GitHub, they must end up in repositories owned by the user.
3. Keep GitHub as a hosting/versioning layer, not as a structured database backend for TTP.
4. Do not imply GitHub endorses or enforces IPClaim, APC, APC-VF, or ValueFlow licensing.
5. Do not operate bot networks of accounts.
6. Do not push massive automated content into repositories the user does not control.
7. If users authenticate, own their repos, and the system writes files there with their permission, keep the model inside those boundaries.
8. Keep the user’s GitHub account as the actor that performs the write, even if TTP prepares the content.
9. Use GitHub OAuth authorization flow rather than manual token entry:
   1. user clicks "Connect GitHub"
   2. browser redirects to GitHub authorization
   3. GitHub returns a temporary code
   4. TTP exchanges the code for an access token
   5. TTP creates repos and commits files on behalf of the user
10. Design around GitHub practical limits:
   1. repo size around 10 GB recommended maximum
   2. individual file size 100 MB hard limit
   3. frequent automated pushes can trigger API rate limits
11. Support safe GitHub publication methods:
   1. direct commit through OAuth
   2. client-side push
   3. GitHub template repo
12. Do not use a central TTP account to push content for everyone.
13. Do not generate thousands of repos automatically without user control.

## Extracted Tasks: IPClaim Connection
1. Harden the ValueFlow repo with cryptographic proof and the new license.
2. Replace the license in the connected repo(s):
   1. Copy `LICENSE-APC-VF.md` into the repo root as `LICENSE-APC-VF.md` or `LICENSE`, but keep the filename consistent with repo references.
   2. Fill in author name, chosen revenue split, and current date.
   3. Fill hash fields after the first timestamp run.
3. Copy `VERIFY.md` into the repo root.
4. Add the GitHub Actions timestamp workflow:
   1. Create `.github/workflows/timestamp.yml`.
   2. Timestamp each push to `main` or `master`.
   3. Save the `.tsr` proof in `.timestamps/`.
   4. Commit and push the evidence.
5. After the Actions run completes, pull the result and update the license with the actual tree hash.
6. Timestamp the backlog / important historical commits so historical content is cryptographically anchored.
7. Add a TTP-facing repo-stamping workflow:
   1. Offer APC or APC-VF license selection.
   2. Copy timestamp workflow and verification instructions into the target repo.
   3. Fill author name, tree hash, and date automatically.
   4. Commit and, where permitted, push to trigger timestamping.
8. Keep independent verification instructions available with OpenSSL-based verification.

## Extracted Tasks: Stamped Service / Bundle Proof Flow
1. Create the stamped service MVP where anyone can submit files and get back a timestamped, licensed bundle.
2. Write the Merkle tree function:
   1. Input: list of file paths.
   2. Output: single SHA-512 root hash.
3. Write the timestamp function:
   1. Input: root hash string.
   2. Output: `.tsr` file path.
   3. Calls `openssl ts` and `curl` via subprocess.
4. Write the license generator:
   1. Input: author name, root hash, timestamp date.
   2. Output: populated `LICENSE-APC-VF.md` text.
5. Write the bundler:
   1. Input: original files + license + `.tsr` + `VERIFY.md`.
   2. Output: ZIP archive.
6. Write the web route(s):
   1. `GET /` -> upload form with consent text.
   2. `POST /` -> process files -> return ZIP.
7. Test locally: submit files, download bundle, verify with OpenSSL.
8. Evaluate deployment options for the stamping service:
   1. Railway
   2. Render
   3. Static frontend + API / serverless split

## Extracted Tasks: GitHub-Backed TTP Architecture
1. Treat GitHub as the public record and mirrored publication layer, not the sole event store for all live platform activity.
2. Mirror the publishable record, not the whole living app state.
3. Good candidates to mirror to GitHub:
   1. the submission itself
   2. its license
   3. a summary
   4. accepted revisions
   5. linked evidence
   6. final decisions
   7. curated discussion snapshots
4. Bad candidates to mirror to GitHub:
   1. every keystroke
   2. drafts
   3. transient UI state
   4. reaction spam
   5. moderation queues
   6. endless conversational churn
5. Keep repositories human-readable, user-owned, and publication-shaped rather than app-database-shaped.
6. Keep repository contents meaningful in the repo itself:
   1. Markdown docs
   2. discussions
   3. issues
   4. specs / ideas / requirements
   5. license file
7. Ensure repositories can stand alone so someone visiting GitHub understands what they are.
8. Avoid large automated structured storage such as JSON databases, telemetry dumps, or binary-blob archives in user publication repos.
9. Define the workable backend-only shape for TTP:
   1. one user-owned repo per person or per project
   2. one main document per submission
   3. comments as GitHub Discussions or Issues
   4. improvement proposals as pull requests
   5. adopted changes merged into the main record
   6. forks for independent evolution
10. Add hard gates before mirroring broad/general review content:
   1. topic classes
   2. size limits
   3. media limits
   4. rules for what counts as an approved/public record

## Extracted Tasks: Business-Safe Entry Angle
1. Separate the core mechanism from the broader philosophical framing, at least initially.
2. Build the first exposure around familiar, practical language and clear functions.
3. Follow this framing order:
   1. plain functional description
   2. demonstrable mechanics
   3. adoption through use
   4. deeper implications later
4. Lead with:
   1. what the platform does
   2. what problem it solves
   3. how users interact with it
5. Show:
   1. visible workflows
   2. examples of how information flows through the system
   3. evidence that it works as intended
6. Reduce initial friction by letting structure and results speak first.
7. Avoid first-exposure claims that sound like “it solves everything”.
8. Prefer an intentionally modest first presentation, for example:
   1. a platform for publishing verifiable public records of reviews, requirements, and ideas
   2. authorship is transparent
   3. revisions are permanent
9. Keep the second-layer outcomes as consequences of simple mechanics, not as promises:
   1. traceable responsibility
   2. cross-linked problem records
   3. accumulation of evidence
   4. collaborative improvement
   5. durable public memory
10. Keep the rollout logic:
    1. clear mechanism
    2. practical use
    3. visible results
    4. people realize the larger implications themselves
11. Reuse the already-present “problem -> mechanism -> resulting capability” format from the larger docs as the business-looking layer.
12. Decide explicitly between the two strategic paths:
    1. publish the concept openly so the structure exists independently and acts as a catalyst
    2. keep control longer and build the system directly with funding, partners, and operator responsibilities
13. If the open-publication path is chosen, treat the first publication as a base layer rather than a final statement.

## Extracted Tasks: TTP Language Layer Over GitHub
1. Do not expose GitHub terminology in the TTP user experience.
2. Translate GitHub mechanics into human language and keep the Git layer invisible.
3. Maintain a vocabulary map:
   1. repository -> project / submission
   2. commit -> revision / record / entry
   3. branch -> proposal path / variation
   4. pull request -> change proposal
   5. merge -> adoption / integration
   6. fork -> independent evolution / derivative
   7. issue -> discussion / critique
   8. discussion -> open forum
4. Keep the visible flow domain-based:
   1. submit idea
   2. idea record created
   3. people discuss
   4. someone proposes improvement
   5. change proposal reviewed
   6. adopt change
   7. new revision recorded

## Extracted Tasks: Identity Accountability and Disclosure
1. Keep verified identity at entry.
2. Keep one account per verified identity.
3. Keep immutable public records of submissions and revisions.
4. Attach identity to each action at the TTP layer.
5. Design the system as identity-governed with post-hoc accountability rather than anonymous participation.
6. Define hard system behavior when lines are crossed:
   1. record
   2. expose
   3. freeze
   4. hide
   5. lock
   6. eject
7. Add a clear disclosure before publication:
   1. "You are publishing this material under your own name."
   2. "You confirm that you own the content or have the right to publish it."
   3. "You accept that this submission will be publicly recorded."
8. Keep the responsibility chain explicit:
   1. individual author
   2. their GitHub repository
   3. public commit history
9. Keep the identity layer in TTP even if GitHub remains pseudonymous.
10. Publish the mapping at the TTP layer:
   1. verified real identity
   2. public TTP profile
   3. mapping to GitHub account
   4. public attribution of submissions
11. Keep GitHub unchanged as storage and revision history while TTP remains responsible for identity.
12. Remember GitHub naming constraints on usernames and repository names:
   1. avoid impersonation
   2. avoid deceptive trademark usage
   3. avoid explicit abusive targeting in names

## Extracted Tasks: ValueFlow Connection
1. Connect TTP submissions and licensing surfaces to ValueFlow profit-sharing logic where APC-VF applies.
2. Document and design the minimum viable revenue infrastructure:
   1. public page listing APC-VF licensed works
   2. stated revenue split
   3. "Pay the creator" button or invoice request form
   4. contact info for commercial licensing inquiries
3. Define the better-later ValueFlow automation path:
   1. simple dashboard for self-reported revenue and share calculation
   2. Stripe Connect integration so payment splits happen automatically at the transaction level
4. Pull in relevant implementation considerations from ValueFlow:
   1. query interfaces to existing patent databases (USPTO, EPO, WIPO, etc.)
   2. import of existing patent records and metadata
   3. mapping between patent numbers and ValueFlow identifiers
   4. payment processor integration patterns
   5. revenue recognition automation
   6. audit trail generation
   7. data minimization
   8. pseudonymization where possible
   9. aggregate reporting without individual identification
5. Pull in directly reusable ValueFlow backlog items:
   1. Implement data collection framework
   2. Create visualization dashboards
   3. Set up real-time monitoring
   4. Set up data import/export
   5. Implement API for custom integrations
   6. Document data models
   7. Add API documentation

## Extracted Tasks: IPClaim Repo Hygiene and Terminology
1. Choose one canonical folder layout and delete or archive competing legacy trees.
2. Keep root only for released files; move draft/archive material out of the public root.
3. Replace scratch-style public folder names with intentional archive naming.
4. Standardize naming/layout so the package does not read like “published product + internal archive” mashed together.
5. Standardize license filename conventions across all files.
6. Decide clearly whether each repo is:
   1. a product toolkit
   2. a manifesto/spec repo
   3. or intentionally both with separate layers
7. Tighten `.gitignore` / ignore policy for tooling repos and make timestamp-artifact policy explicit.
8. Simplify workflow recursion logic where GitHub-native behavior already prevents the loop.
9. Tighten README claims so technical descriptions match implementation layers precisely.
10. Keep these three layers separated explicitly in the docs:
    1. what the system proves
    2. what the system governs
    3. what current states/legal systems still do or do not recognize

## Extracted Tasks: IP / Patent Vocabulary Policy
1. Remove “patent” as the conceptual anchor where the repo is describing the new system itself.
2. Standardize around the system’s own vocabulary:
   1. claims
   2. claimants
   3. disclosure
   4. timestamp proof
   5. licensing terms
3. Keep patents in the text only in these roles:
   1. as part of the existing IP system
   2. as a pain-point / problem the new approach improves
   3. in compatibility discussion with existing law
4. Avoid phrasing like:
   1. “this timestamp is the patent”
   2. “this replaces filing a patent”
5. Prefer phrasing like:
   1. “public IP claim system”
   2. “timestamped disclosure”
   3. “authorship, integrity, and timestamped existence”
   4. “removes the need to rely on patents for authorship proof and disclosure priority”
6. Teach the IP hierarchy near the start of the disclosure:
   1. patents
   2. copyright
   3. trademarks
   4. trade secrets
7. Make clear near the beginning that patents are one category within the broader IP system, not the whole system.

## Extracted Tasks: IPClaim Framing and Disclaimer Structure
1. Make the replacement thesis explicit early:
   1. this is not a request to be treated as the old patent system
   2. this is a claim that the old patent system is obsolete where public proof, authorship traceability, timestamped disclosure, and enforceable licensing perform the essential function better
2. Keep the repo framed as a correction layer / successor regime where appropriate.
3. Add or standardize the scope disclaimer:
   1. not legal advice
   2. claims are asserted only to the extent they are validly claimable under applicable law
   3. any elements that cannot legally be claimed are not asserted as exclusive property
   4. purpose is to establish authorship, integrity, and timestamped disclosure
4. State the three-component framework clearly:
   1. IPClaim
   2. stamped proof layer
   3. ValueFlow license
5. Add one clear framing sentence near the top of the README/disclosure that explains the full system in one line.

## Validated Free-Tier Basis
1. Render free web services and free Postgres limits/trial constraints are documented at https://render.com/docs/free and https://render.com/pricing.
2. Render supports EU deployment regions (including Frankfurt) at https://render.com/docs/regions.
3. Neon free-tier limits are documented at https://neon.com/docs/introduction/pro-plan.
4. Neon supports EU region deployment via project region selection at https://neon.com/docs/introduction/regions.

## Scope Decisions Locked
1. Repo shape: one root repo, not split implementation/doc repos.
2. Hosting model: managed free-tier.
3. Data region: EU.
4. Pilot size target: small pilot (up to ~200 registered users, low concurrency).
5. Cold starts: acceptable.
6. Billing: no in-app billing work for pilot; zero-cost infra only.

## Workstream A: Internal Doc Alignment (`TP/docs/internal`)
1. Update `TP/docs/internal/README.md` with a short “adjacent initiative” note that `PatentMake` and `ValueFlow` are in-scope as supporting tracks.
2. Update `TP/docs/internal/PROJECT_BOUNDARIES.md` with a brief “cross-cutting/adjacent initiatives” note clarifying `PatentMake` and `ValueFlow` complement P01-P33 and are not replacing those boundaries.
3. Update `TP/docs/internal/EarthCraft aka PlanetarY Design/THE_PLATFORM_SOURCE_OF_TRUTH.md` with a one-paragraph operational note linking signature/prior-art traceability to `PatentMake` and value-routing logic to `ValueFlow`.
4. Keep changes concise, non-disruptive, and without creating a new project ID.

## Workstream B: Deployment and Privacy Foundation (`TP`)
1. Keep `psycopg[binary]` support so SQLModel can run on Neon Postgres.
2. Keep production guardrails in startup/config:
   1. Fail startup if `PLATFORM_SECRET` is default in non-dev mode.
   2. Fail startup if `PLATFORM_DATABASE_URL` is missing in non-dev mode.
   3. Restrict CORS default away from `*` for non-dev mode.
   4. Fail startup if bridge identity mode is enabled without `PLATFORM_IDENTITY_BRIDGE_SECRET`.
3. Keep deployment artifacts current:
   1. `Dockerfile`
   2. `render.yaml`
   3. `docs/DEPLOY_FREE_EU.md`
4. Keep `.gitignore` coverage for local databases, env files, logs, and identity cert/key material.
5. Keep SQLite local-dev behavior unchanged.

## Workstream C: Verified Identity and Product Controls (`TP`)
1. Require verified identity tokens at registration.
2. Store identity provider, subject key, country code, and verification timestamp on `User`.
3. Enforce one account per verified identity subject.
4. Provide a dev-safe verification endpoint for local testing and a bridge-token model for real Bank ID / government ID deployment.
5. Keep status lifecycle, reporting/export, audit events, pagination, and anti-abuse controls working after the identity change.

## Workstream D: Data Safety Without Paid Services
1. Keep `scripts/backup_postgres.ps1` for manual/Task Scheduler weekly `pg_dump`.
2. Keep `scripts/restore_postgres.ps1` for documented restore path.
3. Keep `docs/BACKUP_AND_RECOVERY.md` current:
   1. Weekly backup routine.
   2. Retention policy.
   3. Recovery drill checklist.
4. Keep `scripts/migrate_sqlite_to_postgres.py` working for one-time migration, if needed.

## Workstream E: Implementation Plan Update in Repo
1. Keep `TP/PILOT_LAUNCH_PLAN.md` as the implementation source of truth.
2. Include:
   1. Phase milestones with owner-ready task checklists.
   2. Free-tier quotas and operating guardrails.
   3. Go/no-go launch gates.
3. Keep `TP/README.md` aligned with identity, deployment, and backup docs.

## Public API / Interface / Type Changes
1. API additions:
   1. `POST /api/identity/dev/verify`
2. API changes:
   1. `POST /api/register` now requires `identity_verification_token`
   2. `GET /api/ideas` supports `limit`, `offset`
   3. `GET /api/ideas/{idea_id}/comments` supports `limit`, `offset`
3. Schema/type changes:
   1. `User` now stores `legal_name`, `identity_provider`, `identity_subject_key`, `identity_country_code`, `identity_verified_at`
   2. `UserResponse` now returns verified identity metadata except the protected subject key itself
4. Config interface changes:
   1. `PLATFORM_ENV`
   2. `PLATFORM_MAX_PAGE_SIZE`
   3. `PLATFORM_RATE_LIMIT_*`
   4. `PLATFORM_IDENTITY_PROVIDER_MODE`
   5. `PLATFORM_IDENTITY_BRIDGE_SECRET`
   6. `PLATFORM_IDENTITY_TOKEN_MAX_AGE`

## Test Cases and Scenarios
1. Unit tests:
   1. Status transition validation and permission enforcement.
   2. Signature generation consistency after edit/status change.
   3. Verified-identity token validation.
   4. One-person-one-account enforcement.
2. API integration tests:
   1. Verified registration/login/me flow.
   2. Idea create/edit/merge/vote/comment flow.
   3. Status update flow with admin and non-admin users.
   4. Report and export endpoint authorization and output format.
3. Migration tests:
   1. Fresh DB bootstrap on Postgres.
   2. SQLite-to-Postgres migration script against sample dataset.
4. Operational tests:
   1. Cold-start smoke test on free hosting.
   2. Backup + restore dry run.
   3. CORS and secret misconfiguration fail-fast behavior.
   4. Verified-identity bridge misconfiguration fail-fast behavior.

## Acceptance Criteria (Pilot-Ready)
1. App is reachable in EU region on free hosting with Neon EU database.
2. All core MVP flows work with verified identity and pass automated tests.
3. Status lifecycle, reporting, and audit endpoints are functional and documented.
4. Backup/restore process is documented and successfully rehearsed once.
5. README and pilot plan docs reflect real deployment paths and constraints.
6. No paid service is required to run the pilot within small-pilot usage limits.
