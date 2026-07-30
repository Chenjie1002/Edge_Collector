#!/usr/bin/env python3
import base64, hashlib, json, os, pwd, grp, stat, subprocess, sys, time, zlib

AUTHORITY_ID = "PM-D2-R7B-I1-R34-R2-CORRECTED-CANONICAL-ACTIVATION-260729-2123"
FRESH = "sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734"
OLD = "sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a"
BAD = "sha256:7b94217f509619d1bdd63a786cabc3d2632ec84cca455de6dcecd80a6879c55c"
DESCRIPTIVE, ALIAS = "edge-mes-demo-collector:r32-pkg-closed-ca68dd4", "edge-mes-demo-collector:latest"
PROJECT, COMPOSE, PARENT = "edge-mes-demo", "/opt/edge-mes-demo/docker-compose.yml", "/opt/edge-mes-demo/config"
TARGET = PARENT + "/mapping.yaml"
BACKUP = PARENT + "/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
UPLOAD, ROLLBACK = PARENT + "/.mapping.yaml.d2-r7b-new.8de5edb", PARENT + "/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
_B64 = (
"eJzVWW1vI7cR/i/6bEnkcPi234pLgARFmiIxUCBFUQzJoW97slbdXV1jHO6/d9av67Ns2YaRwIZhi7skhxw+z8wz1JdF7rYjtVvuh0Xzzy+LD922tmerH8/pjBfNgssZL895WBY+75a0axcniw8908hF3oICt1R+CeZUqcZAY9zKOacgKgO/SdcfumG8nvEXHkbqx793mzZfyNj9dsPDsBzGbreTyU4WP04zauCAOiFlY8jbHIzNzEFXVSo6xpJySdEESFZlssqCqbZSUZCtVzZM81wvffhIYF0TqzLVeJWMr8XWAqXUgowc2WHB7JJTRkPUir3R2voQgkU0XrtgstYy40/dfjteuec72UW7pbHttmJiTbvdOl/uT7r98o9FU2kz8Mni127f52kR6243ru858a7/6cVu6pLabVl8/dfJ4m90fjnktvuVu68d92FaxKJRMvko7l99x1Tu7F0++r7vu15mWNw++L2VcYVnw37++ae/tpsNfzv22kq7Pfv2xX67vXw69vvbh79Ofbn8ZTwIAr+K1noDEfC3xWzIuBcnLvrrCU8WG0q8kUdfFru++w/n8VvASZ+B+8/tpSsnb3z9enIEormTzeVR/PAIUDU0YBqwKw2oAwYbXwVUmxQnV0NyWqtIxqkUfCo1aqNVyeQEc6BChOA9EBiLMcdEuZQiOAV8CFSVak5UbCICV5K2DkEblwP6UnLOoJUPSA6sd54ikUkxo1borSdhzJ8I1LnT3xFcb6EQbXRvitU7hzyNWBo+po760my6TJvDkIVTFRt0DYaVPBNSgT2C2G67rNRu9j3foNUJ+oxOEjQD2RyRCSHVIGFOMaWsHFXnikeXBE1suXo2KgCoHHwkPoBWKkkRKxWdCwrRmyzQJZ0jeV2DwZRdpkwcoqqESewgFBZMU7DVBDtH6yFI3brmPUFqdlTeKwVWufiGqLrzySFUnfVUaUvr6//NRmwO4wFMuaW2pwobZRrrVyZKtkYdzavCoJwtAirJnMCQi7IE4E2ytlpJ11MyVylWVxF8lT+q1lQ4kTOSxrFqOBAGi06Oo/aGnUYsUVK3HLQP7KuOGskEX5L4jcUqOe2pavnokmT3yNo+GQZ5zDf+WYvHP7eDvLg6ihcFxZtJvg2OJw8s7od+LTvr+c7uPolL13kvrjx/reG74Ufsf6Z+vWnTbMGTvWskP2Gu0EiP7fIQX2fzvwu2CgniqTYN+kstoH3wIhLtG7L1xiOHuCrjz9db2emSf991srT+SbriqfKNjo21K9EAstYYXkfXiCYaUzGjBG1gV0WqSzJwgVU1MQQU1SJ6uyTpYnItor4nLawcMNZS0kO6Wmcso+TP4An0xEobqbBkFEbtRSNVYmsk/IsIAozowSIlTRCcygD5Sbr2XTfW4TGOHAf/R/HPxPP82BTX754zzXDx6EKuXh2lyL3zfk9EuYWfXymlvJRK4Q15ct8tB9ki/j/reWi0e5QfVlbXaLMCgbEoe3NMIx3mR0omkeSVwC5CdiHpSXCLmkeIUn0GjFEVk4JLurpios3gEyhF1eYkUuchP2p0uqgogj1zKcZ7L1UAV02UTOXg5WN2RswaLMbpGhXFwJNIS96LXnqSHzfB/cZB/91cxu2XBfmbwcd5ULr8ifslb8f+Yte123HZbtuxpFV5fhoraT0Neg5fZgt7T1S5QiKuwBlnUH7ekCu3Lnk0qUx/ePzI++EFGQWcNfZ1GUWZgpI9kKwW8Io+00IayaTVZFbAouZYpHABH2uVHEJWYJ6SJ1eqpACqDxmTGYCzZlI1OF8NIUdXQqnG5OSkuvAcROr5UJP2VWWXfBZRWS8rZOP5qAC8c9GL1de9oUfY8sDMc/n4qI2DJLln5R3R5Ap+bhWDVVopfMuUMnPK8RujwS93m7wc2vPDVImnChphtbarABqCMeFVTCmgOVoph4JUxT6lYpjNdKmDsv2ikkXBM8J04YnCDoPZygvW2qjkpWh+yBQjKorYhOzAlCAJSFXvbY0WjbbsjElaUrXWIKV8FmZkyWohe+vAAoAJf9CN0UNqTHO/PFF9lmN6DiXuHei7ocQNzEBKch8MamfhDSkxc8ozKNGe7yV7HLxEvWSvBtFajVIr9A4C4CvLEcOJNU81gQgo7ymj4DciVTYKnQR6Szr6FLSDapX0pqyMEzmVsEp1Yg/cHgTEUCB4l6XmiDklzoVQ0gRFAk+WVbAkJZDGQgkkDUFiU4pyUuXI7594iTp3+rtB7Q0UwKyURHJ0Lr5lDX3nk2eA9mKbl//r+k/8KGxvqwS0VtsQX3f176zOCkDqgaQjRnBeOUshkFTAquZJ9FRMiZIT4HkJ8lXVxCBjoigXMAcuU52MKlkkTJJ63DJJXZC9ztFVrFXKb1eKc9LLZyXvRQyJIQEvWcugwx8VyA+i9p7X3xFur7AAduWVlGcuvG20nXnl6+S3tkxnc08ty4D5t53SnIdDac6/YpLm/A5/as5QKM35zY4054WsNOfaQ5rzW9vFtLrtsJMt/bv7dOW6r/8HqxZwxA=="
# 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"
)
EXPECTED_SNAPSHOT = json.loads(zlib.decompress(base64.b64decode(_B64)).decode("utf-8"))
SERVICES = {"collector", "postgres", "simulator", "s7-plc-sim", "api", "dashboard", "grafana", "prometheus", "node-exporter", "sync-worker"}
COMMAND_PLAN = ("aggregate_image_inspect", "pre_project_ps", "pre_aggregate_inspect", "fresh_ancestor_lookup", "tag", "alias_inspect", "collector_only_compose", "post_project_ps", "post_aggregate_inspect")
AUDIT, HISTORY, OBS, ASSERT = [], [], {}, {}
MUT = {"tag_mutation_count": 0, "compose_recreate_count": 0, "collector_lifecycle_count": 0, "protected_service_lifecycle_count": 0, "rollback_count": 0, "cleanup_count": 0}
def sha(b): return hashlib.sha256(b).hexdigest()
def run(argv, category):
    p = subprocess.run(argv, cwd="/opt/edge-mes-demo" if category == "compose" else None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    AUDIT.append({"argv": argv, "category": category, "returncode": p.returncode, "stdout_bytes": len(p.stdout), "stderr_bytes": len(p.stderr), "stdout_sha256": sha(p.stdout), "stderr_sha256": sha(p.stderr)})
    return p
def parsed(p):
    try: return json.loads(p.stdout.decode("utf-8", "strict")) if p and p.returncode == 0 else None
    except (UnicodeDecodeError, json.JSONDecodeError): return None
def view(x):
    s, c, h, l = x.get("State") or {}, x.get("Config") or {}, x.get("HostConfig") or {}, (x.get("Config") or {}).get("Labels") or {}
    return {"Id":x.get("Id"),"Name":x.get("Name"),"Image":x.get("Image"),"Config.Image":c.get("Image"),"labels":{"project":l.get("com.docker.compose.project"),"service":l.get("com.docker.compose.service")},"Created":x.get("Created"),"State.StartedAt":s.get("StartedAt"),"State.Status":s.get("Status"),"State.Running":s.get("Running"),"State.Restarting":s.get("Restarting"),"State.Dead":s.get("Dead"),"State.ExitCode":s.get("ExitCode"),"State.OOMKilled":s.get("OOMKilled"),"State.Error":s.get("Error"),"RestartCount":x.get("RestartCount"),"HostConfig.RestartPolicy":(h.get("RestartPolicy") or {}).get("Name"),"Mounts":sorted(({"Type":m.get("Type"),"Source":m.get("Source"),"Destination":m.get("Destination"),"RW":m.get("RW")} for m in x.get("Mounts",[])),key=lambda m:(str(m["Type"]),str(m["Source"]),str(m["Destination"]),str(m["RW"]))) }
def canonical(s):
    ids=s.get("ids",[])
    if len(ids)!=len(set(ids)): raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")
    seen=set(); cs=[]
    for x in s.get("containers",[]):
        service=(x.get("labels") or {}).get("service"); project=(x.get("labels") or {}).get("project")
        if project!=PROJECT or not service or service in seen or not x.get("Id"): raise ValueError("DUPLICATE_DISCOVERED_SERVICE")
        seen.add(service); y=dict(x); y["Mounts"]=sorted(y.get("Mounts",[]),key=lambda m:(str(m.get("Type")),str(m.get("Source")),str(m.get("Destination")),str(m.get("RW")))); cs.append(y)
    if len({x["Id"] for x in cs})!=len(cs): raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")
    return {"ids":sorted(set(ids)),"containers":sorted(cs,key=lambda x:(x["labels"]["service"],x["Id"])) ,"inspect_ok":s.get("inspect_ok")}
def snap(ps, ins):
    ids = ps.stdout.decode("utf-8","strict").splitlines() if ps.returncode == 0 else []
    data = parsed(ins) or []
    return {"ids":ids,"containers":[view(x) for x in data],"inspect_ok":bool(ins and ins.returncode == 0)}
def ident(path, n, d):
    try:
        x = os.lstat(path)
        if stat.S_ISLNK(x.st_mode) or not stat.S_ISREG(x.st_mode): return {"path":path,"state":"INVALID_TYPE_OR_SYMLINK"}
        fd = os.open(path, os.O_RDONLY | getattr(os,"O_NOFOLLOW",0))
        try:
            a=os.fstat(fd); data=b""
            while True:
                q=os.read(fd,65536)
                if not q: break
                data += q
            b=os.fstat(fd)
        finally: os.close(fd)
        return {"path":path,"state":"PRESENT","realpath":os.path.realpath(path),"owner":pwd.getpwuid(a.st_uid).pw_name,"group":grp.getgrgid(a.st_gid).gr_name,"mode":format(stat.S_IMODE(a.st_mode),"04o"),"bytes":len(data),"sha256":sha(data),"inode":a.st_ino,"identity_stable":(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns)==(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns),"expected":len(data)==n and sha(data)==d}
    except FileNotFoundError: return {"path":path,"state":"ABSENT"}
    except Exception as e: return {"path":path,"state":"ERROR","error":type(e).__name__}
def absent(path):
    try: return {"path":path,"state":"PRESENT","symlink":stat.S_ISLNK(os.lstat(path).st_mode)}
    except FileNotFoundError: return {"path":path,"state":"ABSENT"}
    except Exception as e: return {"path":path,"state":"ERROR","error":type(e).__name__}
def fs():
    p=os.lstat(PARENT); parent={"directory":stat.S_ISDIR(p.st_mode),"symlink":stat.S_ISLNK(p.st_mode),"realpath":os.path.realpath(PARENT),"owner":pwd.getpwuid(p.st_uid).pw_name,"group":grp.getgrgid(p.st_gid).gr_name,"mode":format(stat.S_IMODE(p.st_mode),"04o")}
    return {"parent":parent,"target":ident(TARGET,7112,"d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"),"backup":ident(BACKUP,5935,"86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3"),"upload":absent(UPLOAD),"rollback":absent(ROLLBACK),"sidecars":sorted(x for x in os.listdir(PARENT) if x.startswith(".mapping.yaml.d2-r7b-"))}
def fsok(x):
    parent={"directory":True,"symlink":False,"realpath":PARENT,"owner":"mari","group":"mari","mode":"0775"}
    return x["parent"]==parent and all(x[k].get("state")=="PRESENT" and x[k].get("identity_stable") and x[k].get("expected") and x[k].get("owner")=="mari" and x[k].get("group")=="mari" and x[k].get("mode")=="0644" for k in ("target","backup")) and x["target"].get("inode")!=x["backup"].get("inode") and x["upload"].get("state")=="ABSENT" and x["rollback"].get("state")=="ABSENT" and x["sidecars"]==[os.path.basename(BACKUP)]
def out(status, cls):
    HISTORY.append({"phase":"FINAL_TERMINAL","completed":True,"classification":cls})
    sys.stdout.write(json.dumps({"schema_version":"d2-r7b-i1-r34-r1-remote-activation/v1","authority_id":AUTHORITY_ID,"status":status,"classification":cls,"phase_history":HISTORY,"observed":OBS,"assertions":ASSERT,"command_audit":AUDIT,"mutation_audit":MUT,"remote_call_budget":{"structured_ssh_calls":1,"retry":0,"resume":0,"supplemental_ssh":0}},sort_keys=True,separators=(",",":")))
def main():
    ip=run(["/usr/bin/docker","image","inspect",FRESH,DESCRIPTIVE,ALIAS,OLD,BAD],"read")
    pa=run(["/usr/bin/docker","ps","-aq","--filter","label=com.docker.compose.project="+PROJECT],"read")
    ia=run(["/usr/bin/docker","inspect"]+pa.stdout.decode("utf-8","strict").splitlines(),"read") if pa.returncode==0 and pa.stdout.strip() else None
    fp=run(["/usr/bin/docker","ps","-q","--filter","ancestor="+FRESH],"read")
    images, pre_raw = parsed(ip), snap(pa,ia); pre=canonical(pre_raw); OBS.update({"images":images,"pre_snapshot_raw":pre_raw,"pre_snapshot_canonical":pre,"foreign_fresh_target":fp.stdout.decode("utf-8","strict").splitlines() if fp.returncode==0 else None,"pre_fs":fs()})
    c=os.lstat(COMPOSE); comp={"regular":stat.S_ISREG(c.st_mode),"symlink":stat.S_ISLNK(c.st_mode),"realpath":os.path.realpath(COMPOSE),"bytes":c.st_size,"sha256":sha(open(COMPOSE,"rb").read())}; OBS["compose"]=comp
    byid={x.get("Id"):x for x in images or []}
    ASSERT.update({"aggregate_images_exact":isinstance(images,list) and set(byid)=={FRESH,OLD,BAD} and byid.get(FRESH,{}).get("Os")=="linux" and byid.get(FRESH,{}).get("Architecture")=="arm64" and DESCRIPTIVE in byid.get(FRESH,{}).get("RepoTags",[]) and ALIAS in byid.get(OLD,{}).get("RepoTags",[]) and DESCRIPTIVE not in byid.get(BAD,{}).get("RepoTags",[]) and ALIAS not in byid.get(BAD,{}).get("RepoTags",[]),"pre_snapshot_b_exact":pre==EXPECTED_SNAPSHOT,"no_old_target_usage":fp.returncode==0 and not OBS["foreign_fresh_target"],"compose_exact":comp=={"regular":True,"symlink":False,"realpath":COMPOSE,"bytes":4897,"sha256":"a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0"},"filesystem_exact":fsok(OBS["pre_fs"])})
    HISTORY.append({"phase":"PRE_MUTATION_RECHECK","completed":True,"command_count":4,"classification":"PASS" if all(ASSERT.values()) else "HOLD"})
    if not all(ASSERT.values()): return out("HOLD","PRE_MUTATION_REMOTE_DRIFT")
    MUT["tag_mutation_count"]=1; p=run(["/usr/bin/docker","image","tag",FRESH,ALIAS],"tag"); ASSERT["tag_ok"]=p.returncode==0; HISTORY.append({"phase":"TAG_MUTATION","completed":True,"command_count":1,"classification":"PASS" if ASSERT["tag_ok"] else "HOLD"})
    if not ASSERT["tag_ok"]: return out("HOLD","TAG_MUTATION_FAILED")
    alias=parsed(run(["/usr/bin/docker","image","inspect",ALIAS],"read")); ASSERT["alias_exact_fresh"]=isinstance(alias,list) and len(alias)==1 and alias[0].get("Id")==FRESH; HISTORY.append({"phase":"TAG_POSTCHECK","completed":True,"command_count":1,"classification":"PASS" if ASSERT["alias_exact_fresh"] else "HOLD"})
    if not ASSERT["alias_exact_fresh"]: return out("HOLD","TAG_POSTCHECK_FAILED")
    MUT["compose_recreate_count"]=MUT["collector_lifecycle_count"]=1; p=run(["/usr/bin/docker","compose","-p",PROJECT,"-f",COMPOSE,"up","-d","--no-deps","--no-build","--force-recreate","collector"],"compose"); ASSERT["compose_ok"]=p.returncode==0; HISTORY.append({"phase":"COLLECTOR_ONLY_RECREATE","completed":True,"command_count":1,"classification":"PASS" if ASSERT["compose_ok"] else "HOLD"})
    if not ASSERT["compose_ok"]: return out("HOLD","ACTIVATION_COMMAND_FAILED")
    time.sleep(3)
    pb=run(["/usr/bin/docker","ps","-aq","--filter","label=com.docker.compose.project="+PROJECT],"read")
    ib=run(["/usr/bin/docker","inspect"]+pb.stdout.decode("utf-8","strict").splitlines(),"read") if pb.returncode==0 and pb.stdout.strip() else None
    post_raw=snap(pb,ib); post=canonical(post_raw); OBS["post_snapshot_raw"],OBS["post_snapshot_canonical"],OBS["post_fs"]=post_raw,post,fs(); preby={x["labels"]["service"]:x for x in pre["containers"]}; postby={x["labels"]["service"]:x for x in post["containers"]}; col=postby.get("collector")
    ASSERT.update({"post_service_set_exact":set(postby)==SERVICES and len(post["containers"])==10,"collector_replaced":bool(col and col["Id"]!=preby["collector"]["Id"]),"collector_fresh":bool(col and col["Image"]==FRESH and col["Config.Image"] in ("edge-mes-demo-collector",ALIAS)),"collector_health_exact":bool(col and col["State.Running"] is True and col["State.Restarting"] is False and col["State.Dead"] is False and col["State.ExitCode"]==0 and col["State.OOMKilled"] is False and col["State.Error"]=="" and col["RestartCount"]==0 and col["HostConfig.RestartPolicy"]=="unless-stopped"),"collector_mount_exact":bool(col and col["Mounts"]==[{"Type":"bind","Source":PARENT,"Destination":"/app/config","RW":False}]),"protected_hard_fields_unchanged":all(postby.get(s)==preby.get(s) for s in SERVICES-{"collector"}),"filesystem_unchanged":OBS["post_fs"]==OBS["pre_fs"]})
    HISTORY.append({"phase":"IMMEDIATE_POST_MUTATION_OBSERVATION","completed":True,"command_count":2,"classification":"PASS" if all(ASSERT.values()) else "HOLD"})
    return out("PASS","PHASE4_MUTATION_EXECUTED_PHASE5_REQUIRED") if all(ASSERT.values()) and len(AUDIT)==9 else out("HOLD","IMMEDIATE_POST_MUTATION_ASSERTION_FAILED")
if __name__=="__main__":
    try: main()
    except Exception: out("HOLD","REMOTE_CONTROLLER_EXCEPTION")
