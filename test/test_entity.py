from unittest import TestCase

from cbac.core.constants.entity_id import *

from cbac.core.mcentity import MCEntity


class TestEntity(TestCase):
    def test_ctor(self):
        ent = MCEntity(ARMOR_STAND, custom_name="a", no_gravity=True)
        self.assertEqual(ent.custom_name, "a")
        self.assertEqual(ent.no_gravity, 1)

        ent = MCEntity(ARMOR_STAND, custom_name="b", no_gravity=False)
        self.assertEqual(ent.custom_name, "b")
        self.assertEqual(ent.no_gravity, 0)

    def test_uuid_name(self):
        """
        Check if two seperate entities without specifieng name will have a different uuid custom name.
        :return:
        """
        ent1 = MCEntity(ARMOR_STAND, no_gravity=True)
        ent2 = MCEntity(ARMOR_STAND, no_gravity=True)
        self.assertIsInstance(ent1.custom_name, str)
        self.assertIsInstance(ent2.custom_name, str)

        self.assertNotEqual(ent1.custom_name, ent2.custom_name)

    def test_parsing(self):
        entity = MCEntity(ARMOR_STAND, custom_name="p_pivot", no_gravity=True)
        tags = entity.parse_tags()
        self.assertEqual(tags["CustomName"], "p_pivot")
        self.assertEqual(tags["NoGravity"], True)
