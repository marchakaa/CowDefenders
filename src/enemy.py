from pygame import sprite
import pygame
from src.map import map1, MAP_START
from src.settings import TILE_SIZE
from src.logger import Logger
from src.effects import EffectManager, Effect

logger = Logger
class Enemy(sprite.Sprite):
    def __init__(self, name:str, health:int, move_speed:float, image_url:str="") -> None:
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
        self.is_dead = False
        self.effect_manager = EffectManager()

        if image_url:
            self.image = pygame.image.load(image_url)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        else:
            self.image = None

    def update(self, delta_time: float) -> None:
        if self.checkpoint < len(map1.map_points) - 1:
            next_target = map1.map_points[self.checkpoint + 1]

            direction = pygame.Vector2(next_target) - pygame.Vector2(self.center_pos)
            distance = direction.length()

            if distance > 0:
                direction = direction.normalize()
                movement = direction * self.move_speed * delta_time

                if movement.length() >= distance:
                    self.center_pos = list(next_target)
                    self.checkpoint += 1
                else:
                    self.center_pos[0] += movement.x
                    self.center_pos[1] += movement.y
        else:
            self.player.remove_health(self.damage)
            self.on_death()

        self.effect_manager.update(delta_time, self)

    def render(self, screen: pygame.Surface) -> None:
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
    def heal(self, amount: float) -> None:
        self.current_health = min (self.max_health, self.current_health + amount)
    # @Logger.log_method()
    def take_damage(self, amount: float) -> None:
        if amount >= self.current_health:
            self.on_death()
            logger.info(f"{self} died")
        else:
            self.current_health -= amount
            # logger.info(f"{self} took {amount} damage")
    @Logger.log_method()
    def on_death(self) -> None:
        enemies_on_map.remove(self)
        self.is_dead = True

    def set_player(self, player) -> None:
        self.player = player

    def apply_effect(self, effect: Effect) -> None:
        self.effect_manager.add_effect(effect)

    def __str__(self) -> str:
        return super().__str__()
    def __repr__(self) -> str:
        return super().__repr__()

    
class EnemyGroup(sprite.Group):
    def update(self, delta_time: float) -> None:
        for enemy in self.sprites():
            enemy.update(delta_time)
enemies_on_map = sprite.Group()