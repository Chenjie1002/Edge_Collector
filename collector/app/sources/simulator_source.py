import httpx

from app.models import MachineState
from app.sources.base import Source


class SimulatorSource(Source):
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def read(self) -> MachineState:
        response = httpx.get(f"{self.base_url}/state", timeout=5.0)
        response.raise_for_status()
        return MachineState.from_payload(response.json())

