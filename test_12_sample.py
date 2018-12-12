import os
from ClueWeb12 import ClueWeb12
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

        file = collection.get_file(ids[0])
        assert 15 == len(file.meta)
        assert b'WARC/1.0\r\n' == file.meta[None]
        assert b'283\r\n\r\n' == file.meta[b'Content-Length']
        assert file.meta[b'description'].startswith(b' The Lemur Project')
        assert file.meta[b'description'].endswith(b'\n\r\n\r\n')

        assert 3 == len(results)
        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>')
        assert results[1].startswith(b'\n\n<!DOCTYPE')
        assert results[1].endswith(b'</html>\n')
        assert results[2].startswith(b'<!DOCTYPE')
        assert results[2].endswith(b'</HTML>\r\n')

        https, warcs = [], []
        results = collection.collect(ids, https, warcs)

        assert 3 == len(results)
        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>')
        assert results[1].startswith(b'\n\n<!DOCTYPE')
        assert results[1].endswith(b'</html>\n')
        assert results[2].startswith(b'<!DOCTYPE')
        assert results[2].endswith(b'</HTML>\r\n')

        assert 3 == len(https)
        assert 7 == len(https[0])
        assert b'HTTP/1.1 200 OK\r\n' == https[0][None]
        assert b'bytes\r\n' == https[0][b'Accept-Ranges']
        assert b'text/html\r\n' == https[0][b'Content-Type']
        assert 11 == len(https[1])
        assert b'HTTP/1.1 200 OK\r\n' == https[1][None]
        assert b'48481\r\n' == https[1][b'Content-Length']
        assert b'close\r\n' == https[1][b'Connection']
        assert 8 == len(https[2])
        assert b'HTTP/1.1 200 OK\r\n' == https[2][None]
        assert b'ASP.NET\r\n' == https[2][b'X-Powered-By']
        assert b'private\r\n' == https[2][b'Cache-control']

        assert 3 == len(warcs)
        assert 10 == len(warcs[0])
        assert b'WARC/1.0\r\n' == warcs[0][None]
        assert b'clueweb12-0013wb-88-00000\r\n' == warcs[0][b'WARC-TREC-ID']
        assert b'44706\r\n' == warcs[0][b'Content-Length']
        assert 10 == len(warcs[1])
        assert b'WARC/1.0\r\n' == warcs[1][None]
        assert b'clueweb12-0013wb-88-00410\r\n' == warcs[1][b'WARC-TREC-ID']
        assert b'48753\r\n' == warcs[1][b'Content-Length']
        assert 10 == len(warcs[2])
        assert b'WARC/1.0\r\n' == warcs[2][None]
        assert b'clueweb12-0013wb-88-00966\r\n' == warcs[2][b'WARC-TREC-ID']
        assert b'11618\r\n' == warcs[2][b'Content-Length']

    def test_get(self):
        collection = self.collection

        results = []
        results.append(collection.get('clueweb12-0013wb-88-00000', None))
        results.append(collection.get('clueweb12-0013wb-88-00410', None))
        results.append(collection.get('clueweb12-0013wb-88-00966', None))
        results.append(collection.get('clueweb12-0013wb-88-99999', None))

        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>')
        assert results[1].startswith(b'\n\n<!DOCTYPE')
        assert results[1].endswith(b'</html>\n')
        assert results[2].startswith(b'<!DOCTYPE')
        assert results[2].endswith(b'</HTML>\r\n')
        assert results[3] is None

        results, https, warcs = [], [], []
        results.append(collection.get('clueweb12-0013wb-88-00000', None, https, warcs))
        results.append(collection.get('clueweb12-0013wb-88-00410', None, https, warcs))
        results.append(collection.get('clueweb12-0013wb-88-00966', None, https, warcs))
        results.append(collection.get('clueweb12-0013wb-88-99999', None, https, warcs))

        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>')
        assert results[1].startswith(b'\n\n<!DOCTYPE')
        assert results[1].endswith(b'</html>\n')
        assert results[2].startswith(b'<!DOCTYPE')
        assert results[2].endswith(b'</HTML>\r\n')
        assert results[3] is None

        assert 4 == len(https)
        assert 7 == len(https[0])
        assert b'HTTP/1.1 200 OK\r\n' == https[0][None]
        assert b'bytes\r\n' == https[0][b'Accept-Ranges']
        assert b'text/html\r\n' == https[0][b'Content-Type']
        assert 11 == len(https[1])
        assert b'HTTP/1.1 200 OK\r\n' == https[1][None]
        assert b'48481\r\n' == https[1][b'Content-Length']
        assert b'close\r\n' == https[1][b'Connection']
        assert 8 == len(https[2])
        assert b'HTTP/1.1 200 OK\r\n' == https[2][None]
        assert b'ASP.NET\r\n' == https[2][b'X-Powered-By']
        assert b'private\r\n' == https[2][b'Cache-control']
        assert https[3] is None

        assert 4 == len(warcs)
        assert 10 == len(warcs[0])
        assert b'WARC/1.0\r\n' == warcs[0][None]
        assert b'clueweb12-0013wb-88-00000\r\n' == warcs[0][b'WARC-TREC-ID']
        assert b'44706\r\n' == warcs[0][b'Content-Length']
        assert 10 == len(warcs[1])
        assert b'WARC/1.0\r\n' == warcs[1][None]
        assert b'clueweb12-0013wb-88-00410\r\n' == warcs[1][b'WARC-TREC-ID']
        assert b'48753\r\n' == warcs[1][b'Content-Length']
        assert 10 == len(warcs[2])
        assert b'WARC/1.0\r\n' == warcs[2][None]
        assert b'clueweb12-0013wb-88-00966\r\n' == warcs[2][b'WARC-TREC-ID']
        assert b'11618\r\n' == warcs[2][b'Content-Length']
        assert warcs[3] is None

    def test_iterate(self):
        def f(body, http, warc):
            results.append(body)
            https.append(http)
            warcs.append(warc)

        collection = self.collection
        file = collection.get_file('clueweb12-0013wb-88-00000')

        results, https, warcs = [], [], []
        file.iterate(f)

        assert 967 == len(results)
        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>')
        assert results[410].startswith(b'\n\n<!DOCTYPE')
        assert results[410].endswith(b'</html>\n')
        assert results[966].startswith(b'<!DOCTYPE')
        assert results[966].endswith(b'</HTML>\r\n')

        assert 0 == len(https[0])
        assert 0 == len(https[410])
        assert 0 == len(https[966])

        assert 0 == len(warcs[0])
        assert 0 == len(warcs[410])
        assert 0 == len(warcs[966])

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