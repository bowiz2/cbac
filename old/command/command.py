class Command(object):
    BASE = "/{command} {oprands}"

    @property
    def command_name(self):
        assert False

    @property
    def oprands(self):
        assert False

    @property
    def raw(self):
        return self.BASE.format(command=self.COMMAND_NAME, oprands="".join(list(self.oprands)))

