from queue import Queue
import pygame
from src.enemy import Enemy, enemies_on_map
from typing import List, Tuple, Dict
from src.settings import FONT_URL
from src.logger import Logger
import random

class WaveAnnouncement:
    def __init__(self) -> None:
        self.font = pygame.font.Font(FONT_URL, 132)
        self.small_font = pygame.font.Font(FONT_URL, 66)
        self.display_duration = 5.0
        self.fade_duration = 1
        self.display_time = 0
        self.is_active = False
        self.message = ""
        self.sub_message = ""

    def show_announcement(self, wave_number: int, enemies_info: str) -> None:
        self.message = f"Wave {wave_number}"
        self.sub_message = enemies_info
        self.display_time = 0
        self.is_active = True

    def update(self, delta_time: float) -> None:
        if self.is_active:
            self.display_time += delta_time
            if self.display_time >= self.display_duration:
                self.is_active = False

    def render(self, screen: pygame.Surface) -> None:
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
        "blue_slime": {
            "name": "Blue Slime",
            "base_health": 100,  
            "base_speed": 100,
            "image": "assets/enemies/blue_slime.png"
        },
        "red_slime": {
            "name": "Red Slime",
            "base_health": 80,   
            "base_speed": 150,
            "image": "assets/enemies/red_slime.png"
        },
        "yellow_slime": {
            "name": "Yellow Slime",
            "base_health": 300,  
            "base_speed": 75,
            "image": "assets/enemies/yellow_slime.png"
        },
        "black_slime": {
            "name": "Black Slime",
            "base_health": 150,  
            "base_speed": 125,
            "image": "assets/enemies/black_slime.png"
        },
        "white_slime": {
            "name": "White Slime",
            "base_health": 120,  
            "base_speed": 110,
            "image": "assets/enemies/white_slime.png"
        },
        "orange_slime": {
            "name": "Orange Slime",
            "base_health": 130,  
            "base_speed": 130,
            "image": "assets/enemies/orange_slime.png"
        },
        "purple_slime": {
            "name": "Purple Slime",
            "base_health": 200,  
            "base_speed": 90,
            "image": "assets/enemies/purple_slime.png"
        },
        "green_slime": {
            "name": "Green Slime",
            "base_health": 110,  
            "base_speed": 115,
            "image": "assets/enemies/green_slime.png"
        }
    }

    def __init__(self, wave_number: int, enemy_data: List[Tuple[str, int, float, str]], spawn_interval: float, reward: int) -> None:
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

    @Logger.log_method()
    def start(self) -> None:
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

    @Logger.log_method()
    def spawn_enemy(self) -> None:
        if not self.enemy_queue.empty():
            enemy = self.enemy_queue.get()
            enemies_on_map.add(enemy)
            self.enemies_spawned += 1
            print(f"Spawned enemy {self.enemies_spawned}/{self.total_enemies}")

    @Logger.log_method()
    def complete_wave(self) -> None:
        self.is_completed = True
        self.is_active = False
        from src.player import player
        player.add_gold(self.reward)
        player.shop.update_chances(self.wave_number+1)
        player.shop.refresh_shop()
        print(f"Wave {self.wave_number} completed! Reward: {self.reward} gold")

    def render_debug(self, screen: pygame.Surface) -> None:
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

    def render(self, screen: pygame.Surface) -> None:
        surface = self.font.render(f"Wave: {self.wave_number}", True, (255, 255, 255))
        screen.blit(surface, (810, 5))
        
    @staticmethod
    def create_wave(wave_number: int) -> Tuple['Wave', str]:
        enemy_counts: Dict[str, int] = {}
        enemy_data = []
        
        base_enemies = 5
        max_enemies = 25
        total_enemies = base_enemies + int((max_enemies - base_enemies) * (wave_number / 20))

        if wave_number <= 3:  # Waves 1-3
            enemy_counts["blue_slime"] = total_enemies
            
        elif wave_number <= 5:  # Waves 4-5
            enemy_counts["blue_slime"] = total_enemies // 2
            enemy_counts["red_slime"] = total_enemies // 4
            enemy_counts["green_slime"] = total_enemies - (enemy_counts["blue_slime"] + enemy_counts["red_slime"])
            
        elif wave_number <= 10:  # Waves 6-10
            available_types = ["blue_slime", "red_slime", "green_slime", "white_slime", "orange_slime"]
            selected_types = random.sample(available_types, 4)
            for type_ in selected_types:
                enemy_counts[type_] = total_enemies // 4
                
        elif wave_number <= 15:  # Waves 11-15
            available_types = list(Wave.ENEMY_TYPES.keys())
            num_types = 6
            selected_types = random.sample(available_types, num_types)
            base_count = total_enemies // num_types
            for type_ in selected_types:
                enemy_counts[type_] = base_count
                
        else:  # Waves 16-20
            available_types = list(Wave.ENEMY_TYPES.keys())
            num_types = 8
            selected_types = random.sample(available_types, num_types)
            base_count = total_enemies // num_types
            remainder = total_enemies % num_types
            for i, type_ in enumerate(selected_types):
                enemy_counts[type_] = base_count + (1 if i < remainder else 0)

        difficulty_multiplier = 1 + (wave_number / 5) ** 2

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

        spawn_interval = max(0.5, 2.0 - (wave_number / 20))
        
        base_reward = 3
        reward = int((base_reward + wave_number)*(1+wave_number/10))

        return Wave(
            wave_number=wave_number,
            enemy_data=enemy_data,
            spawn_interval=spawn_interval,
            reward=reward
        ), enemies_info

wave_announcement = WaveAnnouncement() # type: ignore