    [string]$BackupDir = ".\\backups",
    [int]$KeepSnapshots = 8
if ($KeepSnapshots -lt 1) {
    throw "KeepSnapshots must be >= 1"
if (-not (Get-Command pg_dump -ErrorAction SilentlyContinue)) {
    throw "pg_dump was not found in PATH. Install PostgreSQL client tools first."
New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$plainDump = Join-Path $BackupDir "platform-$timestamp.sql"
$zipDump = Join-Path $BackupDir "platform-$timestamp.zip"
Write-Host "Creating backup $plainDump"
& pg_dump --no-owner --no-privileges --format=plain --file="$plainDump" "$DatabaseUrl"
if (-not (Test-Path $plainDump)) {
    throw "Backup file was not created."
Compress-Archive -Path $plainDump -DestinationPath $zipDump -Force
Remove-Item $plainDump -Force
Write-Host "Backup archive created: $zipDump"
Write-Host "Important: Encrypt this archive at rest (BitLocker, encrypted volume, or external key management)."
$archives = Get-ChildItem -Path $BackupDir -Filter "platform-*.zip" | Sort-Object LastWriteTime -Descending
if ($archives.Count -gt $KeepSnapshots) {
    $toDelete = $archives | Select-Object -Skip $KeepSnapshots
    foreach ($item in $toDelete) {
        Write-Host "Removing old snapshot: $($item.FullName)"
        Remove-Item $item.FullName -Force
