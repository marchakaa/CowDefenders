from random import random
from src.card import cards, Card, Rarity
import yaml
import random
from pygame import Rect, draw


class Shop:
    def __init__(self):
        self.content = []
        self.pool = {} 
        self.chances = {
            '1_cost': 0,
            '2_cost': 0,
            '3_cost': 0,
            '4_cost': 0,
            '5_cost': 0,
        }
        self.refresh_shop()
        self.reroll_button_rect = Rect(260,900, 100, 50)
        

    def update_shop_percentages(self, current_wave):
        with open('assets/chances.yaml', "r") as file:
            data = yaml.safe_load(file)
        wave_data = data["waves"]
        for wave in wave_data:
            if wave["wave"] == current_wave:
                self.chances = {
                    "1_cost": wave["cost_1"],
                    "2_cost": wave["cost_2"],
                    "3_cost": wave["cost_3"],
                    "4_cost": wave["cost_4"],
                    "5_cost": wave["cost_5"]
                }

    def remove_from_shop(self, pos):
        self.content[pos] = cards["Empty"].clone()
        for card in self.content:
            if card.cow_name != "Empty":
                return
        self.refresh_shop()

    def refresh_shop(self):
        self.content = [] 
        while len(self.content) != 5:
            random_key = random.choice(list(cards.keys()))
            random_value = cards[random_key]
            if random_value.cow_name != "Empty":
                card = random_value.clone()
                self.content.append(card)

    def handle_click_event(self, mouse_pos) -> int:
        for i, card in enumerate(self.content):
            if card.is_clicked(mouse_pos):
                return i
        return -1

    def render(self, screen):
        for i, card in enumerate(self.content):
            card.render(screen, shop_positions[i])
        draw.rect(screen, (0, 0, 200), self.reroll_button_rect)
    def set_pool(self, pool):
        pass

    def __repr__(self):
        pass
    def __str__(self):
        return self.content
    
shop_positions = ((401, 866),(625, 866),(849, 866),(1073, 866),(1297, 866))
shop = Shop()