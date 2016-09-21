"""
Listens for a condition, and when this condition met. notify a cba.
"""
from cbac.unit import Unit
from cbac.unit.statements import If
import copy


class Listener(Unit):
    """
    Listens on an event and fires off a callback when the event was reached.
    """
    def __init__(self, event_check, callback):
        """
        Construct the listner unit
        This unit will be active as long as the event was not reached.
        note the supplied event command will be changed.
        :param event_check: a command which tests something, and when the test is true, meaning we reached the event.
        :param callback: what item to activate when the even the reached.
        """
        super(Listener, self).__init__(0)
        self.event_check = copy.copy(event_check)
        self.callback = callback

    def main_logic_commands(self):
        self.event_check.is_repeated = True
        callback_command = self.callback.shell.activate()
        # hack to disable the resetter ot reset the repeated command block.
        callback_command.creates_condition = True
        yield If(self.event_check).then(callback_command)


class IsActiveListener(Listener):
    """
    Listens on an object which has an "is active" bit and fires off the callback if the bit is set to "true"
    """
    def __init__(self, obj, callback):
        super(IsActiveListener, self).__init__(obj.is_active_bit.shell == True, callback)


class IsNotActiveListener(Listener):
    """
    Listens on an object which has an "is active" bit and fires off the callback if the bit is set to "false"
    """
    def __init__(self, obj, callback):
        super(IsNotActiveListener, self).__init__(obj.is_active_bit.shell == False, callback)