class Assertion(object):
    def __init__(self, assert_command, message=None):
        """
        :param assert_command: This command determins if the assert was sucsessfull or not.
        """
        self.commands = assert_command
        self.message = message


def assertTrue(block, message=None):
    """
    Check whenever a block is activated.
    :param block: Block
    :return: None
    """
    return Assertion(block.shell == True, message)


def assertFalse(block, message=None):
    """
    Check whenever a block is deactivated.
    :param block: Block
    :return:None
    """
    return Assertion(block.shell == False, message)


def assertEquals(register, constant, message=None):
    """
    Checks whenever a value of a register equals a value.
    :param register: Register you are checking
    :param constant: The expected value of the register.
    :return: None
    """
    return Assertion(register.shell == constant, message)
