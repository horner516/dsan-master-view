import io
import json
import unittest
from unittest.mock import Mock, patch

from app import Handler

from desktop import APP_VERSION, DesktopApi


class DesktopTests(unittest.TestCase):
    def test_bridge_policy_only_for_local_desktop_requests(self):
        for desktop, address, allowed in [(True, '127.0.0.1', True), (True, '10.21.1.20', False), (False, '127.0.0.1', False)]:
            with self.subTest(desktop=desktop, address=address):
                handler = Handler.__new__(Handler)
                handler.server = Mock(desktop_bridge=desktop)
                handler.client_address = (address, 50000)
                handler.send_response = Mock()
                handler.send_header = Mock()
                handler.end_headers = Mock()
                handler.wfile = io.BytesIO()
                handler.send_bytes(b'ok', 'text/html')
                headers = dict(call.args for call in handler.send_header.call_args_list)
                self.assertEqual("'unsafe-eval'" in headers['Content-Security-Policy'], allowed)

    def test_current_version_message(self):
        release = io.StringIO(json.dumps({'tag_name': f'v{APP_VERSION}', 'assets': []}))
        with patch('desktop.urllib.request.urlopen', return_value=release):
            result = DesktopApi(False).check_for_updates()
        self.assertFalse(result['update_available'])
        self.assertEqual(result['message'], 'you are running the latest version you filthy animal')

    def test_invalid_release_does_not_claim_up_to_date(self):
        with patch('desktop.urllib.request.urlopen', return_value=io.StringIO('{}')):
            result = DesktopApi(False).check_for_updates()
        self.assertIn('Could not read', result['message'])

    def test_browser_display_uses_selected_port(self):
        api = DesktopApi(False)
        api.server_port = 55001
        with patch('desktop.webbrowser.open', return_value=True) as browser:
            api.open_browser_fullscreen()
        browser.assert_called_once_with('http://127.0.0.1:55001/?display=fullscreen', new=1)


if __name__ == '__main__':
    unittest.main()
