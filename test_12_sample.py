from ClueWeb12 import ClueWeb12
import os
from test_params import DISKS_12
from unittest import TestCase


class Test12Sample(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection = ClueWeb12()
        for disk in DISKS_12:
            if not os.path.isdir(disk):
                raise IOError('Please set proper test_params')
            cls.collection.read(disk)

    def test_collect(self):
        collection = self.collection
        ids = [
            'clueweb12-0013wb-88-00000',
            'clueweb12-0013wb-88-00410',
            'clueweb12-0013wb-88-00966',
        ]
        results = collection.collect(ids)

        file = collection['0013wb'][88]
        assert 15 == len(file.meta)
        assert b'WARC/1.0\r\n' == file.meta[None]
        assert b'283\r\n\r\n' == file.meta[b'Content-Length']
        assert file.meta[b'description'].startswith(b' The Lemur Project')
        assert file.meta[b'description'].endswith(b'\n\r\n\r\n')

        assert 3 == len(results)
        result = results['clueweb12-0013wb-88-00000']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</html>')
        result = results['clueweb12-0013wb-88-00410']
        assert result.startswith(b'\n\n<!DOCTYPE')
        assert result.endswith(b'</html>\n')
        result = results['clueweb12-0013wb-88-00966']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</HTML>\r\n')

        https, warcs = {}, {}
        results = collection.collect(ids, https, warcs)

        assert 3 == len(results)
        result = results['clueweb12-0013wb-88-00000']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</html>')
        result = results['clueweb12-0013wb-88-00410']
        assert result.startswith(b'\n\n<!DOCTYPE')
        assert result.endswith(b'</html>\n')
        result = results['clueweb12-0013wb-88-00966']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</HTML>\r\n')

        assert 3 == len(https)
        http = https['clueweb12-0013wb-88-00000']
        assert 7 == len(http)
        assert b'HTTP/1.1 200 OK\r\n' == http[None]
        assert b'bytes\r\n' == http[b'Accept-Ranges']
        assert b'text/html\r\n' == http[b'Content-Type']
        http = https['clueweb12-0013wb-88-00410']
        assert 11 == len(http)
        assert b'HTTP/1.1 200 OK\r\n' == http[None]
        assert b'48481\r\n' == http[b'Content-Length']
        assert b'close\r\n' == http[b'Connection']
        http = https['clueweb12-0013wb-88-00966']
        assert 8 == len(http)
        assert b'HTTP/1.1 200 OK\r\n' == http[None]
        assert b'ASP.NET\r\n' == http[b'X-Powered-By']
        assert b'private\r\n' == http[b'Cache-control']

        assert 3 == len(warcs)
        warc = warcs['clueweb12-0013wb-88-00000']
        assert 10 == len(warc)
        assert b'WARC/1.0\r\n' == warc[None]
        assert b'clueweb12-0013wb-88-00000\r\n' == warc[b'WARC-TREC-ID']
        assert b'44706\r\n' == warc[b'Content-Length']
        warc = warcs['clueweb12-0013wb-88-00410']
        assert 10 == len(warc)
        assert b'WARC/1.0\r\n' == warc[None]
        assert b'clueweb12-0013wb-88-00410\r\n' == warc[b'WARC-TREC-ID']
        assert b'48753\r\n' == warc[b'Content-Length']
        warc = warcs['clueweb12-0013wb-88-00966']
        assert 10 == len(warc)
        assert b'WARC/1.0\r\n' == warc[None]
        assert b'clueweb12-0013wb-88-00966\r\n' == warc[b'WARC-TREC-ID']
        assert b'11618\r\n' == warc[b'Content-Length']

    def test_get(self):
        collection = self.collection

        b, h, w = collection.get('clueweb12-0013wb-88-00000')
        assert b.startswith(b'<!DOCTYPE')
        assert b.endswith(b'</html>')
        assert 7 == len(h)
        assert b'HTTP/1.1 200 OK\r\n' == h[None]
        assert b'bytes\r\n' == h[b'Accept-Ranges']
        assert b'text/html\r\n' == h[b'Content-Type']
        assert 10 == len(w)
        assert b'WARC/1.0\r\n' == w[None]
        assert b'clueweb12-0013wb-88-00000\r\n' == w[b'WARC-TREC-ID']
        assert b'44706\r\n' == w[b'Content-Length']
        b, h, w = collection.get('clueweb12-0013wb-88-00410')
        assert b.startswith(b'\n\n<!DOCTYPE')
        assert b.endswith(b'</html>\n')
        assert 11 == len(h)
        assert b'HTTP/1.1 200 OK\r\n' == h[None]
        assert b'48481\r\n' == h[b'Content-Length']
        assert b'close\r\n' == h[b'Connection']
        assert 10 == len(w)
        assert b'WARC/1.0\r\n' == w[None]
        assert b'clueweb12-0013wb-88-00410\r\n' == w[b'WARC-TREC-ID']
        assert b'48753\r\n' == w[b'Content-Length']
        b, h, w = collection.get('clueweb12-0013wb-88-00966')
        assert b.startswith(b'<!DOCTYPE')
        assert b.endswith(b'</HTML>\r\n')
        assert 8 == len(h)
        assert b'HTTP/1.1 200 OK\r\n' == h[None]
        assert b'ASP.NET\r\n' == h[b'X-Powered-By']
        assert b'private\r\n' == h[b'Cache-control']
        assert 10 == len(w)
        assert b'WARC/1.0\r\n' == w[None]
        assert b'clueweb12-0013wb-88-00966\r\n' == w[b'WARC-TREC-ID']
        assert b'11618\r\n' == w[b'Content-Length']

    def test_iterate(self):
        def f(body, http, warc):
            results.append(body)
            https.append(http)
            warcs.append(warc)

        collection = self.collection
        file = collection['0013wb'][88]

        results, https, warcs = [], [], []
        file.iterate(f)

        assert 967 == len(results)
        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>')
        assert results[410].startswith(b'\n\n<!DOCTYPE')
        assert results[410].endswith(b'</html>\n')
        assert results[966].startswith(b'<!DOCTYPE')
        assert results[966].endswith(b'</HTML>\r\n')

        assert https[0] is None
        assert https[410] is None
        assert https[966] is None

        assert warcs[0] is None
        assert warcs[410] is None
        assert warcs[966] is None

        results, https, warcs = [], [], []
        file.iterate(f, True, True)

        assert 967 == len(results)
        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>')
        assert results[410].startswith(b'\n\n<!DOCTYPE')
        assert results[410].endswith(b'</html>\n')
        assert results[966].startswith(b'<!DOCTYPE')
        assert results[966].endswith(b'</HTML>\r\n')

        assert 967 == len(https)
        assert 7 == len(https[0])
        assert b'HTTP/1.1 200 OK\r\n' == https[0][None]
        assert b'bytes\r\n' == https[0][b'Accept-Ranges']
        assert b'text/html\r\n' == https[0][b'Content-Type']
        assert 11 == len(https[410])
        assert b'HTTP/1.1 200 OK\r\n' == https[410][None]
        assert b'48481\r\n' == https[410][b'Content-Length']
        assert b'close\r\n' == https[410][b'Connection']
        assert 8 == len(https[966])
        assert b'HTTP/1.1 200 OK\r\n' == https[966][None]
        assert b'ASP.NET\r\n' == https[966][b'X-Powered-By']
        assert b'private\r\n' == https[966][b'Cache-control']

        assert 967 == len(warcs)
        assert 10 == len(warcs[0])
        assert b'WARC/1.0\r\n' == warcs[0][None]
        assert b'clueweb12-0013wb-88-00000\r\n' == warcs[0][b'WARC-TREC-ID']
        assert b'44706\r\n' == warcs[0][b'Content-Length']
        assert 10 == len(warcs[410])
        assert b'WARC/1.0\r\n' == warcs[410][None]
        assert b'clueweb12-0013wb-88-00410\r\n' == warcs[410][b'WARC-TREC-ID']
        assert b'48753\r\n' == warcs[410][b'Content-Length']
        assert 10 == len(warcs[966])
        assert b'WARC/1.0\r\n' == warcs[966][None]
        assert b'clueweb12-0013wb-88-00966\r\n' == warcs[966][b'WARC-TREC-ID']
        assert b'11618\r\n' == warcs[966][b'Content-Length']
