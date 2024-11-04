from pygame import sprite
import pygame
from src.map import mapPoints

class Enemy(sprite.Sprite):
    def __init__(self, name, health, move_speed, image_url=""):
        super().__init__()
        self.name = name
        self.hp = health
        self.move_speed = move_speed
        self.size = 32
        self.center_pos = [0, 13 * 32]
        self.checkpoint = 0

        if image_url:
            self.image = pygame.image.load(image_url)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        else:
            self.image = None

    def update(self):
        if self.checkpoint < len(mapPoints) - 1:
            next_target = mapPoints[self.checkpoint + 1]

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
enemytest = Enemy("Asni", 100, 2, "assets/maps/enemy_green_slime.png")
