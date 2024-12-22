from src.tower import Tower
from src.shop import Shop
from src.tower import Tower
from src.settings import BENCH_SIZE
from pygame import sprite
class Player:
    def __init__(self):
        self.bench = sprite.Group()
        self.field = sprite.Group()
        self.chances = [0,0,0,0,0]
        self.gold = 100
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

    def render(self, screen):
        self.shop.render(screen)
        for cow in self.bench:
            cow.render(screen)
            
        # for cow in self.bench:

    def buy_card_from_shop(self, card_index:int):
        card = self.shop.content[card_index]
        if card.cow_name != "Empty":
            if player.gold >= card.rarity.value:
                if len(player.bench) < BENCH_SIZE:
                    tower = Tower(card.cow_name, card.damage, f'assets\maps\{card.cow_name.lower().replace(" ", "_")}.png')
                    tower.set_position_bench(len(self.bench))
                    player.bench.add(tower)
                    player.shop.remove_from_shop(card_index)
                    player.remove_gold(card.rarity.value)
                else:
                    print("Bench is full")
            else:
                print("Not enough gold")

    def handle_click_event(self, mouse_pos):
        card_index = self.shop.handle_click_event(mouse_pos)
        if card_index >= 0:
            self.buy_card_from_shop(card_index)

    def __str__(self):
        pass
    def __repr__(self):
        pass

player = Player()