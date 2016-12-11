#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
from ClueWeb09 import ClueWeb09
from ClueWeb12 import ClueWeb12
from dateutil import parser as date_parser
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer


DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 8080


class ClueWebServer(BaseHTTPRequestHandler):

    @classmethod
    def run(cls, clueweb, addr=DEFAULT_ADDR, port=DEFAULT_PORT):
        cls.clueweb = clueweb
        cls.server = HTTPServer((addr, port), cls)
        cls.server.serve_forever()

    def do_GET(self):
        document_id = self.path.rsplit('/', 1)[1]
        if document_id in ['favicon.ico']:
            return
        http, warc = [], []
        try:
            body = self.clueweb.get(document_id, None, http, warc)
        except Exception:
            self.send_response(500)
            self.wfile.write(b'ClueWebServer: Internal error')
            return
        if body is None:
            self.send_response(404)
            self.wfile.write(b'ClueWebServer: Not found')
            return
        else:
            self.send_response(200)
        http, warc = http[0], warc[0]
        date = http[b'Date'].decode('utf-8').strip()
        date = date_parser.parse(date).timestamp()
        url = warc[b'WARC-Target-URI']
        href = b'http://web.archive.org/web/%i/%s' % (int(date), url)
        base = b'<base href="%s">' % href
        self.send_header('Content-Type',
                         http[b'Content-Type'].decode('utf-8').strip(),
                         )
        self.end_headers()
        self.wfile.write(base)
        self.wfile.write(body)
        return


if __name__ == '__main__':
    argument_parser = ArgumentParser(
        description='Runs a HTTP server which serves ClueWeb collection'
    )
    argument_parser.add_argument('--address', '-a',
                        default=DEFAULT_ADDR,
                        help='the address of the server',
                        metavar='str',
                        type=str,
                        )
    argument_parser.add_argument('disks',
                        help='the path to a ClueWeb disk',
                        metavar='path',
                        nargs='+',
                        type=str,
                        )
    argument_parser.add_argument('--port', '-p',
                        default=DEFAULT_PORT,
                  help='the port of the server',
                        metavar='int',
                        type=int,
                        )
    argument_parser.add_argument('--twelve', '-t',
                        action='store_true',
                        help='loads ClueWeb12 (instead of ClueWeb09)',
                        )
    arg_dict = argument_parser.parse_args()
    if arg_dict.twelve:
        c = ClueWeb12()
    else:
        c = ClueWeb09()
    for disk in arg_dict.disks:
        c.read_disk(disk)
    ClueWebServer.run(c, arg_dict.address, arg_dict.port)
