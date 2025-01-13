from queue import Queue
import pygame
from src.enemy import Enemy, enemies_on_map
from typing import List, Tuple, Dict
from src.settings import FONT_URL
import random

class WaveAnnouncement:
    def __init__(self):
        self.font = pygame.font.Font(FONT_URL, 132)
        self.small_font = pygame.font.Font(FONT_URL, 66)
        self.display_duration = 5.0
        self.fade_duration = 1
        self.display_time = 0
        self.is_active = False
        self.message = ""
        self.sub_message = ""

    def show_announcement(self, wave_number: int, enemies_info: str):
        self.message = f"Wave {wave_number}"
        self.sub_message = enemies_info
        self.display_time = 0
        self.is_active = True

    def update(self, delta_time: float):
        if self.is_active:
            self.display_time += delta_time
            if self.display_time >= self.display_duration:
                self.is_active = False

    def render(self, screen):
        if not self.is_active:
            return

        alpha = 255
        if self.display_time < self.fade_duration:
            alpha = int(255 * (self.display_time / self.fade_duration))
        elif self.display_time > (self.display_duration - self.fade_duration):
            alpha = int(255 * ((self.display_duration - self.display_time) / self.fade_duration))

        #Render main message
        text_surface = self.font.render(self.message, True, (255, 255, 255))
        text_surface.set_alpha(alpha)
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 300))
        screen.blit(text_surface, text_rect)

        #Render sub-message
        sub_surface = self.small_font.render(self.sub_message, True, (0, 0, 0))
        sub_surface.set_alpha(alpha)
        sub_rect = sub_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))
        screen.blit(sub_surface, sub_rect)

class Wave:
    ENEMY_TYPES = {
        "slime": {
            "name": "Slime",
            "base_health": 100,
            "base_speed": 100,
            "image": "assets/maps/enemy_green_slime.png"
        },
        "fast_slime": {
            "name": "Fast Slime",
            "base_health": 75,
            "base_speed": 150,
            "image": "assets/maps/enemy_green_slime.png"
        },
        "tank_slime": {
            "name": "Tank Slime",
            "base_health": 200,
            "base_speed": 75,
            "image": "assets/maps/enemy_green_slime.png" 
        }
    }

    def __init__(self, wave_number: int, enemy_data: List[Tuple[str, int, float, str]], spawn_interval: float, reward: int):
        self.wave_number = wave_number
        self.enemy_queue = Queue()
        for enemy_info in enemy_data:
            name, health, speed, image = enemy_info
            self.enemy_queue.put(Enemy(name, health, speed, image))
        
        self.spawn_interval = spawn_interval
        self.reward = reward
        self.elapsed_time = 0
        self.time_since_last_spawn = 0
        self.is_active = False
        self.is_completed = False
        
        #Debug information
        self.debug_font = pygame.font.Font(None, 24)
        self.font = pygame.font.Font(FONT_URL, 32)
        self.enemies_spawned = 0
        self.total_enemies = self.enemy_queue.qsize()

    def start(self):
        self.is_active = True
        self.elapsed_time = 0
        self.time_since_last_spawn = 0
        print(f"Wave {self.wave_number} started! Total enemies: {self.total_enemies}")

    def update(self, delta_time: float) -> bool:
        if not self.is_active or self.is_completed:
            return False

        self.elapsed_time += delta_time
        self.time_since_last_spawn += delta_time

        if self.time_since_last_spawn >= self.spawn_interval and not self.enemy_queue.empty():
            self.spawn_enemy()
            self.time_since_last_spawn = 0

        if self.enemy_queue.empty() and len(enemies_on_map) == 0:
            self.complete_wave()
            return True

        return False

    def spawn_enemy(self):
        if not self.enemy_queue.empty():
            enemy = self.enemy_queue.get()
            enemies_on_map.add(enemy)
            self.enemies_spawned += 1
            print(f"Spawned enemy {self.enemies_spawned}/{self.total_enemies}")

    def complete_wave(self):
        self.is_completed = True
        self.is_active = False
        from src.player import player
        player.add_gold(self.reward)
        print(f"Wave {self.wave_number} completed! Reward: {self.reward} gold")

    def render_debug(self, screen):
        """Render debug information to verify wave mechanics"""
        debug_info = [
            f"Wave: {self.wave_number}",
            f"Active: {self.is_active}",
            f"Completed: {self.is_completed}",
            f"Enemies Spawned: {self.enemies_spawned}/{self.total_enemies}",
            f"Enemies Alive: {len(enemies_on_map)}",
            f"Enemies Queued: {self.enemy_queue.qsize()}",
            f"Time: {self.elapsed_time:.1f}s",
            f"Next Spawn: {max(0, self.spawn_interval - self.time_since_last_spawn):.1f}s"
        ]

        for i, text in enumerate(debug_info):
            surface = self.debug_font.render(text, True, (255, 255, 255))
            screen.blit(surface, (10, 200 + i * 25))

    def render(self, screen):
        surface = self.font.render(f"Wave: {self.wave_number}", True, (255, 255, 255))
        screen.blit(surface, (810, 5))
        
    @staticmethod
    def create_wave(wave_number: int) -> Tuple['Wave', str]:
        """Create a wave with mixed enemy types"""
        enemy_counts: Dict[str, int] = {}
        enemy_data = []
        total_enemies = 5 + wave_number

        if wave_number < 3:
            enemy_counts["slime"] = total_enemies
        else:
            enemy_counts["slime"] = total_enemies // 2
            enemy_counts["fast_slime"] = total_enemies // 4
            enemy_counts["tank_slime"] = total_enemies - (enemy_counts["slime"] + enemy_counts["fast_slime"])

        difficulty_multiplier = 1 + (wave_number - 1) * 0.2

        for enemy_type, count in enemy_counts.items():
            base_enemy = Wave.ENEMY_TYPES[enemy_type]
            for _ in range(count):
                enemy_data.append((
                    base_enemy["name"],
                    int(base_enemy["base_health"] * difficulty_multiplier),
                    base_enemy["base_speed"],
                    base_enemy["image"]
                ))

        random.shuffle(enemy_data)

        enemies_info = ", ".join(f"{count}x {Wave.ENEMY_TYPES[enemy_type]['name']}" 
                               for enemy_type, count in enemy_counts.items() if count > 0)

        return Wave(
            wave_number=wave_number,
            enemy_data=enemy_data,
            spawn_interval=2.0,
            reward=10 + (wave_number - 1) * 5
        ), enemies_info

wave_announcement = WaveAnnouncement() # type: ignore