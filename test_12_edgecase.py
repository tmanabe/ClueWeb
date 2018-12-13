import os
from ClueWeb12 import ClueWeb12
from test_params import DISKS_12
from unittest import TestCase


class Test12EdgeCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection = ClueWeb12()
        for disk in DISKS_12:
            if not os.path.isdir(disk):
                raise IOError('Please set proper test_params')
            cls.collection.read(disk)

    def test_get_http_header_ends_with_CRCRLF(self):
        b, h, w = self.collection.get('clueweb12-0911wb-16-12565')
        assert b'no-cache\r\r\n' == h[b'Pragma']
        assert b.startswith(b'command not understood :')

        b, h, w = self.collection.get('clueweb12-1805wb-05-27151')
        assert b'text/html\r\r\n' == h[b'Content-type']
        assert b.startswith(b'<HTML>')

    def test_get_http_header_ends_without_CRLF(self):
        b, h, w = self.collection.get('clueweb12-1809wb-59-25680')
        assert b'text/html\n' == h[b'Content-Type']
        assert b'open-file-in failed to open /var/www/joey/src/dream/dream.html' == b

        b, h, w = self.collection.get('clueweb12-1809wb-61-22539')
        assert b'text/html\n' == h[b'Content-Type']
        assert b'open-file-in failed to open /var/www/rebecca/Home.html' == b
