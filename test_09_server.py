from subprocess import Popen
from test_params import DISKS_09
from unittest import TestCase
from urllib.request import Request
from urllib.request import urlopen


class Test09Server(TestCase):

    def test_(self):
        script = __file__.replace('test_09_server', 'ClueWebServer')
        try:
            server = Popen(['python', script, *DISKS_09])

            request = Request('http://127.0.0.1:8080/clueweb09-en0039-05-00121')
            with urlopen(request) as response:
                result = response.read()
                assert result.startswith(b'<!DOCTYPE')
                assert result.endswith(b'</HTML>\n\n')

        finally:
            server.terminate()

    def test_base(self):
        script = __file__.replace('test_09_server', 'ClueWebServer')
        try:
            server = Popen(['python', script, '--base', *DISKS_09])

            request = Request('http://127.0.0.1:8080/clueweb09-en0039-05-00121')
            with urlopen(request) as response:
                result = response.read()
                assert result.startswith(b'<base href="http://web.archive.org/web/1233247077/http://www.londonfoodfilmfiesta.co.uk/Artmai%7E1/A%20Russian%27s%20View%20of%20Modern%20Art.htm">\n<!DOCTYPE')
                assert result.endswith(b'</HTML>\n\n')

        finally:
            server.terminate()
