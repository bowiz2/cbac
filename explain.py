
def jump(compund):
    def _jump():
        compund.start_block.set_true()
    return _jump

def say(text):
    def _say():
        return "/say " + text
    return _say

compund1 = Compund(
    cb(say("hello")),
    cb(say("bye")),
)
compund2 = Compund(
    cb(jump(compund1))
)


#translator.
def translate(items):
    for item in items:
        for cb in item:
            cb.raw_command = cb.command()
#
# class CommandBlock():
#     def __init__(self, command):
#         self.command = command
#
#
# class BlockCompund():
#     def __init__(self, *blocks):
#         self.blocks = blocks
#
#
#
# future_compund = None
#
#
# def command():
#     global future_compund
#     location = future_compund.start
#     return "/setblock {} {} {} redstone_block".format(*location)
#
# my_compund = BlockCompund(CommandBlock(command))
# #.....
#
# future_compund = BlockCompund("redsonte")
#
# print my_compund.blocks[0].command()