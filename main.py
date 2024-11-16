import pygame, math, random, sys, os
from src.constants import *

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
music_channel = pygame.mixer.Channel(0)
music_channel.set_volume(0.2)

from src.Dependencies import *
from src.recourses import *
import src.tween.tween as tween

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((1024, 768))
        self.background_image = pygame.image.load("./graphics/bg.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (1024, 768))  # Resize to fit the screen


        g_state_manager.SetScreen(self.screen)

        states = {
            'start': StartState(),
            'play': PlayState(),
            'game_over': GameOverState(),
            'win': WinState()
        }

        g_state_manager.SetStates(states)


    def PlayGame(self):
        #gSounds['music'].play(-1)
        clock = pygame.time.Clock()

        g_state_manager.Change("start")

        while True:
            pygame.display.set_caption("{:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            events = pygame.event.get()

            g_state_manager.update(dt, events)
            tween.update(dt)

            self.screen.blit(self.background_image, (0, 0))

            g_state_manager.render()
           
            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()



