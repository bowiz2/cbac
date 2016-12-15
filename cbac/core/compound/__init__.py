"""
Holds all the compounds which are derived from the Compound class, including the class itself.
Compounds are objects which consist of an array of blocks.
"""
from .compound_base import Compound
from .cb_array import CommandBlockArray
from .hardware_constant import HardwareConstant
from .register import Register

__all__ = ["Compound", "CommandBlockArray", "Register", "HardwareConstant"]
