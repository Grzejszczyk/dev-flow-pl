import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qsl


BASE_DIR = Path(__file__).parent


def update_record(records, record_id, fields):
    if record_id not in records:
        return 404
    updated = {**records[record_id], **fields}
    if not updated.get("name", "").strip():
        return 422
    records[record_id] = updated
    return 200


class RecordHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write((BASE_DIR / "editor.html").read_bytes())

    def do_POST(self):
        if not self.path.startswith("/records/"):
            self.send_error(404)
            return
        record_id = self.path.removeprefix("/records/")
        body = self.rfile.read(int(self.headers["Content-Length"])).decode()
        fields = dict(parse_qsl(body, keep_blank_values=True))
        status = update_record(self.server.records, record_id, fields)
        self.send_response(status)
        self.end_headers()


if __name__ == "__main__":
    with HTTPServer(("127.0.0.1", 8000), RecordHandler) as server:
        server.records = json.loads((BASE_DIR / "records.json").read_text(encoding="utf-8"))
        server.serve_forever()
