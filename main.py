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
        clock = pygame.time.Clock()
        g_state_manager.Change("start")

        paused = False  # Initialize paused state before the while loop

        while True:
            pygame.display.set_caption("{:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            # Process events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        paused = not paused  # Toggle pause state

            # Clear the screen
            self.screen.fill((0, 0, 0))  # เคลียร์หน้าจอทุกครั้ง

            # Update game state only when not paused
            if not paused:
                g_state_manager.update(dt, events)

            # Render game elements regardless of pause state
            g_state_manager.render()

            # Display "Pause" message when paused
            if paused:
                text = gFonts['zelda_smalls'].render("Paused. Press Backspace to Resume", False, (70, 53, 42))
                rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 48))
                self.screen.blit(text, rect)  # Adjust the position as needed

            # Refresh the screen with all drawn elements
            pygame.display.flip()


if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()



