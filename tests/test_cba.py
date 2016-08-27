from unittest import TestCase

from cbac import CBA


class TestCCBA(TestCase):
    def test_init(self):
        """
        Test constructor.
        """
        commands = ["/say a", "/say b", "/say c"]
        my_cba = CBA(*commands)
        self.assertEqual(len(commands), len(my_cba.commands))
        self.assertEqual(len(commands), len(my_cba.user_command_blocks))

    def test_add(self):
        """
        Test the adding of two CBAs.
        """
        my_cba_1 = CBA("/say a", "/say b", "/say c")
        my_cba_2 = CBA("/say 1", "/say 2", "/say 3")
        added_cba = my_cba_1 + my_cba_2

        print added_cba.commands
        self.assertEqual(added_cba.commands, ("/say a", "/say b", "/say c", "/say 1", "/say 2", "/say 3"))

        combined_length = len(my_cba_1.user_command_blocks) + len(my_cba_2.user_command_blocks)

        self.assertEqual(len(added_cba.user_command_blocks), combined_length)
