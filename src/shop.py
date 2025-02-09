from random import random
from src.card import cards, Rarity
from src.logger import Logger
import yaml
import random
from pygame import Rect, image, font, Surface
from src.settings import FONT_URL
from typing import Tuple

class Shop:
    def __init__(self) -> None:
        self.content = []
        self.chances = {
            '1_cost': 0,
            '2_cost': 0,
            '3_cost': 0,
            '4_cost': 0,
            '5_cost': 0,
        }
        self.update_chances(1)
        self.refresh_shop()
        self.reroll_button_rect = Rect(234,880, 157, 57)
        self.reroll_button_image = image.load("assets/ui/reroll_button.png")
        self.font = font.Font(FONT_URL, 32)
        self.reroll_text_surface = self.font.render("Reroll", True, (54, 0, 0))
        
        
    @Logger.log_method()
    def remove_from_shop(self, pos: Tuple[int, int]) -> None:
        self.content[pos] = cards["Empty"].clone()
        for card in self.content:
            if card.cow_name != "Empty":
                return
        self.refresh_shop()

    def refresh_shop(self) -> None:
        self.content = []
        
        total_chances = sum(self.chances.values())
        if not (99.9 <= total_chances <= 100.1):
            print(f"Warning: Chances sum to {total_chances}, not 100")
        
        while len(self.content) < 5:
            roll = random.uniform(0, 100)
            
            cumulative = 0
            selected_rarity = 1 
            
            for cost_level in range(1, 6):
                chance = self.chances[f"{cost_level}_cost"]
                cumulative += chance
                
                if roll <= cumulative:
                    selected_rarity = cost_level
                    break
            
            rarity_map = {
                1: Rarity.COMMON,
                2: Rarity.UNCOMMON,
                3: Rarity.RARE,
                4: Rarity.EPIC,
                5: Rarity.LEGENDARY
            }
            
            available_cards = [
                card for card in cards.values()
                if card.rarity == rarity_map[selected_rarity] and card.cow_name != "Empty"
            ]
            
            if available_cards:
                card = random.choice(available_cards).clone()
                self.content.append(card)

    def handle_mouse_move_event(self, mouse_pos: Tuple[int, int]) -> None:
        if self.reroll_button_rect.collidepoint(mouse_pos):
            self.reroll_button_image = image.load("assets/ui/reroll_button_hover.png")
        else:
            self.reroll_button_image = image.load("assets/ui/reroll_button.png")
    @Logger.log_method()
    def handle_click_event(self, mouse_pos: Tuple[int, int]) -> int:
        for i, card in enumerate(self.content):
            if card.is_clicked(mouse_pos):
                return i
        return -1
    def handle_button_click(self, mouse_pos: Tuple[int, int]) -> None:
        return self.reroll_button_rect.collidepoint(mouse_pos)
    def render(self, screen: Surface) -> None:
        for i, card in enumerate(self.content):
            card.render(screen, shop_positions[i])
        rect = self.reroll_button_image.get_rect(topleft=(234,880))
        screen.blit(self.reroll_button_image, rect)
        screen.blit(self.reroll_text_surface, (245, 887))

    def update_chances(self, current_wave: int) -> None:
        # print(f"Wave: {current_wave}")
        with open('assets/chances.yaml', "r") as file:
            data = yaml.safe_load(file)

        wave_data = next((wave for wave in data["waves"] if wave["wave"] == current_wave), None)
    
        if wave_data:
            self.chances = {
                "1_cost": wave_data["cost_1"],
                "2_cost": wave_data["cost_2"],
                "3_cost": wave_data["cost_3"],
                "4_cost": wave_data["cost_4"],
                "5_cost": wave_data["cost_5"]
            }
        # print(self.chances)

    def __repr__(self) -> str:
        pass
    def __str__(self) -> str:
        return self.content
    
shop_positions = ((401, 866),(625, 866),(849, 866),(1073, 866),(1297, 866))
shop = Shop()