from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import snap7

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "collector"))
sys.path.insert(0, str(ROOT))

from app.plc import build_read_plans, decode_read_plan, load_edge_mapping  # noqa: E402


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "s7-plc-sim"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1102
    mapping_path = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("/app/config/mapping.yaml")
    wait_seconds = int(sys.argv[4]) if len(sys.argv) > 4 else 0

    if wait_seconds:
        time.sleep(wait_seconds)

    mapping = load_edge_mapping(mapping_path)
    plans = [plan for plan in build_read_plans(mapping) if plan.scope in {"WS01", "WS02", "WS03"}]

    client = snap7.client.Client()
    client.connect(host, 0, 1, tcp_port=port)
    try:
        result = {}
        for plan in plans:
            data = client.db_read(plan.db_number, plan.read_start, plan.read_size)
            decoded = decode_read_plan(data, plan, mapping.timezone)
            result[plan.scope] = {
                "db_number": plan.db_number,
                "station_status": decoded["station_status"],
                "cycle_counter": decoded["cycle_counter"],
                "payload_ready": decoded["payload_ready"],
                "read_done": decoded["read_done"],
                "cycle_valid": decoded["cycle_valid"],
                "result": decoded["result"],
                "station_dmc": decoded["station_dmc"],
                "plc_start_time": decoded["plc_start_time"],
                "plc_end_time": decoded["plc_end_time"],
            }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
