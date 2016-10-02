from command_shell import EntityShell
from utils import memoize
import uuid


class Entity(object):
    def __init__(self, mc_type, custom_name=None, rotation=None, fall_distance=None, fire=None, air=None,
                 on_ground=None, no_gravity=None, custom_name_visible=None, silent=None, glowing=None, tags=None):
        """
        :param mc_type: the minecraft type of this entity.
        :param custom_name: The custom name of this entity. Appears in player death messages and villager trading
        interfaces, as well as above the entity when your cursor is over it. May not exist, or may exist and be empty.
        If no name was specified, a uuid string will be assigned to this entity.
        :param rotation: Two floats representing rotation in degrees.
        :param fall_distance: Distance the entity has fallen. Larger values cause more damage when the entity lands.
        :param fire: Number of ticks until the fire is put out. Negative values reflect how long the entity can stand
        in fire before burning.
        :param air:How much air the entity has, in ticks. Fills to a maximum of 300 in air, giving 15 seconds submerged
        before the entity starts to drown, and a total of up to 35 seconds before the entity dies (if it has 20 health).
        Decreases while underwater. If 0 while underwater, the entity loses 1 health per second.
        :param on_ground: True if the entity is touching the ground.
        :param no_gravity: If true, the entity will not fall if in the air.
        :param custom_name_visible:if true, and this entity has a custom name, it will always appear above them,
        whether or not the cursor is pointing at it. If the entity hasn't a custom name, a default name will be shown.
        May not exist.
        :param silent: If true, this entity will not make sound. May not exist.
        :param glowing: True if the entity has a glowing outline.
        :param tags: List of custom string data.
        """
        self.mc_type = mc_type
        if not custom_name:
            custom_name = str(uuid.uuid4())
        self.custom_name = custom_name
        self.rotation = rotation
        self.fall_distance = fall_distance
        self.fire = fire
        self.air = air
        self.on_ground = on_ground
        self.no_gravity = no_gravity
        self.custom_name_visible = custom_name_visible
        self.silent = silent
        self.glowing = glowing

        if tags is None:
            tags = {}
        self.misc_tags = tags

    def parse_tags(self):
        parsed_tags = {}
        # Include isoteric tags.
        for tagname, tagvalue in self.misc_tags.items():
            parsed_tags[tagname] = tagvalue

        parsed_tags["CustomName"] = self.custom_name
        parsed_tags["Rotation"] = self.rotation
        parsed_tags["FallDistance"] = self.fall_distance
        parsed_tags["Fire"] = self.fire
        parsed_tags["Air"] = self.air
        parsed_tags["OnGround"] = 1 if self.on_ground else 0
        parsed_tags["NoGravity"] = 1 if self.no_gravity else 0
        parsed_tags["CustomNameVisible"] = self.custom_name_visible
        parsed_tags["Silent"] = self.silent

        return parsed_tags

    @property
    def selector(self):
        """
        :return: Command selector of the entity. For example "@e[name=test_entity]"
        """
        assert self.custom_name is not None
        return "@e[name={0}]".format(self.custom_name)

    @property
    @memoize
    def shell(self):
        assert self.custom_name is not None
        return EntityShell(self)


class CommandStats(object):
    """
    Information identifying scoreboard parameters to modify relative to the last command run
    """

    def __init__(self, success_count_objective=None, success_count_name=None, affected_blocks_objective=None,
                 affected_blocks_name=None, affected_entities_objective=None, affected_entities_name=None,
                 affected_items_objective=None, affected_items_name=None, query_result_objective=None,
                 query_result_name=None):
        """
        :param success_count_objective: Objective's name about the number of successes
        of the last command (will be an int)
        :param success_count_name: Fake player name about the number of successes of the last command
        :param affected_blocks_objective: Objective's name about how many blocks were
        modified in the last command (will be an int)
        :param affected_blocks_name: Fake player name about how many blocks were modified in the last command
        :param affected_entities_objective: Objective's name about how many entities were altered
         in the last command (will be an int)
        :param affected_entities_name: Fake player name about how many entities were altered in the last command
        :param affected_items_objective: Objective's name about how many items were altered
         in the last command (will be an int)
        :param affected_items_name: Fake player name about how many items were altered in the last command
        :param query_result_objective: Objective's name about the query result of the last command
        :param query_result_name: Fake player name about the query result of the last command
        """

        self.success_count_objective = success_count_objective
        self.success_count_name = success_count_name
        self.affected_blocks_objective = affected_blocks_objective
        self.affected_blocks_name = affected_blocks_name
        self.affected_entities_objective = affected_entities_objective
        self.affected_entities_name = affected_entities_name
        self.affected_items_objective = affected_items_objective
        self.affected_items_name = affected_items_name
        self.query_result_objective = query_result_objective
        self.qery_result_name = query_result_name


