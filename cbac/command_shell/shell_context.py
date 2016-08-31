class ShellContext(object):
    """
    A context is the state from which the commands in the command command_shell are compiled.
    """

    def __init__(self, blockspace, executor):
        """
        :param blockspace: The blockspace the wrapped object is located at. will be bound later by the assembler.
        :param executor: the place from where the commands will be executed. will be bound later by the assembler.
        """
        self.blockspace = blockspace
        self.executor = executor

    def get_absolute_location(self, thing):
        """
        Get the absolute location of an object. In the context of the blockspace.
        """
        assert self.blockspace is not None, "To use shell context, blockspace must be assigned"
        return self.blockspace.get_location_of(thing)

    def get_relative_location(self, thing):
        """
        Get hte location of an object, in relation to the executor in the context of the blockspace.
        """
        return self.get_absolute_location(thing) - self.blockspace.get_location_of(self.executor)

    def get_absolute_area(self, thing):
        """
        Get the absolute area of an item.
        """
        assert self.blockspace is not None, "To use shell context, blockspace must be assigned"
        return self.blockspace.get_area_of(thing)

    def get_relative_area(self, thing):
        thing_area = self.get_absolute_area(thing)
        executor_area = self.get_absolute_area(self.executor)

        return tuple([thing_point - executor_point for thing_point, executor_point in zip(thing_area, executor_area)])
