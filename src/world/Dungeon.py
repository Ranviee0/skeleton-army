from src.world.Room import Room
from src.constants import *
from src.recourses import *
import src.tween.tween as tween
import math

class Dungeon:
    def __init__(self, player):
        self.player = player

        self.rooms = {}

        self.current_room = Room(self.player)

        self.next_room = None

        self.camera_x = 0
        self.camera_y = 0
        self.shifting = False

    def BeginShifting(self, shift_x, shift_y):
        self.shifting = True
        self.next_room = Room(self.player)

        for doorway in self.next_room.doorways:
            doorway.open = True

        self.next_room.adjacent_offset_x = shift_x
        self.next_room.adjacent_offset_y = shift_y

        def next():
            self.FinishShifting()
            if shift_x < 0:
                self.player.ChangeCoord(x=MAP_RENDER_OFFSET_X + (MAP_WIDTH * TILE_SIZE) - TILE_SIZE - self.player.width)
                self.player.direction = 'left'
            elif shift_x > 0:
                self.player.ChangeCoord(x=MAP_RENDER_OFFSET_X+TILE_SIZE)
                self.player.direction = 'right'
            elif shift_y < 0:
                self.player.ChangeCoord(y=MAP_RENDER_OFFSET_Y + (MAP_HEIGHT * TILE_SIZE) - TILE_SIZE - self.player.height)
                self.player.direction = 'up'
            else:
                self.player.ChangeCoord(y=MAP_RENDER_OFFSET_Y + self.player.height / 2)

                # -- close all doors in the current room

            for doorway in self.current_room.doorways:
                doorway.open = False

        tween.to(self, 'camera_x', shift_x, 0.01, ease_type='linear')
        tween.to(self, 'camera_y', shift_y, 0.01, ease_type='linear').on_complete(next)

        self.player.room += 1
        print(self.player.room)


    def FinishShifting(self):
        self.camera_x = 0
        self.camera_y = 0
        self.shifting = False

        self.current_room = self.next_room
        self.next_room = None

        self.current_room.adjacent_offset_x = 0
        self.current_room.adjacent_offset_y = 0


    def update(self, dt, events):
        self.current_room.update(dt, events)

    def render(self, screen):
        self.current_room.render(screen, WIDTH/2 - self.player.x, HEIGHT/2 - self.player.y, self.shifting)