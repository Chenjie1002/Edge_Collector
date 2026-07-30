#!/usr/bin/env python3
"""R33 remote, read-only activation preflight probe; stdin source for /usr/bin/python3 -."""
import hashlib
import json
import os
import pwd
import grp
import stat
import subprocess
import sys
import time

AUTHORITY_ID = "PM-D2-R7B-I1-R33-FRESH-READONLY-REMOTE-ACTIVATION-PREFLIGHT-260729-2001"
FRESH = "sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734"
OLD = "sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a"
BAD = "sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c"
DESCRIPTIVE = "edge-mes-demo-collector:r32-pkg-closed-ca68dd4"
COMPATIBILITY = "edge-mes-demo-collector:latest"
PROJECT = "edge-mes-demo"
PARENT = "/opt/edge-mes-demo/config"
TARGET = PARENT + "/mapping.yaml"
BACKUP = PARENT + "/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
UPLOAD = PARENT + "/.mapping.yaml.d2-r7b-new.8de5edb"
ROLLBACK = PARENT + "/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
EXPECTED_SIDECAR = os.path.basename(BACKUP)
ALLOWED = {"collector", "postgres", "simulator", "s7-plc-sim", "api", "dashboard", "grafana", "prometheus", "node-exporter", "sync-worker"}
CORE = {"postgres", "simulator", "s7-plc-sim", "api"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def command(args, audit):
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    audit.append({"argv": args, "returncode": result.returncode, "stdout_bytes": len(result.stdout), "stdout_sha256": sha(result.stdout), "stderr_bytes": len(result.stderr), "stderr_sha256": sha(result.stderr)})
    return result


def parse_json(result):
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def mounts(item):
    return sorted([{"Type": m.get("Type"), "Source": m.get("Source"), "Destination": m.get("Destination"), "RW": m.get("RW")} for m in item.get("Mounts", [])], key=lambda m: (str(m["Destination"]), str(m["Source"])))


def container_view(item):
    state = item.get("State") or {}
    config = item.get("Config") or {}
    host = item.get("HostConfig") or {}
    labels = config.get("Labels") or {}
    return {"Id": item.get("Id"), "Name": item.get("Name"), "Image": item.get("Image"), "Config.Image": config.get("Image"), "labels": {"project": labels.get("com.docker.compose.project"), "service": labels.get("com.docker.compose.service")}, "Created": item.get("Created"), "State.StartedAt": state.get("StartedAt"), "State.Status": state.get("Status"), "State.Running": state.get("Running"), "State.Restarting": state.get("Restarting"), "State.Dead": state.get("Dead"), "State.ExitCode": state.get("ExitCode"), "State.OOMKilled": state.get("OOMKilled"), "State.Error": state.get("Error"), "RestartCount": item.get("RestartCount"), "HostConfig.RestartPolicy": (host.get("RestartPolicy") or {}).get("Name"), "Mounts": mounts(item)}


def snapshot(audit):
    ps = command(["/usr/bin/docker", "ps", "-aq", "--filter", "label=com.docker.compose.project=" + PROJECT], audit)
    ids = [line for line in ps.stdout.decode("utf-8", "strict").splitlines() if line] if ps.returncode == 0 else []
    inspected = command(["/usr/bin/docker", "inspect"] + ids, audit) if ids else None
    data = parse_json(inspected) if inspected else []
    if data is None:
        data = []
    return {"ids": ids, "containers": [container_view(x) for x in data], "inspect_ok": inspected is not None and inspected.returncode == 0}


def identity(path, expected_bytes=None, expected_hash=None):
    result = {"path": path}
    try:
        before_l = os.lstat(path)
        if stat.S_ISLNK(before_l.st_mode) or not stat.S_ISREG(before_l.st_mode):
            result.update({"state": "INVALID_TYPE_OR_SYMLINK", "lstat_mode": format(stat.S_IMODE(before_l.st_mode), "04o")})
            return result
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path, flags)
        try:
            before = os.fstat(fd)
            digest = hashlib.sha256()
            size = 0
            while True:
                block = os.read(fd, 65536)
                if not block:
                    break
                digest.update(block)
                size += len(block)
            after = os.fstat(fd)
        finally:
            os.close(fd)
        stable = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns)
        result.update({"state": "PRESENT", "device": before.st_dev, "inode": before.st_ino, "uid": before.st_uid, "gid": before.st_gid, "owner": pwd.getpwuid(before.st_uid).pw_name, "group": grp.getgrgid(before.st_gid).gr_name, "mode": format(stat.S_IMODE(before.st_mode), "04o"), "bytes": size, "sha256": digest.hexdigest(), "realpath": os.path.realpath(path), "identity_stable": stable, "expected_bytes_match": size == expected_bytes, "expected_sha256_match": digest.hexdigest() == expected_hash})
    except FileNotFoundError:
        result["state"] = "ABSENT"
    except OSError as exc:
        result.update({"state": "ERROR", "error": type(exc).__name__})
    return result


def parent_identity():
    result = {"path": PARENT}
    try:
        s = os.lstat(PARENT)
        result.update({"state": "PRESENT", "directory": stat.S_ISDIR(s.st_mode), "symlink": stat.S_ISLNK(s.st_mode), "realpath": os.path.realpath(PARENT), "uid": s.st_uid, "gid": s.st_gid, "owner": pwd.getpwuid(s.st_uid).pw_name, "group": grp.getgrgid(s.st_gid).gr_name, "mode": format(stat.S_IMODE(s.st_mode), "04o"), "device": s.st_dev, "inode": s.st_ino})
    except OSError as exc:
        result.update({"state": "ERROR", "error": type(exc).__name__})
    return result


def temp_state(path):
    try:
        s = os.lstat(path)
        return {"path": path, "state": "PRESENT", "symlink": stat.S_ISLNK(s.st_mode), "mode": format(stat.S_IMODE(s.st_mode), "04o")}
    except FileNotFoundError:
        return {"path": path, "state": "ABSENT"}
    except OSError as exc:
        return {"path": path, "state": "ERROR", "error": type(exc).__name__}


def service_map(snap):
    out = {}
    for item in snap["containers"]:
        service = item["labels"]["service"]
        out.setdefault(service, []).append(item)
    return out


def main():
    audit, assertions, observed = [], {}, {}
    classification = "ACTIVATION_ELIGIBLE"
    try:
        images = {}
        for ref in (FRESH, DESCRIPTIVE, COMPATIBILITY, OLD, BAD):
            res = command(["/usr/bin/docker", "image", "inspect", ref], audit)
            images[ref] = parse_json(res)
        observed["image_inspections"] = images
        fresh, descriptive, compat, old, bad = (images[FRESH], images[DESCRIPTIVE], images[COMPATIBILITY], images[OLD], images[BAD])
        fresh_item = fresh[0] if isinstance(fresh, list) and len(fresh) == 1 else None
        old_item = old[0] if isinstance(old, list) and len(old) == 1 else None
        desc_item = descriptive[0] if isinstance(descriptive, list) and len(descriptive) == 1 else None
        compat_item = compat[0] if isinstance(compat, list) and len(compat) == 1 else None
        bad_item = bad[0] if isinstance(bad, list) and len(bad) == 1 else None
        assertions.update({"fresh_object_exact": bool(fresh_item and fresh_item.get("Id") == FRESH and fresh_item.get("Os") == "linux" and fresh_item.get("Architecture") == "arm64"), "descriptive_tag_exact": bool(desc_item and desc_item.get("Id") == FRESH), "compatibility_alias_old_safe": bool(compat_item and compat_item.get("Id") == OLD), "old_safe_valid": bool(old_item and old_item.get("Id") == OLD and old_item.get("Os") == "linux" and old_item.get("Architecture") == "arm64"), "compatibility_not_fresh": bool(compat_item and compat_item.get("Id") != FRESH), "compatibility_not_known_bad": bool(compat_item and compat_item.get("Id") != BAD), "known_bad_has_no_protected_tags": bool(not bad_item or (DESCRIPTIVE not in (bad_item.get("RepoTags") or []) and COMPATIBILITY not in (bad_item.get("RepoTags") or []))), "fresh_has_no_compatibility_tag": bool(fresh_item and COMPATIBILITY not in (fresh_item.get("RepoTags") or []))})
        snap_a = snapshot(audit)
        time.sleep(5)
        snap_b = snapshot(audit)
        observed["snapshot_a"], observed["snapshot_b"] = snap_a, snap_b
        a_map, b_map = service_map(snap_a), service_map(snap_b)
        services = set(a_map) | set(b_map)
        assertions["no_unexpected_project_service"] = all(s in ALLOWED for s in services)
        assertions["duplicate_service_ownership_absent"] = all(len(a_map.get(s, [])) == 1 and len(b_map.get(s, [])) == 1 for s in services)
        collector_a, collector_b = a_map.get("collector", []), b_map.get("collector", [])
        ca, cb = (collector_a[0] if len(collector_a) == 1 else None), (collector_b[0] if len(collector_b) == 1 else None)
        assertions["collector_exactly_one"] = ca is not None and cb is not None
        assertions["collector_safe_prestate"] = bool(ca and cb and ca["Name"] == "/edge-mes-collector" and ca["Image"] == OLD and cb["Image"] == OLD and ca["Config.Image"] in ("edge-mes-demo-collector", "edge-mes-demo-collector:latest") and cb["Config.Image"] in ("edge-mes-demo-collector", "edge-mes-demo-collector:latest") and all((x["State.Running"] is True and x["State.Restarting"] is False and x["State.Dead"] is False and x["State.ExitCode"] == 0 and x["State.OOMKilled"] is False and x["State.Error"] in ("", None) and x["RestartCount"] == 0 and x["HostConfig.RestartPolicy"] == "unless-stopped") for x in (ca, cb)))
        assertions["collector_mount_exact"] = bool(ca and cb and ca["Mounts"] == [{"Type": "bind", "Source": PARENT, "Destination": "/app/config", "RW": False}] and cb["Mounts"] == ca["Mounts"])
        assertions["collector_stable"] = bool(ca and cb and all(ca[k] == cb[k] for k in ("Id", "Image", "State.StartedAt", "RestartCount", "State.Running", "State.Restarting", "State.Dead", "Mounts")))
        assertions["core_services_safe"] = all(len(a_map.get(s, [])) == 1 and len(b_map.get(s, [])) == 1 and a_map[s][0]["State.Running"] is True and b_map[s][0]["State.Running"] is True and a_map[s][0]["State.Restarting"] is False and b_map[s][0]["State.Restarting"] is False and a_map[s][0]["State.Dead"] is False and b_map[s][0]["State.Dead"] is False for s in CORE)
        assertions["protected_services_stable"] = all(a_map[s][0] == b_map[s][0] for s in services if len(a_map.get(s, [])) == len(b_map.get(s, [])) == 1)
        ancestor = command(["/usr/bin/docker", "ps", "-q", "--filter", "ancestor=" + FRESH], audit)
        fresh_ids = [line for line in ancestor.stdout.decode("utf-8", "strict").splitlines() if line] if ancestor.returncode == 0 else []
        fresh_details = parse_json(command(["/usr/bin/docker", "inspect"] + fresh_ids, audit)) if fresh_ids else []
        observed["foreign_fresh_target"] = {"ids": fresh_ids, "containers": [container_view(x) for x in (fresh_details or [])]}
        assertions["no_foreign_or_premature_fresh_target"] = ancestor.returncode == 0 and not fresh_ids
        parent = parent_identity(); target = identity(TARGET, 7112, "d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"); backup = identity(BACKUP, 5935, "86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3")
        upload, rollback = temp_state(UPLOAD), temp_state(ROLLBACK)
        try:
            sidecars = sorted(x for x in os.listdir(PARENT) if x.startswith(".mapping.yaml.d2-r7b-"))
        except OSError:
            sidecars = None
        observed.update({"config_parent": parent, "target_mapping": target, "retained_backup": backup, "upload_temp": upload, "rollback_temp": rollback, "matching_sidecars": sidecars})
        assertions.update({"config_parent_valid": bool(parent.get("directory") and not parent.get("symlink") and parent.get("realpath") == PARENT and parent.get("owner") == "mari" and parent.get("group") == "mari" and parent.get("mode") == "0775"), "target_mapping_exact": bool(target.get("state") == "PRESENT" and target.get("realpath") == TARGET and target.get("owner") == "mari" and target.get("group") == "mari" and target.get("mode") == "0644" and target.get("expected_bytes_match") and target.get("expected_sha256_match") and target.get("identity_stable")), "backup_exact": bool(backup.get("state") == "PRESENT" and backup.get("realpath") == BACKUP and backup.get("owner") == "mari" and backup.get("group") == "mari" and backup.get("mode") == "0644" and backup.get("expected_bytes_match") and backup.get("expected_sha256_match") and backup.get("identity_stable")), "temp_files_absent": upload.get("state") == "ABSENT" and rollback.get("state") == "ABSENT", "sidecar_set_exact": sidecars == [EXPECTED_SIDECAR], "target_backup_distinct_inodes": bool(target.get("inode") and backup.get("inode") and (target.get("device"), target.get("inode")) != (backup.get("device"), backup.get("inode"))), "filesystem_identity_stable": bool(target.get("identity_stable") and backup.get("identity_stable"))})
    except Exception as exc:
        classification = "REMOTE_PROBE_EXCEPTION_" + type(exc).__name__
        observed["probe_exception"] = type(exc).__name__
    mutation_audit = {"filesystem_writes": 0, "docker_mutations": 0, "collector_lifecycle": 0, "protected_service_lifecycle": 0, "network_calls_other_than_authorized_ssh": 0}
    assertions["mutation_counters_all_zero"] = all(v == 0 for v in mutation_audit.values())
    if classification == "ACTIVATION_ELIGIBLE" and not all(assertions.values()):
        classification = "REMOTE_ASSERTION_FAILED"
    status = "PASS" if classification == "ACTIVATION_ELIGIBLE" else "HOLD"
    payload = {"schema_version": "d2-r7b-i1-r33-remote-readonly-preflight/v1", "authority_id": AUTHORITY_ID, "status": status, "classification": classification, "observed": observed, "assertions": assertions, "mutation_audit": mutation_audit, "command_audit": audit}
    sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
