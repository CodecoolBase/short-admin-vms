from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import json
from .argument_parser import get_args


def run_webhook_server_thread(args):
    server = _create_webhook_server(args)
    Thread(target=lambda: server.serve_forever(), daemon=True).start()
    return server.server_address


def _create_webhook_server(cli_args):
    class WebhookHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            self.send_response(200)
            self.end_headers()
            length = int(self.headers["Content-Length"])
            bytes = self.rfile.read(length)
            text = bytes.decode("utf-8")
            if cli_args.debug:
                print(json.dumps(json.loads(text), indent=4))

        def log_message(self, format, *args):
            if cli_args.debug:
                super().log_message(format, *args)

    return HTTPServer(("", 0), WebhookHTTPRequestHandler)


def main():
    args = get_args()
    server = _create_webhook_server(args)
    if args.debug:
        print(":".join(map(str, server.server_address)))
    server.serve_forever()


if __name__ == "__main__":
    main()
