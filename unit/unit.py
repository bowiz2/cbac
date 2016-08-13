from compound import Memory, CBA


class MainLogicJump(object):
    """
    Main logic jump is a statement used in the main logic of a unit to jump to another item.
    """
    def __init__(self, jump_destination):
        self.jump_destination= jump_destination


class Unit(object):
    def __init__(self, bits=None):
        self.bits = bits
        self.compounds = []
        self.inputs = []
        self.outputs = []
        # Logic cbas are cbac which excecute the logic of the unit. the entry point is the first logic_cba
        self.logic_cbas = []

    @property
    def entry_point(self):
        return self.logic_cbas[0]

    def generate_main_logic_cbas(self):

        class Lazy(object):
            def __init__(self, target):
                self.target = target

        class LazyCallbackSet(Lazy):
            pass

        class LazyJump(Lazy):
            pass

        temp_logic_cbas = []

        commands = []

        for commnad_generator in [self.on_entry_init_commands(), self.main_logic_commands(), self.on_exit_commands()]:
            for statement in list(commnad_generator):
                if isinstance(statement, MainLogicJump):
                    # Lazy init some stuff.
                    commands.append(LazyCallbackSet(statement.jump_destination))
                    commands.append(LazyJump(statement.jump_destination))
                    temp_logic_cbas.append(self.add_compound(CBA(*commands)))
                    commands = []
                else:
                    commands.append(statement)
        if len(commands) > 0:
            temp_logic_cbas.append(self.add_compound(CBA(*commands)))

        # Repace the lazy inits with the real thing.
        for i, cba in enumerate(temp_logic_cbas):
            for cb in cba.user_command_blocks:
                if isinstance(cb.command, Lazy):
                    lazy_target = cb.command.target
                    if isinstance(cb.command, LazyCallbackSet):
                        cb.command = lazy_target.shell.set_callback(temp_logic_cbas[i+1])
                    if isinstance(cb.command, LazyJump):
                        cb.command = lazy_target.activator.shell.activate()

        # rewire the callbacks of all the cbac to be the actaull callback block of the last block.
        for cba in temp_logic_cbas[:-1]:
            cba.cb_callback_reserved = temp_logic_cbas[-1].cb_callback_reserved

        self.logic_cbas = temp_logic_cbas

    def add_compound(self, compound):
        self.compounds.append(compound)
        return compound

    def add_input(self, memory):
        self.inputs.append(memory)
        self.add_compound(memory)
        return memory

    def add_output(self, memory):
        self.outputs.append(memory)
        self.add_compound(memory)
        return memory

    def create_input(self, bits):
        """
        Creates a memory compound, adds it to the "inputs" list and returns it.
        """
        inp = Memory(size=bits)
        return self.add_input(inp)

    def create_output(self, bits):
        """
        Creates a memory compound, adds it to the "inputs" list and returns it.
        """
        output = Memory(size=bits)
        return self.add_output(output)

    def on_entry_init_commands(self):
        """
        Generate the commands which are executed when the entry pointed activated.
        """
        for output_memory in self.outputs:
            yield output_memory.shell.reset()

    def main_logic_commands(self):
        """
        Generates the main logic of the entry point cba.
        """
        pass

    def on_exit_commands(self):
        """
        Generate the commands which will be called when the main activation of the entry point is finished.
        :return:
        """
        for input_memory in self.inputs:
            yield input_memory.shell.reset()
