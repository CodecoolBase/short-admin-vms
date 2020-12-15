from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread


def run_file_server_thread(debug):
    server = _create_file_server(debug)
    Thread(target=lambda: server.serve_forever(), daemon=True).start()
    return server.server_address


def _create_file_server(debug):
    class FileHTTPRequestHandler(SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            if debug:
                super().log_message(format, *args)

    return HTTPServer(("", 0), partial(FileHTTPRequestHandler, directory='files'))


def main(debug):
    server = _create_file_server(debug)
    if debug:
        print(":".join(map(str, server.server_address)))
    server.serve_forever()


if __name__ == "__main__":
    main(True)
