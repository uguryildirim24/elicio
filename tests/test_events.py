from __future__ import annotations

import math
import unittest

from elicio.harness.events import GestureEvent


class GestureEventTests(unittest.TestCase):
    def test_stable_tuple_contract(self) -> None:
        event = GestureEvent("wrist_down", 0.92, 123.5)

        self.assertEqual(event.as_tuple(), ("wrist_down", 0.92, 123.5))
        self.assertEqual(
            event.to_dict(),
            {
                "symbol": "wrist_down",
                "confidence": 0.92,
                "timestamp": 123.5,
            },
        )

    def test_rejects_blank_or_padded_symbols(self) -> None:
        for symbol in ("", "   ", " wrist_down", "wrist_down "):
            with self.subTest(symbol=symbol):
                with self.assertRaises(ValueError):
                    GestureEvent(symbol, 0.9, 1.0)

    def test_rejects_confidence_outside_contract(self) -> None:
        for confidence in (-0.01, 1.01, math.inf, -math.inf, math.nan):
            with self.subTest(confidence=confidence):
                with self.assertRaises(ValueError):
                    GestureEvent("wrist_down", confidence, 1.0)

    def test_rejects_invalid_timestamp(self) -> None:
        for timestamp in (-0.01, math.inf, -math.inf, math.nan):
            with self.subTest(timestamp=timestamp):
                with self.assertRaises(ValueError):
                    GestureEvent("wrist_down", 0.9, timestamp)


if __name__ == "__main__":
    unittest.main()
