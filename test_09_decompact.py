import os
from subprocess import Popen
from tempfile import TemporaryDirectory
from test_params import DISKS_09
from unittest import TestCase
from urllib.request import Request
from urllib.request import urlopen


class Test09Decompact(TestCase):

    def test_(self):
        ids = [
            'clueweb09-en0039-05-00000',
            'clueweb09-en0039-05-00121',
            'clueweb09-en0039-05-00683',
        ]
        script = __file__.replace(
            'test_09_decompact',
            'ClueWebCompactor')
        disks = ' '.join(DISKS_09)
        with TemporaryDirectory() as dir:
            stdin = os.path.join(dir, 'stdin')
            with open(stdin, 'w') as f:
                for id in ids:
                    f.write(id)
                    f.write('\n')
            pickle = os.path.join(dir, 'pickle')
            assert 0 == os.system('cat %s | python %s %s %s' % (
                stdin,
                script,
                disks,
                pickle))

            script = __file__.replace(
                'test_09_decompact',
                'ClueWebDecompactor')
            try:
                server = Popen(['python', script, pickle])
                request = Request('http://127.0.0.1:8080/clueweb09-en0039-05-00121')
                with urlopen(request) as response:
                    result = response.read()
                    assert result.startswith(b'<!DOCTYPE')
                    assert result.endswith(b'</HTML>\n\n')

            finally:
                server.terminate()

            gzipped_pickle = pickle + '.gz'
            assert 0 == os.system('cat %s | gzip > %s' % (pickle, gzipped_pickle))
            try:
                server = Popen(['python', script, pickle])
                request = Request('http://127.0.0.1:8080/clueweb09-en0039-05-00121')
                with urlopen(request) as response:
                    result = response.read()
                    assert result.startswith(b'<!DOCTYPE')
                    assert result.endswith(b'</HTML>\n\n')

            finally:
                server.terminate()
