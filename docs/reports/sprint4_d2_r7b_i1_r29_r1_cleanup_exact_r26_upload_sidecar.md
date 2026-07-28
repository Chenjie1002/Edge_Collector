# Sprint 4 D2-R7B-I1 R29-R1 Exact R26 Upload Sidecar Cleanup

## Durable manifest

报告名称：Sprint 4 D2-R7B-I1 R29-R1 Exact R26 Upload Sidecar Cleanup
任务名称：D2-R7B-I1 R29-R1 — Cleanup-Only Removal of the Proven R26 Upload Sidecar
执行 Thread：Architecture / Integration
Authority ID：`PM-R29-R1-260728-CLEANUP-01`
Report delivery mode：`REPOSITORY_DURABLE_REPORT`
Exact report path：`docs/reports/sprint4_d2_r7b_i1_r29_r1_cleanup_exact_r26_upload_sidecar.md`
Exact artifact paths：`none`

Docs authority state：`CONSUMED / WRITTEN`
Remote cleanup authority state：`CONSUMED / COMPLETED`
结论：`PASS`
Classification：`EXACT_R26_UPLOAD_SIDECAR_REMOVED`

## Local hard gate

- Project：`/Users/chenjie/Documents/MES/edge-mes-demo`
- `HEAD`：`5fe72282d1b1bcbf602712982e814ef488368122`
- `origin/main`：`5fe72282d1b1bcbf602712982e814ef488368122`
- ahead/behind：`0/0`
- index：empty
- `git diff --check`：PASS
- `git diff --cached --check`：PASS
- `config/mapping.yaml` relative `HEAD`：clean
- local task-owned process count：`0`
- report path before write：`ABSENT`
- `docs/reports`：regular non-symlink directory, uid `501`, mode `0755`
- pre-report status snapshot：`223` entries, SHA-256 `f7e401c5fd9003ef12b355b78da56d914d54a36252a423362afc643539f035c9`

### Local identities and manifests

- `config/mapping.yaml`：`7112` bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`
- R28-R2 accepted report：`12618` bytes, SHA-256 `862db8035c1050c93809c616e6b98234835375622e2cd8d65ae0dcae9f7f8702`
- P2-R2 manifest：fresh `6/6 PASS`
- P2-R3 manifest：fresh `9/9 PASS`
- R26 manifest：fresh `3/3 PASS`
- retained root：`/private/var/folders/tk/bv85b0cs00v5x5x04n5816240000gn/T/d2-r7b-p2-r2.0mW7V5`
- retained root：regular non-symlink directory, uid `501`, mode `0700`
- retained entries：exactly `config`, `config/mapping.yaml`
- retained mapping：regular non-symlink, uid `501`, mode `0600`, `7112` bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`
- SSH key metadata：regular non-symlink, uid `501`, mode `0600`; private-key contents not read

## GitHub reachability

- Single best-effort `git ls-remote origin refs/heads/main`：`VERIFIED / MATCH`
- Observed remote ref：`5fe72282d1b1bcbf602712982e814ef488368122`
- Blocking：`no`

## Accepted prior gate and boundary

R28-R2 was accepted as `PASS / PM-VERIFIED / PM-ACCEPTED` with classification `RETAINED_R26_UPLOAD_IDENTITY_PROVEN`. Its accepted report is the exact report identity recorded above. This task used that identity only as a fresh precondition; it did not inherit eligibility, upload, deployment, rollback, restart, activation or Git authority.

## SSH transaction

- Endpoint：`mari@10.0.0.217:22`
- Identity：`/Users/chenjie/.ssh/edge_pi_codex`
- Frozen options：`-T`, `BatchMode=yes`, `IdentitiesOnly=yes`, `ControlMaster=no`, `ControlPersist=no`, `ForwardAgent=no`, `StrictHostKeyChecking=yes`, `ConnectTimeout=10`, `ServerAliveInterval=5`, `ServerAliveCountMax=2`, `LogLevel=ERROR`
- SSH parent invocation count：`1`
- SSH exit：`0`
- retry/resume/second SSH：`0`
- stdout：one complete authoritative JSON object
- remote host/user：`Pi-5b-Li` / `mari` / uid `1000`
- remote observer mutation count before unlink：`0`
- only external command：`docker inspect edge-mes-collector` (pre and post observation)

## Remote pre-cleanup

- config parent：regular non-symlink directory, realpath exact, `mari/mari`, uid/gid `1000/1000`, mode `0775`, device/inode `2050/518154`
- target `/opt/edge-mes-demo/config/mapping.yaml`：regular non-symlink, realpath exact, `5935` bytes, SHA-256 `86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3`, `mari/mari`, mode `0644`, device/inode `2050/550698`, stable
- exact upload `/opt/edge-mes-demo/config/.mapping.yaml.d2-r7b-new.8de5edb`：regular non-symlink, realpath exact, `7112` bytes, SHA-256 `d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d`, `mari/mari`, mode `0644`, device/inode `2050/550822`, stable
- upload path stat and opened fd：same device/inode; streaming hash and `fstat` before/after stable
- backup：`ABSENT`
- rollback temp：`ABSENT`
- matching sidecars：`1`, only `.mapping.yaml.d2-r7b-new.8de5edb`
- Collector：`edge-mes-collector`, ID `5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524`, running/status `true/running`, image ID `sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a`, configured image `edge-mes-demo-collector`, restart count `0`, started_at `2026-07-23T12:23:25.959624Z`, bind `/opt/edge-mes-demo/config` → `/app/config`, `RW=false`
- remote task process count：`0`
- precondition checks：`10/10 PASS`

## Cleanup mutation

- authorized remote mutation：exactly one
- primitive：`os.unlink(UPLOAD_BASENAME, dir_fd=verified_config_parent_fd)`
- exact basename：`.mapping.yaml.d2-r7b-new.8de5edb`
- final path/fd binding：PASS; both identified device/inode `2050/550822`
- unlink attempts：`1`
- successful unlinks：`1`
- deleted device/inode：`2050/550822`
- remote mutation count：`1`
- all other remote filesystem mutation：`0`
- upload/deploy/rollback：`0`
- eligibility：`0`
- Docker/Compose lifecycle：`0`
- Collector lifecycle：`0`

## Remote post-cleanup

- exact upload path：`ABSENT` by `ENOENT`
- matching sidecars：`0`
- target：`UNCHANGED OLD_EXACT`; `5935` bytes, SHA-256 `86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3`, device/inode `2050/550698`, stable
- backup：`ABSENT`
- rollback temp：`ABSENT`
- Collector：`UNCHANGED`; same ID, status, image, restart count, started_at and read-only bind mount
- remote task process count：`0`
- parent：same realpath, device/inode `2050/518154`, owner/group/mode unchanged; mtime/ctime changed as expected from unlink
- directory entries：only the authorized upload entry removed; no other entry drift
- postcondition checks：`11/11 PASS`

## Final local audit and authority status

- final local `HEAD`/`origin/main`：still frozen commit / `0/0`
- index：empty
- diff checks：PASS
- mapping：clean relative to `HEAD`
- task-owned process count：`0`
- Git mutation：`0`
- changed repository files by this task：only the exact report path above
- pre-existing `.gitignore`, `pm_operating_rules.md`, untracked evidence and other dirty artifacts：preserved; not staged, cleaned, reclassified or modified
- R29-R1 artifacts：`WRITTEN / NOT YET PM-ACCEPTED / UNSTAGED / UNCOMMITTED / UNPUSHED`
- cleanup：`COMPLETED`
- current remote state：`OBSERVED IN CLEANUP TRANSACTION`
- eligibility：`NOT RUN`
- deployment：`NOT RUN`

## Blockers, recommendations and next gate

- Blockers：none for this exact cleanup terminal
- Recommendations：PM should perform durable intake from this exact repository path and independently verify this report's final bytes/SHA; any later eligibility requires separately authorized fresh read-only work
- Next gate：`R29-R1 cleanup report WRITTEN → ChatGPT PM durable cleanup intake`
- Non-inheritance：this PASS does not authorize eligibility, upload, deployment, rollback, restart, activation, runtime-load validation, production acceptance, status/roadmap sync or Git write

## MVP and Thread assessment

- MVP alignment：`MVP-ALIGNED`; this removes only the proven retained R26 upload sidecar and adds no product capability or runtime lifecycle action
- scope expansion：`no`
- output length：`中`
- current Thread can continue carrying the next task：`no`
- next round should start a new Thread：`yes`
- reason：the bounded mutation and durable report are complete; independent PM intake and any later gate require a fresh authority boundary
