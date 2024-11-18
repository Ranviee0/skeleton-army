from src.states.BaseState import BaseState
import pygame, sys
from src.recourses import *
from src.constants import *

class StoryState(BaseState):
    def __init__(self):
        pass

    def Exit(self):
        pass
    def Enter(self, params):
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
                    g_state_manager.Change('play')


    def render(self, screen):
        # Render the title
        t_title = gFonts['zelda'].render("Story", False, (175, 53, 42))
        rect = t_title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 144))
        screen.blit(t_title, rect)

    # Render the paragraph
        lorem_ipsum = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
            "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
        )
        font = gFonts['zelda_small']
        color = (175, 53, 42)
        line_spacing = 5  # Space between lines
        paragraph_width = WIDTH - 80  # Padding of 40px on each side

    # Split paragraph into lines that fit the width
        words = lorem_ipsum.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] > paragraph_width:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

        # Render each line
        y_offset = HEIGHT / 2 - 48  # Start rendering slightly below the title
        for line in lines:
            text_surface = font.render(line, False, color)
            text_rect = text_surface.get_rect(center=(WIDTH / 2, y_offset))
            screen.blit(text_surface, text_rect)
            y_offset += font.size(line)[1] + line_spacing  # Move down for the next line

        # Render the "Press Enter" prompt
        t_press_enter = font.render("Press Enter", False, color)
        rect = t_press_enter.get_rect(center=(WIDTH / 2, y_offset + 40))  # Adjust y position
        screen.blit(t_press_enter, rect)

