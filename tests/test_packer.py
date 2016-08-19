"""Test the packer module"""
from unittest import TestCase

from blockspace import packer


class AreaMock(packer.Area):
    """
    Used for tests
    """
    def __init__(self, compound=None):
        self.compound = compound
        self.packed_blocks = None


class CompoundMock(object):
    def __init__(self, isolated=False):
        self.isolated = isolated


class TestPacker(TestCase):
    """
    Test the packet functionality.
    """

    def test_pack(self):
        pass

    def test_pack_areas(self):
        pass


class TestArea(TestCase):
    """
    Test the area class.
    """

    def test_init(self):
        pass

    def test_pack(self):
        pass

    def test_dimensions(self):
        pass


