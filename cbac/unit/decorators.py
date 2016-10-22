def auto_synthesis(f):
    # TODO: write tests for this
    def wrapper(u_self, *args, **kwargs):
        do_synthesise = True
        if "auto_synthesis" in kwargs.keys():
            do_synthesise = kwargs.pop("auto_synthesis")

        f(u_self, *args, **kwargs)
        if do_synthesise:
            u_self.synthesis()

    wrapper.func_defaults = f.func_defaults
    wrapper.__name__ = f.__name__
    return wrapper

# This is the vision for MHDL
