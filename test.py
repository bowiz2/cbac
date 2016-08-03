def test_block():
    import block
    cb = block.CommandBlock("/say hello", facing=block.direction.SOUTH, action=block.cb_action.CHAIN)
    redstone = block.Block(block.ids.REDSTONE_BLOCK)


def test_compound():
    from compound import Compound, Constant
    import block

    cp = Compound([block.Block(1), block.Block(1)])
    const = Constant(28)
    for bit, b in zip(const.bits, const.blocks):
        if bit:
            assert b.block_id == block.ids.TRUE_BLOCK
        else:
            assert b.block_id == block.ids.FALSE_BLOCK


def test_blockspace():
    from compound import Constant, Memory
    from blockspace import BlockSpace

    bs = BlockSpace((200, 200, 200))
    TEST_SIZE = 10
    for i in xrange(TEST_SIZE):
        bs.add_compound(Constant(i+1))
        # Some bugs found.
    assert len(bs.compounds) == TEST_SIZE

    bs = BlockSpace((200, 200, 200))

    MEMORY_SIZE = 8

    for i in xrange(TEST_SIZE):
        bs.add_compound(Memory(MEMORY_SIZE))
        # Some bugs found.
    assert len(bs.blocks) == MEMORY_SIZE * TEST_SIZE


def test_get_area():
    from compound import Constant, Memory
    from blockspace import BlockSpace
    mem = Memory(8)
    bs = BlockSpace((200, 200, 200), mem)
    area = bs.get_area_of(mem)
    assert area == ((0, 0, 0), (0, 0, 7))

test_block()
test_compound()
test_blockspace()
test_get_area()