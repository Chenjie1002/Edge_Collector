from __future__ import annotations

from collections import deque
from datetime import datetime
import logging
from typing import Any
import uuid
from zoneinfo import ZoneInfo


logger = logging.getLogger("s7-plc-sim.parameter-audit")
TZ = ZoneInfo("Asia/Shanghai")


class ParameterAuditRecorder:
    def __init__(self, dsn: str | None = None, *, max_memory_records: int = 200) -> None:
        self.dsn = dsn
        self._changes: deque[dict[str, Any]] = deque(maxlen=max_memory_records)
        self._snapshots: deque[dict[str, Any]] = deque(maxlen=max_memory_records)

    def record_change(self, event: dict[str, Any]) -> dict[str, Any]:
        record = {
            "change_id": str(event.get("change_id") or uuid.uuid4()),
            "changed_at": str(event.get("changed_at") or datetime.now(TZ).isoformat()),
            "plc_boot_id": event.get("plc_boot_id"),
            "station_id": event.get("station_id"),
            "parameter_name": event.get("parameter_name"),
            "old_value": event.get("old_value"),
            "new_value": event.get("new_value"),
            "source": event.get("source") or "INTERNAL",
            "actor": event.get("actor") or "system",
            "client_ip": event.get("client_ip"),
            "request_id": event.get("request_id") or str(uuid.uuid4()),
            "reason": event.get("reason") or "internal update",
            "profile": event.get("profile"),
            "accepted": bool(event.get("accepted")),
            "rejection_reason": event.get("rejection_reason"),
        }
        self._changes.appendleft(record)
        self._persist_change(record)
        return record

    def record_snapshot(self, snapshot: dict[str, Any]) -> dict[str, Any]:
        record = {
            "snapshot_id": str(snapshot.get("snapshot_id") or uuid.uuid4()),
            "captured_at": str(snapshot.get("captured_at") or datetime.now(TZ).isoformat()),
            "snapshot_type": snapshot.get("snapshot_type") or "runtime",
            "plc_boot_id": snapshot.get("plc_boot_id"),
            "profile": snapshot.get("profile"),
            "cycle_scale": snapshot.get("cycle_scale"),
            "config_source": snapshot.get("config_source"),
            "config_hash": snapshot.get("config_hash"),
            "parameters": snapshot.get("parameters") or {},
        }
        self._snapshots.appendleft(record)
        self._persist_snapshot(record)
        return record

    def recent_changes(self, limit: int = 100) -> list[dict[str, Any]]:
        bounded_limit = max(0, min(limit, 200))
        persisted = self._load_persisted_changes(bounded_limit)
        return persisted if persisted else list(self._changes)[:bounded_limit]

    def recent_snapshots(self, limit: int = 100) -> list[dict[str, Any]]:
        bounded_limit = max(0, min(limit, 200))
        persisted = self._load_persisted_snapshots(bounded_limit)
        return persisted if persisted else list(self._snapshots)[:bounded_limit]

    def _load_persisted_changes(self, limit: int) -> list[dict[str, Any]]:
        if not self.dsn or limit <= 0:
            return []
        try:
            import psycopg
            from psycopg.rows import dict_row

            with psycopg.connect(self.dsn, row_factory=dict_row) as conn:
                rows = conn.execute(
                    """
                    SELECT change_id::text, changed_at, plc_boot_id, station_id,
                           parameter_name, old_value, new_value, source, actor,
                           client_ip, request_id, reason, profile, accepted,
                           rejection_reason
                    FROM vplc_parameter_change_log
                    ORDER BY changed_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                ).fetchall()
            return [dict(row) for row in rows]
        except Exception:
            logger.exception("failed to query persisted V-PLC parameter changes")
            return []

    def _load_persisted_snapshots(self, limit: int) -> list[dict[str, Any]]:
        if not self.dsn or limit <= 0:
            return []
        try:
            import psycopg
            from psycopg.rows import dict_row

            with psycopg.connect(self.dsn, row_factory=dict_row) as conn:
                rows = conn.execute(
                    """
                    SELECT snapshot_id::text, captured_at, snapshot_type, plc_boot_id,
                           profile, cycle_scale, config_source, config_hash, parameters
                    FROM vplc_parameter_snapshot
                    ORDER BY captured_at DESC
                    LIMIT %s
                    """,
                    (limit,),
                ).fetchall()
            return [dict(row) for row in rows]
        except Exception:
            logger.exception("failed to query persisted V-PLC parameter snapshots")
            return []

    def _persist_change(self, record: dict[str, Any]) -> None:
        if not self.dsn:
            return
        try:
            import psycopg
            from psycopg.types.json import Jsonb

            with psycopg.connect(self.dsn) as conn:
                conn.execute(
                    """
                    INSERT INTO vplc_parameter_change_log (
                        change_id, changed_at, plc_boot_id, station_id, parameter_name,
                        old_value, new_value, source, actor, client_ip, request_id,
                        reason, profile, accepted, rejection_reason
                    ) VALUES (
                        %(change_id)s, %(changed_at)s, %(plc_boot_id)s, %(station_id)s,
                        %(parameter_name)s, %(old_value)s, %(new_value)s, %(source)s,
                        %(actor)s, %(client_ip)s, %(request_id)s, %(reason)s, %(profile)s,
                        %(accepted)s, %(rejection_reason)s
                    )
                    """,
                    {**record, "old_value": Jsonb(record["old_value"]), "new_value": Jsonb(record["new_value"])},
                )
        except Exception:
            logger.exception("failed to persist V-PLC parameter change change_id=%s", record["change_id"])

    def _persist_snapshot(self, record: dict[str, Any]) -> None:
        if not self.dsn:
            return
        try:
            import psycopg
            from psycopg.types.json import Jsonb

            with psycopg.connect(self.dsn) as conn:
                conn.execute(
                    """
                    INSERT INTO vplc_parameter_snapshot (
                        snapshot_id, captured_at, snapshot_type, plc_boot_id, profile,
                        cycle_scale, config_source, config_hash, parameters
                    ) VALUES (
                        %(snapshot_id)s, %(captured_at)s, %(snapshot_type)s, %(plc_boot_id)s,
                        %(profile)s, %(cycle_scale)s, %(config_source)s, %(config_hash)s,
                        %(parameters)s
                    )
                    """,
                    {**record, "parameters": Jsonb(record["parameters"])},
                )
        except Exception:
            logger.exception("failed to persist V-PLC parameter snapshot snapshot_id=%s", record["snapshot_id"])
