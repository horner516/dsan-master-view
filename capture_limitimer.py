#!/usr/bin/env python3
import json
import socket
import sys
import time
from datetime import datetime, timezone


HOST = "10.21.0.119"
PORT = 6120
OUTPUT = "limitimer_capture.jsonl"
MAX_SECONDS = 12 * 60


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def parse_time(frame, offset):
    return frame[offset] * 128 * 128 + frame[offset + 1] * 128 + frame[offset + 2]


def main():
    started = time.monotonic()
    buffer = bytearray()
    counts = {6: 0, 55: 0, "other": 0}

    with socket.create_connection((HOST, PORT), timeout=5) as sock, open(
        OUTPUT, "a", buffering=1
    ) as capture:
        sock.settimeout(1)
        print(f"Connected to {HOST}:{PORT}; recording to {OUTPUT}", flush=True)

        try:
            while time.monotonic() - started < MAX_SECONDS:
                try:
                    chunk = sock.recv(4096)
                except socket.timeout:
                    continue
                if not chunk:
                    print("Controller closed the connection", flush=True)
                    return 1
                buffer.extend(chunk)

                while buffer:
                    if buffer[0] != 0x81:
                        del buffer[0]
                        counts["other"] += 1
                        continue

                    frame_len = 6 if len(buffer) >= 2 and buffer[1] == 0x10 else 55
                    if len(buffer) < frame_len:
                        break

                    frame = bytes(buffer[:frame_len])
                    del buffer[:frame_len]
                    if frame[-1] != 0xFF:
                        counts["other"] += frame_len
                        continue

                    counts[frame_len] += 1
                    record = {
                        "utc": utc_now(),
                        "elapsed": round(time.monotonic() - started, 3),
                        "length": frame_len,
                        "hex": frame.hex(),
                    }
                    capture.write(json.dumps(record) + "\n")

                    if frame_len == 55 and counts[55] % 20 == 1:
                        selected = frame[5]
                        offset = 6 + selected * 11
                        total = parse_time(frame, offset + 2)
                        elapsed = parse_time(frame, offset + 8)
                        remaining = total - elapsed
                        sign = "-" if remaining < 0 else ""
                        remaining = abs(remaining)
                        print(
                            f"Receiving: program={selected + 1}, "
                            f"remaining={sign}{remaining // 60}:{remaining % 60:02d}, "
                            f"running={bool(frame[offset] & 1)}, frames={counts[55]}",
                            flush=True,
                        )
        except KeyboardInterrupt:
            print(f"Capture stopped: {counts}", flush=True)
            return 0

        print(f"Capture complete: {counts}", flush=True)
        return 0


if __name__ == "__main__":
    sys.exit(main())
