from src.EntityBase import EntityBase
from src.Dependencies import *
from src.Inventory import Inventory  
import math

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
        

    
    
 

   

        
 