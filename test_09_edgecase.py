from ClueWeb09 import ClueWeb09
import os
from test_params import DISKS_09
from unittest import TestCase


class Test09EdgeCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection = ClueWeb09()
        for disk in DISKS_09:
            if not os.path.isdir(disk):
                raise IOError('Please set proper test_params')
            cls.collection.read_disk(disk)

    def test_get_warc_header_includes_blank_line(self):
        b, h, w = self.collection.get('clueweb09-en0001-06-14249')
        assert b'12756\n' == w[b'Content-Length']
        assert b.startswith(b'<!DOCTYPE')

        b, h, w = self.collection.get('clueweb09-en0001-41-14942')
        assert b'29106\n' == w[b'Content-Length']
        assert b.startswith(b'<!DOCTYPE')

        b, h, w = self.collection.get('clueweb09-en0007-91-00094')
        assert b'66008\n' == w[b'Content-Length']
        assert b.startswith(b'<!DOCTYPE')
