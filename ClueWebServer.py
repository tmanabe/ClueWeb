#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
from ClueWeb09 import ClueWeb09
from ClueWeb12 import ClueWeb12
from dateutil import parser as date_parser
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import json
from socketserver import ThreadingMixIn
import subprocess
import sys


DEFAULT_ADDR = '127.0.0.1'
DEFAULT_PORT = 8080
HASH = None


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class ClueWebServer(BaseHTTPRequestHandler):

    @classmethod
    def run(cls, clueweb, addr=DEFAULT_ADDR, port=DEFAULT_PORT):
        cls.clueweb = clueweb
        cls.server = ThreadedHTTPServer((addr, port), cls)
        cls.server.serve_forever()

    def do_GET(self):
        if HASH is not None and self.headers.get('Authorization') != 'Basic ' + HASH:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return
        document_id = self.path.rsplit('/', 1)[1]
        if document_id in ['favicon.ico']:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'ClueWebServer: Not found')
            return
        try:
            file_path = self.clueweb.get_file(document_id)
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'ClueWebServer: Internal error')
            return
        command = sys.argv[0].replace('ClueWebServer', 'helper')
        result = subprocess.check_output(['python',
                                          command,
                                          file_path,
                                          document_id])
        result = result.decode('utf-8')
        result = json.loads(result)
        if result['body'] is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'ClueWebServer: Not found')
            return
        self.send_response(200)
        date = result['http']['Date']
        date = date_parser.parse(date).timestamp()
        url = result['warc']['WARC-Target-URI'].strip()
        href = 'http://web.archive.org/web/%i/%s' % (int(date), url)
        base = '<base href="%s">' % href
        try:
            self.send_header('Content-Type', result['http']['Content-Type'])
        except Exception:
            self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(base.encode('utf-8'))
        self.wfile.write(result['body'].encode('utf-8'))
        return


if __name__ == '__main__':
    argument_parser = ArgumentParser(
        description='Runs a HTTP server which serves ClueWeb collection'
    )
    argument_parser.add_argument('--address', '-a',
                                 default=DEFAULT_ADDR,
                                 help='the address of the server',
                                 metavar='str',
                                 type=str)
    argument_parser.add_argument('disks',
                                 help='the path to a ClueWeb disk',
                                 metavar='path',
                                 nargs='+',
                                 type=str)
    argument_parser.add_argument('--port', '-p',
                                 default=DEFAULT_PORT,
                                 help='the port of the server',
                                 metavar='int',
                                 type=int)
    argument_parser.add_argument('--twelve', '-t',
                                 action='store_true',
                                 help='loads ClueWeb12 (instead of 09)')
    arg_dict = argument_parser.parse_args()
    if arg_dict.twelve:
        c = ClueWeb12()
        for disk in arg_dict.disks:
            c.read(disk)
    else:
        c = ClueWeb09()
        for disk in arg_dict.disks:
            c.read_disk(disk)
    ClueWebServer.run(c, arg_dict.address, arg_dict.port)
