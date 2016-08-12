from compound import Memory, CBA


class Unit(object):
    def __init__(self, bits=None):
        self.bits = bits
        self.compounds = []
        self.inputs = []
        self.outputs = []
        self.entry_point = None

    def generate_main_point_entry(self):
        commands = []
        for commnad_generator in [self.on_entry_init_commands(), self.main_logic_commands(), self.on_exit_commands()]:
            commands += list(commnad_generator)

        self.entry_point = self.add_compound(CBA(*commands))

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
