"""Test the packer module"""
from unittest import TestCase

from blockspace import packer


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
        area = packer.DummyArea()
        area.packed_blocks = (
            (None, (1, 4, 1), None), (None, (0, 3, 5), None), (None, (8, 5, 1), None), (None, (7, 3, 27), None))
        self.assertEqual(area.dimensions, (8, 5, 27))