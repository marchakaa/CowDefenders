from pygame import sprite, image, transform, draw, font, Surface, SRCALPHA
from src.settings import TILE_SIZE
from src.enemy import enemies_on_map, Enemy
from math import sqrt, degrees, atan2
from src.map import Tile, map1
from src.logger import Logger
import os

logger = Logger()

class Tower(sprite.Sprite):
    def __init__(self, name:str, dmg:float, attack_speed: float, attack_range: int, image_url:str=""):
        super().__init__()
        self.name = name
        self.dmg = dmg
        self.attack_speed = attack_speed
        self.attack_cooldown = 0
        self.range = attack_range
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

    def update(self, delta_time):
        if self.attack_cooldown > 0:
            self.attack_cooldown = max(0, self.attack_cooldown - delta_time)

        self.find_closest_target()
        self.rotate_to_target()
        self.attack_enemy(delta_time)

    def render(self, screen):
        # self.render_range(screen)
        if self.image:
            rect = self.image.get_rect(center=self.center_pos)
            screen.blit(self.image, rect)
        else:
            draw.rect(screen, (0, 255, 0), (self.center_pos[0] - self.size / 2, self.center_pos[1] - self.size / 2, self.size, self.size))
        
        #Render level
        level_text = self.font.render(f"Lvl {self.level}", True, (255, 255, 255))
        text_rect = level_text.get_rect(center=(self.center_pos[0], self.center_pos[1] - self.size / 2 - 10))
        screen.blit(level_text, text_rect)

        #Render attack cooldown indicator
        if self.attack_cooldown > 0:
            cooldown_pct = self.attack_cooldown / (1 / self.attack_speed)
            draw.arc(screen, (255, 200, 0), 
                    (self.center_pos[0] - self.size/2, self.center_pos[1] - self.size/2, 
                     self.size, self.size), 
                    0, cooldown_pct * 6.28, 2)

    def render_range(self, screen):
        if self.name != "Sniper Cow":
            range_surface = Surface((self.range * 2, self.range * 2), SRCALPHA).convert_alpha()
            draw.circle(range_surface, (0, 0, 0, 50), (self.range, self.range), self.range)

            screen.blit(range_surface, (self.center_pos[0] - self.range, self.center_pos[1] - self.range))
        else:
            range_surface = Surface((64 * 23, 64 * 10), SRCALPHA).convert_alpha()
            draw.rect(range_surface, (0, 0, 0, 50), (0, 0, 64 * 23, 64 * 10))
            screen.blit(range_surface, (225, 121))

    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()
    
    @Logger.log_method()
    def set_pos(self, pos):
        self.center_pos = pos

    @Logger.log_method()
    def set_position(self, tile:Tile):
        self.center_pos = tuple(coord + TILE_SIZE / 2 for coord in tile.pos_top_left)
    @Logger.log_method()
    def set_position_bench(self, index):
        row = index // 2
        col = index % 2
        self.center_pos = (38 + (TILE_SIZE/2) + 84*col, 198 + (TILE_SIZE/2) + 84*row)
    def rotate_to_target(self):
        if self.target_enemy:
            #Calculate angle to the target enemy
            dx = self.target_enemy.center_pos[0] - self.center_pos[0]
            dy = self.target_enemy.center_pos[1] - self.center_pos[1]
            self.angle = degrees(atan2(-dy, dx)) - 90 

            #Rotate the image
            self.image = transform.rotate(self.original_image, self.angle)


    def find_closest_target(self):
        enemies = enemies_on_map.sprites()
        if not enemies:
            self.target_enemy = None
            return
        if self.target_enemy == None:
            self.target_enemy = enemies[0]
        for enemy in enemies:
            if self.distance_to_enemy(enemy) < self.distance_to_enemy(self.target_enemy) \
            and self.distance_to_enemy(enemy) <= self.range:
                if self.target_enemy != enemy:
                    self.target_enemy = enemy
                    logger.info(f"{self.name} has now targeted {self.target_enemy}")
        if self.distance_to_enemy(self.target_enemy) > self.range:
            self.target_enemy = None

    def distance_to_enemy(self, enemy) -> float:
        dx = self.center_pos[0] - enemy.center_pos[0]
        dy = self.center_pos[1] - enemy.center_pos[1]
        return sqrt(dx**2 + dy**2)

    @Logger.log_method()
    def handle_left_click(self, mouse_pos):
        rect = self.image.get_rect(center=self.center_pos)
        if rect.collidepoint(mouse_pos):
            return self


    @Logger.log_method()
    def handle_right_click(self, mouse_pos):
        rect = self.image.get_rect(center=self.center_pos)
        if rect.collidepoint(mouse_pos):
            return self
        
    @Logger.log_method()
    def star_up(self):
        self.level += 1

    def attack_enemy(self, delta_time):
        if self.target_enemy: 
            if  self.target_enemy.is_dead:
                self.target_enemy = None
            if self.attack_cooldown <= 0:
                if type(self.target_enemy) == Enemy:
                    logger.info(f"{self.name} attacked {self.target_enemy}")
                    self.target_enemy.take_damage(self.dmg)
                    # Set cooldown based on attacks per second
                    self.attack_cooldown = 1 / self.attack_speed


# for j in range(0, 10):
#     for i in range(0, 20):
#         tower = Tower("Cow", 10, 'assets\maps\Cow.png')
#         tower.set_position(map1.tiles[i][j])
#         towers_on_map.add(tower)