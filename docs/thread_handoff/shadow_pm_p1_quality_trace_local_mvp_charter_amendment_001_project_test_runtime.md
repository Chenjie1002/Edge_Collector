# Shadow PM P1 Quality + Trace Local MVP Charter Amendment 001

状态：`OWNER_AUTHORIZED / DURABLE / CONTROL_PLANE_ONLY`

## 1. Amendment identity and precedence

适用 Goal：

```text
P1-SHADOW-PM-QUALITY-TRACE-LOCAL-MVP-V1
```

本文件是 Owner-authorized durable clarification/amendment materialization，针对当前 Goal 的 G2 source/test repair autonomy 与 local project test-runtime interpretation。原文件保持 immutable：

```text
docs/thread_handoff/shadow_pm_p1_quality_trace_local_mvp_charter.md
```

本 amendment 不修改 PM Rules，不修改原 Charter，不新增 DB、remote、Docker、deployment、production、PLC/V-PLC 或 Git mutation authority。与原 Charter 冲突时，仅对本文件明确列出的 G2 local source/test repair authority 和 local test-runtime interpretation 生效；PM Rules 仍高于原 Charter 与本 amendment。

本 amendment 不重置任何现有 Gate、failure-family、product-repair、control-plane-recovery、total-dispatch 或 no-product-progress counter。

## 2. Existing Charter authority clarification

Current resume context for this amendment is:

```text
CURRENT_GATE = P1-G2-I_QUALITY_TRACE_IMPLEMENTATION
CURRENT_FAILURE_FAMILY = G2_I_FOCUSED_TEST_COLLECTION_DUPLICATE_FACT_KEY
PRIMARY_CLASS = TEST_DEFECT
MVP_ALIGNMENT = YES
```

现有 Charter Section 9.3 已经授权：

fresh G2 implementation/repair task 可以在 exact-path allowlist 下修改 `api/` / `api/tests/` 中为当前 Quality + accepted-fact Trace slice 必需的 source/test paths。

只要同时满足以下条件，G2 source/test repair 不需要逐次重新申请 Owner product/test mutation authority：

- current blocker 仍在本 Goal；
- `MVP_ALIGNMENT = YES`；
- `architecture redesign = NO`；
- no Owner-intervention condition is true；
- failure-family budget 未耗尽；
- product-repair budget 未耗尽；
- total Gate budget 未耗尽；
- exact task allowlist 被机械冻结。

Controller 应自行创建最小 fresh repair task、dispatch 一个 disposable specialist、独立 intake，并按 Charter budget 自动继续。

普通 `PRODUCT_DEFECT` / `TEST_DEFECT` 不得仅因 failure classification 被提升为 `OWNER_AUTHORITY_REQUIRED`。只有真正命中 Charter Section 13 Owner-intervention condition 时才停止等待 Owner。

## 3. CONTROL_PLANE_PYTHON

控制面 runtime 继续冻结为：

```text
/opt/homebrew/opt/python@3.14/bin/python3.14
```

必须继续用于：

- task/report identity；
- SHA-256；
- control-plane parsing；
- PM evidence；
- governance helper；
- authority-bearing control-plane Python。

固定 identity：

```text
Python       = 3.14.6
architecture = arm64
resolved bytes = 52448
SHA-256      = b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

本 runtime 不因 project test runtime amendment 而改变。

## 4. PROJECT_TEST_RUNTIME

对于本 Goal 剩余所有明确授权的 local Python tests / compile/import validation：

```text
P1-G2-I
P1-G2-R
P1-G2-DQ
P1-G2-V
```

授权使用项目既有：

```text
<project-root>/.venv/bin/python
```

每个 fresh task 在第一次使用前必须机械验证：

- `.venv/pyvenv.cfg version = 3.13.3`；
- runtime Python = `3.13.3`；
- architecture = `arm64`；
- resolved base interpreter = `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3.13`；
- resolved base interpreter 是 regular file；
- resolved bytes = `119328`；
- resolved SHA-256 = `f5d584368bd127649722baa482517054d3c941ea5fbd29a669a8c5323dd21be5`；
- pytest = `9.1.1`；
- fastapi = `0.115.6`；
- psycopg = `3.2.3`。

若 identity/package precondition 不匹配，terminal 必须是：

```text
HOLD / PROJECT_TEST_RUNTIME_DRIFT
```

不得 fallback、install、upgrade、recreate 或 mutate `.venv`。

## 5. PROJECT_TEST_RUNTIME scope boundary

`PROJECT_TEST_RUNTIME` 仅用于：

- Python compile/import validation；
- task-authorized pytest；
- task-authorized local test utilities。

它不替代 `CONTROL_PLANE_PYTHON`，也不授权：

- PM/task hashing；
- control-plane evidence generation；
- DB runtime；
- API live server；
- Docker；
- remote；
- Git mutation。

本 amendment 对本 Goal 剩余 local validation Gates 持续有效，不是 one-shot override，也不向其他 Goal 继承。

## 6. Gate and budget interpretation

Amendment materialization 是 Owner-authorized `A0_CONTROL_PLANE` action：

```text
PRODUCT_REPAIR_GATE       = +0
CONTROL_PLANE_RECOVERY_GATE = +0
TOTAL_DISPATCHED_GATES    = +0
```

它不重置任何既有 counter，不接受任何 product candidate，不改变 `P1_G3_EXECUTION_AUTHORIZED = NO`，也不改变 Git stage/commit/push/tag、DB runtime、Docker、remote、PLC/V-PLC authority 均为 0 的约束。

## 7. Parent audit obligation

Parent controller 在本文件写入后必须使用 `CONTROL_PLANE_PYTHON` 机械计算本文件的 regular/non-symlink、bytes、SHA-256，并在 Goal Ledger 记录 exact identity。原 Charter identity 必须同时保持不变。

只有完成该 amendment 的 durable materialization 与独立审计后，parent 才能按 Section 2 的 autonomous continuation rule 创建新的 G2 source/test repair task。
