#!/usr/bin/env python3
import hashlib,json,os,pwd,grp,stat,subprocess,sys,time
AUTHORITY_ID="PM-D2-R7B-I1-R34-COLLECTOR-ONLY-ACTIVATION-260729-2034"
FRESH="sha256:168bd07db0a427f003d1733a62354d3356b8ef6b362a15fed88d48728392f734"; OLD="sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a"
DESCRIPTIVE="edge-mes-demo-collector:r32-pkg-closed-ca68dd4"; ALIAS="edge-mes-demo-collector:latest"; PROJECT="edge-mes-demo"; COMPOSE="/opt/edge-mes-demo/docker-compose.yml"; PARENT="/opt/edge-mes-demo/config"
TARGET=PARENT+"/mapping.yaml"; BACKUP=PARENT+"/.mapping.yaml.d2-r7b-backup.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"; UPLOAD=PARENT+"/.mapping.yaml.d2-r7b-new.8de5edb"; ROLLBACK=PARENT+"/.mapping.yaml.d2-r7b-rollback.8de5edb.86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3.yaml"
EXPECTED_SNAPSHOT_B=json.loads(r'''{"containers":[{"Config.Image":"edge-mes-demo-collector","Created":"2026-07-23T12:23:25.124184859Z","HostConfig.RestartPolicy":"unless-stopped","Id":"5b0eb6f8b61109a360b87bdf91310dca6f37208928772a23549c9bacddd70524","Image":"sha256:0bfcbad5baa26db15642136c847ddccc210784a625767a9aa3b9c4104757ab4a","Mounts":[{"Destination":"/app/config","RW":false,"Source":"/opt/edge-mes-demo/config","Type":"bind"}],"Name":"/edge-mes-collector","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-07-23T12:23:25.959624Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"collector"}},{"Config.Image":"edge-mes-demo-api","Created":"2026-07-23T00:32:36.666029032Z","HostConfig.RestartPolicy":"unless-stopped","Id":"12e841b4ac33a75c835cee81f0df46e4dbcdb9382b50ca50523f5fad02c57058","Image":"sha256:9f03f370b37fd5fd2ddfd4e4e9e64d4c6b60312910e731157888544371683c11","Mounts":[{"Destination":"/app/config","RW":false,"Source":"/opt/edge-mes-demo/config","Type":"bind"}],"Name":"/edge-mes-api","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-07-23T00:32:37.955732924Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"api"}},{"Config.Image":"edge-mes-dashboard:local","Created":"2026-07-22T09:46:48.20229225Z","HostConfig.RestartPolicy":"on-failure","Id":"649c31bb508a5c94ea42bf84430eabc06af66d746b475e5ef7e308220c879ae4","Image":"sha256:adb0ae00966804473cad5a1c9a71f834bc6cacae890fa4b30e42de564a85f385","Mounts":[],"Name":"/edge-mes-dashboard","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-07-22T09:46:48.770025069Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"dashboard"}},{"Config.Image":"edge-mes-demo-s7-plc-sim","Created":"2026-06-19T02:05:15.82128338Z","HostConfig.RestartPolicy":"unless-stopped","Id":"d21e950b98ae87bbd3ee321074100d0b54b174235ce46df34c5100e1130b785f","Image":"sha256:3a28ae38c623d8cb80f775f954315e633b1108112082c37ece698c7562522238","Mounts":[{"Destination":"/app/config","RW":false,"Source":"/opt/edge-mes-demo/config","Type":"bind"},{"Destination":"/app/data","RW":true,"Source":"/opt/edge-mes-demo/data/vplc","Type":"bind"}],"Name":"/edge-mes-s7-plc-sim","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-06-19T02:05:27.378341652Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"s7-plc-sim"}},{"Config.Image":"grafana/grafana:latest","Created":"2026-06-15T04:03:57.392904193Z","HostConfig.RestartPolicy":"unless-stopped","Id":"fa442407312e2cd05a2273b55f546e2e840b9f6f427ff420ffbdeba63cdb4f12","Image":"sha256:0d1b6e9173e6144d970bead78e7f1914a387dbabee073a617af1e076bfd59e15","Mounts":[{"Destination":"/etc/grafana/provisioning","RW":false,"Source":"/opt/edge-mes-demo/config/grafana","Type":"bind"},{"Destination":"/usr/share/grafana/public/custom","RW":false,"Source":"/opt/edge-mes-demo/config/grafana/custom","Type":"bind"},{"Destination":"/var/lib/grafana","RW":true,"Source":"/opt/edge-mes-demo/data/grafana","Type":"bind"}],"Name":"/edge-mes-grafana","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-06-19T13:47:25.117873705Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"grafana"}},{"Config.Image":"edge-mes-demo-simulator","Created":"2026-06-14T12:13:00.476282483Z","HostConfig.RestartPolicy":"unless-stopped","Id":"3ebe1e4725af577ac477594afe3046f7e5a197b8162f503ebac036d09b4fcfd5","Image":"sha256:08448d2876c30e9cbbecda4f0ca9a27a5e085a33f14dab2a6d2be3dd06430430","Mounts":[{"Destination":"/app/config","RW":false,"Source":"/opt/edge-mes-demo/config","Type":"bind"}],"Name":"/edge-mes-simulator","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-06-14T12:13:23.098546695Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"simulator"}},{"Config.Image":"prom/prometheus:latest","Created":"2026-06-14T07:19:55.078265353Z","HostConfig.RestartPolicy":"unless-stopped","Id":"03d48e04a511f991418b1370f3ce02e0d1e770d279ffe4fa54d3bb7a6df286af","Image":"sha256:ce22ec1ea0f867f3a4e96d8df33cb671f7e8d5978fb17f0c6b7cbdefcc21037e","Mounts":[{"Destination":"/etc/prometheus","RW":false,"Source":"/opt/edge-mes-demo/config/prometheus","Type":"bind"},{"Destination":"/prometheus","RW":true,"Source":"/opt/edge-mes-demo/data/prometheus","Type":"bind"}],"Name":"/edge-mes-prometheus","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-06-14T07:19:56.985010048Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"prometheus"}},{"Config.Image":"prom/node-exporter:latest","Created":"2026-06-14T07:19:55.078178983Z","HostConfig.RestartPolicy":"unless-stopped","Id":"943933f4c48042e6f0294ea68e0f39884f37ceedbf4c3cfd35c5443062e4fddb","Image":"sha256:5635e459687a21bee059ade06ae4170ebfae5330e2a224947254ab1a2860c22c","Mounts":[{"Destination":"/host/proc","RW":false,"Source":"/proc","Type":"bind"},{"Destination":"/host/sys","RW":false,"Source":"/sys","Type":"bind"},{"Destination":"/rootfs","RW":false,"Source":"/","Type":"bind"}],"Name":"/edge-mes-node-exporter","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-06-14T07:19:57.00079108Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"node-exporter"}},{"Config.Image":"edge-mes-demo-sync-worker","Created":"2026-06-14T05:57:13.45515899Z","HostConfig.RestartPolicy":"unless-stopped","Id":"651c0226e4b1949267065a88a7a20fc2e0df4bbab6a4f7ee3f0fbe2c029e8d23","Image":"sha256:a6c2edcfccb2945ea87ec71c96f4ff3066dd66a6c7c0945d8d20f2a6a55e2188","Mounts":[{"Destination":"/app/config","RW":false,"Source":"/opt/edge-mes-demo/config","Type":"bind"}],"Name":"/edge-mes-sync-worker","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-06-14T05:57:25.700976852Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"sync-worker"}},{"Config.Image":"postgres:16","Created":"2026-06-14T05:57:13.239812435Z","HostConfig.RestartPolicy":"unless-stopped","Id":"bb3ba0738e692c68b14a62ca64296e484990d3b86b1f6d395c27b200af5cb890","Image":"sha256:f961d097a9cedd37779baef1aab3fe87ef1c63b3b34d361f90a98ea5c9b77e56","Mounts":[{"Destination":"/docker-entrypoint-initdb.d","RW":false,"Source":"/opt/edge-mes-demo/db/init","Type":"bind"},{"Destination":"/var/lib/postgresql/data","RW":true,"Source":"/opt/edge-mes-demo/data/postgres","Type":"bind"}],"Name":"/edge-mes-postgres","RestartCount":0,"State.Dead":false,"State.Error":"","State.ExitCode":0,"State.OOMKilled":false,"State.Restarting":false,"State.Running":true,"State.StartedAt":"2026-06-14T05:57:14.263634444Z","State.Status":"running","labels":{"project":"edge-mes-demo","service":"postgres"}}],"ids":["5b0eb6f8b611","12e841b4ac33","649c31bb508a","d21e950b98ae","fa442407312e","3ebe1e4725af","03d48e04a511","943933f4c480","651c0226e4b1","bb3ba0738e69"],"inspect_ok":true}''')
SERVICES={"collector","postgres","simulator","s7-plc-sim","api","dashboard","grafana","prometheus","node-exporter","sync-worker"}
def sha(b): return hashlib.sha256(b).hexdigest()
def run(argv,audit,c):
 p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False,cwd="/opt/edge-mes-demo" if c=="compose" else None)
 audit.append({"argv":argv,"category":c,"started":True,"completed":True,"returncode":p.returncode,"stdout_bytes":len(p.stdout),"stderr_bytes":len(p.stderr),"stdout_sha256":sha(p.stdout),"stderr_sha256":sha(p.stderr),"timeout":False,"interrupted":False})
 return p
def parsed(p):
 try:return json.loads(p.stdout.decode("utf-8","strict")) if p.returncode==0 else None
 except (UnicodeDecodeError,json.JSONDecodeError):return None
def view(x):
 s=x.get("State") or {}; c=x.get("Config") or {}; h=x.get("HostConfig") or {}; l=c.get("Labels") or {}
 return {"Id":x.get("Id"),"Name":x.get("Name"),"Image":x.get("Image"),"Config.Image":c.get("Image"),"labels":{"project":l.get("com.docker.compose.project"),"service":l.get("com.docker.compose.service")},"Created":x.get("Created"),"State.StartedAt":s.get("StartedAt"),"State.Status":s.get("Status"),"State.Running":s.get("Running"),"State.Restarting":s.get("Restarting"),"State.Dead":s.get("Dead"),"State.ExitCode":s.get("ExitCode"),"State.OOMKilled":s.get("OOMKilled"),"State.Error":s.get("Error"),"RestartCount":x.get("RestartCount"),"HostConfig.RestartPolicy":(h.get("RestartPolicy") or {}).get("Name"),"Mounts":sorted([{"Type":m.get("Type"),"Source":m.get("Source"),"Destination":m.get("Destination"),"RW":m.get("RW")} for m in x.get("Mounts",[])],key=lambda m:(str(m["Destination"]),str(m["Source"])))}
def snapshot(audit):
 q=run(["/usr/bin/docker","ps","-aq","--filter","label=com.docker.compose.project="+PROJECT],audit,"read")
 ids=[z for z in q.stdout.decode("utf-8","strict").splitlines() if z] if q.returncode==0 else []
 ins=run(["/usr/bin/docker","inspect"]+ids,audit,"read") if ids else None
 data=parsed(ins) if ins else []
 return {"ids":ids,"containers":sorted([view(x) for x in (data or [])],key=lambda x:x["labels"]["service"]),"inspect_ok":bool(ins and ins.returncode==0)}
def identity(path,n,d):
 out={"path":path}
 try:
  l=os.lstat(path)
  if stat.S_ISLNK(l.st_mode) or not stat.S_ISREG(l.st_mode): return dict(out,state="INVALID_TYPE_OR_SYMLINK")
  fd=os.open(path,os.O_RDONLY|getattr(os,"O_NOFOLLOW",0))
  try:
   b=os.fstat(fd); h=hashlib.sha256(); z=0
   while True:
    q=os.read(fd,65536)
    if not q:break
    h.update(q);z+=len(q)
   a=os.fstat(fd)
  finally:os.close(fd)
  return dict(out,state="PRESENT",realpath=os.path.realpath(path),owner=pwd.getpwuid(b.st_uid).pw_name,group=grp.getgrgid(b.st_gid).gr_name,mode=format(stat.S_IMODE(b.st_mode),"04o"),bytes=z,sha256=h.hexdigest(),identity_stable=(b.st_dev,b.st_ino,b.st_size,b.st_mtime_ns)==(a.st_dev,a.st_ino,a.st_size,a.st_mtime_ns),expected=(z==n and h.hexdigest()==d))
 except FileNotFoundError:return dict(out,state="ABSENT")
 except Exception as e:return dict(out,state="ERROR",error=type(e).__name__)
def absent(path):
 try: s=os.lstat(path);return {"path":path,"state":"PRESENT","symlink":stat.S_ISLNK(s.st_mode)}
 except FileNotFoundError:return {"path":path,"state":"ABSENT"}
 except Exception as e:return {"path":path,"state":"ERROR","error":type(e).__name__}
def fsstate():
 p=os.lstat(PARENT); parent={"directory":stat.S_ISDIR(p.st_mode),"symlink":stat.S_ISLNK(p.st_mode),"realpath":os.path.realpath(PARENT),"owner":pwd.getpwuid(p.st_uid).pw_name,"group":grp.getgrgid(p.st_gid).gr_name,"mode":format(stat.S_IMODE(p.st_mode),"04o")}
 side=sorted(x for x in os.listdir(PARENT) if x.startswith(".mapping.yaml.d2-r7b-"))
 return {"parent":parent,"target":identity(TARGET,7112,"d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d"),"backup":identity(BACKUP,5935,"86af360ae3aeae603a97add4150245dcfe9b58dbcf9c44fe3a79a62ba82604c3"),"upload":absent(UPLOAD),"rollback":absent(ROLLBACK),"sidecars":side}
def validfs(x):
 return x["parent"]=={"directory":True,"symlink":False,"realpath":PARENT,"owner":"mari","group":"mari","mode":"0775"} and all(x[k].get("state")=="PRESENT" and x[k].get("identity_stable") and x[k].get("expected") and x[k].get("realpath")==({"target":TARGET,"backup":BACKUP}[k]) and x[k].get("owner")=="mari" and x[k].get("group")=="mari" and x[k].get("mode")=="0644" for k in ("target","backup")) and x["upload"]["state"]=="ABSENT" and x["rollback"]["state"]=="ABSENT" and x["sidecars"]==[os.path.basename(BACKUP)]
def phase(ph,h,body):
 r={"phase":ph,"started":True,"completed":False,"command_count_before":len(AUDIT),"mutation_started":False,"mutation_completed":False,"classification":"PASS"}
 try: body(r)
 except Exception as e: r["classification"]="HOLD"; r["exception"]=type(e).__name__
 r["command_count"]=len(AUDIT)-r["command_count_before"];r["completed"]=True;h.append(r);return r
AUDIT=[]; HISTORY=[]; OBS={}; ASSERT={}; MUT={"tag_mutation_count":0,"compose_recreate_count":0,"collector_lifecycle_count":0,"protected_service_lifecycle_count":0,"rollback_count":0,"cleanup_count":0}
def main():
 def pre(r):
  imgs={}
  for ref in (FRESH,DESCRIPTIVE,ALIAS,OLD):imgs[ref]=parsed(run(["/usr/bin/docker","image","inspect",ref],AUDIT,"read"))
  OBS["images"]=imgs; f,d,a,o=[imgs[x][0] if isinstance(imgs[x],list) and len(imgs[x])==1 else None for x in (FRESH,DESCRIPTIVE,ALIAS,OLD)]
  q=run(["/usr/bin/docker","ps","-q","--filter","ancestor="+FRESH],AUDIT,"read"); foreign=[x for x in q.stdout.decode("utf-8","strict").splitlines() if x]; OBS["foreign_fresh_target"]=foreign
  OBS["pre_snapshot"]=snapshot(AUDIT); OBS["pre_fs"]=fsstate()
  try: cs=os.lstat(COMPOSE); comp={"regular":stat.S_ISREG(cs.st_mode),"symlink":stat.S_ISLNK(cs.st_mode),"realpath":os.path.realpath(COMPOSE),"bytes":cs.st_size,"sha256":hashlib.sha256(open(COMPOSE,"rb").read()).hexdigest()}
  except Exception as e: comp={"error":type(e).__name__}
  OBS["compose"]=comp
  ASSERT.update({"fresh_object_exact":bool(f and f.get("Id")==FRESH and f.get("Os")=="linux" and f.get("Architecture")=="arm64"),"descriptive_tag_exact":bool(d and d.get("Id")==FRESH),"alias_old_exact":bool(a and a.get("Id")==OLD),"old_safe_exact":bool(o and o.get("Id")==OLD and o.get("Os")=="linux" and o.get("Architecture")=="arm64"),"no_foreign_fresh":q.returncode==0 and not foreign,"compose_exact":comp=={"regular":True,"symlink":False,"realpath":COMPOSE,"bytes":5698,"sha256":"c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66"},"prestate_exact":OBS["pre_snapshot"]==EXPECTED_SNAPSHOT_B,"fs_exact":validfs(OBS["pre_fs"])})
 phase("PRE_MUTATION_RECHECK",HISTORY,pre)
 if not all(ASSERT.values()): return terminal("HOLD","PRE_MUTATION_REMOTE_DRIFT")
 def tag(r):
  r["mutation_started"]=True;MUT["tag_mutation_count"]+=1;p=run(["/usr/bin/docker","image","tag",FRESH,ALIAS],AUDIT,"tag");r["mutation_completed"]=p.returncode==0;ASSERT["tag_command_ok"]=p.returncode==0
 phase("TAG_MUTATION",HISTORY,tag)
 if not ASSERT.get("tag_command_ok"): return terminal("HOLD","TAG_MUTATION_FAILED")
 def posttag(r):
  p=parsed(run(["/usr/bin/docker","image","inspect",ALIAS],AUDIT,"read"));OBS["alias_postcheck"]=p;ASSERT["alias_postcheck"]=bool(isinstance(p,list) and len(p)==1 and p[0].get("Id")==FRESH)
 phase("TAG_POSTCHECK",HISTORY,posttag)
 if not ASSERT.get("alias_postcheck"):return terminal("HOLD","TAG_POSTCHECK_FAILED")
 def recreate(r):
  r["mutation_started"]=True;MUT["compose_recreate_count"]+=1;MUT["collector_lifecycle_count"]+=1;p=run(["/usr/bin/docker","compose","-p",PROJECT,"-f",COMPOSE,"up","-d","--no-deps","--no-build","--force-recreate","collector"],AUDIT,"compose");OBS["compose_returncode"]=p.returncode;r["mutation_completed"]=p.returncode==0;ASSERT["compose_ok"]=p.returncode==0
 phase("COLLECTOR_ONLY_RECREATE",HISTORY,recreate)
 if not ASSERT.get("compose_ok"):return terminal("HOLD","ACTIVATION_COMMAND_FAILED")
 def observe(r):
  post=snapshot(AUDIT);OBS["post_snapshot"]=post;OBS["post_fs"]=fsstate();pre={x["labels"]["service"]:x for x in OBS["pre_snapshot"]["containers"]};now={x["labels"]["service"]:x for x in post["containers"]};c=now.get("collector");OBS["immediate_collector"]=c
  ASSERT.update({"post_service_set":set(now)==SERVICES and len(post["containers"])==10,"collector_replaced":bool(c and c["Id"]!=pre["collector"]["Id"]),"collector_fresh":bool(c and c["Image"]==FRESH and c["Config.Image"] in ("edge-mes-demo-collector","edge-mes-demo-collector:latest")),"collector_safe":bool(c and c["State.Running"] is True and c["State.Restarting"] is False and c["State.Dead"] is False and c["State.ExitCode"]==0 and c["State.OOMKilled"] is False and c["State.Error"] in ("",None) and c["RestartCount"]==0 and c["HostConfig.RestartPolicy"]=="unless-stopped"),"collector_mount":bool(c and c["Mounts"]==[{"Type":"bind","Source":PARENT,"Destination":"/app/config","RW":False}]),"protected_unchanged":all(now.get(s)==pre.get(s) for s in SERVICES-{"collector"}),"post_fs_unchanged":OBS["post_fs"]==OBS["pre_fs"]})
 phase("IMMEDIATE_POST_MUTATION_OBSERVATION",HISTORY,observe)
 if not all(ASSERT.values()): return terminal("HOLD","IMMEDIATE_POST_MUTATION_ASSERTION_FAILED")
 return terminal("PASS","PHASE4_MUTATION_EXECUTED_PHASE5_REQUIRED")
def terminal(status,classification):
 HISTORY.append({"phase":"FINAL_TERMINAL","started":True,"completed":True,"command_count":0,"mutation_started":False,"mutation_completed":False,"classification":classification})
 out={"schema_version":"d2-r7b-i1-r34-remote-activation/v1","authority_id":AUTHORITY_ID,"status":status,"classification":classification,"phase_history":HISTORY,"last_started_phase":HISTORY[-1]["phase"],"last_completed_phase":HISTORY[-1]["phase"],"observed":OBS,"assertions":ASSERT,"command_audit":AUDIT,"mutation_audit":MUT,"remote_call_budget":{"structured_ssh_calls":1,"retry":0,"resume":0,"supplemental_ssh":0}}
 sys.stdout.write(json.dumps(out,sort_keys=True,separators=(",",":")))
if __name__=="__main__":
 try: main()
 except Exception:
  sys.stdout.write(json.dumps({"schema_version":"d2-r7b-i1-r34-remote-activation/v1","authority_id":AUTHORITY_ID,"status":"HOLD","classification":"REMOTE_CONTROLLER_EXCEPTION","phase_history":HISTORY,"last_started_phase":HISTORY[-1]["phase"] if HISTORY else "NONE","last_completed_phase":HISTORY[-1]["phase"] if HISTORY else "NONE","observed":OBS,"assertions":ASSERT,"command_audit":AUDIT,"mutation_audit":MUT,"remote_call_budget":{"structured_ssh_calls":1,"retry":0,"resume":0,"supplemental_ssh":0}},sort_keys=True,separators=(",",":")))

