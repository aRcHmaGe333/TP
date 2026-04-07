# Backup and Recovery (Pilot)

## Goal
Maintain weekly recoverable snapshots for the free-tier pilot without paid backup services.

## Weekly Backup Routine
1. Install PostgreSQL client tools (`pg_dump`, `psql`) on the operator machine.
2. Run:
`powershell -ExecutionPolicy Bypass -File .\\scripts\\backup_postgres.ps1 -DatabaseUrl \"<PLATFORM_DATABASE_URL>\" -BackupDir \".\\backups\" -KeepSnapshots 8`
3. Verify a new `platform-<timestamp>.zip` archive exists in `backups`.
4. Store the archive on encrypted storage (BitLocker/encrypted volume).

## Retention Policy
1. Keep the latest 8 weekly snapshots.
2. Delete older snapshots automatically (script handles this).
3. Keep one copy off the primary workstation when possible.

## Recovery Procedure
1. Confirm target DB and downtime window.
2. Run:
`powershell -ExecutionPolicy Bypass -File .\\scripts\\restore_postgres.ps1 -DatabaseUrl \"<PLATFORM_DATABASE_URL>\" -BackupArchive \".\\backups\\platform-YYYYMMDD-HHMMSS.zip\"`
3. Validate:
   - Login works.
   - Idea feed returns expected count.
   - Reporting endpoints load.

## Recovery Drill Checklist (Monthly)
1. Restore latest backup into a non-production database.
2. Run application against restored DB.
3. Verify critical flows: register/login, create idea, vote, comment, status update.
4. Record drill date, operator, restore duration, and any failures.
