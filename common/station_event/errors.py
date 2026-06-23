from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class ValidationError:
    path: str
    code: str
    message: str


class StationEventValidationError(ValueError):
    def __init__(self, errors: tuple[ValidationError, ...]) -> None:
        self.errors = errors
        summary = "; ".join(f"{error.path}: {error.code}" for error in errors)
        super().__init__(summary)
