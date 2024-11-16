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
        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("attack_" + self.player.direction)

    def Enter(self, params):
        # Reset player offsets
        self.player.offset_x = 0
        self.player.offset_y = 0

        # Check and set the hitbox based on the equipped item state
        self.check_item_state()

        # Refresh animation
        self.player.curr_animation.Refresh()
        self.player.ChangeAnimation("attack_" + self.player.direction)

    def check_item_state(self):
        """Sets hitbox size and position based on the player's equipped item."""
        if self.player.item_type == "wide_attack":
            # Configure a large circular hitbox around the player for wide attack
            hitbox_radius = 80  # Radius for the wide area effect
            hitbox_x = self.player.x - hitbox_radius
            hitbox_y = self.player.y - hitbox_radius
            hitbox_width = hitbox_radius * 2
            hitbox_height = hitbox_radius * 2
        else:
            # Default narrow hitbox for normal attacks or one-hit attack
            hitbox_width, hitbox_height = self.get_default_hitbox_size()
            hitbox_x, hitbox_y = self.calculate_hitbox_position(hitbox_width, hitbox_height)

        # Initialize or update the sword hitbox
        self.sword_hitbox = Hitbox(hitbox_x, hitbox_y, hitbox_width, hitbox_height)

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

    def get_default_hitbox_size(self):
        """Return default hitbox dimensions for normal attacks."""
        if self.player.direction in ['left', 'right']:
            return 24, 48
        return 48, 24

    def Exit(self):
        pass

    def update(self, dt, events):
        # Apply attack effect to all entities within the hitbox
        for entity in self.dungeon.current_room.entities:
            if entity.Collides(self.sword_hitbox) and not entity.invulnerable:
                # Use item_type to determine damage effect
                damage = entity.health if self.player.item_type == "one_hit" else 1
                entity.Damage(damage)
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
        # pygame.draw.rect(screen, (255, 0, 255), pygame.Rect(self.sword_hitbox.x, self.sword_hitbox.y, self.sword_hitbox.width, self.sword_hitbox.height))