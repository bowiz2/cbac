"""
Build all the units which are in the std_unit folder.
"""
import cbac
import os
import re
import sys


def camel_to_underscore(string):
    """
    Converts string in camel case into snake notation ("ExampleString" into "example_class")
    :param string: the string you want ot convert.
    :return: converted string.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def get_unit_filename(unit_class):
    """
    Get the name of the schematic file to which the unit will be saved.
    :param unit_class: Class of the unit
    :return: filename of the unit schematic.
    """
    return "{0}.{1}".format(camel_to_underscore(unit_class.__name__), "schematic")


def build_simple_unit(build_folder, unit_class, bits):
    """
    Builds a unit into a schematic file.
    :param build_folder: folder to which the unit will be saved.
    :param unit_class: class of the unit you want to build
    :param bits: the size of the io bus of the unit.
    :return: unit file path.
    """
    # Create the blockspace to which the units are added.
    blockspace = cbac.BlockSpace()

    # Add the unit to the blockspace.
    blockspace.add_unit(unit_class(bits))

    # Save the blockspace to a schematic file.
    blockspace.build(os.path.join(build_folder, get_unit_filename(unit_class)))

    # Print progress.
    print "  - {0} : {1}".format(unit_class.__name__, get_unit_filename(unit_class))


def main(build_folder, bits=4):
    """
    Iterate over all the units imported from cbac.std_unit and build them into the output folder.
    """
    print "Building units for {0} bits in folder {1}".format(bits, os.path.abspath(build_folder))
    print
    print "Start building gate arrays..."
    for unit in cbac.shortcuts.std_unit_gates:
        build_simple_unit(build_folder, unit.Array(), bits)
    print "Finished building gate arrays."
    print
    print "Start building arithmetic units..."
    for unit in cbac.shortcuts.std_unit_arithmetics:
        build_simple_unit(build_folder, unit, bits)
    print "Finished building arithmetics units."
    print
    print "Build complete! checkout the results at the folder -> {0}".format(os.path.abspath(build_folder))


def usage():
    """
    Display usage information.
    """
    print "usage: build_str_units.py <build_folder> [bits]"


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        usage()

    if len(sys.argv) > 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main(sys.argv[1])
