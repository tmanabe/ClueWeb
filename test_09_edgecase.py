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
            cls.collection.read(disk)
