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
        if item.type == 'health':
           
            self.player.health = min(self.player.health + 2, 10)  
        elif item.type == 'other':
            gSounds['upgrade'].play()
            self.player.attack_damage += 1 
        elif item.type == 'other2':
            self.player.walk_speed += 50 
        elif item.type == 'shield_potion':
            if self.player.shield < 5:
                self.player.shield += 1  # Add shield points
                print("Shield potion collected! Shield increased.")
        elif item.type == 'sword0':
            self.player.sword0 = True

        self.inventory.remove_item(item) 


    def render(self, screen):
        #dungen render
        self.dungeon.render(screen)

        health_left = self.player.health
        shield_left = self.player.shield
        
        if self.player.sword0:
             screen.blit(gsword0[0], ((TILE_SIZE+900), 6))

            

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

