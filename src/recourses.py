import pygame
from src.Util import SpriteManager, Animation
import src.Util as Util
from src.StateMachine import *

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

gHealth = [sprite_collection["health"].image]
gShieldPotion = [sprite_collection["shield_potion"].image]
gShield = [sprite_collection["shield"].image]
gsword0 = [sprite_collection["sword0"].image]
gsword1 = [sprite_collection["sword1"].image]
gsword2 = [sprite_collection["sword2"].image]

gPlayer_animation_list = {"down": sprite_collection["character_walk_down"].animation,
                         "right": sprite_collection["character_walk_right"].animation,
                         "up": sprite_collection["character_walk_up"].animation,
                         "left": sprite_collection["character_walk_left"].animation,
                        "attack_down": sprite_collection["character_attack_down"].animation,
                        "attack_right": sprite_collection["character_attack_right"].animation,
                        "attack_up": sprite_collection["character_attack_up"].animation,
                        "attack_left": sprite_collection["character_attack_left"].animation
}

gSkeleton_animation_list = {"down": sprite_collection["skeleton_walk_down"].animation,
                         "right": sprite_collection["skeleton_walk_right"].animation,
                         "up": sprite_collection["skeleton_walk_up"].animation,
                         "left": sprite_collection["skeleton_walk_left"].animation
}
gBoss_animation_list = {"boss":{"down": sprite_collection["other_walk_down"].animation,
                         "right": sprite_collection["other_walk_right"].animation,
                         "up": sprite_collection["other_walk_up"].animation,
                         "left": sprite_collection["other_walk_left"].animation},
    "boss1": {
        "down": sprite_collection["boss1_walk_down"].animation,
        "right": sprite_collection["boss1_walk_right"].animation,
        "up": sprite_collection["boss1_walk_up"].animation,
        "left": sprite_collection["boss1_walk_left"].animation
    },
    "boss2": {
        "down": sprite_collection["boss2_walk_down"].animation,
        "right": sprite_collection["boss2_walk_right"].animation,
        "up": sprite_collection["boss2_walk_up"].animation,
        "left": sprite_collection["boss2_walk_left"].animation
    },
    "boss3": {
        "down": sprite_collection["boss3_walk_down"].animation,
        "right": sprite_collection["boss3_walk_right"].animation,
        "up": sprite_collection["boss3_walk_up"].animation,
        "left": sprite_collection["boss3_walk_left"].animation
    },
    "boss4": {
        "down": sprite_collection["boss4_walk_down"].animation,
        "right": sprite_collection["boss4_walk_right"].animation,
        "up": sprite_collection["boss4_walk_up"].animation,
        "left": sprite_collection["boss4_walk_left"].animation
    }
}



gHeart_image_list = [sprite_collection["heart_0"].image,sprite_collection["heart_2"].image,
                    sprite_collection["heart_4"].image]

gRoom_image_list = Util.GenerateTiles("./graphics/tilesheet_new.png", 16, 16)
gDoor_image_list = Util.GenerateTiles("./graphics/tilesheet_new.png", 16, 16, colorkey=(13, 7, 17, 255))
gSwitch_image_list = Util.GenerateTiles("./graphics/switches.png", 16, 18)

gSounds = {
    'music': pygame.mixer.Sound('sounds/music.mp3'),
    'sword':  pygame.mixer.Sound('sounds/sword.wav'),
    'hit_enemy':  pygame.mixer.Sound('sounds/hit_enemy.wav'),
    'hit_player':  pygame.mixer.Sound('sounds/hit_player.wav'),
    'door':  pygame.mixer.Sound('sounds/door.wav')
}

gFonts = {
    'small': pygame.font.Font('fonts/font.ttf', 24),
    'medium': pygame.font.Font('fonts/font.ttf', 48),
    'large': pygame.font.Font('fonts/font.ttf', 96),
    'zelda_small': pygame.font.Font('fonts/zelda.otf', 96),
    'zelda': pygame.font.Font('fonts/zelda.otf', 192),
    'gothic_medium': pygame.font.Font('fonts/GothicPixels.ttf', 48),
    'gothic_large': pygame.font.Font('fonts/GothicPixels.ttf', 96),
    'halo': pygame.font.Font('fonts/Halo.ttf', 192),
    'dna': pygame.font.Font('fonts/dna.ttf', 52),
    
}