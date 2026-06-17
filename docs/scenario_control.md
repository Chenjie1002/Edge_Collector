# Scenario Control Guide

The simulator includes a lightweight scenario control API and web page for demo
workflows. It drives the business simulator first, then the S7 PLC simulator
copies the state into `DB100`, and the collector reads the values through Snap7.

## Web Control Page

Open:

```text
http://<raspberry-pi-ip>:8100/control
```

The page shows the current machine state and provides buttons for:

| Scenario | Effect |
| --- | --- |
| 正常生产 | Clears manual alarm/stop/profile states |
| 第1岗位缺料 | Stop condition, `stop_reason_code=2` |
| 气缸传感器故障 | Alarm condition, `alarm_code=1002` |
| 换型/调机 | Stop condition, `stop_reason_code=4`, product type rotates |
| 计划保养 | Stop condition, `stop_reason_code=5` |
| 节拍变慢 | Machine keeps running, cycle time increases |
| 熟练稳定生产 | Machine keeps running, cycle time decreases and NG rate lowers |

Manual scenarios take priority over random background events. When a manual
scenario expires, the simulator returns to normal production.

## API

List scenarios:

```bash
curl http://<raspberry-pi-ip>:8100/scenarios
```

Read current state:

```bash
curl http://<raspberry-pi-ip>:8100/state
```

Trigger a scenario with a duration in seconds:

```bash
curl -X POST http://<raspberry-pi-ip>:8100/scenario/material_shortage \
  -H 'Content-Type: application/json' \
  -d '{"duration_seconds": 180}'
```

Return to normal:

```bash
curl -X POST http://<raspberry-pi-ip>:8100/scenario/normal \
  -H 'Content-Type: application/json' \
  -d '{}'
```

Reset counters:

```bash
curl -X POST http://<raspberry-pi-ip>:8100/reset-counts
```

## PLC Mapping

The active scenario is also written to `DB100.DBB30` as `scenario_code`.
See `docs/plc_address_map.md` for the full address map.
