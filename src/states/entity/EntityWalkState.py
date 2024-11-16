import random

from src.states.BaseState import BaseState
from src.constants import *
from src.Player import Player
from datetime import datetime
import random
import time

class EntityWalkState(BaseState):
    def __init__(self, entity, dungeon=None):
        self.entity = entity
        self.entity.ChangeAnimation('down')
        self.dungeon = dungeon

        #AI control
        self.move_duration = 0
        self.movement_timer = 0

        #hit wall?
        self.bumped = False

    def delta_xy(self, coords, x, y):
        x1, y1 = coords
        delta_x = x1 - x
        delta_y = y1 - y
        return delta_x, delta_y
    
    def return_direction(self, coords, x, y):
        x1, y1 = coords

        if x1 >= x and y1 >= y:
            return random.choice(["right", "down"])
        elif x1 < x and y1 >= y:
            return random.choice(["left", "down"])
        elif x1 < x and y1 < y:
            return random.choice(["left", "up"])
        elif x1 >= x and y1 < y:
            return random.choice(["right", "up"])

    def update(self, dt, events):
        self.bumped=False

        if self.entity.direction == "left":
            self.entity.MoveX(-self.entity.walk_speed*dt)
            if self.entity.rect.x<=TILE_SIZE:
                self.entity.ChangeCoord(x=TILE_SIZE)
                self.bumped=True
        elif self.entity.direction == "right":
            self.entity.MoveX(self.entity.walk_speed * dt)
            if self.entity.rect.x >= TILE_SIZE*MAP_WIDTH - TILE_SIZE*2 + self.entity.width:
                self.entity.ChangeCoord(x = TILE_SIZE*MAP_WIDTH - TILE_SIZE*2 + self.entity.width)
                self.bumped=True

        elif self.entity.direction == 'up':
            self.entity.MoveY(-self.entity.walk_speed * dt)
            if self.entity.rect.y <= TILE_SIZE - self.entity.height /2:
                self.entity.ChangeCoord(y= TILE_SIZE - self.entity.height /2)
                self.bumped = True

        elif self.entity.direction == 'down':
            self.entity.MoveY(self.entity.walk_speed * dt)
            bottom_edge = (MAP_HEIGHT * TILE_SIZE)
            if self.entity.rect.y + self.entity.height >= bottom_edge:
                self.entity.ChangeCoord(y=bottom_edge-self.entity.height)
                self.bumped=True

    def Enter(self, params):
        pass
    def Exit(self):
        pass

    def calculate_distance(self, coords, x2, y2):
        x1, y1 = coords
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def ProcessBossAI(self, params, playerCoords, dt):
        self.move_duration = 0.7
        #print(str(playerCoords) + " " + str(round(self.entity.x)) + " " + str(round(self.entity.y)))
        if playerCoords is None:
            pass
        else:
            if self.movement_timer > self.move_duration:
                self.movement_timer = 0
                direction = self.return_direction(playerCoords, self.entity.x, self.entity.y)
                self.entity.direction = direction
                self.entity.ChangeAnimation(direction)
            else:
                pass

        self.movement_timer = self.movement_timer+dt


    def ProcessAI(self, params, bossCoords, dt):
        directions = ['left', 'right', 'up', 'down']

        if self.move_duration == 0 or self.bumped:
            self.move_duration = random.randint(0, 5)
            self.entity.direction = random.choice(directions)
            self.entity.ChangeAnimation(self.entity.direction)

        elif self.movement_timer > self.move_duration:
            self.movement_timer = 0
            if random.randint(0, 3) == 1:
                self.entity.ChangeState('idle')
            else:
                self.move_duration = random.randint(0, 5)
                self.entity.direction = random.choice(directions)
                self.entity.ChangeAnimation(self.entity.direction)

        self.movement_timer = self.movement_timer+dt


    def render(self, screen):
        animation = self.entity.curr_animation.image

        # screen.blit(animation, (math.floor(self.entity.rect.x - self.entity.offset_x), math.floor(self.entity.rect.y - self.entity.offset_y)))
        screen.blit(animation, ((math.floor(self.entity.rect.x - self.entity.xDisplay + WIDTH/2)), math.floor((self.entity.rect.y - self.entity.yDisplay + HEIGHT/2))))