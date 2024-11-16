import pygame
from src.object_defs import GAME_OBJECT_DEFS  

class Inventory:
    def __init__(self, max_slots=8):
        self.items = []  
        self.max_slots = max_slots  

    def add_item(self, item):
        if len(self.items) < self.max_slots:
            self.items.append(item)
            return True
        else:
            print("Inventory is full!")
            return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def render(self, screen):
        slot_size = 48 
        padding = 10   
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        total_width = self.max_slots * slot_size + (self.max_slots - 1) * padding
        start_x = (screen_width - total_width) // 2
        start_y = screen_height - slot_size - 20  # 20 pixels from the bottom

        for i in range(self.max_slots):
            x = start_x + i * (slot_size + padding)
            y = start_y

            pygame.draw.rect(screen, (150, 150, 150), (x, y, slot_size, slot_size), 0)
            if i < len(self.items):
                item_type = self.items[i].type 
                item_image = self.get_item_image(item_type)  
                if item_image:
                    screen.blit(item_image, (x, y))

    def get_item_image(self, item_type):
        if item_type in GAME_OBJECT_DEFS:
            item_conf = GAME_OBJECT_DEFS[item_type]
            return item_conf.image[item_conf.state_list[item_conf.default_state]]
        return None

    def get_clicked_item(self, mouse_pos):
        slot_size = 48  
        padding = 10
        screen = pygame.display.get_surface()
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        total_width = self.max_slots * slot_size + (self.max_slots - 1) * padding
        start_x = (screen_width - total_width) // 2
        start_y = screen_height - slot_size - 20

        for i in range(self.max_slots):
            x = start_x + i * (slot_size + padding)
            y = start_y
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)

            if slot_rect.collidepoint(mouse_pos):
                return i, self.items[i] if i < len(self.items) else None

        return None, None  
