from unittest import TestCase
from entity import Entity
from constants.entity_id import *
from blockspace import BlockSpace
from compound import CBA
from compound import Memory
from .decorators import save_schematic
import assembler
from constants.direction import *


class TestEntity(TestCase):

    def test_ctor(self):

        ent = Entity(ARMOR_STAND, custom_name="a", no_gravity=True)
        self.assertEqual(ent.custom_name, "a")
        self.assertEqual(ent.no_gravity, 1)

        ent = Entity(ARMOR_STAND, custom_name="b", no_gravity=False)
        self.assertEqual(ent.custom_name, "b")
        self.assertEqual(ent.no_gravity, 0)

    def test_parsing(self):
        entity = Entity(ARMOR_STAND, custom_name="p_pivot", no_gravity=True)
        tags = entity.parse_tags()
        self.assertEqual(tags["CustomName"], "p_pivot")
        self.assertEqual(tags["NoGravity"], True)

    @save_schematic
    def test_shell(self):

        entity = Entity(ARMOR_STAND, no_gravity=True)
        # The shell will throw an exception because a name is needed for the shell to work.
        try:
            _ = entity.shell
        except Exception as e:
            self.assertTrue(isinstance(e, AssertionError))

        entity.custom_name = "test_pivot"
        blockspace = BlockSpace((10, 10, 10))
        memory = Memory(8)
        blockspace.add_compound(memory)
        blockspace.add_compound(CBA(
            entity.shell.summon(memory.blocks[0]),
            entity.shell.activate(),
            entity.shell.move(UP),
            entity.shell.activate(),
            entity.shell.move(UP),
            entity.shell.activate(),
            entity.shell.move(UP),
            entity.shell.kill()))

        blockspace.pack()
        blockspace.shrink()
        schematic = assembler.build(blockspace)
        return schematic

