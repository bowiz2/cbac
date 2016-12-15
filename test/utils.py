import context
import subprocess
import re

products_opened = False


def open_products():
    global products_opened
    if not products_opened:
        subprocess.Popen(r'explorer /select,"{}"'.format(context.product_dir))
        products_opened = True

def camel_to_underscore(string):
    """
    Converts string in camel case into snake notation ("ExampleString" into "example_class")
    :param string: the string you want ot convert.
    :return: converted string.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()