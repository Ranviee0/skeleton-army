import random

from src.states.BaseState import BaseState
from src.constants import *

class PlayerWalkStateBase(BaseState):
    def __init__(self, entity, dungeon=None):
        self.entity = entity
        self.entity.ChangeAnimation('down')
        self.dungeon = dungeon

        #AI control
        self.move_duration = 0
        self.movement_timer = 0

        #hit wall?
        self.bumped = False

    def update(self, dt, events):
        self.bumped=False

        if self.entity.direction == "left":
            self.entity.MoveX(-self.entity.walk_speed*dt)
            if self.entity.rect.x <=TILE_SIZE:
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

    def render(self, screen):
        animation = self.entity.curr_animation.image

        screen.blit(animation, (WIDTH/2,HEIGHT/2))