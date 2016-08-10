import assembler
import block
from block import CommandBlock
from blockspace import BlockSpace
from command_shell import BlockShell
from command_shell import CompoundShell
from compound import CBA, Extender, Constant, Memory, SwitchFlow
from compound import Compound
from constants.block_id import TRUE_BLOCK
from unit import OrUnit, NotUnit
from unittest import TestCase



def test_assembler():
    cbs = Compound([CommandBlock("/say what")], isolated=True)
    constants = [Constant(i + 5, 8) for i in xrange(7)]
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


def test_or():
    u = OrUnit(4)
    block_space = BlockSpace((30, 10, 30), *u.compounds)
    schematic = assembler.build(block_space)
    schematic.saveToFile(r'./schematics/test.schematic')


def test_not():
    u = NotUnit(4)
    block_space = BlockSpace((30, 10, 30), *u.compounds)
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
# test_flow()
# test_or()
# test_not()
