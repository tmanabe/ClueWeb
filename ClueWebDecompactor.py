#!/usr/bin/env python
# coding: utf-8

from ClueWebServer import ClueWebServer
from ClueWebServer import generate_basic_parser
from ClueWebServer import ThreadedHTTPServer
import gzip
from pickle import load


class ClueWebDecompactor(ClueWebServer):
    @classmethod
    def run(cls, arg_dict):
        cls.arg_dict = arg_dict
        with (gzip.open if arg_dict.pickle.endswith('.gz') else open)(
                arg_dict.pickle,
                'rb') as f:
            cls.bodies, cls.https, cls.warcs = load(f)
        ThreadedHTTPServer((arg_dict.address, arg_dict.port), cls).serve_forever()

    def get_document(self, document_id):
        return self.bodies[document_id], self.https[document_id], self.warcs[document_id]


if __name__ == '__main__':
    argument_parser = generate_basic_parser()
    argument_parser.add_argument('pickle',
                                 help='the path to a target pickle',
                                 type=str)
    arg_dict = argument_parser.parse_args()
    ClueWebDecompactor.run(arg_dict)
