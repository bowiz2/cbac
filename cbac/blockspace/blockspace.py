"""
Holds the blockspace Class.
"""
import packer
from cbac.utils import Vector
from cbac import utils


class BlockSpace(object):
    """
    Logical representation of blocks in the world
    """

    def __init__(self, size, packer_instance=packer):
        """
        :param size: The size of the blockspace, for packing purposes.
        :param packer_instance: an instance of an object which can pack compounds. is a dependency injection.
        """
        # Tuple which describes the size of the block space (x,y,z)
        self.size = size

        self.packer = packer_instance
        # An item can be a compound, block-box or anything else.
        self.packed_items = {}

        self.unpacked_items = []

    def add(self, *items):
        """
        Schedule an item for packing.
        :param item: Item you want to pack in this blockspace.
        :return: None
        """
        for item in items:
            if item in self.unpacked_items:
                continue
            self.unpacked_items.append(item)

    def add_unit(self, unit):
        """
        takes a unit and tries to place it in the blockspace.
        :param unit: dict of compounds and relative poistion
        """
        for compound in unit.compounds_to_pack:
            self.add(compound)

        for other_unit in unit.dependent_units:
            self.add_unit(other_unit)

    # Checkers
    def is_location_out_of_bounds(self, location):
        """
        Check if a location is not outside of the bounds of this block-space.
        """
        for location_d, size_d in zip(location, self.size):
            if location_d < 0:
                return True
            if location_d > size_d - 1:
                return True

    # Getters
    def get_area_of(self, item):
        """
        Gets the area of an item.
        """
        # Check if the item is actuall a block.
        if item in self.packed_blocks:
            # If the item provided was a block, just return its location in an area form.
            location = self.packed_blocks[item]
            return location, location

        # If the item was packed.
        if item in self.packed_items:
            # If the item was a compound, Calculate the minimal vectors.
            location, block_packings = self.packed_items[item]
            block_locations = [self.packed_blocks[block] for block, location, direction in block_packings]

        # In the case the item was constructed from an already packed item.
        elif hasattr(item, "blocks") and all(block in self.packed_blocks for block in item.blocks):
            block_locations = [self.packed_blocks[block] for block in item.blocks]
        else:
            raise Exception("Item was nor packed or constructed from a packed item.")

        return utils.min_corner(block_locations), utils.max_corner(block_locations)

    def get_location_of(self, item):
        """
        Get a location of an item which is stored in the block space.
        """
        # if item is a location, return itself.
        if isinstance(item, Vector):
            return item
        if item in self.packed_blocks.keys():
            location = self.packed_blocks[item]
        elif item in self.packed_items.keys():
            location = self.packed_items[item].location
        else:
            if hasattr(item, "blocks") and all(block in self.packed_blocks for block in item.blocks):
                location = utils.min_corner([self.packed_blocks[block] for block in item.blocks])
            else:
                raise Exception("The unit, compound or block {0} was not added to this blockspace.".format(item))

        return location

    def pack(self):
        """
        Take the unpacked compounds which are in the blockspace and pack them.
        """
        block_packings = self.packer.pack(self.unpacked_items)
        for packed_item, block_packing in block_packings.items():
            self.packed_items[packed_item] = block_packing

    @property
    def packed_blocks(self):
        """
        :return: A dict of the packed blocks in this blockspace mapped with their location.
        """
        to_return = {}
        for compound in self.packed_items.values():
            for block, location, build_direction in compound.block_assignments:
                try:
                    block.facing = build_direction
                except AttributeError:
                    pass
                to_return[block] = location
        return to_return

    def shrink(self):
        """
        Shrinks the blockspace size to the minimal, according to its blocks.
        """
        if len(self.packed_blocks) > 0:
            # TODO: remove code duplication.
            block_locations = self.packed_blocks.values()
            max_x = sorted(block_locations, key=lambda item: item[0])[-1].x
            max_y = sorted(block_locations, key=lambda item: item[1])[-1].y
            max_z = sorted(block_locations, key=lambda item: item[2])[-1].z
            self.size = (max_x + 1, max_y + 1, max_z + 1)
