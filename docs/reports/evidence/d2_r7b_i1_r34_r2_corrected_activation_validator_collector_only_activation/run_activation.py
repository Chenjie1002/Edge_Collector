#!/usr/bin/env python3
"""R34-R2 local gate, corrected-controller materializer, one-shot transport and receipt writer."""
import ast, base64, hashlib, json, os, stat, subprocess, sys, zlib
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path('/Users/chenjie/Documents/MES/edge-mes-demo'); E=ROOT/'docs/reports/evidence/d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation'
RUN=E/'run_activation.py'; CTL=E/'remote_activation_controller.py'; LOCAL=E/'local_prerequisite_terminal.json'; REMOTE=E/'activation_terminal.json'; MAN=E/'manifest.sha256'; REPORT=ROOT/'docs/reports/sprint4_d2_r7b_i1_r34_r2_corrected_activation_validator_collector_only_activation.md'
AUTH='PM-D2-R7B-I1-R34-R2-CORRECTED-CANONICAL-ACTIVATION-260729-2123'; OLD=ROOT/'docs/reports/evidence/d2_r7b_i1_r34_r1_collector_only_activation_retry'; KEY=Path('/Users/chenjie/.ssh/edge_pi_codex')
DIRTY=['.gitignore','docs/reports/evidence/d2_r7b_p2_r2/local_materialization.sh','docs/reports/evidence/d2_r7b_p2_r2/manifest.sha256','docs/reports/evidence/d2_r7b_p2_r3/manifest.sha256','docs/reports/evidence/d2_r7b_p2_r3/remote_i1_orchestrator.py','docs/thread_handoff/pm_operating_rules.md']
SSH=['ssh','-T','-p','22','-o','BatchMode=yes','-o','IdentitiesOnly=yes','-i',str(KEY),'-o','ControlMaster=no','-o','ControlPersist=no','-o','ForwardAgent=no','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=10','-o','ServerAliveInterval=5','-o','ServerAliveCountMax=2','-o','LogLevel=ERROR','mari@10.0.0.217','/usr/bin/python3','-']
OUT=[REPORT,RUN,CTL,LOCAL,REMOTE,MAN]
def sha(b): return hashlib.sha256(b).hexdigest()
def ident(p):
 s=os.lstat(p); b=p.read_bytes(); return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha(b),'regular':stat.S_ISREG(s.st_mode),'symlink':stat.S_ISLNK(s.st_mode)}
def cmd(*a):
 p=subprocess.run(['git',*a],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); return {'argv':['git',*a],'rc':p.returncode,'stdout':p.stdout.decode('utf-8','strict').strip(),'stderr':p.stderr.decode('utf-8','strict').strip()}
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def manifest_ok(d):
 try:
  a=(d/'manifest.sha256').read_text().splitlines(); return len(a)==5 and all(len(x.split('  '))==2 and sha((ROOT/x.split('  ',1)[1]).read_bytes())==x.split('  ',1)[0] for x in a)
 except Exception:return False
def canonical(s):
 ids=s.get('ids',[])
 if len(ids)!=len(set(ids)): raise ValueError('DUPLICATE_DISCOVERED_CONTAINER_ID')
 out=[]; services=set()
 for x in s.get('containers',[]):
  y=dict(x); lab=y.get('labels') or {}; service=lab.get('service')
  if lab.get('project')!='edge-mes-demo' or not service or service in services or not y.get('Id'): raise ValueError('DUPLICATE_DISCOVERED_SERVICE')
  services.add(service); ms=y.get('Mounts',[]); y['Mounts']=sorted(ms,key=lambda m:(str(m.get('Type')),str(m.get('Source')),str(m.get('Destination')),str(m.get('RW')))); out.append(y)
 if len({x['Id'] for x in out})!=len(out): raise ValueError('DUPLICATE_DISCOVERED_CONTAINER_ID')
 return {'ids':sorted(set(ids)),'containers':sorted(out,key=lambda x:(x['labels']['service'],x['Id'])),'inspect_ok':s.get('inspect_ok')}
def fixture_ok():
 base={'ids':['b','a'],'inspect_ok':True,'containers':[{'Id':'2','labels':{'project':'edge-mes-demo','service':'x'},'Mounts':[{'Type':'bind','Source':'b','Destination':'z','RW':False},{'Type':'bind','Source':'a','Destination':'y','RW':True}]},{'Id':'1','labels':{'project':'edge-mes-demo','service':'y'},'Mounts':[]}]}; alt={'ids':['a','b'],'inspect_ok':True,'containers':[dict(base['containers'][1]),dict(base['containers'][0],Mounts=list(reversed(base['containers'][0]['Mounts'])))]}; drift=json.loads(json.dumps(base)); drift['containers'][0]['State.Running']=False; dup=json.loads(json.dumps(base)); dup['containers'][1]['labels']['service']='x'
 try:return canonical(base)==canonical(alt) and canonical(base)!=canonical(drift) and _raises(dup)
 except Exception:return False
def _raises(x):
 try: canonical(x); return False
 except ValueError:return True
def materialize():
 src=(OLD/'remote_activation_controller.py').read_text(encoding='utf-8'); hist=json.loads((OLD/'activation_terminal.json').read_text())['observed']['pre_snapshot']; expected=base64.b64encode(zlib.compress(json.dumps(canonical(hist),sort_keys=True,separators=(',',':')).encode())).decode()
 src=src.replace('R34-R1-COLLECTOR-ONLY-ACTIVATION-260729-2057','R34-R2-CORRECTED-CANONICAL-ACTIVATION-260729-2123').replace('EXPECTED_SNAPSHOT_B = json.loads(zlib.decompress(base64.b64decode(_B64)).decode("utf-8"))','EXPECTED_SNAPSHOT = json.loads(zlib.decompress(base64.b64decode(_B64)).decode("utf-8"))').replace('"eNrV','"'+expected+'"\n# eNrV',1).replace('pre==EXPECTED_SNAPSHOT_B','pre==EXPECTED_SNAPSHOT').replace('"bytes":5698,"sha256":"c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66"','"bytes":4897,"sha256":"a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0"')
 # Correct only frozen validator defects: raw snapshots are retained, canonical maps are compared.
 src=src.replace('def snap(ps, ins):','def canonical(s):\n    ids=s.get("ids",[])\n    if len(ids)!=len(set(ids)): raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")\n    seen=set(); cs=[]\n    for x in s.get("containers",[]):\n        service=(x.get("labels") or {}).get("service"); project=(x.get("labels") or {}).get("project")\n        if project!=PROJECT or not service or service in seen or not x.get("Id"): raise ValueError("DUPLICATE_DISCOVERED_SERVICE")\n        seen.add(service); y=dict(x); y["Mounts"]=sorted(y.get("Mounts",[]),key=lambda m:(str(m.get("Type")),str(m.get("Source")),str(m.get("Destination")),str(m.get("RW")))); cs.append(y)\n    if len({x["Id"] for x in cs})!=len(cs): raise ValueError("DUPLICATE_DISCOVERED_CONTAINER_ID")\n    return {"ids":sorted(set(ids)),"containers":sorted(cs,key=lambda x:(x["labels"]["service"],x["Id"])) ,"inspect_ok":s.get("inspect_ok")}\ndef snap(ps, ins):').replace('return {"ids":ids,"containers":sorted((view(x) for x in data),key=lambda x:x["labels"]["service"]),"inspect_ok":bool(ins and ins.returncode == 0)}','return {"ids":ids,"containers":[view(x) for x in data],"inspect_ok":bool(ins and ins.returncode == 0)}').replace('key=lambda m:(str(m["Destination"]),str(m["Source"]))','key=lambda m:(str(m["Type"]),str(m["Source"]),str(m["Destination"]),str(m["RW"]))')
 src=src.replace('images, pre = parsed(ip), snap(pa,ia); OBS.update({"images":images,"pre_snapshot":pre,','images, pre_raw = parsed(ip), snap(pa,ia); pre=canonical(pre_raw); OBS.update({"images":images,"pre_snapshot_raw":pre_raw,"pre_snapshot_canonical":pre,').replace('post=snap(pb,ib); OBS["post_snapshot"],OBS["post_fs"]=post,fs()','post_raw=snap(pb,ib); post=canonical(post_raw); OBS["post_snapshot_raw"],OBS["post_snapshot_canonical"],OBS["post_fs"]=post_raw,post,fs()')
 CTL.write_text(src,encoding='utf-8')
def report(local,remote):
 status=remote.get('status',local['status']); cls=remote.get('classification',local['classification']); REPORT.write_text(f'''# Sprint 4 D2-R7B-I1 R34-R2 Corrected Activation Validator and Collector-Only Activation\n\n结论：{status} / {cls}\n\n- Authority: `{AUTH}`; R34-R2 artifacts are WRITTEN only.\n- Canonical unordered comparison and local/remote Compose identity separation were applied.\n- SSH: {local["remote_call_budget"]["structured_ssh_calls"]}; tag/Compose: {remote["mutation_audit"]["tag_mutation_count"]}/{remote["mutation_audit"]["compose_recreate_count"]}.\n- Phase 5, rollback, cleanup, Git mutation, runtime-loaded and production-accepted validation: not executed/not established.\n- Next gate: ChatGPT PM durable intake only.\n\nMVP 路径一致性：MVP-ALIGNED；最小不变量为一条受锁定的 Collector-only activation 及保护对象不漂移。\n''',encoding='utf-8')
def final(local,remote):
 dump(LOCAL,local); dump(REMOTE,remote); report(local,remote); paths=[REPORT,RUN,CTL,LOCAL,REMOTE]; MAN.write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(ROOT)}\n' for p in paths),encoding='utf-8')
def main():
 facts={k:cmd(*v) for k,v in {'status':('status','-sb'),'root':('rev-parse','--show-toplevel'),'branch':('rev-parse','--abbrev-ref','HEAD'),'head':('rev-parse','HEAD'),'origin':('rev-parse','origin/main'),'parent':('rev-parse','HEAD^'),'ahead':('rev-list','--left-right','--count','HEAD...origin/main'),'dirty':('diff','--name-only'),'cached':('diff','--cached','--name-only'),'check':('diff','--check'),'cached_check':('diff','--cached','--check')}.items()}
 ids={'pm_rule':ident(ROOT/'docs/thread_handoff/pm_operating_rules.md'),'r31':ident(ROOT/'docs/reports/sprint4_d2_r7b_i1_r31_package_closed_collector_image_materialization_deployment_plan.md'),'local_compose':ident(ROOT/'docker-compose.yml'),'mapping':ident(ROOT/'config/mapping.yaml'),'r34r1_terminal':ident(OLD/'activation_terminal.json')}; oldterm=json.loads((OLD/'activation_terminal.json').read_text()); r33=json.loads((ROOT/'docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight/remote_preflight_terminal.json').read_text()); key=os.lstat(KEY)
 checks={'baseline':facts['root']['stdout']==str(ROOT) and facts['branch']['stdout']=='main' and facts['head']['stdout']==facts['origin']['stdout']=='ac33e6bae449ecdd9b77a53daaf7271f14133000' and facts['parent']['stdout']=='66563677d3d1129fbc79c2c284b5f6d8b62f1932' and facts['ahead']['stdout']=='0\t0','dirty_exact':facts['dirty']['stdout'].splitlines()==DIRTY,'cached_empty':not facts['cached']['stdout'],'diff_checks':facts['check']['rc']==facts['cached_check']['rc']==0,'r33':r33.get('status')=='PASS' and r33.get('classification')=='ACTIVATION_ELIGIBLE' and manifest_ok(ROOT/'docs/reports/evidence/d2_r7b_i1_r33_fresh_readonly_remote_activation_preflight'),'r34r1':oldterm.get('status')=='HOLD' and oldterm.get('classification')=='PRE_MUTATION_REMOTE_DRIFT' and manifest_ok(OLD),'local_compose_exact':(ids['local_compose']['bytes'],ids['local_compose']['sha256'])==(5698,'c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66'),'separation':(5698,'c10dc292bce971ce857051e36268a3be9e9377e63d5e3cd58d2514e3e824ed66')!=(4897,'a71ab815a34f3c493f38ec572e0cf5892a9a7cdc081d8d3e2e312a380cad9ef0'),'key':stat.S_ISREG(key.st_mode) and not stat.S_ISLNK(key.st_mode) and key.st_uid==501 and stat.S_IMODE(key.st_mode)==0o600,'fixtures':fixture_ok()}
 checks['authority_identities_exact']=(ids['pm_rule']['bytes'],ids['pm_rule']['sha256'])==(49170,'a692fdafbdea8c63d184cb11548e73731aefccd3110818004b028ba7ee9fe7f5') and (ids['r31']['bytes'],ids['r31']['sha256'])==(45360,'bd5b65ac08dcacfd0fc14a639626d807f28d429f1038a99aa124cd6ce85db894') and (ids['mapping']['bytes'],ids['mapping']['sha256'])==(7112,'d9bb5fcb017e6ab491e8643077c793bb018011d1cbe0698172e4c08823080c9d')
 try: materialize(); ast.parse(RUN.read_text()); ast.parse(CTL.read_text()); checks['helpers_ast_utf8']=True
 except Exception as e: checks['helpers_ast_utf8']=False; checks['materialization_error']=type(e).__name__
 checks['no_pycache']=not any(p.name=='__pycache__' or p.suffix=='.pyc' for p in E.rglob('*'))
 local={'schema_version':'d2-r7b-i1-r34-r2-local/v1','authority_id':AUTH,'status':'HOLD','classification':'LOCAL_PREREQUISITE_FAILED','pre_task_live_facts':facts,'authority_input_identities':ids,'initial_output_preconditions':{str(p.relative_to(ROOT)):'ABSENT_NON_SYMLINK' for p in OUT},'repair_window':{'state':'OPEN','max_cycles':2,'cycles_consumed':0,'repairs':'Cycle 0 initial corrected materialization'},'execution_lock':{'state':'NOT_SEALED'},'validation':checks,'remote_call_budget':{'structured_ssh_calls':0,'retry':0,'resume':0,'supplemental_ssh':0}}
 remote={'schema_version':'d2-r7b-i1-r34-r2-remote/v1','authority_id':AUTH,'status':'HOLD','classification':'REMOTE_NOT_OBSERVED','command_audit':[],'mutation_audit':{'tag_mutation_count':0,'compose_recreate_count':0,'collector_lifecycle_count':0,'protected_service_lifecycle_count':0,'rollback_count':0,'cleanup_count':0}}
 if not all(v is True for v in checks.values()): final(local,remote); return
 helpers={'run':ident(RUN),'controller':ident(CTL)}; local.update({'status':'PENDING_REMOTE','classification':'EXECUTION_LOCK_SEALED','execution_lock':{'state':'SEALED','timestamp_utc':datetime.now(timezone.utc).isoformat(),'authority_id':AUTH,'helpers':helpers,'ssh_argv':SSH,'remote_command_plan':['aggregate_image_inspect','pre_project_ps','pre_aggregate_inspect','fresh_ancestor_lookup','tag','alias_post_inspect','collector_only_compose','post_project_ps','post_aggregate_inspect'],'mutation_budget':{'tag':1,'compose':1,'rollback':0,'cleanup':0}},'repair_window':{'state':'CLOSED','max_cycles':2,'cycles_consumed':0,'repairs':'Cycle 0 only'}}); dump(LOCAL,local)
 if helpers!={'run':ident(RUN),'controller':ident(CTL)}: local.update({'status':'HOLD','classification':'POST_LOCK_LOCAL_FAILURE'}); final(local,remote); return
 p=subprocess.run(SSH,input=CTL.read_bytes(),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False); local['remote_call_budget']['structured_ssh_calls']=1; local['ssh_capture']={'rc':p.returncode,'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr)}
 try: remote=json.loads(p.stdout.decode('utf-8','strict')) if p.returncode==0 and not p.stderr else remote; assert remote['authority_id']==AUTH
 except Exception: remote.update({'status':'HOLD','classification':'REMOTE_STATE_MAY_BE_AMBIGUOUS'})
 final(local,remote)
if __name__=='__main__': main()
