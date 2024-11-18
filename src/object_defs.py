from src.recourses import *
class ObjectConf:
    def __init__(self, type, img, frame, solid, default_state, states, width, height):
        self.type = type
        self.image = img
        self.frame = frame
        self.solid = solid
        self.default_state = default_state
        self.state_list = states
        self.width = width
        self.height = height

GAME_OBJECT_DEFS = {
    'switch': ObjectConf('switch', gSwitch_image_list, 2, False, "unpressed", {'unpressed':1, 'pressed':0}, width=24, height=24),
    'health' : ObjectConf('health', gHealth, 1, False, "default", {'default' : 0}, width=48, height=48),
    'shield_potion': ObjectConf('shield_potion', gShieldPotion, 1, False, "default", {'default': 0}, width=48, height=48) ,
    'sword0': ObjectConf('sword0', gsword0, 1, False, "default", {'default': 0}, width=48, height=48)  ,# New shield potion object
    'sword1': ObjectConf('sword1', gsword1, 1, False, "default", {'default': 0}, width=48, height=48),
    'sword2': ObjectConf('sword2', gsword2, 1, False, "default", {'default': 0}, width=48, height=48),
    'solid': ObjectConf('solid', gSwitch_image_list, 2, True, "default", {'default': 0}, width=48, height=48)

}