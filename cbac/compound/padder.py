"""
Provides functionality for padding commands.
"""
from cbac.block import CommandBlock


class PadBlock(CommandBlock):
    """
    This is the blocks which is used for padding.
    """

    def __init__(self):
        # TODO: consider applying condition-creating command.
        super(PadBlock, self).__init__("/say padding", conditional=True, action="chain", always_active=True)


def check_conditional(item):
    """
    Check if command block has conditional command.
    :param item: command block
    :return: bool
    """
    if isinstance(item, CommandBlock):
        command = item.command
        try:
            if command.is_conditional:
                return True
        except AttributeError:
            pass
        try:
            if command.creates_condition:
                return True
        except AttributeError:
            pass

    return False


def segments(mask):
    """
    Separate the mask into segments.
    :param mask: iterator of bits.
    :return: generator of tuples.
    """
    buff = []
    last_bit = True
    for mask_bit in mask:
        if mask_bit == last_bit:
            buff.append(mask_bit)
        else:
            yield tuple(buff)
            buff = [mask_bit]
            last_bit = mask_bit

    yield tuple(buff)


def pad(blocks, pad_size=8):
    """
    Pad array of blocks to fit pad size accounting for conditional commands.
    :param blocks: iter of blocks you want to pad.
    :param pad_size: the pad size you need to reach.
    :return: iter of blocks
    :raises: AssertionError when any conditional segment exceeds pad size.
    """

    pad_counter = 0
    danger_zone = (0, pad_size - 1)

    block = blocks.next()
    first_block = True

    while block:
        if pad_counter % pad_size in danger_zone and check_conditional(block) and not first_block:
            yield PadBlock()
        else:
            yield block
            block = blocks.next()

        first_block = False
        pad_counter += 1
