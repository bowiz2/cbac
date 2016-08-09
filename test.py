from compound import Memory, Compound
from block import CommandBlock
from command_shell import CompoundShell
import block
from blockspace import BlockSpace
from compound import CBA, Extender, Constant, Memory, SwitchFlow
import assembler
from command_shell import BlockShell
from constants.block_id import TRUE_BLOCK


def test_block():
    cb = block.CommandBlock("/say hello", facing=block.direction.SOUTH, action=block.cb_action.CHAIN)
    redstone = block.Block(block.ids.REDSTONE_BLOCK)


def test_compound():
    cp = Compound([block.Block(1), block.Block(1)])
    const = Constant(28)
    for bit, b in zip(const.bits, const.blocks):
        if bit:
            assert b.block_id == block.ids.TRUE_BLOCK
        else:
            assert b.block_id == block.ids.FALSE_BLOCK


def test_blockspace():
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

    mem = Memory(8)
    bs = BlockSpace((200, 200, 200), mem)
    area = bs.get_area_of(mem)
    assert area == ((0, 0, 0), (0, 0, 7))


def test_get_block_location():
    mem = Memory(8)
    bs = BlockSpace((200, 200, 200), mem)
    loc = bs.get_location_of(mem.blocks[2])
    assert loc == (0, 0, 2)


def test_commands():
    mem = Memory(8)
    cb = CommandBlock("/say what")
    cbs = Compound([cb], isolated=True)
    block_space = BlockSpace((8, 8, 8), mem, cbs)
    shl = CompoundShell(mem, block_space, cb)
    cb.command = shl.fill(block.ids.GLASS_BLOCK)

    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_assembler():
    cbs = Compound([CommandBlock("/say what")], isolated=True)
    constants = [Constant(i+5, 8) for i in xrange(7)]
    block_space = BlockSpace((8, 8, 8), cbs, *constants)
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_cba():
    cba = CBA("/say what what", "/say in the butt.", "/say look at me!", "/say this is so cool.")
    block_space = BlockSpace((8, 3, 8), cba)
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_unit():
    cba = CBA("/say what what", "/say in the butt.", "/say look at me!", "/say this is so cool.")
    cba2 = CBA("/say this is totaly a new cba", "/say really.")
    my_uniy = {cba: (0, 1, 1), cba2: (2, 3, 1)}

    block_space = BlockSpace((8, 8, 8))
    block_space.add_unit(my_uniy)
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_extender():
    cba = CBA("/say what what", "/say in the butt.", "/say look at me!", "/say this is so cool.")
    cba2 = CBA("/say this is totaly a new cba", "/say really.")
    ext = Extender(cba, cba2)

    block_space = BlockSpace((8, 8, 8), cba, cba2, ext)

    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_build_direction():
    cba = CBA("/say what what", "/say in the butt.", "/say look at me!", "/say this is so cool.")
    cba2 = CBA("/say this is totaly a new cba", "/say really.")
    ext = Extender(cba, cba2)

    block_space = BlockSpace((8, 8, 8), cba, cba2, ext)

    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_condition():
    const = Constant(3)
    cba = CBA(BlockShell(const.blocks[0]) == TRUE_BLOCK, "/say it is true.")
    block_space = BlockSpace((8, 8, 8), const, cba)
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_flow():
    def msg(something):
        return "/say {}".format(something)

    memory = Memory(8)
    # TODO: fix isolation bug.
    switch = SwitchFlow(memory, {
        Constant(0): msg("Empty :("),
        Constant(1): msg("Wow 1 is so nice."),
        Constant(2): msg("2 is so much better"),
        Constant(3): msg("3 is ruller!")
    })


    switch.isolated = True
    block_space = BlockSpace((15, 20, 15), memory, *(switch.comparables + [switch]))
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')

# test_block()
# test_compound()w
# test_blockspace()
# test_get_area()
# test_get_block_location()
# test_commands()
# test_assembler()
# test_cba()
# test_unit()
# test_extender()
test_flow()