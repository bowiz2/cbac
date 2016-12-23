"""Test the packer module"""
from unittest import TestCase

from cbac import Block, Compound
from cbac.core.blockspace import packer
from cbac.core.block import BlockID


class TestPacker(TestCase):
    """
    Test the packet functionality.
    """

    def test_compound_pack(self):
        snow_count = 4
        compound_count = 3

        # Create a few snow blocks.
        compounds = [Compound([Block(BlockID.SNOW_BLOCK) for i in xrange(snow_count)]) for j in xrange(compound_count)]
        pack_results = packer.pack(compounds)

        # Check if all the compounds are in the pack result.
        for compound in compounds:
            self.assertIn(compound, pack_results.keys(), "Compound is not in the pack results But he must be.")
            self.assertEqual(len(compound.blocks), len(pack_results[compound].block_assignments))


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
