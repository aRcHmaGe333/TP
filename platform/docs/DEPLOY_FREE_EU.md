# Deploy Guide (Free-Only, EU)
This guide targets a zero-cost pilot deployment:
- App hosting: Render Free Web Service (Frankfurt region).
- Database: Neon Free Postgres (EU region).
## 1) Create Neon Free Postgres (EU)
1. Create a Neon project and select an EU region.
2. Create a database and capture the connection string.
3. Keep this URL for `PLATFORM_DATABASE_URL`.
Example format:
`postgresql+psycopg://USER:PASSWORD@HOST/DBNAME?sslmode=require`
## 2) Create Render Free Web Service (Frankfurt)
1. Connect your repo/service to Render.
2. Set region to Frankfurt.
3. Use Docker with `render.yaml` in this folder.
4. Set plan to Free.
## 3) Environment Variables
Set these in Render:
- `PLATFORM_ENV=prod`
- `PLATFORM_SECRET=<long-random-secret>`
- `PLATFORM_DATABASE_URL=<neon-eu-url>`
- `PLATFORM_CORS_ORIGINS=https://<your-render-domain>`
- `PLATFORM_ADMIN_DISPLAY_NAMES=<comma-separated-admin-names>`
Recommended guardrails:
- `PLATFORM_MAX_PAGE_SIZE=50`
- `PLATFORM_DEFAULT_PAGE_SIZE=20`
- `PLATFORM_MAX_REQUEST_BYTES=262144`
- `PLATFORM_RATE_LIMIT_WINDOW_SECONDS=60`
- `PLATFORM_RATE_LIMIT_REGISTER_PER_IP=20`
- `PLATFORM_RATE_LIMIT_LOGIN_PER_IP=60`
- `PLATFORM_RATE_LIMIT_IDEA_PER_IP=30`
- `PLATFORM_RATE_LIMIT_IDEA_PER_USER=20`
- `PLATFORM_RATE_LIMIT_VOTE_PER_IP=120`
- `PLATFORM_RATE_LIMIT_VOTE_PER_USER=60`
- `PLATFORM_RATE_LIMIT_COMMENT_PER_IP=60`
- `PLATFORM_RATE_LIMIT_COMMENT_PER_USER=40`
## 4) Startup Validation Behavior
In `prod` mode the app will fail startup if:
- `PLATFORM_SECRET` is default.
- `PLATFORM_DATABASE_URL` is missing.
- `PLATFORM_CORS_ORIGINS` is missing or contains `*`.
## 5) Launch Smoke Test
1. `GET /` returns UI.
2. Register and log in.
3. Create idea, vote, comment, and merge.
4. `PATCH /api/ideas/{id}/status` works for author/admin.
5. `GET /api/reports/summary` returns metrics.
6. Admin can access:
   - `GET /api/reports/export.csv`
   - `GET /api/audit-events`
## 6) Free-Tier Operating Notes
- Cold starts are expected on free web services.
- Keep pilot traffic small (about 200 users, low concurrency).
- Review quotas monthly in both Render and Neon dashboards.
