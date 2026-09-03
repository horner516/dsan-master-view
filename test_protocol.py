import unittest

from app import LOCAL_PORT, SERVER_BIND_HOST, SharedState, base128_time, crc16_modbus, parse_limitimer_frame, validate_config


CAPTURED_FRAME = bytes.fromhex(
    "8100217f0600010000045800007800000d0600000000000000000000060000000000000000000006000000000000000000000083e926ff"
)


class ProtocolTests(unittest.TestCase):
    def test_local_application_port(self):
        self.assertEqual(LOCAL_PORT, 53971)
        self.assertEqual(SERVER_BIND_HOST, "0.0.0.0")

    def test_base128_time(self):
        self.assertEqual(base128_time(bytes.fromhex("000458"), 0), 600)
        self.assertEqual(base128_time(bytes.fromhex("000078"), 0), 120)

    def test_crc(self):
        self.assertEqual(crc16_modbus(CAPTURED_FRAME[:52]), 0xE926)

    def test_captured_limitimer_frame(self):
        parsed = parse_limitimer_frame(CAPTURED_FRAME)
        self.assertEqual(parsed["selected_program"], 1)
        self.assertTrue(parsed["countdown"])
        self.assertTrue(parsed["active"]["running"])
        self.assertEqual(parsed["active"]["total_seconds"], 600)
        self.assertEqual(parsed["active"]["sumup_seconds"], 120)
        self.assertEqual(parsed["active"]["elapsed_seconds"], 13)
        self.assertEqual(parsed["active"]["remaining"], "9:47")

    def test_perfectcue_event(self):
        state = SharedState()
        state.perfectcue_event(0x0F)
        cue = state.snapshot()["perfectcue"]
        self.assertEqual(cue["last_event"]["kind"], "next")
        self.assertEqual(cue["last_event"]["code"], "0x0F")
        self.assertEqual(cue["event_count"], 1)

    def test_bad_checksum_is_rejected(self):
        damaged = bytearray(CAPTURED_FRAME)
        damaged[16] += 1
        with self.assertRaisesRegex(ValueError, "checksum"):
            parse_limitimer_frame(bytes(damaged))

    def test_overtime_display_setting(self):
        config = validate_config(
            {
                "limitimer": {"host": "10.21.0.119", "port": 6120, "enabled": True},
                "perfectcue": {"host": "", "port": 6120, "enabled": False},
                "display": {"overtime": "stop"},
            }
        )
        self.assertEqual(config["display"]["overtime"], "stop")

    def test_display_preferences(self):
        config = validate_config(
            {
                "limitimer": {"host": "10.21.0.119", "port": 6120, "enabled": True},
                "perfectcue": {"host": "", "port": 6120, "enabled": False},
                "display": {"overtime": "continue", "font": "condensed", "show_lights": False},
            }
        )
        self.assertEqual(config["display"]["font"], "condensed")
        self.assertFalse(config["display"]["show_lights"])


if __name__ == "__main__":
    unittest.main()
