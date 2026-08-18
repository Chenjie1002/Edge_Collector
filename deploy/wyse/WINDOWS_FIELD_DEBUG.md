# Windows / Wyse amd64 Field Debug Handoff

Date: 2026-08-18
Purpose: carry the Edge MES x86/Wyse debug capability from the MacBook development environment to a Windows field-debug laptop without putting Docker image binaries into Git history.

This is a non-mainline durable handoff. It prepares a Windows Codex field-debug checkout and
rebuildable Wyse images; it does not transfer runtime, real-PLC, production, FV2 or FV3 authority.

```text
HANDOFF_CLASS                 = FIELD_DEBUG_ENVIRONMENT
TARGET_ENVIRONMENT            = WINDOWS_CODEX + WYSE_LINUX_AMD64
MAINLINE_PM_AUTHORITY_TRANSFER = NO
REAL_PLC_AUTHORITY_TRANSFER   = NO
WYSE_RUNTIME_AUTHORITY_TRANSFER = NO
FV2_AUTHORITY                 = NO
FV3_AUTHORITY                 = NO
```

## 1. What goes through Git

Git/GitHub is the source of truth for editable and rebuildable assets:

- application source code;
- Dockerfiles and dependency manifests;
- `deploy/wyse/docker-compose.wyse-r1.yml`;
- `deploy/wyse/docker-compose.wyse-field-tags.yml`;
- Wyse deployment READMEs;
- x86/FV build and validation reports already tracked by Git;
- PowerShell build/export helper `scripts/wyse_amd64_field_build.ps1`.

Docker image tar archives do **not** belong in Git. Both `*.tar` and `*.tgz` are offline-only artifacts,
and the repository `.gitignore` already excludes them. They must never be committed.

## 2. What should also be carried offline

For field work, keep a second artifact set containing the currently accepted amd64 images exported one image per tar file.

Reason:

- Git proves which source can be rebuilt;
- a rebuilt image can differ because of dependency/base-image resolution;
- the offline tar files provide a known-good rollback/start point when field network access or Docker builds are unavailable.

Wyse 3040 field constraints are `linux/amd64`, RAM approximately `1.8 GiB`, and `2 GiB` swap.
An earlier aggregate load caused OOM, reboot, and Docker image-store/layer corruption.
The field rule is **ONE IMAGE AT A TIME**: never create or load one aggregate six-project-image archive.
Transfer/load each image separately and re-check RAM, swap, and OOM state before the next image.

Historical accepted R1 project image names:

```text
edge-mes-demo-api:fv1b-a-r1-amd64
edge-mes-demo-collector:fv1b-a-r1-amd64
edge-mes-demo-dashboard:fv1b-a-r1-amd64
edge-mes-demo-s7-plc-sim:fv1b-a-r1-amd64
edge-mes-demo-simulator:fv1b-a-r1-amd64
edge-mes-demo-sync-worker:fv1b-a-r1-amd64
```

Do not rebuild new source under those historical R1 tags. Use a new field tag such as:

```text
field-20260818-01
field-20260818-02
```

This keeps the historical R1 image identity distinguishable from later field rebuilds.

## 3. Windows prerequisites

Recommended Windows field laptop:

1. Git for Windows.
2. Docker Desktop using Linux containers / WSL2 backend.
3. PowerShell 5.1+ or PowerShell 7.
4. OpenSSH client (`scp`) or WinSCP for file transfer to the Wyse.
5. Docker Buildx, available as `docker buildx`.

Docker must be able to build `linux/amd64` images.

Check:

```powershell
docker version
docker buildx version
docker info --format '{{.OSType}} {{.Architecture}}'
```

Expected Docker container OS for this workflow: `linux`.

## 4. Obtain the field branch on Windows

After the field branch has been pushed to GitHub:

```powershell
git clone https://github.com/Chenjie1002/Edge_Collector.git
cd Edge_Collector
git fetch origin
git switch --track origin/field-debug/windows-wyse-x86-20260818
```

For an existing clone:

```powershell
git fetch origin
git switch field-debug/windows-wyse-x86-20260818
git pull --ff-only
```

Windows Codex mandatory read order:

1. `AGENTS.md`
2. `deploy/wyse/WINDOWS_FIELD_DEBUG.md`
3. `deploy/wyse/README-r1.md`
4. `docs/reports/fv1b_a_r1_wyse_amd64_bundle_refresh_report_20260817.md`
5. Current field-branch `git status --short` and `git rev-parse HEAD`
6. Task-specific source and tests for the current onsite defect

Before changing anything onsite, record:

```powershell
git status --short
git rev-parse HEAD
git log -5 --oneline
```

## 5. Build only the service that changed

The helper builds Linux amd64 images from the same Dockerfile/context boundaries used by the accepted x86 package flow.

Examples:

```powershell
# Collector only
.\scripts\wyse_amd64_field_build.ps1 `
  -Service collector `
  -Tag field-20260818-01

# API only
.\scripts\wyse_amd64_field_build.ps1 `
  -Service api `
  -Tag field-20260818-01

# All six project images when a complete refresh is genuinely required
.\scripts\wyse_amd64_field_build.ps1 `
  -Service all `
  -Tag field-20260818-01
```

Do not rebuild all six images after every field edit. Normally rebuild only the service whose source/dependency surface changed.

## 6. Build and export a portable image tar

The same helper can export each built image as a separate tar:

```powershell
.\scripts\wyse_amd64_field_build.ps1 `
  -Service collector `
  -Tag field-20260818-01 `
  -ExportDirectory artifacts\wyse
```

The helper prints the tar byte length and SHA-256. Record both before transfer.

Example output path:

```text
artifacts\wyse\collector-field-20260818-01.tar
```

`*.tar` and `*.tgz` are ignored by Git and must not be committed.

## 7. Keep a known-good MacBook image backup before going onsite

Before leaving for the field, export the accepted MacBook amd64 images as **separate files** to an external disk/USB drive. Use `docker save` once per image and calculate SHA-256 for each file.

Example for one image on macOS:

```bash
docker save -o edge-mes-demo-collector-fv1b-a-r1-amd64.tar \
  edge-mes-demo-collector:fv1b-a-r1-amd64
shasum -a 256 edge-mes-demo-collector-fv1b-a-r1-amd64.tar
```

Repeat only for the images you want as offline fallback. Do not aggregate them into one archive for Wyse loading.

## 8. Transfer one rebuilt image from Windows to Wyse

Example using OpenSSH from PowerShell:

```powershell
scp .\artifacts\wyse\collector-field-20260818-01.tar <user>@<wyse-ip>:/home/<user>/
```

On the Wyse, verify the transferred file before loading:

```bash
sha256sum ~/collector-field-20260818-01.tar
free -h
swapon --show
```

Then load **one image only**:

```bash
docker load -i ~/collector-field-20260818-01.tar
docker image inspect edge-mes-demo-collector:field-20260818-01 \
  --format '{{.Id}} {{.Os}}/{{.Architecture}} {{.Size}}'
```

Expected platform: `linux/amd64`.

Check resource/OOM state again before any next image load.

## 9. Select a field image tag without rewriting the historical R1 Compose

`docker-compose.wyse-r1.yml` remains the historical R1 base. Do not edit its historical image tags merely to deploy a new field build.

Use the tag-only override:

```text
deploy/wyse/docker-compose.wyse-field-tags.yml
```

Example for a Collector-only field build on the Wyse:

```bash
export WYSE_COLLECTOR_TAG=field-20260818-01

docker compose \
  -f deploy/wyse/docker-compose.wyse-r1.yml \
  -f deploy/wyse/docker-compose.wyse-field-tags.yml \
  config --quiet
```

Only after the intended field deployment/lifecycle action is explicitly approved, the same pair of Compose files can select the new Collector image. The override changes image tags only; it does not itself grant lifecycle, remote, PLC, DB-write or Read_Done authority.

Each project image has its own optional tag variable:

```text
WYSE_API_TAG
WYSE_COLLECTOR_TAG
WYSE_DASHBOARD_TAG
WYSE_S7_PLC_SIM_TAG
WYSE_SIMULATOR_TAG
WYSE_SYNC_WORKER_TAG
```

Unset variables fall back to the historical `fv1b-a-r1-amd64` tags.

## 10. Field source-change workflow

Preferred onsite loop:

```text
Git field branch
  -> record current HEAD
  -> make one bounded source change
  -> run focused tests
  -> commit the source change
  -> build only the changed service as linux/amd64
  -> inspect the image and confirm linux/amd64
  -> export one image tar
  -> record image tag + image ID + tar bytes + SHA-256
  -> transfer one image
  -> load one image
  -> select it through the field tag override
  -> perform the separately authorized runtime/PLC validation
```

If a field change fails, Git history tells which source commit produced the image, and the known-good offline image tar provides the rollback object.

## 11. Current field context

Current packaging baseline when this handoff was prepared:

```text
source repository = https://github.com/Chenjie1002/Edge_Collector.git
source HEAD       = 4e11fb595f458885db537d32be2a5e1eb9621f5f
platform target   = linux/amd64
Wyse role         = debug / field validation only
```

Current real-PLC target identified by Owner:

```text
Siemens CPU = S7-315-2 PN/DP
MLFB        = 6ES7315-2EH14-0AB0
```

The real-PLC data contract/runtime may continue to evolve during field preparation. Do not treat the historical V-PLC R1 mapping as proof of real-PLC addresses.

## 12. Authority boundary for the next Windows Codex

This handoff authorizes the Windows Codex to read the field branch, make bounded source changes,
run focused local tests, rebuild only the changed `linux/amd64` project image, inspect it, and
export one image tar for separately controlled transfer. It does not authorize Windows Docker
Compose lifecycle, SSH, Wyse deployment or mutation, real PLC connection/read/write, `Read_Done`,
FV2 or FV3. Windows Codex must wait for a new Owner/Main PM authority before any runtime or PLC
action. Preserve `NO_DB_COMMIT -> NO_READ_DONE`.

## 13. Important safety / traceability rules

- Git branch stores rebuildable source and records, not image binaries.
- Image tar files are portable field artifacts, not Git artifacts.
- Keep historical R1 tags immutable in meaning.
- Give every field rebuild a new tag.
- Build only `linux/amd64` for the Wyse.
- Load images into Wyse **ONE IMAGE AT A TIME**.
- Do not infer real PLC write authority from image availability or Compose configuration.
- Preserve `NO_DB_COMMIT -> NO_READ_DONE` for real PLC integration.
