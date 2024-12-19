from pygame import sprite, image, transform, draw
from src.settings import TILE_SIZE
from src.enemy import enemies_on_map
from math import sqrt, degrees, atan2
from src.map import Tile, map1

class Tower(sprite.Sprite):
    def __init__(self, name:str, dmg:float, image_url:str=""):
        super().__init__()
        self.name = name
        self.dmg = dmg
        self.size = TILE_SIZE
        self.center_pos = [257,153]
        self.target_enemy = None
        
        if image_url:
            self.original_image = image.load(image_url)  # Keep the original image unrotated
            self.original_image = transform.scale(self.original_image, (self.size, self.size))
            self.image = self.original_image
        else:
            self.image = None

    def update(self):
        self.find_closest_target()
        self.rotate_to_target()

    def render(self, screen):
        if self.image:
            rect = self.image.get_rect(center=self.center_pos)
            screen.blit(self.image, rect)
        else:
            draw.rect(screen, (0,255,0), (self.center_pos[0] - self.size / 2, self.center_pos[1] - self.size / 2, self.size, self.size))
        
    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()

    def set_position(self, tile:Tile):
        self.center_pos = tuple(coord + TILE_SIZE / 2 for coord in tile.pos_top_left)

    def rotate_to_target(self):
        if self.target_enemy:
            # Calculate angle to the target enemy
            dx = self.target_enemy.center_pos[0] - self.center_pos[0]
            dy = self.target_enemy.center_pos[1] - self.center_pos[1]
            self.angle = degrees(atan2(-dy, dx)) - 90 

            # Rotate the image
            self.image = transform.rotate(self.original_image, self.angle)


    def find_closest_target(self):
        enemies = enemies_on_map.sprites()
        if not enemies:
            self.target_enemy = None
            return
        if self.target_enemy == None:
            self.target_enemy = enemies[0]
        for enemy in enemies:
            if self.distance_to_enemy(enemy) < self.distance_to_enemy(self.target_enemy):
                self.target_enemy = enemy
    
    def distance_to_enemy(self, enemy) -> float:
        dx = self.center_pos[0] - enemy.center_pos[0]
        dy = self.center_pos[1] - enemy.center_pos[1]
        return sqrt(dx**2 + dy**2)

towers_on_map = sprite.Group()
tower1 = Tower("Cow", 10, 'assets\maps\Cow.png')
tower2 = Tower("Cow2", 10, 'assets\maps\Cow.png')
tower2.set_position(map1.tiles[5][6])
towers_on_map.add(tower1, tower2)