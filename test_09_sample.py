from ClueWeb09 import ClueWeb09
import os
from test_params import DISKS_09
from unittest import TestCase


class Test09Sample(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collection = ClueWeb09()
        for disk in DISKS_09:
            if not os.path.isdir(disk):
                raise IOError('Please set proper test_params')
            cls.collection.read_disk(disk)

    def test_collect(self):
        collection = self.collection
        ids = [
            'clueweb09-en0039-05-00000',
            'clueweb09-en0039-05-00121',
            'clueweb09-en0039-05-00683',
        ]
        results = collection.collect(ids)

        file = collection['en0039'][5]
        assert 11 == len(file.meta)
        assert b'WARC/0.18\n' == file.meta[None]
        assert b'219\n\n' == file.meta[b'Content-Length']
        assert file.meta[b'conformsTo'].startswith(b'http://')
        assert file.meta[b'conformsTo'].endswith(b'0.18.html\n\n')

        assert 3 == len(results)
        result = results['clueweb09-en0039-05-00000']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</html>\n\n')
        result = results['clueweb09-en0039-05-00121']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</HTML>\n\n')
        result = results['clueweb09-en0039-05-00683']
        assert result.startswith(b'\n\t<!DOCTYPE')
        assert result.endswith(b'</html>\n\n\n')

        https, warcs = {}, {}
        results = collection.collect(ids, https, warcs)

        assert 3 == len(results)
        result = results['clueweb09-en0039-05-00000']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</html>\n\n')
        result = results['clueweb09-en0039-05-00121']
        assert result.startswith(b'<!DOCTYPE')
        assert result.endswith(b'</HTML>\n\n')
        result = results['clueweb09-en0039-05-00683']
        assert result.startswith(b'\n\t<!DOCTYPE')
        assert result.endswith(b'</html>\n\n\n')

        assert 3 == len(https)
        http = https['clueweb09-en0039-05-00000']
        assert 12 == len(http)
        assert b'HTTP/1.1 200 OK\n' == http[None]
        assert b'Mon, 26 Jan 2009 01:35:15 GMT\n' == http[b'Date']
        assert b'24005\n' == http[b'Content-Length']
        http = https['clueweb09-en0039-05-00121']
        assert 9 == len(http)
        assert b'HTTP/1.1 200 OK\n' == http[None]
        assert b'Wed, 16 Jul 2008 13:38:47 GMT\n' == http[b'Last-Modified']
        assert b'20710\n' == http[b'Content-Length']
        http = https['clueweb09-en0039-05-00683']
        assert 9 == len(http)
        assert b'HTTP/1.1 200 OK\n' == http[None]
        assert b'Thu, 22 Jan 2009 11:56:36 GMT\n' == http[b'Last-Modified']
        assert b'5931\n' == http[b'Content-Length']

        assert 3 == len(warcs)
        warc = warcs['clueweb09-en0039-05-00000']
        assert 10 == len(warc)
        assert b'WARC/0.18\n' == warc[None]
        assert b'clueweb09-en0039-05-00000\n' == warc[b'WARC-TREC-ID']
        assert b'24553\n' == warc[b'Content-Length']
        warc = warcs['clueweb09-en0039-05-00121']
        assert 10 == len(warc)
        assert b'WARC/0.18\n' == warc[None]
        assert b'clueweb09-en0039-05-00121\n' == warc[b'WARC-TREC-ID']
        assert b'21056\n' == warc[b'Content-Length']
        warc = warcs['clueweb09-en0039-05-00683']
        assert 10 == len(warc)
        assert b'WARC/0.18\n' == warc[None]
        assert b'clueweb09-en0039-05-00683\n' == warc[b'WARC-TREC-ID']
        assert b'6297\n' == warc[b'Content-Length']

    def test_get(self):
        collection = self.collection

        b, h, w = collection.get('clueweb09-en0039-05-00000')
        assert b.startswith(b'<!DOCTYPE')
        assert b.endswith(b'</html>\n\n')
        assert 12 == len(h)
        assert b'HTTP/1.1 200 OK\n' == h[None]
        assert b'Mon, 26 Jan 2009 01:35:15 GMT\n' == h[b'Date']
        assert b'24005\n' == h[b'Content-Length']
        assert 10 == len(w)
        assert b'WARC/0.18\n' == w[None]
        assert b'clueweb09-en0039-05-00000\n' == w[b'WARC-TREC-ID']
        assert b'24553\n' == w[b'Content-Length']
        b, h, w = collection.get('clueweb09-en0039-05-00121')
        assert b.startswith(b'<!DOCTYPE')
        assert b.endswith(b'</HTML>\n\n')
        assert 9 == len(h)
        assert b'HTTP/1.1 200 OK\n' == h[None]
        assert b'Wed, 16 Jul 2008 13:38:47 GMT\n' == h[b'Last-Modified']
        assert b'20710\n' == h[b'Content-Length']
        assert 10 == len(w)
        assert b'WARC/0.18\n' == w[None]
        assert b'clueweb09-en0039-05-00121\n' == w[b'WARC-TREC-ID']
        assert b'21056\n' == w[b'Content-Length']
        b, h, w = collection.get('clueweb09-en0039-05-00683')
        assert b.startswith(b'\n\t<!DOCTYPE')
        assert b.endswith(b'</html>\n\n\n')
        assert 9 == len(h)
        assert b'HTTP/1.1 200 OK\n' == h[None]
        assert b'Thu, 22 Jan 2009 11:56:36 GMT\n' == h[b'Last-Modified']
        assert b'5931\n' == h[b'Content-Length']
        assert 10 == len(w)
        assert b'WARC/0.18\n' == w[None]
        assert b'clueweb09-en0039-05-00683\n' == w[b'WARC-TREC-ID']
        assert b'6297\n' == w[b'Content-Length']

    def test_iterate(self):
        def f(body, http, warc):
            results.append(body)
            https.append(http)
            warcs.append(warc)

        collection = self.collection
        file = collection['en0039'][5]

        results, https, warcs = [], [], []
        file.iterate(f)

        assert 43060 == len(results)
        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>\n\n')
        assert results[121].startswith(b'<!DOCTYPE')
        assert results[121].endswith(b'</HTML>\n\n')
        assert results[683].startswith(b'\n\t<!DOCTYPE')
        assert results[683].endswith(b'</html>\n\n\n')

        assert https[0] is None
        assert https[410] is None
        assert https[966] is None

        assert warcs[0] is None
        assert warcs[410] is None
        assert warcs[966] is None

        results, https, warcs = [], [], []
        file.iterate(f, True, True)

        assert 43060 == len(results)
        assert results[0].startswith(b'<!DOCTYPE')
        assert results[0].endswith(b'</html>\n\n')
        assert results[121].startswith(b'<!DOCTYPE')
        assert results[121].endswith(b'</HTML>\n\n')
        assert results[683].startswith(b'\n\t<!DOCTYPE')
        assert results[683].endswith(b'</html>\n\n\n')

        assert 43060 == len(https)
        assert 12 == len(https[0])
        assert b'HTTP/1.1 200 OK\n' == https[0][None]
        assert b'Mon, 26 Jan 2009 01:35:15 GMT\n' == https[0][b'Date']
        assert b'24005\n' == https[0][b'Content-Length']
        assert 9 == len(https[121])
        assert b'HTTP/1.1 200 OK\n' == https[121][None]
        assert b'Wed, 16 Jul 2008 13:38:47 GMT\n' == https[121][b'Last-Modified']
        assert b'20710\n' == https[121][b'Content-Length']
        assert 9 == len(https[683])
        assert b'HTTP/1.1 200 OK\n' == https[683][None]
        assert b'Thu, 22 Jan 2009 11:56:36 GMT\n' == https[683][b'Last-Modified']
        assert b'5931\n' == https[683][b'Content-Length']

        assert 43060 == len(warcs)
        assert 10 == len(warcs[0])
        assert b'WARC/0.18\n' == warcs[0][None]
        assert b'clueweb09-en0039-05-00000\n' == warcs[0][b'WARC-TREC-ID']
        assert b'24553\n' == warcs[0][b'Content-Length']
        assert 10 == len(warcs[121])
        assert b'WARC/0.18\n' == warcs[121][None]
        assert b'clueweb09-en0039-05-00121\n' == warcs[121][b'WARC-TREC-ID']
        assert b'21056\n' == warcs[121][b'Content-Length']
        assert 10 == len(warcs[683])
        assert b'WARC/0.18\n' == warcs[683][None]
        assert b'clueweb09-en0039-05-00683\n' == warcs[683][b'WARC-TREC-ID']
        assert b'6297\n' == warcs[683][b'Content-Length']
