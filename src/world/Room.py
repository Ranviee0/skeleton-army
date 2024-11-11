import random

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
import pygame


class Room:
    def __init__(self, player):
        
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.tiles = []
        self.GenerateWallsAndFloors()

        self.objects = []
        self.GenerateObjects()

        self.doorways = []
        #self.doorways.append(Doorway('top', False, self))
        #self.doorways.append(Doorway('botoom', False, self))
        #self.doorways.append(Doorway('left', False, self))
        self.doorways.append(Doorway('right', False, self))

        # for collisions
        self.player = player

        self.entities = []
        self.GenerateEntities()

        # centering the dungeon rendering
        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y

        self.render_entity=True

        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0
        

    def GenerateWallsAndFloors(self):
        for y in range(1, self.height+1):
            self.tiles.append([])
            for x in range(1, self.width+1):
                id = TILE_EMPTY

                # Wall Corner
                if x == 1 and y == 1:
                    id = TILE_TOP_LEFT_CORNER
                elif x ==1 and y == self.height:
                    id = TILE_BOTTOM_LEFT_CORNER
                elif x == self.width and y == 1:
                    id = TILE_TOP_RIGHT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_RIGHT_CORNER

                #Wall, Floor
                elif x==1:
                    id = random.choice(TILE_LEFT_WALLS)
                elif x == self.width:
                    id = random.choice(TILE_RIGHT_WALLS)
                elif y == 1:
                    id = random.choice(TILE_TOP_WALLS)
                elif y == self.height:
                    id = random.choice(TILE_BOTTOM_WALLS)
                else:
                    id = random.choice(TILE_FLOORS)

                self.tiles[y-1].append(id)

    def GenerateEntities(self):
        
        types = ['skeleton']
        boss_type = 'boss'  
        boss_generated = False

        print(str(NUMBER_OF_MONSTER*self.player.room) + " monsters")

        xboss = random.randrange(TILE_SIZE, (TILE_SIZE*(MAP_WIDTH-3)))
        yboss = random.randrange(TILE_SIZE, (TILE_SIZE*(MAP_WIDTH-3)))

        for i in range(NUMBER_OF_MONSTER*self.player.room):
            
            if not boss_generated:
                type = boss_type
                boss_generated = True
            else:
                type = random.choice(types)

            conf = 0

            if type == "boss":
                conf = EntityConf(entityType = type, animation = ENTITY_DEFS[type].animation,walk_speed = ENTITY_DEFS[type].walk_speed,
                                x=xboss,
                                y=yboss,
                                width=ENTITY_DEFS[type].width, height=ENTITY_DEFS[type].height, health=ENTITY_DEFS[type].health)
            else:
                conf = EntityConf(entityType = type, animation = ENTITY_DEFS[type].animation,walk_speed = ENTITY_DEFS[type].walk_speed,
                                x=random.randrange(xboss-100,xboss+100),
                                y=random.randrange(yboss-100,yboss+100),
                                width=ENTITY_DEFS[type].width, height=ENTITY_DEFS[type].height, health=ENTITY_DEFS[type].health)

            self.entities.append(EntityBase(conf))

            self.entities[i].state_machine = StateMachine()
            self.entities[i].state_machine.SetScreen(pygame.display.get_surface())
            self.entities[i].state_machine.SetStates({
                "walk": EntityWalkState(self.entities[i]),
                "idle": EntityIdleState(self.entities[i])
            })
            self.entities[i].ChangeState("walk")
        
    def has_boss_entity(self):
        return any(entity.entityType == "boss" for entity in self.entities)
    
    def get_boss_coords(self):
        for entity in self.entities:
            if entity.entityType == "boss":
                return entity.x, entity.y
        return None

    def boss_location(self):
        return 

    def GenerateObjects(self):
        for _ in range(NUMBER_OF_HEALTH):
            health = GameObject(GAME_OBJECT_DEFS['health'], 
                x=random.randint(MAP_RENDER_OFFSET_X + TILE_SIZE, WIDTH - TILE_SIZE * 2 - 48),
                y=random.randint(MAP_RENDER_OFFSET_Y + TILE_SIZE, HEIGHT - (HEIGHT - MAP_HEIGHT * TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 48)
            )
            self.objects.append(health)

    def remove_closest_health(self):
        # Initialize variables to track the closest "heart" object
        closest_object = None
        min_distance = float('inf')

        # Iterate through objects to find the closest "heart"
        for obj in self.objects:
            if getattr(obj, 'type', None) == 'health':
                distance = math.sqrt((obj.x - self.player.x) ** 2 + (obj.y - self.player.y) ** 2)
            
             # Update if this is the closest "heart" so far
                if distance < min_distance:
                    min_distance = distance
                    closest_object = obj

    # Remove the closest object if it was found
        if closest_object:
            self.objects.remove(closest_object)
            print(f"Removed closest 'health' object at ({closest_object.x}, {closest_object.y}) with distance {min_distance:.2f}")
        else:
            print("No 'health' object found.")



    def update(self, dt, events):

        if(not self.has_boss_entity()):
            for doorway in self.doorways:
                doorway.open = True

        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return

        self.player.update(dt, events)

        for entity in self.entities:
            if entity.health <= 0:
                entity.is_dead = True
                self.entities.remove(entity)

            elif not entity.is_dead and entity.entityType == "boss":
                entity.xDisplay = self.player.x
                entity.yDisplay = self.player.y
                entity.ProcessBossAI({"room":self}, dt)
                entity.update(dt, events)
            
            elif not entity.is_dead and entity.entityType != "boss":
                entity.xDisplay = self.player.x
                entity.yDisplay = self.player.y
                entity.ProcessAI({"room":self}, self.get_boss_coords(), dt)
                entity.update(dt, events)


            if not entity.is_dead and self.player.Collides(entity) and not self.player.invulnerable:
                gSounds['hit_player'].play()
                self.player.Damage(1)
                self.player.SetInvulnerable(1.5)

        for object in self.objects:
            if object.solid and self.player.Collides(object):
                self.player.undo_move()

            if self.player.Collides(object):
                if object.type == "health":
                    self.remove_closest_health()
                    self.player.health += 2

    def render(self, screen, x_mod, y_mod, shifting):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                # need to access tile_id - 1  <-- actual list is start from 0
                screen.blit(gRoom_image_list[tile_id-1], (x * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod,
                    y * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod))


        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        for object in self.objects:
            object.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        if not shifting:
            for entity in self.entities:
                if not entity.is_dead:
                    entity.render()
            if self.player:
                self.player.render()

