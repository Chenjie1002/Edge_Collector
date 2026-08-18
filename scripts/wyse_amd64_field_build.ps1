param(
    [ValidateSet("all", "api", "collector", "dashboard", "s7-plc-sim", "simulator", "sync-worker")]
    [string]$Service = "all",

    [Parameter(Mandatory = $true)]
    [ValidatePattern('^field-[0-9]{8}-[0-9]{2}(-[A-Za-z0-9_.-]+)?$')]
    [string]$Tag,

    [string]$ExportDirectory = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Tag) -or $Tag -eq "fv1b-a-r1-amd64") {
    throw "Tag must be a new field tag such as field-20260818-01; historical R1 tags are not allowed."
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$Builds = [ordered]@{
    "api" = @{
        Image = "edge-mes-demo-api"
        Dockerfile = "api/Dockerfile"
        Context = "."
    }
    "collector" = @{
        Image = "edge-mes-demo-collector"
        Dockerfile = "collector/Dockerfile"
        Context = "."
    }
    "dashboard" = @{
        Image = "edge-mes-demo-dashboard"
        Dockerfile = "frontend/Dockerfile"
        Context = "frontend"
    }
    "s7-plc-sim" = @{
        Image = "edge-mes-demo-s7-plc-sim"
        Dockerfile = "s7_plc_sim/Dockerfile"
        Context = "s7_plc_sim"
    }
    "simulator" = @{
        Image = "edge-mes-demo-simulator"
        Dockerfile = "simulator/Dockerfile"
        Context = "simulator"
    }
    "sync-worker" = @{
        Image = "edge-mes-demo-sync-worker"
        Dockerfile = "sync_worker/Dockerfile"
        Context = "sync_worker"
    }
}

$Targets = if ($Service -eq "all") { @($Builds.Keys) } else { @($Service) }

Write-Host "Repo root: $RepoRoot"
Write-Host "Target platform: linux/amd64"
Write-Host "Tag: $Tag"
Write-Host "Services: $($Targets -join ', ')"

foreach ($Name in $Targets) {
    $Spec = $Builds[$Name]
    $ImageRef = "$($Spec.Image):$Tag"
    $Dockerfile = Join-Path $RepoRoot $Spec.Dockerfile
    $Context = Join-Path $RepoRoot $Spec.Context

    Write-Host ""
    Write-Host "=== BUILD $Name -> $ImageRef ==="
    & docker buildx build --platform linux/amd64 --load -f $Dockerfile -t $ImageRef $Context
    if ($LASTEXITCODE -ne 0) {
        throw "docker buildx build failed for $Name"
    }

    $Platform = (& docker image inspect $ImageRef --format '{{.Os}}/{{.Architecture}}').Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "docker image inspect failed for $ImageRef"
    }
    if ($Platform -ne "linux/amd64") {
        throw "unexpected image platform for $ImageRef`: $Platform"
    }
    $ImageIdentity = (& docker image inspect $ImageRef --format '{{.Id}} {{.Os}}/{{.Architecture}} {{.Size}}').Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "docker image identity inspect failed for $ImageRef"
    }
    Write-Host "IMAGE $Name $ImageIdentity"

    if ($ExportDirectory) {
        $ResolvedExportDirectory = if ([System.IO.Path]::IsPathRooted($ExportDirectory)) {
            $ExportDirectory
        } else {
            Join-Path $RepoRoot $ExportDirectory
        }
        New-Item -ItemType Directory -Force -Path $ResolvedExportDirectory | Out-Null
        $SafeTag = $Tag -replace '[^A-Za-z0-9_.-]', '_'
        $TarPath = Join-Path $ResolvedExportDirectory "$Name-$SafeTag.tar"
        Write-Host "Exporting one image only: $TarPath"
        & docker save -o $TarPath $ImageRef
        if ($LASTEXITCODE -ne 0) {
            throw "docker save failed for $ImageRef"
        }
        $Hash = (Get-FileHash -Algorithm SHA256 $TarPath).Hash.ToLowerInvariant()
        $Bytes = (Get-Item $TarPath).Length
        Write-Host "EXPORT $Name bytes=$Bytes sha256=$Hash"
    }
}

Write-Host ""
Write-Host "DONE"
Write-Host "Do not aggregate-load all project images on the Wyse 3040. Transfer/load one image at a time."
