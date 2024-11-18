import random
import math
import pygame
from src.entity_defs import *
from src.constants import *
from src.Dependencies import *
from src.world.Doorway import Doorway
from src.EntityBase import EntityBase
from src.entity_defs import EntityConf
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState
from src.StateMachine import StateMachine
from src.GameObject import GameObject
from src.object_defs import *
from src.generating import generate_flat_maze

class Room:
    def __init__(self, player):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.tiles = []
        self.GenerateWallsAndFloors()

        self.objects = []
        self.GenerateObjects()

        self.doorways = [Doorway('right', False, self)]
        self.player = player
        self.entities = []
        self.boss_generated = False  # Track if the boss has been generated
        self.skeletons_cleared = False
        self.GenerateEntities()

        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y
        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

        # Define items with random positions for player interaction
        self.items = [
            {
                'item_type': 'wide_attack',
                'x': random.randint(TILE_SIZE, TILE_SIZE * (MAP_WIDTH - 3)),
                'y': random.randint(TILE_SIZE, TILE_SIZE * (MAP_HEIGHT - 3)),
                'radius': 8,
                'color': (255, 0, 0),
                'on_collide': lambda player: setattr(player, "item_type", "wide_attack")
            },
            {
                'item_type': 'one_hit',
                'x': random.randint(TILE_SIZE, TILE_SIZE * (MAP_WIDTH - 3)),
                'y': random.randint(TILE_SIZE, TILE_SIZE * (MAP_HEIGHT - 3)),
                'radius': 8,
                'color': (0, 0, 255),
                'on_collide': lambda player: setattr(player, "item_type", "one_hit")
            }
        ]

    def GenerateWallsAndFloors(self):
        # Define wall and floor tile generation
        for y in range(1, self.height + 1):
            self.tiles.append([])
            for x in range(1, self.width + 1):
                id = TILE_EMPTY
                if x == 1 and y == 1:
                    id = TILE_TOP_LEFT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_LEFT_CORNER
                elif x == self.width and y == 1:
                    id = TILE_TOP_RIGHT_CORNER
                elif x == self.width and y == self.height:
                    id = TILE_BOTTOM_RIGHT_CORNER
                elif x == 1:
                    id = random.choice(TILE_LEFT_WALLS)
                elif x == self.width:
                    id = random.choice(TILE_RIGHT_WALLS)
                elif y == 1:
                    id = random.choice(TILE_TOP_WALLS)
                elif y == self.height:
                    id = random.choice(TILE_BOTTOM_WALLS)
                else:
                    id = random.choice(TILE_FLOORS)
                self.tiles[y - 1].append(id)

    def get_boss_coords(self):
        for entity in self.entities:
            if entity.entityType == "boss":
                return round(entity.x), round(entity.y)
        return None
    
    def get_player_coords(self):
        return round(self.player.x), round(self.player.y)

    def remove_closest_health(self):
        closest_object = None
        min_distance = float('inf')

        # Find the closest health object
        for obj in self.objects:
            if getattr(obj, 'type', None) == 'health':
                distance = math.sqrt((obj.x - self.player.x) ** 2 + (obj.y - self.player.y) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_object = obj

        if closest_object:
            self.objects.remove(closest_object)
        else:
            print("No 'health' object found.")

    def GenerateEntities(self):
        types = ['skeleton']

        for _ in range(NUMBER_OF_MONSTER * self.player.room):
            type = random.choice(types)
            
            def generate_coordinates(self):
                x_, y_ = 0, 0  # Initialize variables

                while True:
                    x_ = random.randrange(TILE_SIZE, TILE_SIZE * (MAP_WIDTH - 3))
                    y_ = random.randrange(TILE_SIZE, TILE_SIZE * (MAP_WIDTH - 3))
                    if not self.is_in_range(x_, y_):  # Stop when x_, y_ is out of range
                        break
                return x_, y_

            x_,y_ = generate_coordinates(self)

            conf = EntityConf(
                entityType=type,
                animation=ENTITY_DEFS[type].animation,
                walk_speed=ENTITY_DEFS[type].walk_speed,
                x=x_,
                y=y_,
                width=ENTITY_DEFS[type].width,
                height=ENTITY_DEFS[type].height,
                health=ENTITY_DEFS[type].health
            )

            entity = EntityBase(conf)
            entity.state_machine = StateMachine()
            entity.state_machine.SetScreen(pygame.display.get_surface())
            entity.state_machine.SetStates({
                "walk": EntityWalkState(entity, self.player),
                "idle": EntityIdleState(entity)
            })
            entity.ChangeState("walk")
            self.entities.append(entity)

            
    def GenerateObjects(self):
        my_array = ["sword1", "sword1", "sword1", "sword2", "sword2", "sword0", "sword0", "sword0", "sword0", "sword0"]

        def generate_coordinates(self):
            x_, y_ = 0, 0  # Initialize variables

            while True:
                x_ = random.randrange(TILE_SIZE, TILE_SIZE * (MAP_WIDTH - 3))
                y_ = random.randrange(TILE_SIZE, TILE_SIZE * (MAP_WIDTH - 3))
                if not self.is_in_range(x_, y_):  # Stop when x_, y_ is out of range
                    break
            return x_, y_

        x_,y_ = generate_coordinates(self)

        for _ in range(NUMBER_OF_HEALTH):
            x_,y_ = generate_coordinates(self)
            health = GameObject(GAME_OBJECT_DEFS['health'], 
                x=x_,
                y=y_
            )
            self.objects.append(health)

        for _ in range(1):
            random_sword = random.choice(my_array)
            x_,y_ = generate_coordinates(self)
            sword = GameObject(GAME_OBJECT_DEFS[random_sword], 
                x=x_,
                y=y_
            )
            if(random.randint(1,3) > 1):
                self.objects.append(sword)

        for _ in range(NUMBER_OF_SHIELD_POTIONS):
            shield_potion = GameObject(GAME_OBJECT_DEFS['shield_potion'], 
                x=x_,
                y=y_
            )
            self.objects.append(shield_potion)

        maze_list = generate_flat_maze(MAP_WIDTH, path_width=MAZE_SPACE)

        for x_ in range(MAP_WIDTH):  # Outer loop for MAP_WIDTH
            for y_ in range(MAP_HEIGHT):  # Inner loop for MAP_HEIGHT
                if (maze_list[y_ * MAP_WIDTH + x_] == 0) and (x_>2) and (y_>2):
                    wall = GameObject(GAME_OBJECT_DEFS['solid'], 
                    x=TILE_SIZE*x_,
                    y=TILE_SIZE*y_
                    )
                    self.objects.append(wall)

    def is_in_range(self, x, y):
        for obj in self.objects:
            if obj.type == 'solid':
                x_start = obj.x
                x_end = obj.x + (TILE_SIZE)
                y_start = obj.y
                y_end = obj.y + (TILE_SIZE)

                if x_start <= x <= x_end and y_start <= y <= y_end:
                    return True
        return False

    def spawn_boss_if_all_skeletons_dead(self):
        if not self.boss_generated:
            all_skeletons_dead = all(entity.is_dead or entity.entityType == 'boss' for entity in self.entities)
            if all_skeletons_dead:
                gSounds['warning'].play()
                self.skeletons_cleared = True
                self.warning_start_time = pygame.time.get_ticks()  # Start the warning timer
                self.warning_window_open = True  # Open warning window

                xboss = random.randrange(TILE_SIZE, TILE_SIZE * (MAP_WIDTH - 3))
                yboss = random.randrange(TILE_SIZE, TILE_SIZE * (MAP_HEIGHT - 3))
                conf = EntityConf(
                    entityType='boss',
                    animation=ENTITY_DEFS['boss'].animation,
                    walk_speed=ENTITY_DEFS['boss'].walk_speed,
                    x=xboss,
                    y=yboss,
                    width=ENTITY_DEFS['boss'].width,
                    height=ENTITY_DEFS['boss'].height,
                    health=ENTITY_DEFS['boss'].health
                )
                boss = EntityBase(conf)
                boss.state_machine = StateMachine()
                boss.state_machine.SetScreen(pygame.display.get_surface())
                boss.state_machine.SetStates({
                    "walk": EntityWalkState(boss),
                    "idle": EntityIdleState(boss)
                })
                boss.ChangeState("walk")
                self.entities.append(boss)
                self.boss_generated = True

    def update_boss_tracking(self, boss, player, dt):
        """Update the boss's position to track the player smoothly."""
        # Calculate the direction to the player
        dx, dy = player.x - boss.x, player.y - boss.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        # Normalize and apply speed, adjusting with delta time (dt)
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            # Scale movement to make the boss track more gradually
            smoothing_factor = 0.5  # Reduces speed for smoother tracking
            boss.x += dx * boss.walk_speed * dt * smoothing_factor
            boss.y += dy * boss.walk_speed * dt * smoothing_factor

    def has_boss_entity(self):
        return any(entity.entityType == "boss" for entity in self.entities)
    def render_warning_overlay(self, screen):
        """Render a warning overlay on the main game screen."""
        # Calculate elapsed time since the warning started
        elapsed_time = (pygame.time.get_ticks() - self.warning_start_time) / 1000

        if elapsed_time <= 5:  # Show warning for 5 seconds
            # Create a semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # RGBA, with 180 alpha for transparency

            # Render warning message
            font = pygame.font.Font(None, 64)
            message = font.render("All Skeletons Defeated! Boss Incoming...", True, (255, 255, 0))
            message_rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            # Blit overlay and message onto the main screen
            screen.blit(overlay, (0, 0))
            screen.blit(message, message_rect)
        

    def update(self, dt, events):
        self.spawn_boss_if_all_skeletons_dead()

        # Check if all entities are defeated
        all_dead = all(entity.is_dead for entity in self.entities)
        if all_dead:
            for doorway in self.doorways:
                doorway.open = True  # Open the exit doorway
        
        self.player.update(dt, events)

        for entity in self.entities:
            if entity.health <= 0:
                gSounds['scream'].play()
                entity.is_dead = True
                self.entities.remove(entity)
            elif not entity.is_dead:
                entity.xDisplay = self.player.x
                entity.yDisplay = self.player.y

                # Process boss AI if the entity is the boss
                if entity.entityType == "boss":
                    entity.ProcessBossAI({"room": self}, self.get_player_coords(), dt)
                else:
                    # For skeletons or other entities
                    entity.ProcessAI({"room": self}, self.get_boss_coords(), dt)
                
                entity.update(dt, events)
                
                

            if not entity.is_dead and self.player.Collides(entity) and not self.player.invulnerable:
                gSounds['hit_player'].play()
                self.player.PlayerDamage(1)
                self.player.SetInvulnerable(1.5)
        
        for object in self.objects:
            if object.solid and self.player.Collides(object):
                self.player.undo_move()
            for entity in self.entities:
                if object.solid and entity.Collides(object):
                    entity.undo_move()
                    if entity.direction == 'down':
                        choices = ['up','left','right']
                        entity.direction = random.choice(choices)
                    elif entity.direction == 'up':
                        choices = ['down','left','right']
                        entity.direction = random.choice(choices)
                    elif entity.direction == 'left':
                        choices = ['down','up','right']
                        entity.direction = random.choice(choices)
                    elif entity.direction == 'right':
                        choices = ['down','up','left']
                        entity.direction = random.choice(choices)

            if self.player.Collides(object):
                if not object.type == 'solid':
                    gSounds['pick_up_item'].play()
                    self.player.add_to_inventory(object)
                    self.objects.remove(object)


        for item in self.items[:]:
            item_x, item_y = item['x'], item['y']
            if math.hypot(self.player.x - item_x, self.player.y - item_y) < item['radius'] + self.player.width / 2:
                item['on_collide'](self.player)
                self.items.remove(item)

    def render(self, screen, x_mod, y_mod, shifting):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                screen.blit(
                    gRoom_image_list[tile_id - 1],
                    (x * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod,
                     y * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod)
                )

        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x + x_mod, self.adjacent_offset_y + y_mod)

        
        for object in self.objects:
            object.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        if not shifting:
            for entity in self.entities:
                if not entity.is_dead:
                    entity.render()
            if self.player:
                self.player.render()
        if self.skeletons_cleared and self.warning_start_time:
            self.render_warning_overlay(screen)