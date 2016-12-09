import handler
import mov
import inc
import nop
import add
import addc
import anl
import dec
from mov import *
from inc import *
from add import *
from addc import *
from anl import *
from dec import *

all_handlers = mov.all_handlers + inc.all_handlers + add.all_handlers + addc.all_handlers + anl.all_handlers + \
               dec.all_handles
