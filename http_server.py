import json
import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, test
from pathlib import Path


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == '/files':
            response = bytes(self._get_response(), 'utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            return

        return super().do_GET()

    def _get_response(self) -> str:
        results = []

        for item in Path(self.directory).rglob('*'):
            if item.is_file():
                if __file__ in str(item):
                    continue

                file_size = str(os.stat(item).st_size)
                relative_file_path = os.path.relpath(item, self.directory)

                if sys.platform == 'win32':
                    relative_file_path = relative_file_path.replace('\\', '/')

                results.append(dict(file=relative_file_path, size=file_size))

        return json.dumps(results)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bind', metavar='ADDRESS',
                        help='Bind to this address '
                        '(default: all interfaces)')
    parser.add_argument('-d', '--directory', default=os.getcwd(),
                        help='Serve this directory '
                        '(default: current directory)')
    parser.add_argument('-p', '--protocol', metavar='VERSION',
                        default='HTTP/1.1',
                        help='Conform to this HTTP version '
                        '(default: %(default)s)')
    parser.add_argument('port', default=8000, type=int, nargs='?',
                        help='Bind to this port '
                        '(default: %(default)s)')
    args = parser.parse_args()

    HTTPRequestHandler.protocol_version = args.protocol
    handler_class = partial(HTTPRequestHandler, directory=args.directory)

    test(HandlerClass=handler_class, port=args.port, bind=args.bind)
