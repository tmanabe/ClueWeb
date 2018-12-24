#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
from ClueWeb09 import ClueWeb09
from ClueWeb12 import ClueWeb12
from dateutil import parser as date_parser
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from socketserver import ThreadingMixIn


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class ClueWebServer(BaseHTTPRequestHandler):

    @classmethod
    def run(cls, arg_dict):
        cls.arg_dict = arg_dict
        if arg_dict.twelve:
            cls.collection = ClueWeb12()
            for disk in arg_dict.disks:
                cls.collection.read(disk)
        else:
            cls.collection = ClueWeb09()
            for disk in arg_dict.disks:
                cls.collection.read_disk(disk)
        ThreadedHTTPServer((arg_dict.address, arg_dict.port), cls).serve_forever()

    def get_document(self, document_id):
        return self.collection.get(document_id)

    def do_GET(self):
        hash = self.arg_dict.password
        if hash is not None and self.headers.get('Authorization') != 'Basic ' + hash:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return

        document_id = self.path.rsplit('/', 1)[-1]
        try:
            b, h, w = self.get_document(document_id)
        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'ClueWebServer: Internal error')
            import traceback
            traceback.print_exc()
            return

        codec = self.arg_dict.codec
        if b'Content-Type' in h:
            content_type = h[b'Content-Type'].decode(*codec).strip()
        else:
            content_type = 'text/html; charset=utf-8'

        base = ''
        if self.arg_dict.base:
            if b'Date' in h:
                date = h[b'Date'].decode(*codec).rstrip()
            else:
                date = 'Thu, 10 May 2012 23:59:59 GMT'
            date = date_parser.parse(date).timestamp()
            uri = w[b'WARC-Target-URI'].rstrip().decode(*codec)
            href = 'http://web.archive.org/web/%i/%s' % (int(date), uri)
            base = '<base href="%s">\n' % href

        self.send_response(200)
        try:
            self.send_header('Content-Type', content_type)
        except UnicodeEncodeError:
            self.send_header('Content-Type', b'text/html')
        self.end_headers()
        self.wfile.write(base.encode(codec[0]))
        self.wfile.write(b)
        return


def generate_basic_parser():
    argument_parser = ArgumentParser(
        description='Runs a HTTP server which serves ClueWeb collection'
    )
    argument_parser.add_argument('--address', '-a',
                                 default='127.0.0.1',
                                 help='the address of the server',
                                 metavar='str',
                                 type=str)
    argument_parser.add_argument('--base', '-b',
                                 action='store_true',
                                 help='injects a base element')
    argument_parser.add_argument('--codec', '-c',
                                 help='codec of the response',
                                 default=['utf-8', 'replace'],
                                 metavar='str',
                                 nargs='+',
                                 type=str)
    argument_parser.add_argument('--password', '-P',
                                 default=None,
                                 help='basic password hash',
                                 metavar='str',
                                 type=str)
    argument_parser.add_argument('--port', '-p',
                                 default=8080,
                                 help='the port of the server',
                                 metavar='int',
                                 type=int)
    return argument_parser


if __name__ == '__main__':
    argument_parser = generate_basic_parser()
    argument_parser.add_argument('disks',
                                 help='the path to a ClueWeb disk',
                                 metavar='path',
                                 nargs='+',
                                 type=str)
    argument_parser.add_argument('--twelve', '-t',
                                 action='store_true',
                                 help='loads ClueWeb12 (instead of 09)')
    arg_dict = argument_parser.parse_args()
    ClueWebServer.run(arg_dict)
