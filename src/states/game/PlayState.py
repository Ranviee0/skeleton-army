from src.states.BaseState import BaseState
import pygame, sys
from src.recourses import *
from src.constants import *
from src.entity_defs import *
from src.Inventory import Inventory  

from src.entity_defs import EntityConf
from src.Player import Player

from src.states.entity.player.PlayerWalkState import PlayerWalkState
from src.states.entity.player.PlayerIdleState import PlayerIdleState
from src.states.entity.player.PlayerAttackState import PlayerAttackState
from src.StateMachine import StateMachine

from src.world.Dungeon import Dungeon

class PlayState(BaseState):
    def __init__(self):
        # Inventory is always shown; no need for 'show_inventory'
        self.inventory = Inventory()  
        self.item_menu_open = False  
        self.selected_item = None  
        self.menu_position = (0, 0)  

    def Enter(self, params):
        entity_conf = ENTITY_DEFS['player']
        self.player = Player(entity_conf)
        self.dungeon = Dungeon(self.player)
        self.player.inventory = self.inventory 

        self.player.state_machine = StateMachine()
        self.player.state_machine.SetScreen(pygame.display.get_surface())
        self.player.state_machine.SetStates({
            'walk': PlayerWalkState(self.player, self.dungeon),
            'idle': PlayerIdleState(self.player),
            'swing_sword': PlayerAttackState(self.player, self.dungeon),
        })

        self.player.ChangeState('walk')

    def update(self, dt, events):
        # Handle events
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.handle_inventory_click(mouse_pos)

        self.dungeon.update(dt, events)
        keys = pygame.key.get_pressed()

        if self.player.health == 0:
            self.player.inventory.items = []
            g_state_manager.Change('game_over')

        if self.player.room == 5:
            self.player.inventory.items = []
            g_state_manager.Change('win')

        #temp
        #self.room.update(dt, events)
    def handle_inventory_click(self, mouse_pos):
        if not self.item_menu_open:
            slot_index, item = self.inventory.get_clicked_item(mouse_pos)
            if item:  
                self.selected_item = item  
                self.item_menu_open = True  
                self.menu_position = mouse_pos  
        else:
            menu_x, menu_y = self.menu_position
            if menu_x <= mouse_pos[0] <= menu_x + 100:
                if menu_y <= mouse_pos[1] <= menu_y + 30:  
                    self.use_inventory_item(self.selected_item)
                    self.item_menu_open = False
                elif menu_y + 30 <= mouse_pos[1] <= menu_y + 60:
                    self.inventory.remove_item(self.selected_item)
                    self.item_menu_open = False
            else:
                # Clicked outside the menu; close it
                self.item_menu_open = False

    def use_inventory_item(self, item):
        print(f"Attempting to use item: {item.type}")
        damage = self.player.attack_damage
        if item.type == 'health':
            print(f"Player health before: {self.player.health}")
            self.player.health = min(self.player.health + 2, 10)
            print(f"Player health after: {self.player.health}")
        elif item.type == 'shield_potion':
            print(f"Player shield before: {self.player.shield}")
            if self.player.shield < 5:
                self.player.shield += 1
                print(f"Player shield after: {self.player.shield}")
        elif item.type == 'sword0':

            self.player.sword0 = True
            self.player.sword1 = False
            self.player.sword2 = False

            print(f"Player sword0 status: {self.player.sword0}")
            print(f"Player attack damage after: {self.player.attack_damage}")
        elif item.type == 'sword1':
            self.player.sword1 = True
            self.player.sword0 = False
            self.player.sword2 = False
        elif item.type == 'sword2':
            print("Equipped Sword2: Instant Kill effect!")
            print(f"Player attack damage before: {self.player.attack_damage}")
            self.player.sword2 = True
            self.player.sword1 = False
            self.player.sword0 = False
        self.inventory.remove_item(item)
        print(f"Item {item.type} removed from inventory.")


    def render(self, screen):
        #dungen render
        self.dungeon.render(screen)

        health_left = self.player.health
        shield_left = self.player.shield
        
        if self.player.sword0:
            screen.blit(gsword0[0], ((TILE_SIZE+900), 6))

        if self.player.sword1:
            screen.blit(gsword1[0], ((TILE_SIZE+900), 6))

        if self.player.sword2:
            screen.blit(gsword2[0], ((TILE_SIZE+900), 6))

        for i in range(shield_left):
            screen.blit(gShield[0], (i * (TILE_SIZE+3), 50))
           

        for i in range(10):
            if health_left > 1:
                heart_frame = 2
            elif health_left ==1:
                heart_frame = 1
            else:
                heart_frame = 0

            screen.blit(gHeart_image_list[heart_frame], (i * (TILE_SIZE+3), 6))
            health_left -=2
        
        self.inventory.render(screen)
        if self.item_menu_open:
            self.render_item_menu(screen)

    def render_item_menu(self, screen):
        menu_x, menu_y = self.menu_position
        menu_width, menu_height = 100, 60

        pygame.draw.rect(screen, (200, 200, 200), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, (128, 128, 128), (menu_x, menu_y, menu_width, 30))
        pygame.draw.rect(screen, (128, 128, 128), (menu_x, menu_y + 30, menu_width, 30))

        font = pygame.font.Font(None, 24)
        use_text = font.render("Use", True, (0, 0, 0))
        delete_text = font.render("Delete", True, (0, 0, 0))
        screen.blit(use_text, (menu_x + 10, menu_y + 5))
        screen.blit(delete_text, (menu_x + 10, menu_y + 35))

        #temp
        #self.room.render(screen)


    def Exit(self):
        pass

