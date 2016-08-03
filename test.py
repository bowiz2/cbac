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
    print const.blocks

def test_blockspace():
    from compound import Constant
    from blockspace import BlockSpace
    const = Constant(72)
    bs = BlockSpace((200, 200, 200))
    print "init ok."
    bs.add_compound(const)
    for i in xrange(50,100):
        bs.add_compound(Constant(i))
        # Some bugs found.
    print bs.blocks

test_block()
test_compound()
test_blockspace()