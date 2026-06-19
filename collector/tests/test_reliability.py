from __future__ import annotations

import unittest

from app.services.reliability import CounterDecision, classify_counter, validate_plc_boot_id


class PlcIdentityValidationTest(unittest.TestCase):
    def test_accepts_uuid_boot_id(self) -> None:
        self.assertEqual(
            "12345678-1234-1234-1234-123456789abc",
            validate_plc_boot_id("12345678-1234-1234-1234-123456789abc"),
        )

    def test_rejects_missing_or_collector_identity(self) -> None:
        for value in ("", "UNKNOWN", "COLLECTOR-123"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_plc_boot_id(value)


class CounterClassificationTest(unittest.TestCase):
    def test_first_and_increasing_counter_are_accepted(self) -> None:
        self.assertEqual(CounterDecision.ACCEPT, classify_counter(None, 1))
        self.assertEqual(CounterDecision.ACCEPT, classify_counter(8, 9))
        self.assertEqual(CounterDecision.ACCEPT, classify_counter(8, 12))

    def test_same_counter_is_duplicate_for_idempotent_ack_recovery(self) -> None:
        self.assertEqual(CounterDecision.DUPLICATE, classify_counter(8, 8))

    def test_lower_counter_is_reset_and_must_not_be_acked(self) -> None:
        self.assertEqual(CounterDecision.RESET, classify_counter(8, 1))


if __name__ == "__main__":
    unittest.main()
