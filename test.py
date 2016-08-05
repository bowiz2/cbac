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
    from compound import Memory
    from blockspace import BlockSpace
    mem = Memory(8)
    bs = BlockSpace((200, 200, 200), mem)
    area = bs.get_area_of(mem)
    assert area == ((0, 0, 0), (0, 0, 7))


def test_get_block_location():
    from compound import Memory
    from blockspace import BlockSpace
    mem = Memory(8)
    bs = BlockSpace((200, 200, 200), mem)
    loc = bs.get_location_of(mem.blocks[2])
    assert loc == (0, 0, 2)


def test_commands():
    from compound import Memory, Compound
    from block import CommandBlock
    from blockspace import BlockSpace
    from command_shell import CompoundShell
    import assembler
    import block

    mem = Memory(8)
    cb = CommandBlock("/say what")
    cbs = Compound([cb], isolated=True)
    block_space = BlockSpace((8, 8, 8), mem, cbs)
    shl = CompoundShell(mem, block_space, cb)
    cb.command = shl.fill(block.ids.GLASS_BLOCK)

    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_assembler():
    from blockspace import BlockSpace
    from compound import Compound, Constant
    from block import CommandBlock
    import assembler

    cbs = Compound([CommandBlock("/say what")], isolated=True)
    constants = [Constant(i+5, 8) for i in xrange(7)]
    block_space = BlockSpace((8, 8, 8), cbs, *constants)
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_cba():
    from blockspace import BlockSpace
    from compound import CBA
    import assembler

    cba = CBA("/say what what", "/say in the butt.", "/say look at me!", "/say this is so cool.")
    block_space = BlockSpace((8, 3, 8), cba)
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')

# test_block()
# test_compound()
# test_blockspace()
# test_get_area()
# test_get_block_location()
# test_commands()
# test_assembler()
test_cba()
