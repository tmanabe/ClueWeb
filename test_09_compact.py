import gzip
import os
from pickle import load
from tempfile import TemporaryDirectory
from test_params import DISKS_09
from unittest import TestCase


class Test09Compact(TestCase):

    def test_(self):
        ids = [
            'clueweb09-en0039-05-00000',
            'clueweb09-en0039-05-00121',
            'clueweb09-en0039-05-00683',
        ]
        script = __file__.replace(
            'test_09_compact',
            'ClueWebCompactor')
        disks = ' '.join(DISKS_09)
        for filename in ['pickle', 'pickle.gz']:
            with TemporaryDirectory() as dir:
                stdin = os.path.join(dir, 'stdin')
                with open(stdin, 'w') as f:
                    for id in ids:
                        f.write(id)
                        f.write('\n')
                pickle = os.path.join(dir, filename)
                assert 0 == os.system('cat %s | python %s %s %s' % (
                    stdin,
                    script,
                    disks,
                    pickle))
                with (gzip.open if pickle.endswith('.gz') else open)(
                        pickle,
                        'rb') as f:
                    bodies, https, warcs = load(f)
                assert 3 == len(bodies)
                for body in bodies:
                    assert 0 < len(body)
                assert 3 == len(https)
                for http in https.values():
                    assert 0 < len(http)
                    assert http[None].startswith(b'HTTP')
                assert 3 == len(warcs)
                for warc in warcs.values():
                    assert 0 < len(warc)
                    assert warc[None].startswith(b'WARC')

    def test_update(self):
        ids = [
            'clueweb09-en0039-05-00000',
            'clueweb09-en0039-05-00121',
            'clueweb09-en0039-05-00683',
        ]
        script = __file__.replace(
            'test_09_compact',
            'ClueWebCompactor')
        disks = ' '.join(DISKS_09)
        for filename in ['pickle', 'pickle.gz']:
            with TemporaryDirectory() as dir:
                stdin = os.path.join(dir, 'stdin')
                with open(stdin, 'w') as f:
                    for id in ids:
                        f.write(id)
                        f.write('\n')
                pickle = os.path.join(dir, filename)

                for count in [1, 2, 3]:
                    assert 0 == os.system('cat %s | head -%i | python %s %s %s' % (
                        stdin,
                        count,
                        script,
                        disks,
                        pickle))
                    with (gzip.open if pickle.endswith('.gz') else open)(
                            pickle,
                            'rb') as f:
                        bodies, https, warcs = load(f)
                    assert count == len(bodies)
                    for body in bodies:
                        assert 0 < len(body)
                    assert count == len(https)
                    for http in https.values():
                        assert 0 < len(http)
                        assert http[None].startswith(b'HTTP')
                    assert count == len(warcs)
                    for warc in warcs.values():
                        assert 0 < len(warc)
                        assert warc[None].startswith(b'WARC')
