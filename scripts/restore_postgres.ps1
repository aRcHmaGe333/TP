param(
    [Parameter(Mandatory = $true)]
    [string]$DatabaseUrl,

    [Parameter(Mandatory = $true)]
    [string]$BackupArchive
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
    throw "psql was not found in PATH. Install PostgreSQL client tools first."
}

if (-not (Test-Path $BackupArchive)) {
    throw "Backup archive not found: $BackupArchive"
}

$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("platform-restore-" + [System.Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

try {
    Expand-Archive -Path $BackupArchive -DestinationPath $tempDir -Force
    $sqlFile = Get-ChildItem -Path $tempDir -Filter "*.sql" | Select-Object -First 1
    if (-not $sqlFile) {
        throw "No .sql dump found in archive: $BackupArchive"
    }

    Write-Host "Restoring from $($sqlFile.FullName)"
    & psql "$DatabaseUrl" -f "$($sqlFile.FullName)"
    Write-Host "Restore completed."
}
finally {
    if (Test-Path $tempDir) {
        Remove-Item -Recurse -Force $tempDir
    }
}
