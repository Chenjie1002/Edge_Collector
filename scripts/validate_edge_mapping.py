from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

from snap7 import util

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT))

from app.plc import build_read_plans, decode_read_plan, load_edge_mapping  # noqa: E402


def main() -> None:
    mapping_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "config" / "mapping.yaml"
    mapping = load_edge_mapping(mapping_path)
    plans = build_read_plans(mapping)
    by_scope = {plan.scope: plan for plan in plans}

    assert by_scope["line"].db_number == 104
    assert by_scope["WS01"].db_number == 101
    assert by_scope["WS02"].db_number == 102
    assert by_scope["WS03"].db_number == 103
    assert by_scope["WS01"].read_start == 0
    assert by_scope["WS01"].read_size >= 124

    line = by_scope["line"]
    line_sample = bytearray(line.read_size)
    util.set_int(line_sample, 0, 1)
    util.set_dint(line_sample, 4, 27)
    util.set_dint(line_sample, 8, 4)
    boot_id = b"12345678-1234-1234-1234-123456789abc"
    line_sample[12] = 36
    line_sample[13] = len(boot_id)
    line_sample[14 : 14 + len(boot_id)] = boot_id
    util.set_bool(line_sample, 52, 3, True)
    line_decoded = decode_read_plan(line_sample, line, mapping.timezone)
    assert line_decoded["protocol_version"] == 1
    assert line_decoded["heartbeat_counter"] == 27
    assert line_decoded["plc_restart_counter"] == 4
    assert line_decoded["plc_boot_id"] == boot_id.decode("ascii")
    assert line_decoded["ignore_edge"] is True

    ws01 = by_scope["WS01"]
    sample = bytearray(ws01.read_size)
    util.set_int(sample, 0, 2)
    util.set_dint(sample, 2, 123)
    util.set_bool(sample, 6, 0, True)
    util.set_bool(sample, 6, 1, False)
    util.set_dint(sample, 8, 1781490600)
    util.set_dint(sample, 12, 1781490630)
    util.set_int(sample, 16, 1)
    util.set_int(sample, 18, 1)
    util.set_int(sample, 20, 10001)
    sample[40] = 40
    sample[41] = 12
    sample[42:54] = b"CHILD-000001"
    sample[100:104] = struct.pack(">f", 1.42)

    decoded = decode_read_plan(sample, ws01, mapping.timezone)
    assert decoded["station_status"] == 2
    assert decoded["cycle_counter"] == 123
    assert decoded["payload_ready"] is True
    assert decoded["result"] == 1
    assert decoded["nok_codes_1"] == 10001
    assert decoded["station_dmc"] == "CHILD-000001"
    assert decoded["screw_1_torque_nm"] == 1.42

    print(
        json.dumps(
            [
                {
                    "scope": plan.scope,
                    "db_number": plan.db_number,
                    "read_start": plan.read_start,
                    "read_size": plan.read_size,
                    "field_count": len(plan.fields),
                }
                for plan in plans
            ],
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
