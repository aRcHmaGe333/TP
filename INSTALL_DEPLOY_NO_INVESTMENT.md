# No-Investment Installation and Deployment Guide

## 1) Build the platform files from the merged repository documents

```bash
python scripts/build_platform_from_merged.py
```

This creates the runnable project in `platform/`.

## 2) Local installation

```bash
cd platform
python -m venv .venv
source .venv/bin/activate   # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3) Enable required configuration

Set environment variables:

```bash
export PLATFORM_ENV=dev
export PLATFORM_SECRET='change-this-to-a-long-random-value'
export PLATFORM_DATABASE_URL='sqlite:///./platform.db'
export PLATFORM_CORS_ORIGINS='http://localhost:8000'
export PLATFORM_ADMIN_DISPLAY_NAMES='admin'
export PLATFORM_MAX_PAGE_SIZE='50'
export PLATFORM_DEFAULT_PAGE_SIZE='20'
export PLATFORM_MAX_REQUEST_BYTES='262144'
```

## 4) Run locally

```bash
uvicorn platform.main:app --host 0.0.0.0 --port 8000
```

Open:
- App UI: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`

## 5) Use the platform (pilot workflow)

1. Register a user.
2. Log in and keep the bearer token.
3. Create an idea.
4. Vote and comment on ideas.
5. Merge related ideas if needed.
6. Update idea status (`submitted -> acknowledged -> in_progress -> resolved`).
7. Use admin user(s) for report export and audit event access.

## 6) Deploy with zero-cost starting setup (EU)

### A) Database (Neon Free, EU)
1. Create a free Neon project in an EU region.
2. Copy connection string:
   `postgresql+psycopg://USER:PASSWORD@HOST/DBNAME?sslmode=require`

### B) App hosting (Render Free, Frankfurt)
1. Push this repo to GitHub.
2. In Render, create a Web Service from the repo.
3. Use Docker and point to `platform/Dockerfile`.
4. Set region: Frankfurt.
5. Set plan: Free.
6. Optionally import values from `platform/render.yaml`.

### C) Production environment variables
Set in Render:

```bash
PLATFORM_ENV=prod
PLATFORM_SECRET=<long-random-secret>
PLATFORM_DATABASE_URL=<neon-eu-url>
PLATFORM_CORS_ORIGINS=https://<your-render-domain>
PLATFORM_ADMIN_DISPLAY_NAMES=<comma-separated-admin-names>
PLATFORM_MAX_PAGE_SIZE=50
PLATFORM_DEFAULT_PAGE_SIZE=20
PLATFORM_MAX_REQUEST_BYTES=262144
```

### D) Deploy and smoke test
1. Trigger deploy.
2. Confirm `/` loads.
3. Register/login.
4. Create idea, vote, comment, merge.
5. Confirm reports endpoint works.
6. Confirm admin-only exports/audit endpoints work.
