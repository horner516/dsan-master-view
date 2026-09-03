"""Exercise the update button in a real desktop webview without device connections."""
import sys
import threading
import time
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import webview
from app import create_server
from desktop import DesktopApi

with patch('app.LimitimerWorker'), patch('app.PerfectCueWorker'):
    server = create_server(0)
server.desktop_bridge = '--desktop-policy' in sys.argv
threading.Thread(target=server.serve_forever, daemon=True).start()
api = DesktopApi(False)
api.server_port = server.server_port
window = webview.create_window('Update check verification', f'http://127.0.0.1:{server.server_port}', js_api=api)

def verify():
    try:
        time.sleep(3)
        print('BRIDGE:', window.evaluate_js('typeof window.pywebview.api.check_for_updates'), flush=True)
        window.evaluate_js("document.getElementById('update-button').click()")
        time.sleep(12)
        print('RESULT:', window.evaluate_js("document.getElementById('update-message').textContent"), flush=True)
    finally:
        window.destroy()

try:
    webview.start(verify)
finally:
    server.shutdown()
    server.server_close()
