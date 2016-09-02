SCHEMATIC_FORMAT = "./products/{0}_{1}.schematic"


def save_schematic(f):
    def _wrapper(self, *args, **kwargs):
        schematic = f(self, *args, **kwargs)
        schematic.saveToFile(SCHEMATIC_FORMAT.format(self.__class__.__name__, f.__name__))

    _wrapper.__name__ = f.__name__
    return _wrapper


def named_schematic(f):
    def _wrapper(self, *args, **kwargs):
        self.schematic_path = SCHEMATIC_FORMAT.format(self.__class__.__name__, f.__name__.replace("test_",""))
        return f(self, *args, **kwargs)


    _wrapper.__name__ = f.__name__
    return _wrapper