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

    def __init__(self, conditions, callbacks):
        """
        Construct the listner unit
        This unit will be active as long as the event was not reached.
        note the supplied event command will be changed.
        :param conditions: a command which tests something, and when the test is true, meaning we reached the event.
        :param callbacks: what item to activate when the even the reached.
        """
        super(Listener, self).__init__(0)
        if not isinstance(conditions, list):
            conditions = [conditions]
        self.conditions = [copy.copy(condition) for condition in conditions]
        if not isinstance(callbacks, list):
            callbacks = [callbacks]
        self.callbacks = callbacks
        self.synthesis()
        # TODO : fix hack, this makes the return command block conditional
        self.logic_cbas[0].cb_re_setter.conditional = True

    def architecture(self):
        self.conditions[0].is_repeated = True
        # TODO: fix horrible code.
        real_callbacks = []
        for callback in self.callbacks:
            if hasattr(callback, "shell"):
                real_callbacks.append(callback.shell.activate())
            else:
                real_callbacks.append(callback)
        yield If(self.conditions).then(*real_callbacks)


class IsActiveListener(Listener):
    """
    Listens on a bit and fires off the callback if the bit is set to "true"
    """

    def __init__(self, bit, callbacks):
        super(IsActiveListener, self).__init__(bit.shell == True, callbacks)


class IsNotActiveListener(Listener):
    """
    Listens on a bit and fires off the callback if the bit is set to "false"
    """

    def __init__(self, bit, callbacks):
        super(IsNotActiveListener, self).__init__(bit.shell == False, callbacks)


class ListenerReSetter(Unit):
    """
    Resets all the listeners
    """
    def __init__(self, listeners):
        """
        :param listeners: Listeners you want to reset.
        """
        super(ListenerReSetter, self).__init__(0)
        self.listeners = listeners

    def architecture(self):
        """
        resetting logic.
        """
        for listener in self.listeners:
            yield listener.shell.reset()