from unittest import TestCase
from cpu8051.opcode import OpcodeSet
from test_std_unit import StdUnitTestCase, named_schematic

class TestOpcodeSet(TestCase):
    def setUp(self):
        self.subject = OpcodeSet("01rr", 8)

    def test_opcodes(self):
        self.assertEquals(max(self.subject.all()), 7)
        self.assertEquals(min(self.subject.all()), 4)

    def test_get_register(self):
        self.assertEquals(self.subject.get_arg(0b0111, 'r'), 0b11)

    def test_match(self):
        self.assertTrue(self.subject.match(0b0101))
        self.assertTrue(self.subject.match(0b0111))
        self.assertFalse(self.subject.match(0b1111))