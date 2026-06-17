from abc import ABC, abstractmethod

from app.models import MachineState


class Source(ABC):
    @abstractmethod
    def read(self) -> MachineState:
        raise NotImplementedError

