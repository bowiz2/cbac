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
        self.synthesis()
        # TODO : fix hack, this makes the return command block conditional
        self.logic_cbas[0].cb_callback_reserved.conditional = True
        self.logic_cbas[0].cb_re_setter.conditional = True

    def architecture(self):
        self.event_check.is_repeated = True
        callback_command = self.callback.shell.activate()
        yield If(self.event_check).then(callback_command)


class IsActiveListener(Listener):
    """
    Listens on a bit and fires off the callback if the bit is set to "true"
    """

    def __init__(self, bit, callback):
        super(IsActiveListener, self).__init__(bit.shell == True, callback)


class IsNotActiveListener(Listener):
    """
    Listens on a bit and fires off the callback if the bit is set to "false"
    """

    def __init__(self, bit, callback):
        super(IsNotActiveListener, self).__init__(bit.shell == False, callback)
