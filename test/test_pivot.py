
from unittest import TestCase

import cbac.assembler
from cbac.blockspace import BlockSpace
from cbac.compound import CBA
from cbac.compound import Register
from cbac.constants.entity_id import *
from cbac.constants.mc_direction import *
from entity.entity_base import Entity
from test.decorators import save_schematic
from test.test_sul import SULTestCase, named_schematic
from cbac.entity.pivot import Pivot


class TestEntity(TestCase):
    def test_ctor(self):

        ent = Entity(ARMOR_STAND, custom_name="a", no_gravity=True)
        self.assertEqual(ent.custom_name, "a")
        self.assertEqual(ent.no_gravity, 1)

        ent = Entity(ARMOR_STAND, custom_name="b", no_gravity=False)
        self.assertEqual(ent.custom_name, "b")
        self.assertEqual(ent.no_gravity, 0)

    def test_uuid_name(self):
        """
        Check if two seperate entities without specifieng name will have a different uuid custom name.
        :return:
        """
        ent1 = Entity(ARMOR_STAND, no_gravity=True)
        ent2 = Entity(ARMOR_STAND, no_gravity=True)
        self.assertIsInstance(ent1.custom_name, str)
        self.assertIsInstance(ent2.custom_name, str)

        self.assertNotEqual(ent1.custom_name, ent2.custom_name)

    def test_parsing(self):
        entity = Entity(ARMOR_STAND, custom_name="p_pivot", no_gravity=True)
        tags = entity.parse_tags()
        self.assertEqual(tags["CustomName"], "p_pivot")
        self.assertEqual(tags["NoGravity"], True)


class TestPivot(SULTestCase):
    @named_schematic
    def test_pivot_basic(self):
        blockspace = self.block_space
        memory = Register(8)
        my_pivot = Pivot()
        blockspace.add(memory)
        blockspace.add(CBA(
            my_pivot.shell.summon(memory.blocks[0]),
            my_pivot.shell.activate(),
            my_pivot.shell.move(UP),
            my_pivot.shell.activate(),
            my_pivot.shell.move(UP),
            my_pivot.shell.activate(),
            my_pivot.shell.move(UP),
            my_pivot.shell.kill()))

    @named_schematic
    def test_pivot_temp_movement(self):
        register = Register(8)
        self.block_space.add(register)
        my_pivot = Pivot()

        self.block_space.add(CBA(
            my_pivot.shell.summon(register.blocks[0]),
            my_pivot.shell.store_to_temp(register),
            my_pivot.shell.move(UP),
            my_pivot.shell.load_from_temp(register),
            my_pivot.shell.kill()
        ))
