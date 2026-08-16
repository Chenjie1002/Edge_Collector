from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RuntimeLayoutRegistry:
    """Reusable S7 layout/decoder metadata, without topology ownership."""

    snapshot_id: str
    decoder_id: str
    decoder_version: str
    common_header: dict[str, Any]
    payload_layouts: dict[str, dict[str, Any]]
    code_tables: dict[str, dict[int, str]]

    @property
    def content_hash(self) -> str:
        content = {
            "snapshot_id": self.snapshot_id,
            "decoder_id": self.decoder_id,
            "decoder_version": self.decoder_version,
            "common_header": self.common_header,
            "payload_layouts": self.payload_layouts,
            "code_tables": self.code_tables,
        }
        encoded = json.dumps(
            content,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def payload_for(self, template_id: str | None) -> dict[str, Any]:
        if not template_id or template_id not in self.payload_layouts:
            raise KeyError(f"runtime payload layout is not registered: {template_id}")
        return self.payload_layouts[template_id]


def default_runtime_layout_registry() -> RuntimeLayoutRegistry:
    """Return the fixed reusable layout family used by the R3 projection.

    The registry contains only field layouts, decoder identity and interpretation
    tables. Station order, route edges, terminal identity, PLC selection and DB
    allocation are deliberately supplied by ``LineConfig`` to the compiler.
    """

    common_header = {
        "station_status": {"address": "{db}.DBW0", "type": "word"},
        "cycle_counter": {"address": "{db}.DBD2", "type": "dint"},
        "payload_ready": {"address": "{db}.DBX6.0", "type": "bool"},
        "read_done": {
            "address": "{db}.DBX6.1",
            "type": "bool",
            "direction": "read_write",
        },
        "ack_timeout": {"address": "{db}.DBX6.2", "type": "bool"},
        "cycle_valid": {"address": "{db}.DBX6.3", "type": "bool"},
        "plc_start_time": {"address": "{db}.DBD8", "type": "unix_time_seconds"},
        "plc_end_time": {"address": "{db}.DBD12", "type": "unix_time_seconds"},
        "result": {"address": "{db}.DBW16", "type": "word"},
        "nok_code_count": {"address": "{db}.DBW18", "type": "word"},
        "nok_codes": {
            "type": "array",
            "items": [
                {"address": "{db}.DBW20", "type": "word"},
                {"address": "{db}.DBW22", "type": "word"},
                {"address": "{db}.DBW24", "type": "word"},
            ],
        },
        "alarm_code": {"address": "{db}.DBW26", "type": "word"},
        "downtime_type": {"address": "{db}.DBW28", "type": "word"},
        "pallet_id_numeric": {
            "address": "{db}.DBD30",
            "type": "dint",
            "required": False,
        },
        "station_dmc": {"address": "{db}.DBB40", "type": "string", "max_length": 40},
        "unit_id": {"address": "{db}.DBB200", "type": "string", "max_length": 48},
        "route_step": {"address": "{db}.DBW250", "type": "word"},
        "route_state": {"address": "{db}.DBW252", "type": "word"},
        "process_status": {"address": "{db}.DBW254", "type": "word"},
        "skip_reason": {"address": "{db}.DBW256", "type": "word"},
        "defect_origin_station": {"address": "{db}.DBW258", "type": "word"},
        "defect_code": {"address": "{db}.DBW260", "type": "word"},
        "final_label_code": {
            "address": "{db}.DBB262",
            "type": "string",
            "max_length": 40,
        },
        "reject_id": {"address": "{db}.DBB304", "type": "string", "max_length": 40},
    }

    payload_layouts = {
        "screwdriving_payload_v1": {
            "screw_1_torque_nm": {"address": "{db}.DBD100", "type": "real"},
            "screw_1_angle_deg": {"address": "{db}.DBD104", "type": "real"},
            "screw_2_torque_nm": {"address": "{db}.DBD108", "type": "real"},
            "screw_2_angle_deg": {"address": "{db}.DBD112", "type": "real"},
            "screw_3_torque_nm": {"address": "{db}.DBD116", "type": "real"},
            "screw_3_angle_deg": {"address": "{db}.DBD120", "type": "real"},
        },
        "eol_test_payload_v1": {
            "avg_current_a": {"address": "{db}.DBD100", "type": "real"},
            "avg_voltage_v": {"address": "{db}.DBD104", "type": "real"},
            "clockwise_time_ms": {"address": "{db}.DBD108", "type": "dint"},
            "counterclockwise_time_ms": {"address": "{db}.DBD112", "type": "dint"},
            "stall_peak_current_a": {"address": "{db}.DBD116", "type": "real"},
            "stall_time_ms": {"address": "{db}.DBD120", "type": "dint"},
            "upstream_ws01_end_time": {
                "address": "{db}.DBD124",
                "type": "unix_time_seconds",
            },
            "upstream_ws01_result": {"address": "{db}.DBW128", "type": "word"},
            "upstream_child_dmc": {
                "address": "{db}.DBB130",
                "type": "string",
                "max_length": 40,
            },
        },
        "manual_confirm_payload_v1": {
            "serial_no": {"address": "{db}.DBD100", "type": "dint"},
            "product_model_code": {"address": "{db}.DBW104", "type": "word"},
            "upstream_ws02_end_time": {
                "address": "{db}.DBD106",
                "type": "unix_time_seconds",
            },
            "upstream_ws02_result": {"address": "{db}.DBW110", "type": "word"},
            "upstream_child_dmc": {
                "address": "{db}.DBB112",
                "type": "string",
                "max_length": 40,
            },
            "upstream_ws02_dmc": {
                "address": "{db}.DBB154",
                "type": "string",
                "max_length": 40,
            },
        },
        "flexible_payload_v1": {
            "status_word": {"address": "{db}.DBW100", "type": "word"},
            "process_value": {"address": "{db}.DBD104", "type": "real", "required": False},
        },
        "generic_status_v1": {
            "status_word": {"address": "{db}.DBW100", "type": "word"},
        },
    }

    code_tables = {
        "result": {0: "UNKNOWN", 1: "OK", 2: "NOK", 3: "SKIPPED"},
        "route_state": {
            0: "UNKNOWN",
            1: "NORMAL",
            2: "BYPASSING",
            3: "COMPLETED_OK",
            4: "COMPLETED_NOK",
        },
        "process_status": {0: "UNKNOWN", 1: "PROCESSED", 2: "SKIPPED"},
        "skip_reason": {0: "NONE", 1: "UPSTREAM_NOK"},
    }
    return RuntimeLayoutRegistry(
        snapshot_id="runtime-layout-registry-r3-10ws-v1",
        decoder_id="collector.app.plc.decoder.decode_runtime_raw_hex_payload",
        decoder_version="1.0.0",
        common_header=common_header,
        payload_layouts=payload_layouts,
        code_tables=code_tables,
    )
