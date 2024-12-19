from random import random
import yaml


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

    def remove_from_shop(self, cow):

        # self.pool[cow] = 
        pass

    def refresh_shop(self):
        pass

    def set_pool(self, pool):
        pass

    def __repr__(self):
        pass
    def __str__(self):
        return self.content
    

shop = Shop()