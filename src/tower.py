from pygame import sprite, image, transform, draw, font
from src.settings import TILE_SIZE
from src.enemy import enemies_on_map
from math import sqrt, degrees, atan2
from src.map import Tile, map1
import os

class Tower(sprite.Sprite):
    def __init__(self, name:str, dmg:float, image_url:str=""):
        super().__init__()
        self.name = name
        self.dmg = dmg
        self.size = TILE_SIZE
        self.center_pos = [257,153]
        self.target_enemy = None
        self.level = 1        
        if image_url:
            self.original_image = image.load(image_url)  # Keep the original image unrotated
            self.original_image = transform.scale(self.original_image, (self.size, self.size))
            self.image = self.original_image
        else:
            self.image = None
        self.font = font.Font(None, 24)

    def update(self):
        self.find_closest_target()
        self.rotate_to_target()

    def render(self, screen):
        if self.image:
            rect = self.image.get_rect(center=self.center_pos)
            screen.blit(self.image, rect)
        else:
            draw.rect(screen, (0,255,0), (self.center_pos[0] - self.size / 2, self.center_pos[1] - self.size / 2, self.size, self.size))
        level_text = self.font.render(f"Lvl {self.level}", True, (255, 255, 255))
        text_rect = level_text.get_rect(center=(self.center_pos[0], self.center_pos[1] - self.size / 2 - 10))
        screen.blit(level_text, text_rect)


    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()
    
    def set_pos(self, pos):
        self.center_pos = pos

    def set_position(self, tile:Tile):
        self.center_pos = tuple(coord + TILE_SIZE / 2 for coord in tile.pos_top_left)
    def set_position_bench(self, index):
        row = index // 2
        col = index % 2
        self.center_pos = (38 + (TILE_SIZE/2) + 84*col, 198 + (TILE_SIZE/2) + 84*row)
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

    def handle_left_click(self, mouse_pos):
        rect = self.image.get_rect(center=self.center_pos)
        if rect.collidepoint(mouse_pos):
            return self


    def handle_right_click(self, mouse_pos):
        rect = self.image.get_rect(center=self.center_pos)
        if rect.collidepoint(mouse_pos):
            return self
        
    def star_up(self):
        self.level += 1


# for j in range(0, 10):
#     for i in range(0, 20):
#         tower = Tower("Cow", 10, 'assets\maps\Cow.png')
#         tower.set_position(map1.tiles[i][j])
#         towers_on_map.add(tower)