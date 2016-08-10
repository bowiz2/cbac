def save_schematic(f):
    def _wrapper(_self, *args, **kwargs):
        schematic = f(_self, *args, **kwargs)
        print "{}_{}.schematic".format(_self.__name__, f.__name__)
        # schematic.saveToFile()
