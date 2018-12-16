from subprocess import Popen
from test_params import DISKS_12
from unittest import TestCase
from urllib.request import Request
from urllib.request import urlopen


class Test12Server(TestCase):

    def test_(self):
        script = __file__.replace('test_12_server', 'ClueWebServer')
        try:
            server = Popen(['python', script, '--twelve', *DISKS_12])

            request = Request('http://127.0.0.1:8080/clueweb12-0013wb-88-00410')
            with urlopen(request) as response:
                result = response.read()
                assert result.startswith(b'\n\n<!DOCTYPE')
                assert result.endswith(b'</html>\n')

        finally:
            server.terminate()

    def test_base(self):
        script = __file__.replace('test_12_server', 'ClueWebServer')
        try:
            server = Popen(['python', script, '--base', '--twelve', *DISKS_12])

            request = Request('http://127.0.0.1:8080/clueweb12-0013wb-88-00410')
            with urlopen(request) as response:
                result = response.read()
                assert result.startswith(b'<base href="http://web.archive.org/web/1329035574/http://www.adrhi.com/oahu-real-estate/hawaii-kai/napali-haweo/">\n\n\n<!DOCTYPE')
                assert result.endswith(b'</html>\n')

        finally:
            server.terminate()
