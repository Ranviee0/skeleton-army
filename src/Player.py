from src.EntityBase import EntityBase
from src.Dependencies import *
from src.Inventory import Inventory  
import math
import time

class Player(EntityBase):

    def __init__(self, conf):
        super(Player, self).__init__(conf)
        
        # Initialize item_type to track the currently equipped item (None by default)
        self.entityType = "player"
        self.item_type = None
        self.attack_damage = 1
        self.inventory = Inventory() 
        self.shield = 0
        self.sword0 = False
        self.sword1 = False
        self.sword2 = False
        self.sword_timers = {
            "sword0": None,
            "sword1": None,
            "sword2": None,
        }
        self.previous_position = (self.x, self.y)

    def update_sword_status(self):
        current_time = time.time()

        # Check if 30 seconds have passed for each sword
        for sword, activation_time in self.sword_timers.items():
            if activation_time and current_time - activation_time > 30:
                setattr(self, sword, False)  # Set the sword's status to False
                self.sword_timers[sword] = None  # Reset the timer

    def activate_sword(self, sword_name):
        setattr(self, sword_name, True)  # Set the sword's status to True
        self.sword_timers[sword_name] = time.time()  # Record the activation time
    
    def getRoom(self):
        print(self.room)

    def update(self, dt, events):
        super().update(dt, events)

    def Collides(self, target):
        y, height = self.y + self.height/2, self.height-self.height/2

        return not (self.x + self.width < target.x or self.x > target.x + target.width or
                    y + height < target.y or y > target.y + target.height)
    def render(self):
        super().render()

    def CreateAnimations(self):
        self.animation_list = gPlayer_animation_list

    def add_to_inventory(self, item):
        if len(self.inventory.items) < 8: 
            self.inventory.add_item(item)
        else:
            print("Inventory is full!")

    def equip_item(self, item_type):
        """Sets the item type that the player has equipped."""
        self.item_type = item_type
        print(f"Equipped item: {item_type}")  # Debugging message

    def use_item(self, item_type):
        if item_type == 'health':
            self.health = min(self.health + 1, 6)  
        elif item_type == 'other':
            self.attack_damage += 1 
        
        self.inventory.remove_item(item_type)  

    def PlayerDamage(self, dmg):
        if self.shield > 0:
            self.shield -= dmg
        else: 
            self.health -= dmg
        

    
    
 

   

        
 