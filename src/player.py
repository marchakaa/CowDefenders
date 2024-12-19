from src.tower import Tower
from src.shop import Shop
class Player:
    def __init__(self):
        self.bench = []
        self.field = []
        self.chances = [0,0,0,0,0]
        self.gold = 0
        self.hp = 100
        self.shop = Shop()

    #Setters
    def add_to_bench(self, tower:Tower):
        self.bench.append(tower)
    def remover_from_bench(self, tower:Tower):
        self.bench.remove(tower)

    def add_to_field(self, tower:Tower):
        self.field.append(tower)
    def remover_from_field(self, tower:Tower):
        self.field.remove(tower)
        
    def add_gold(self, amount:int):
        self.gold += amount
    def remove_gold(self, amount:int):
        self.gold -= amount
        
    def add_hp(self, amount:int):
        self.hp += amount
    def remove_hp(self, amount:int):
        self.hp -= amount
    def set_hp(self, amount:int):
        self.hp = amount

    #Update Chances

    def __str__(self):
        pass
    def __repr__(self):
        pass