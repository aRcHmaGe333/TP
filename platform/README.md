# Innovative Feedback Platform
A FastAPI web application for transparent, signed requirement elicitation. Users register with a display name, create or merge requirements, vote, comment, and move requirements through a status lifecycle. Submissions are signed and key actions are captured in an append-only audit stream.
## Running locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn platform.main:app --reload
Then open http://localhost:8000.
Default local behavior:
- `PLATFORM_ENV=dev` (implicit default)
- SQLite at `platform.db` when `PLATFORM_DATABASE_URL` is not set
- CORS defaults to `*` in dev only
## Pilot deployment (free-only, EU)
Use:
- `render.yaml`
- `Dockerfile`
- `docs/DEPLOY_FREE_EU.md`
Production startup guardrails (`PLATFORM_ENV=prod`):
- Fails startup if `PLATFORM_SECRET` is default.
- Fails startup if `PLATFORM_DATABASE_URL` is missing.
- Fails startup if `PLATFORM_CORS_ORIGINS` is missing or contains `*`.
## Key config knobs
- `PLATFORM_ENV`: `dev` or `prod`.
- `PLATFORM_SECRET`: token signing secret.
- `PLATFORM_DATABASE_URL`: SQLAlchemy database URL.
- `PLATFORM_CORS_ORIGINS`: comma-separated allowlist.
- `PLATFORM_SESSION_MAX_AGE`: token lifetime seconds.
- `PLATFORM_ADMIN_DISPLAY_NAMES`: comma-separated admin display names.
- `PLATFORM_MAX_PAGE_SIZE`: hard cap for paginated endpoints.
- `PLATFORM_DEFAULT_PAGE_SIZE`: default page size when `limit` is omitted.
- `PLATFORM_MAX_REQUEST_BYTES`: request-body size guard (header-based).
- `PLATFORM_RATE_LIMIT_*`: rate-limit knobs for register/login/idea/vote/comment flows.
## Features
- Identity creation with per-user fingerprints and signed tokens
- Signed idea creation, editing, merging, and verification metadata
- Status lifecycle (`submitted`, `acknowledged`, `in_progress`, `resolved`)
- Upvotes/downvotes with live scores
- Comment threads with signed posts
- Reporting summary endpoint
- Admin CSV export endpoint
- Admin audit event endpoint
- Pagination on idea and comment listing endpoints
- Baseline anti-abuse controls (request-size + in-memory rate limiting)
- Embedded spec viewer sourced from `segment_000.md`
- Sorting by score or recency and tag labeling for discoverability
## Pilot operations docs
- `PILOT_LAUNCH_PLAN.md`
- `docs/BACKUP_AND_RECOVERY.md`
## Data migration and safety scripts
- `scripts/migrate_sqlite_to_postgres.py`
- `scripts/backup_postgres.ps1`
- `scripts/restore_postgres.ps1`
