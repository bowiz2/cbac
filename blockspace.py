class AssigmentError(BaseException):
    """
    Thrown when the block space cannot assign location for a compound.
    """
    pass
class BlockSpace(object):
    def __init__(self, *compounds):

        self.compounds = list()
        self.blocks = dict()

        for compound in compounds:
            self.add_compund(compound)

    def add_compund(self, compound):
        # work in progress.

        for location in self.possible_locations_for(compound):
            try:
                for assignment in self.possible_assigments(location, compound):
                    self.compounds.append(compound)
                    for coordinate, block in assignment:
                        self.blocks[coordinate] = block
            except AssertionError:
                pass

    def find_location_for(self, compound):
        """
        Find a start location to which all of the blocks in the compound will be related to.
        :param compound: Compound to which you want to find the location.
        :return: the found location.
        """
        # TODO: implement.
        pass

    def assign_cordinates(self, location, compound):
        """
        For each block in the compound, assign a cordinate for it.
        :param location:
        :param compound:
        :return:
        """