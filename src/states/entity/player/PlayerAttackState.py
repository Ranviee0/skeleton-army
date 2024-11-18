import math
from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.constants import *
from src.recourses import *

class PlayerAttackState(BaseState):
    def __init__(self, player, dungeon=None):
        self.player = player
        self.dungeon = dungeon
        self.sword_hitbox = Hitbox(self.player.x, self.player.y, 100, 100)
        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("attack_" + self.player.direction)

    def Enter(self, params):
        # Reset player offsets
        self.player.offset_x = 0
        self.player.offset_y = 0

        # Check and set the hitbox based on the equipped item state
        # Refresh animation
        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("attack_" + self.player.direction)

    def calculate_hitbox_position(self, width, height):
        """Calculate default hitbox position based on the player's direction."""
        direction = self.player.direction
        if direction == 'left':
            return self.player.x - width, self.player.y + 6
        elif direction == 'right':
            return self.player.x + self.player.width, self.player.y + 6
        elif direction == 'up':
            return self.player.x, self.player.y - height
        elif direction == 'down':
            return self.player.x, self.player.y + self.player.height

    def Exit(self):
        pass

    def update(self, dt, events):
        self.sword_hitbox = Hitbox(self.player.x, self.player.y, self.sword_hitbox.width, self.sword_hitbox.height)
        # Apply attack effect to all entities within the hitbox
        for entity in self.dungeon.current_room.entities:
            if entity.Collides(self.sword_hitbox) and not entity.invulnerable:
                # Initialize default damage

                if self.player.sword0:
                    # Wide attack: Deals extra damage
                    self.sword_hitbox = Hitbox(self.player.x, self.player.y, 100, 100)
                    self.player.attack_damage = 25  # Example: +10 extra damage
                    print(f"Wide attack hits {entity.entityType} for 25 damage!")
                    
                elif self.player.sword1:
                    self.sword_hitbox = Hitbox(self.player.x, self.player.y, 5000, 5000)
                    self.player.attack_damage = 5  # Moderate extra damage
                    print(f"Area slash hits {entity.entityType} for 5 damage!")
                elif self.player.sword2:
                    # Instant kill sword
                    self.sword_hitbox = Hitbox(self.player.x, self.player.y, 100, 100)
                    self.player.attack_damage = 9999  # Kill the entity outright
                    print(f"Instant kill slays {entity.entityType}!")

                # Apply damage to the entity
                entity.Damage(self.player.attack_damage)
                entity.SetInvulnerable(0.2)
                gSounds['hit_enemy'].play()

        # Reset attack animation after it's played once
        if self.player.curr_animation.times_played > 0:
            self.player.curr_animation.times_played = 0
            self.player.ChangeState("idle")

    def render(self, screen):
        # Render player's attack animation
        animation = self.player.curr_animation.image
        screen.blit(animation, (WIDTH / 2, HEIGHT / 2))

        # Debug: Render hitbox for testing
        # Uncomment the line below to visualize the hitbox
        # pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.player.x, self.player.y, self.player.x + self.sword_hitbox.width, self.player.y + self.sword_hitbox.height))