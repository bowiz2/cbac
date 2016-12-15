import inspect
from unittest import TestCase
import os.path
import logging

from case import McTestCase


def test_dir(path):
    """
    test all the classes in the path.
    :param path:
    :return:
    """
    test_files(reduce(lambda x, y: x + y, [files for root, subdirs, files in os.walk(path)]))


def test_files(names):
    m_globals = {}
    m_locals = {}
    for filename in names:
        try:
            execfile(filename, m_globals, m_locals)

        except Exception as e:
            logging.error(str(e))
    classes = filter(lambda x: inspect.isclass(x), m_locals.values())
    print cases



test_files(["example.py"])
