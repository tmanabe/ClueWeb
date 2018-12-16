from os import system
from unittest import TestCase


class TestOthers(TestCase):
    def test_flake8(self):
        assert 0 == system('flake8 . --ignore D,E501')
