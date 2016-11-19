from unittest import TestCase
from cpu8051.handlers.handler import Handler


class TestHandler(TestCase):
    def setUp(self):

        class CpuMock(object):
            bits = 8

        class TestSubject(Handler):
            encoding = "01rr"

        self.subject = TestSubject(CpuMock())

    def test_opcodes(self):
        self.assertEquals(max(self.subject.opcodes), 7)
        self.assertEquals(min(self.subject.opcodes), 4)

    def test_get_register(self):
        self.assertEquals(self.subject.get_arg(0b0111, 'r'), 0b11)

    def test_match(self):
        self.assertTrue(self.subject.match(0b0101))
        self.assertTrue(self.subject.match(0b0111))
        self.assertFalse(self.subject.match(0b1111))
