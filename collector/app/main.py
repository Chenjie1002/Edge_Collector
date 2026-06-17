import logging
import threading
import time

from app.config import database_url, event_collector_enabled, load_config, simulator_url, snap7_host, snap7_port
from app.services.event_detector import EventDetector
from app.services.event_collector import EventCollectorWorker
from app.services.storage import Storage
from app.sources.snap7_source import Snap7Source
from app.sources.simulator_source import SimulatorSource

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("edge-collector")


def main() -> None:
    config = load_config()
    interval_ms = int(config.get("collector", {}).get("polling_interval_ms", 1000))
    source_type = config.get("collector", {}).get("source_type", "simulator")
    if source_type == "snap7":
        source = Snap7Source(snap7_host(), snap7_port())
    else:
        source = SimulatorSource(simulator_url())
    storage = Storage(database_url())
    detector = EventDetector(storage)
    if event_collector_enabled():
        event_worker = EventCollectorWorker(dsn=database_url(), host=snap7_host(), port=snap7_port())
        threading.Thread(
            target=event_worker.run_forever,
            name="event-collector",
            daemon=True,
        ).start()

    logger.info("collector started source_type=%s interval_ms=%s", source_type, interval_ms)
    while True:
        try:
            state = source.read()
            storage.ensure_machine(state)
            storage.insert_snapshot(state)
            detector.process(state)
            logger.info(
                "snapshot machine=%s running=%s total=%s ct=%sms alarm=%s stop=%s",
                state.machine_id,
                state.running,
                state.total_count,
                state.cycle_time_ms,
                state.alarm_code,
                state.stop_reason_code,
            )
        except Exception:
            logger.exception("collector loop failed")
            time.sleep(5)
        time.sleep(interval_ms / 1000)


if __name__ == "__main__":
    main()
