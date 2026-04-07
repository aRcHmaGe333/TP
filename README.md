# The Transparency Platform (TTP)

Single repo for The Transparency Platform (TTP): the runnable FastAPI product lives at repo root, internal strategy and source materials live in `docs/internal`, and public-facing positioning lives in `docs/public`.

## Running locally

```bash
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open `http://localhost:8000`.

Default local behavior:
- `PLATFORM_ENV=dev`
- SQLite at `platform.db` when `PLATFORM_DATABASE_URL` is not set
- CORS defaults to `*` in dev only

## Repo layout
- App code: `main.py`, `auth.py`, `config.py`, `database.py`, `models.py`, `schemas.py`, `identity.py`
- Static UI: `static/`
- Tests: `tests/`
- Scripts: `scripts/`
- Ops docs: `docs/DEPLOY_FREE_EU.md`, `docs/BACKUP_AND_RECOVERY.md`
- Internal docs: `docs/internal/`
- Public docs: `docs/public/`

## Verified identity

TTP now requires verified identity at registration. No verified person means no account, and one verified person maps to one account.

Local/dev flow:
- `POST /api/identity/dev/verify` issues a short-lived dev verification token for `bankid` or `government_id`
- `POST /api/register` requires `identity_verification_token`

Production flow:
- Set `PLATFORM_IDENTITY_PROVIDER_MODE=bridge`
- Set `PLATFORM_IDENTITY_BRIDGE_SECRET`
- Have your Bank ID or government ID gateway mint short-lived verification tokens that TTP can verify

## Pilot deployment

Use `render.yaml`, `Dockerfile`, and `docs/DEPLOY_FREE_EU.md`.

Production startup guardrails (`PLATFORM_ENV=prod`):
- Fails startup if `PLATFORM_SECRET` is default
- Fails startup if `PLATFORM_DATABASE_URL` is missing
- Fails startup if `PLATFORM_CORS_ORIGINS` is missing or contains `*`
- Fails startup if bridge identity mode is enabled without `PLATFORM_IDENTITY_BRIDGE_SECRET`

## Features
- Verified-identity registration, signed login, ideas, comments, merges, and audit events
- Status lifecycle: `submitted`, `acknowledged`, `in_progress`, `resolved`
- Voting, comments, pagination, reporting, CSV export, and admin audit access
- Baseline anti-abuse controls: request-size guard plus in-memory rate limits
- Embedded spec viewer sourced from `segment_000.md`

## Ops docs
- `PILOT_LAUNCH_PLAN.md`
- `docs/DEPLOY_FREE_EU.md`
- `docs/BACKUP_AND_RECOVERY.md`

## Scripts
- `scripts/migrate_sqlite_to_postgres.py`
- `scripts/backup_postgres.ps1`
- `scripts/restore_postgres.ps1`
