# Pilot Launch Plan (Free-Only, EU)
## Target Outcome
Launch a pilot-ready requirement intelligence product on free infrastructure in EU region with operational safeguards, reporting, and auditability.
## Constraints
1. Zero paid infrastructure.
2. EU hosting/data region.
3. Small pilot (around 200 users, low concurrency).
4. Cold starts are acceptable.
## Phase 1: Foundation
1. Deployment
- Render free web service in Frankfurt.
- Neon free Postgres in EU region.
- `render.yaml` and `Dockerfile` used as deployment source.
2. Runtime controls
- `prod` startup validation for secret, DB URL, and CORS allowlist.
- Request size guard (`PLATFORM_MAX_REQUEST_BYTES`).
- Pagination guard (`PLATFORM_MAX_PAGE_SIZE`, `PLATFORM_DEFAULT_PAGE_SIZE`).
- In-memory rate limiting for register/login/post/vote/comment.
3. Documentation
- Deployment runbook: `docs/DEPLOY_FREE_EU.md`.
- Backup runbook: `docs/BACKUP_AND_RECOVERY.md`.
## Phase 2: Product Readiness
1. Status lifecycle
- `submitted -> acknowledged -> in_progress -> resolved`.
- Author/admin update support via `PATCH /api/ideas/{idea_id}/status`.
2. Reporting and export
- `GET /api/reports/summary`.
- Admin export: `GET /api/reports/export.csv`.
3. Auditability
- Append-only `AuditEvent` table for key actions.
- Admin audit listing: `GET /api/audit-events`.
## Phase 3: Data Safety
1. Weekly backups via `scripts/backup_postgres.ps1`.
2. Restore utility via `scripts/restore_postgres.ps1`.
3. One-time data migration utility via `scripts/migrate_sqlite_to_postgres.py`.
## Phase 4: Launch Gate
1. Smoke tests on deployed environment.
2. Admin endpoints verified.
3. Backup + restore drill completed once.
4. Pilot cohort onboarding checklist prepared.
## Go / No-Go Criteria
Go if all are true:
1. Service deploys in EU and stays within free-tier limits.
2. Core flows pass automated tests.
3. Reporting and audit endpoints work for admin users.
4. Backup and restore process is proven.
No-Go if any are true:
1. Startup fails due to missing production config.
2. DB connectivity or migrations are unstable.
3. Core user flows regress.
4. No recent successful backup.
## Operational Guardrails
1. Keep CORS restricted to known frontend domains.
2. Keep admin users limited via `PLATFORM_ADMIN_DISPLAY_NAMES`.
3. Review rate-limit defaults monthly and adjust only with incident notes.
4. Keep pilot scope fixed; defer non-critical features until post-pilot review.
