from src.constants import *
from src.recourses import *
class EntityConf:
    def __init__(self, entityType, animation, walk_speed=60, x=None, y=None, width=48, height=48, health=1, offset_x=0, offset_y=0):

        self.entityType = entityType

        self.animation = animation
        self.walk_speed = walk_speed

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.health = health

        self.offset_x = offset_x
        self.offset_y = offset_y

gOther_animation_list = {"down": sprite_collection["other_walk_down"].animation,
                         "right": sprite_collection["other_walk_right"].animation,
                         "up": sprite_collection["other_walk_up"].animation,
                         "left": sprite_collection["other_walk_left"].animation,}

ENTITY_DEFS = {
    'player': EntityConf(entityType="player", animation=gPlayer_animation_list, walk_speed=PLAYER_WALK_SPEED,
                         x=WIDTH/2-24, y=HEIGHT/2 -33, width=48, height=66,
                         health=6, offset_x=0, offset_y=15),
    'skeleton':EntityConf(entityType="skeleton", animation=gSkeleton_animation_list, width=48, height=48, health=2, walk_speed=100),
    'boss':EntityConf(entityType="boss", animation=gOther_animation_list, width=48,height=48, health=10, walk_speed=30)
}