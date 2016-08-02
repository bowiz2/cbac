from .command import Command


class AreaCommand(Command):
    def __init__(self, target_area):
        super(AreaCommand, self).__init__()
        self.target_area = target_area

    @property
    def params(self):
        for x, y, z in self.target_area:
            yield "{} {} {}".format(x, y, z)


class Clone(AreaCommand):
    COMMAND_NAME = "clone"

    def __init__(self, target_area, dest):
        super(Clone,self).__init__(target_area)
        self.dest = dest
    
    @property
    def params(self):
        for area_param in super(Clone, self).params:
            yield area_param
        x, y, z = dest
        yield "{} {} {}".format(x, y, z)


class Fill(AreaCommand):
    COMMAND_NAME = "fill"   

    def __init__(self, target_area, materail):
        super(Clone,self).__init__(target_area)
        self.materail = materail

    @property
    def params(self):
        for area_param in super(Clone, self).params:
            yield area_param
        yield self.materail


class FillConst(Fill):
    def __init__(self, target_area):
        super(FillConst,self).__init__(target_area, self.FILL_MATERIAL)


class Activate(FillConst):
    FILL_MATERIAL = "redstone_block"


class DeActivate(FillConst):
    FILL_MATERIAL = "glass"