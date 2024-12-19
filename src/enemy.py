from pygame import sprite
import pygame
from src.map import map1, MAP_START
from src.settings import TILE_SIZE

class Enemy(sprite.Sprite):
    def __init__(self, name:str, health:int, move_speed:float, image_url:str=""):
        super().__init__()
        self.name = name
        self.hp = health
        self.move_speed = move_speed
        self.size = TILE_SIZE
        self.center_pos = [MAP_START[0], MAP_START[1] + 8 * TILE_SIZE]
        self.checkpoint = 0

        if image_url:
            self.image = pygame.image.load(image_url)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        else:
            self.image = None

    def update(self):
        if self.checkpoint < len(map1.map_points) - 1:
            next_target = map1.map_points[self.checkpoint + 1]

            if self.center_pos[0] < next_target[0]:
                self.center_pos[0] += self.move_speed
            elif self.center_pos[0] > next_target[0]:
                self.center_pos[0] -= self.move_speed

            if self.center_pos[1] < next_target[1]:
                self.center_pos[1] += self.move_speed
            elif self.center_pos[1] > next_target[1]:
                self.center_pos[1] -= self.move_speed

            if self.center_pos == list(next_target):
                self.checkpoint += 1

    def render(self, screen):
        if self.image:
            rect = self.image.get_rect(center=self.center_pos)
            screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.center_pos[0] - self.size / 2, self.center_pos[1] - self.size / 2, self.size, self.size))

    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()
# Example usage
enemy1 = Enemy("Asni", 100, 2, "assets/maps/enemy_green_slime.png")
enemies_on_map = sprite.Group()
enemies_on_map.add(enemy1)