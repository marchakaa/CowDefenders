from pygame import sprite, image, transform, draw, font, Surface, SRCALPHA
from math import sqrt, degrees, atan2
from enum import Enum
from typing import Tuple
import yaml

from src.settings import TILE_SIZE
from src.enemy import enemies_on_map, Enemy
from src.map import Tile, map1
from src.logger import Logger
import src.effects as effects


logger = Logger()


class TargetType(Enum):
    CLOSEST_TARGET = "CLOSEST_TARGET"
    FIRST_TARGET = "FIRST_TARGET"
    LAST_TARGET = "LAST_TARGET"
    HIGHEST_HEALTH_TARGET = "HIGHEST_HEALTH_TARGET"
    LOWEST_HEALTH_TARGET = "LOWEST_HEALTH_TARGET"

class Tower(sprite.Sprite):
    def __init__(self, name:str, dmg:float, attack_speed: float, attack_range: int, starting_fury: int, max_fury: int, \
                 fury_gain: int, fury_lock: bool, target_type: TargetType, image_url:str="") -> None:
        super().__init__()
        #BASIC STATS
        self.name = name
        self.current_fury = starting_fury
        self.max_fury = max_fury
        self.level = 1        
        self.ability = self._create_ability(name)
        self.fury_lock = fury_lock
        self.target_type = TargetType(target_type)
        #BASE STATS
        self.base_dmg = dmg
        self.base_attack_speed = attack_speed
        self.base_range = attack_range
        self.base_fury_gain = fury_gain
        #BONUS STATS
        self.bonus_dmg = 0
        self.bonus_attack_speed = 0
        self.bonus_range = 0
        self.bonus_fury_gain = 0
        #ADITIONAL STATS
        self.attack_cooldown = 0
        self.effect_manager = effects.EffectManager()
        self.appliable_effects = []
        self.target_enemy = None
        #RENDER STATS
        self.center_pos = [257,153]
        self.size = TILE_SIZE
        if image_url:
            self.original_image = image.load(image_url)  # Keep the original image unrotated
            self.original_image = transform.scale(self.original_image, (self.size, self.size))
            self.image = self.original_image
        else:
            self.image = None
        self.font = font.Font(None, 24)


    #RENDER AND UPDATE
    def update(self, delta_time: float) -> None:
        if self.attack_cooldown > 0:
            self.attack_cooldown = max(0, self.attack_cooldown - delta_time)

        self.find_closest_target()
        self.rotate_to_target()
        self.attack_enemy(delta_time)
        if self.ability:
            self.ability.update(self, delta_time)
    def render(self, screen: Surface) -> None:
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


        # Render fury bar
        fury_height = 4
        fury_width = self.size
        fury_x = self.center_pos[0] - fury_width / 2
        fury_y = self.center_pos[1] + self.size / 2 + 5

        # Background
        draw.rect(screen, (50, 50, 50), (fury_x, fury_y, fury_width, fury_height))
        # Fury amount
        fury_fill = (fury_width * self.current_fury) / self.max_fury
        draw.rect(screen, (255, 165, 0), (fury_x, fury_y, fury_fill, fury_height))

        #Render attack cooldown indicator
        if self.attack_cooldown > 0:
            cooldown_pct = self.attack_cooldown / (1 / self.get_total_attack_speed())
            draw.arc(screen, (255, 200, 0), 
                    (self.center_pos[0] - self.size/2, self.center_pos[1] - self.size/2, 
                     self.size, self.size), 
                    0, cooldown_pct * 6.28, 2)
    def render_range(self, screen: Surface) -> None:
        if self.name != "Sniper Cow":
            total_range = self.get_total_range()
            range_surface = Surface((total_range * 2, total_range * 2), SRCALPHA).convert_alpha()
            draw.circle(range_surface, (0, 0, 0, 50), (total_range, total_range), total_range)

            screen.blit(range_surface, (self.center_pos[0] - total_range, self.center_pos[1] - total_range))
        else:
            range_surface = Surface((64 * 23, 64 * 10), SRCALPHA).convert_alpha()
            draw.rect(range_surface, (0, 0, 0, 50), (0, 0, 64 * 23, 64 * 10))
            screen.blit(range_surface, (225, 121))



    #GETTER METHODS
    def get_total_dmg(self) -> float:
        return self.base_dmg + self.bonus_dmg
    def get_total_attack_speed(self) -> int:
        return self.base_attack_speed + self.bonus_attack_speed
    def get_total_range(self) -> int:
        return self.base_range + self.bonus_range
    def get_total_fury_gain(self) -> int:
        return self.base_fury_gain + self.bonus_fury_gain

    #POSITION MECHANICS
    # @Logger.log_method()
    def set_pos(self, pos: Tuple[int, int]) -> None:
        self.center_pos = pos

    # @Logger.log_method()
    def set_position(self, tile:Tile) -> None:
        self.center_pos = tuple(coord + TILE_SIZE / 2 for coord in tile.pos_top_left)

    # @Logger.log_method()
    def set_position_bench(self, index: int) -> None:
        row = index // 2
        col = index % 2
        self.center_pos = (38 + (TILE_SIZE/2) + 84*col, 198 + (TILE_SIZE/2) + 140*row)



    #FINDING ENEMY, DEALING DAMAGE AND ROTATING
    def find_closest_target(self) -> None:
        enemies = enemies_on_map.sprites()
        if not enemies:
            self.target_enemy = None
            return

        in_range_enemies = [enemy for enemy in enemies if self.distance_to_enemy(enemy) <= self.get_total_range()]
        if not in_range_enemies:
            self.target_enemy = None
            return

        if self.target_type == TargetType.CLOSEST_TARGET:
            self.target_enemy = min(in_range_enemies, key=self.distance_to_enemy)
        elif self.target_type == TargetType.FIRST_TARGET:
            self.target_enemy = max(in_range_enemies, key=lambda enemy: enemy.checkpoint)
        elif self.target_type == TargetType.LAST_TARGET:
            self.target_enemy = min(in_range_enemies, key=lambda enemy: enemy.checkpoint)
        elif self.target_type == TargetType.HIGHEST_HEALTH_TARGET:
            self.target_enemy = max(in_range_enemies, key=lambda enemy: enemy.current_health)
        elif self.target_type == TargetType.LOWEST_HEALTH_TARGET:
            self.target_enemy = min(in_range_enemies, key=lambda enemy: enemy.current_health)

    def distance_to_enemy(self, enemy: Enemy) -> float:
        dx = self.center_pos[0] - enemy.center_pos[0]
        dy = self.center_pos[1] - enemy.center_pos[1]
        return sqrt(dx**2 + dy**2)

    def attack_enemy(self, delta_time) -> None:
        if self.target_enemy: 
            if  self.target_enemy.is_dead:
                self.target_enemy = None
            if self.attack_cooldown <= 0:
                if type(self.target_enemy) == Enemy:
                    # logger.info(f"{self.name} attacked {self.target_enemy}")
                    self.target_enemy.take_damage(self.get_total_dmg())
                    #Apply effects
                    for effect in self.appliable_effects:
                        self.target_enemy.apply_effect(effect)

                    # Set cooldown based on attacks per second
                    self.attack_cooldown = 1 / self.get_total_attack_speed()
                    self.add_fury()

    def rotate_to_target(self) -> None:
        if self.target_enemy:
            #Calculate angle to the target enemy
            dx = self.target_enemy.center_pos[0] - self.center_pos[0]
            dy = self.target_enemy.center_pos[1] - self.center_pos[1]
            self.angle = degrees(atan2(-dy, dx)) - 90 

            #Rotate the image
            self.image = transform.rotate(self.original_image, self.angle)


    #EVENTS
    # @Logger.log_method()
    def handle_left_click(self, mouse_pos: Tuple[int, int]):
        rect = self.image.get_rect(center=self.center_pos)
        if rect.collidepoint(mouse_pos):
            return self
    # @Logger.log_method()
    def handle_right_click(self, mouse_pos: Tuple[int, int]):
        rect = self.image.get_rect(center=self.center_pos)
        if rect.collidepoint(mouse_pos):
            return self



    #UTILITY FUNCTIONS
    @Logger.log_method()
    def star_up(self) -> None:
        self.level += 1

        with open("assets/towers.yaml", 'r') as file:
            data = yaml.safe_load(file)
        attrs = data.get(self.name)

        if not attrs:
            return

        level_attrs = attrs.get(f'level_{self.level}')
        if not level_attrs:
            return

        self.base_dmg = level_attrs.get('damage', self.base_dmg)
        self.base_attack_speed = level_attrs.get('attack_speed', self.base_attack_speed)
        self.base_range = level_attrs.get('range', self.base_range)
        self.base_fury_gain = level_attrs.get('fury_gain', self.base_fury_gain)
        self.ability.upgrade(self)

    def add_fury(self) -> None:
        if self.ability.active and self.fury_lock:
            return
        if self.current_fury + self.get_total_fury_gain() >= self.max_fury:
            self.current_fury = 0
            if self.ability:
                self.ability.activate(self)
                logger.info(f"{self.name} activated {self.ability.name}")
        else:
            self.current_fury += self.get_total_fury_gain()

    def _create_ability(self, tower_name: str) -> "TowerAbility":
            ability_map = {
                "Cow": lambda: RageAbility(),
                "Air Cow": lambda: RageAbility(),
                "Fire Cow": lambda: BlazeAbility(),
                "Ice Cow": lambda: IceNovaAbility(),
                "Sniper Cow": lambda: DeadeyeAbility(),
            }
            
            ability_creator = ability_map.get(tower_name)
            if ability_creator:
                return ability_creator()
            return None
    
    #CLASS FUNCTIONS
    def __str__(self) -> str:
        return super().__str__()
    def __repr__(self) -> str:
        return super().__repr__()
    
class TowerAbility():
    def __init__(self, fury_cost: int, name: str, duration: float = 0, has_duration: bool = False) -> None:
        self.name = name
        self.fury_cost = fury_cost
        self.active = False
        self.elapsed_time = 0
        self.duration = duration
        self.has_duration = has_duration

    def __str__(self) -> str:
        base_info = f"{self.name}\nFury Cost: {self.fury_cost}"
        if self.has_duration:
            return f"{base_info}\nDuration: {self.duration:.1f}s"
        return base_info
    
    def activate(self) -> None:
        pass
    def deactivate(self) -> None:
        pass        
    def upgrade(self, level: int) -> None:
        pass
    def update(self, tower: Tower, delta_time: float) -> None:
        if self.active and self.has_duration:
            self.elapsed_time += delta_time
            if self.elapsed_time >= self.duration:
                self.deactivate(tower)
                self.active = False
                self.elapsed_time = 0
        
class RageAbility(TowerAbility): #Machinegun Cow
    def __init__(self) -> None:
        super().__init__(100, "Rage", 3, True)
        self.attack_speed_multiplier = 2

    def activate(self, tower: Tower) -> None:
        tower.bonus_attack_speed += tower.base_attack_speed
        tower.bonus_range += 50;
        self.active = True

    def deactivate(self, tower: Tower) -> None:
        tower.bonus_attack_speed -= tower.base_attack_speed
        tower.bonus_range -= 50;
    def __str__(self) -> str:
        return f"Doubles the tower attack speed for {self.duration} seconds."

class BlazeAbility(TowerAbility): #Fire Cow
    def __init__(self) -> None:
        super().__init__(40, "Blaze")
        self.stacks = 0
        self.stack_dmg_amplifier = 0.5

    def activate(self, tower: Tower) -> None:
        if self.stacks >= 25:
            burn_dmg = 10 + 0.1*tower.get_total_dmg()
            tower.appliable_effects.append(effects.BurnEffect(10, 5))
        if self.stacks == 50:
            tower.bonus_range += 100
        if self.stacks == 100:
            tower.bonus_range += 100
        self.stacks += 1
        tower.bonus_dmg += self.stack_dmg_amplifier
        self.active = True
    
    def upgrade(self, tower: Tower) -> None:
        if tower.level == 2:
            tower.bonus_dmg -= self.stacks*self.stack_dmg_amplifier
            self.stack_dmg_amplifier *= 2
            tower.bonus_dmg += self.stacks*self.stack_dmg_amplifier
        if tower.level == 3:
            tower.bonus_dmg -= self.stacks*self.stack_dmg_amplifier
            self.stack_dmg_amplifier *= 2.5
            tower.bonus_dmg += self.stacks*self.stack_dmg_amplifier
    def __str__(self) -> str:
        return f"Stacks: {self.stacks}, bonus damage: {self.stacks*self.stack_dmg_amplifier}"

class IceNovaAbility(TowerAbility): #Ice Cow
    def __init__(self) -> None:
        super().__init__(70, "Ice Nova", 3, True)
        self.range = 300
        # self.targets = []
    def activate(self, tower: Tower) -> None:
        for enemy in enemies_on_map:
            if tower.distance_to_enemy(enemy) <= self.range:
                # self.targets.append(enemy)
                enemy.apply_effect(effects.SlowEffect(duration=self.duration, amount=90))
        self.active = True
    def deactivate(self, tower: Tower) -> None:
        pass
    def upgrade(self, tower: Tower) -> None:
        if tower.level == 2:
            self.range = 330
            self.duration = 4
        if tower.level == 3:
            self.range = 330
            self.duration = 5
    def __str__(self) -> str:
        return f"Stuns all the slimes in {self.range} range for {self.duration} seconds"

class DeadeyeAbility(TowerAbility):
    def __init__(self) -> None:
        super().__init__(100, "Deadeye", 5, True)
        self.bonus_dmg = 1000
    def activate(self, tower: Tower) -> None:
        self.active = True
        tower.bonus_dmg += self.bonus_dmg
    def deactivate(self, tower: Tower) -> None:
        tower.bonus_dmg -= self.bonus_dmg
    def upgrade(self, tower: Tower) -> None:
        if tower.level == 2:
            self.range = 330
            self.duration = 5.5
        if tower.level == 3:
            self.range = 330
            self.duration = 6.5
    def __str__(self) -> str:
        return f"Oneshots enemies for {self.duration} seconds"

class ArtileryBombingAbility(TowerAbility):
    def __init__(self) -> None:
        super().__init__(120, "Artilery Bombing")
        self.range = 400
        self.damage = 80
    def activate(self, tower: Tower) -> None:
        self.active = True
        for enemy in enemies_on_map:
            if tower.distance_to_enemy(enemy) <= self.range:
                enemy.take_damage(self.damage)
