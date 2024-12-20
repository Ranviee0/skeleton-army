import pygame
from src.constants import *


class EntityBase():
    def __init__(self, conf):

        self.room = 1

        self.entityType = conf.entityType

        self.xDisplay = 0
        self.yDisplay = 0

        self.direction = 'down'
        self.animation_list = conf.animation

        # dims
        self.x = conf.x
        self.y = conf.y
        self.width = conf.width
        self.height = conf.height

        # sprite offset check
        self.offset_x = conf.offset_x or 0
        self.offset_y = conf.offset_y or 0

        self.walk_speed = conf.walk_speed

        self.health = conf.health

        #invincible
        self.invulnerable = False
        self.invulnerable_duration = 0
        self.invulnerable_timer = 0

        #timer for turning transparency (flash)
        self.flash_timer = 0

        self.is_dead = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.state_machine = None
        self.curr_animation = None

        self.previous_position = (self.x, self.y)

    def CreateAnimations(self):
        pass

    def ChangeCoord(self, x=None, y=None):
        if x is not None:
            self.x = x
            self.rect.x = self.x

        if y is not None:
            self.y=y
            self.rect.y = self.y

    def MoveX(self, x):
        self.x += x
        self.rect.x = self.x

    def MoveY(self, y):
        self.y += y
        self.rect.y = self.y

    def Collides(self, target):
        y, height = self.y + self.height/2, self.height-self.height/2

        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height < target.y or y > target.y + target.height)
    
    def undo_move(self):
        # Revert to the previous position if a collision occurred
        a = 0
        if self.entityType == 'player':
            a = 3
        else:
            a = 8
        if self.direction == 'right':
            self.x = self.x - a
        elif self.direction == 'left':
            self.x = self.x + a
        elif self.direction == 'up':
            self.y = self.y + a
        elif self.direction == 'down':
            self.y = self.y - a

    def Damage(self, dmg):
        self.health -= dmg

    def SetInvulnerable(self, duration):
        self.invulnerable = True
        self.invulnerable_duration = duration

    def ChangeState(self, name):
        self.state_machine.Change(name)

    def ChangeAnimation(self, name):
        self.curr_animation = self.animation_list[name]

    def update(self, dt, events):
        if self.invulnerable:
            self.flash_timer = self.flash_timer+dt
            self.invulnerable_timer = self.invulnerable_timer+dt

            if self.invulnerable_timer > self.invulnerable_duration:
                self.invulnerable = False
                self.invulnerable_timer = 0
                self.invulnerable_duration=0
                self.flash_timer=0

        self.state_machine.update(dt, events)

        if self.curr_animation:
            self.curr_animation.update(dt)

    def ProcessAI(self, params, bossCoords, dt):
        self.state_machine.ProcessAI(params, bossCoords, dt)

    def ProcessBossAI(self, params, playerCoords, dt):
        self.state_machine.ProcessBossAI(params, playerCoords, dt)

    def render(self):
        if self.invulnerable and self.flash_timer > 0.06:
            self.flash_timer = 0
            if self.curr_animation.idleSprite is not None:
                self.curr_animation.idleSprite.set_alpha(64)
            self.curr_animation.image.set_alpha(64)

        self.state_machine.render()
        if self.curr_animation.idleSprite is not None:
            self.curr_animation.idleSprite.set_alpha(255)
        self.curr_animation.image.set_alpha(255)

        

