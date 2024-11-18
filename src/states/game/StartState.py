from src.states.BaseState import BaseState
import pygame, sys

from src.constants import *
from src.recourses import *

class StartState(BaseState):
    def __init__(self):
        self.bg_image = pygame.image.load("./graphics/alienbackground.jpg")
        self.bg_image = pygame.transform.scale(
            self.bg_image, (WIDTH + 5, HEIGHT + 5))

    def Enter(self, params):
        print(self.bg_image)
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_RETURN:
                    ROOM = 1
                    g_state_manager.Change('story')

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        t_title = gFonts['zelda_large'].render("Alien Z", False, (181,119,5))
        rect = t_title.get_rect(center=(WIDTH / 2 + 6, HEIGHT / 2 - 90))
        screen.blit(t_title, rect)
        t_title = gFonts['zelda_large'].render("Alien Z", False, (255,184,36))
        rect = t_title.get_rect(center=(WIDTH / 2 , HEIGHT / 2 - 96))
        screen.blit(t_title, rect)

        t_press_enter = gFonts['zelda_small'].render("Press Enter", False, (255,184,36))
        rect = t_press_enter.get_rect(center=(WIDTH / 2, HEIGHT / 2 +192))
        screen.blit(t_press_enter, rect)

    def Exit(self):
        pass

