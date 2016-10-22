class Assertion(object):
    def __init__(self, assert_command):
        """
        :param assert_command: This command determins if the assert was sucsessfull or not.
        """
        self.command = assert_command


def assertTrue(block):
    """
    Check whenever a block is activated.
    :param block: Block
    :return: None
    """
    return Assertion(block.shell == True)


def assertFalse(block):
    """
    Check whenever a block is deactivated.
    :param block: Block
    :return:None
    """
    return Assertion(block.shell == False)


def assertEquals(register, constant):
    """
    Checks whenever a value of a register equals a value.
    :param register: Register you are checking
    :param constant: The expected value of the register.
    :return: None
    """
    return Assertion(register.shell == constant)
