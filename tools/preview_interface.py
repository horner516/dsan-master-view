"""Isolated interface preview: sample data, no device connections or real settings writes."""
import sys
import tempfile
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import app
from test_protocol import CAPTURED_FRAME

app.CONFIG_PATH = Path(tempfile.mkdtemp(prefix='dsan-ui-preview-')) / 'config.json'
app.SHARED.config = app.deepcopy(app.DEFAULT_CONFIG)
app.SHARED.config['limitimer']['enabled'] = False
app.SHARED.config['display'].update(fixed_color=False)
app.SHARED.data['limitimer'].update(status='connected', packet_count=1, data=app.parse_limitimer_frame(CAPTURED_FRAME))

class PreviewHandler(app.Handler):
    def send_bytes(self, body, content_type, status=app.HTTPStatus.OK):
        if content_type.startswith('text/html'):
            panel = parse_qs(urlsplit(self.path).query).get('panel', [''])[0]
            button = {'settings':'open-settings', 'message':'open-message'}.get(panel)
            script = "document.title='D’San — interface preview';"
            if button:
                script += "setTimeout(()=>document.getElementById('%s').click(),700);" % button
            body = body.replace(b'</body>', ('<script>'+script+'</script></body>').encode())
        super().send_bytes(body, content_type, status)

server = ThreadingHTTPServer(('127.0.0.1', int(sys.argv[1]) if len(sys.argv) > 1 else 0), PreviewHandler)
app.SHARED.server_port = server.server_port
print(f'PREVIEW_URL=http://127.0.0.1:{server.server_port}', flush=True)
server.serve_forever()
