#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
from ClueWeb09 import ClueWeb09
from ClueWeb12 import ClueWeb12
import gzip
import os
from pickle import dump
from pickle import load
from sys import stdin


class ClueWebCompactor(object):
    def __init__(self, arg_dict):
        self.pickle = arg_dict.pickle
        self.opener = gzip.open if arg_dict.pickle.endswith('.gz') else open
        if arg_dict.twelve:
            self.collection = ClueWeb12()
            for disk in arg_dict.disks:
                self.collection.read(disk)
        else:
            self.collection = ClueWeb09()
            for disk in arg_dict.disks:
                self.collection.read_disk(disk)

    def compact(self, document_ids):
        bodies, https, warcs = {}, {}, {}
        if os.path.exists(self.pickle):
            with self.opener(self.pickle, 'rb') as f:
                bodies, https, warcs = load(f)
        document_ids_to_collect = set()
        for document_id in document_ids:
            if (
                document_id not in bodies or
                document_id not in https or
                document_id not in warcs
            ):
                document_ids_to_collect.add(document_id)
        bodies.update(self.collection.collect(
            sorted(document_ids_to_collect),
            https,
            warcs))
        with (self.opener)(self.pickle, 'wb') as f:
            dump((bodies, https, warcs), f)


if __name__ == '__main__':
    argument_parser = ArgumentParser(
        description='Collect ClueWeb documents into a pickle'
    )
    argument_parser.add_argument('disks',
                                 help='the path to a ClueWeb disk',
                                 nargs='+',
                                 type=str)
    argument_parser.add_argument('pickle',
                                 help='the path to a target pickle',
                                 type=str)
    argument_parser.add_argument('--twelve', '-t',
                                 action='store_true',
                                 help='loads ClueWeb12 (instead of 09)')
    arg_dict = argument_parser.parse_args()
    compactor = ClueWebCompactor(arg_dict)

    document_ids = set()
    for l in stdin:
        for did in l.strip().split():
            document_ids.add(did)

    compactor.compact(document_ids)
