from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from typing import Any


RawDecoder = Callable[[Mapping[str, Any], Mapping[str, Any]], Mapping[str, Any]]


@dataclass(frozen=True)
class DecoderBinding:
    decoder_id: str
    decoder_version: str
    callable_ref: str
    decoder: RawDecoder | None
    payload_template: str | None = None


@dataclass(frozen=True)
class DecoderRegistrySnapshot:
    registry_snapshot_id: str
    registry_content_hash: str
    decoders: tuple[DecoderBinding, ...]
    schema_version: str = "decoder-registry/v1"
    hash_algorithm: str = "sha256"

    def compute_content_hash(self) -> str:
        return compute_decoder_registry_hash(self)

    def with_content_hash(self) -> "DecoderRegistrySnapshot":
        return replace(self, registry_content_hash=self.compute_content_hash())

    def content_hash_matches(self) -> bool:
        return self.compute_content_hash() == self.registry_content_hash

    def decode_raw_payload(
        self,
        *,
        decoder_id: str,
        decoder_version: str,
        raw_payload: Mapping[str, Any],
        event: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        if not self.content_hash_matches():
            raise ValueError("DECODER_REGISTRY_HASH_MISMATCH")
        binding = self._binding_for(decoder_id)
        if binding is None:
            raise ValueError("DECODER_ID_UNKNOWN")
        if binding.decoder_version != decoder_version:
            raise ValueError("DECODER_VERSION_MISMATCH")
        if binding.decoder is None:
            raise ValueError("DECODER_CALLABLE_MISSING")
        if binding.payload_template is not None:
            payload_template = event.get("correlation", {}).get("payload_template")
            if payload_template != binding.payload_template:
                raise ValueError("DECODER_PAYLOAD_TEMPLATE_MISMATCH")
        decoded = binding.decoder(raw_payload, event)
        if not isinstance(decoded, Mapping):
            raise ValueError("DECODER_OUTPUT_INVALID")
        return dict(decoded)

    def _binding_for(self, decoder_id: str) -> DecoderBinding | None:
        return next((item for item in self.decoders if item.decoder_id == decoder_id), None)


def compute_decoder_registry_hash(snapshot: DecoderRegistrySnapshot) -> str:
    content = {
        "schema_version": snapshot.schema_version,
        "registry_snapshot_id": snapshot.registry_snapshot_id,
        "hash_algorithm": snapshot.hash_algorithm,
        "decoders": [
            {
                "decoder_id": decoder.decoder_id,
                "decoder_version": decoder.decoder_version,
                "callable_ref": decoder.callable_ref,
                "payload_template": decoder.payload_template,
            }
            for decoder in sorted(
                snapshot.decoders,
                key=lambda item: (item.decoder_id, item.decoder_version, item.callable_ref),
            )
        ],
    }
    encoded = json.dumps(
        content,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
