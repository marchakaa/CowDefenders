from pygame import sprite
import pygame
from src.map import map1, MAP_START
from src.settings import TILE_SIZE

class Enemy(sprite.Sprite):
    def __init__(self, name:str, health:int, move_speed:float, image_url:str=""):
        super().__init__()
        self.name = name
        self.max_health = health
        self.current_health = health
        self.move_speed = move_speed
        self.damage = 10
        self.size = TILE_SIZE
        self.center_pos = [MAP_START[0], MAP_START[1] + 8 * TILE_SIZE]
        self.checkpoint = 0
        self.player = None

        if image_url:
            self.image = pygame.image.load(image_url)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        else:
            self.image = None

    def update(self, delta_time):
        if self.checkpoint < len(map1.map_points) - 1:
            next_target = map1.map_points[self.checkpoint + 1]

            dx = next_target[0] - self.center_pos[0]
            dy = next_target[1] - self.center_pos[1]

            distance = (dx**2 + dy**2)**0.5
            if distance != 0:
                dx = (dx / distance) * self.move_speed * delta_time
                dy = (dy / distance) * self.move_speed * delta_time

                self.center_pos[0] += dx
                self.center_pos[1] += dy

            if abs(next_target[0] - self.center_pos[0]) < 1 and abs(next_target[1] - self.center_pos[1]) < 1:
                self.center_pos = list(next_target)
                self.checkpoint += 1
        else:
            self.player.remove_health(self.damage)
            self.on_death()

    def render(self, screen):
        if self.image:
            rect = self.image.get_rect(center=self.center_pos)
            screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.center_pos[0] - self.size / 2, self.center_pos[1] - self.size / 2, self.size, self.size))

        #Draw healthbar
        health_bar_width = self.size
        health_bar_height = 5
        health_bar_x = self.center_pos[0] - self.size / 2
        health_bar_y = self.center_pos[1] - self.size / 2 - health_bar_height - 2

        current_health_width = int((self.current_health / self.max_health) * health_bar_width)
        health_bar_background = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        current_health_rect = pygame.Rect(health_bar_x, health_bar_y, current_health_width, health_bar_height)

        pygame.draw.rect(screen, (128, 128, 128), health_bar_background)

        pygame.draw.rect(screen, (0, 255, 0), current_health_rect)

    def take_damage(self, amount):
        if amount >= self.current_health:
            self.on_death()
        else:
            self.current_health -= amount
    def on_death(self):
        enemies_on_map.remove(self)

    def set_player(self, player):
        self.player = player
    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()
    
class EnemyGroup(sprite.Group):
    def update(self, delta_time):
        for enemy in self.sprites():
            enemy.update()
# Example usage
enemy1 = Enemy("Asni", 100, 100, "assets/maps/enemy_green_slime.png")
# enemy2 = Enemy("Asni", 100, 2, "assets/maps/enemy_green_slime.png")
# enemy3 = Enemy("Asni", 100, 2, "assets/maps/enemy_green_slime.png")
enemies_on_map = sprite.Group()
enemies_on_map.add(enemy1)