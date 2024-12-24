from src.tower import Tower
from src.shop import Shop
from src.tower import Tower
from src.settings import BENCH_SIZE
from pygame import sprite
from src.map import map1
class Player:
    def __init__(self):
        self.bench = sprite.Group()
        self.field = sprite.Group()
        self.chances: list[int] = [0,0,0,0,0]
        self.gold: int = 100
        self.hp: int = 100
        self.shop: Shop = Shop()
        self.cow_on_hold = None

    def add_to_bench(self, tower:Tower):
        self.bench.append(tower)
    def remove_from_bench(self, tower:Tower):
        self.bench.remove(tower)

    def add_to_field(self, tower:Tower):
        if tower in self.bench:
            self.remove_from_bench(tower)
        self.field.add(tower)
        print(self.bench)

    def remove_from_field(self, tower:Tower):
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

    def update(self):
        self.field.update()
    def render(self, screen):
        self.shop.render(screen)
        for cow in self.bench:
            cow.render(screen)
        for cow in self.field:
            cow.render(screen)
        if self.cow_on_hold:
            self.cow_on_hold.render(screen)
            
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

    def handle_click_event(self, mouse_click_event):
        if mouse_click_event.button == 1:
            card_index = self.shop.handle_click_event(mouse_click_event.pos)
            if card_index >= 0:
                self.buy_card_from_shop(card_index)
            if self.cow_on_hold and map1.get_tile_by_pos(mouse_click_event.pos):
                self.cow_on_hold.set_position(map1.get_tile_by_pos(mouse_click_event.pos))
                self.add_to_field(self.cow_on_hold)
                self.cow_on_hold = None
        if mouse_click_event.button == 3:
            if self.cow_on_hold == None:
                for cow in self.bench:
                    clicked_cow = cow.handle_right_click(mouse_click_event.pos)
                    if clicked_cow:
                        self.cow_on_hold = clicked_cow
                        break
        
    def mouse_move_event(self, pos):
        if self.cow_on_hold:
            self.cow_on_hold.set_pos(pos)
    def __str__(self):
        pass
    def __repr__(self):
        pass

player = Player()

tower1 = Tower("Cow", 10, 'assets\maps\cow.png')
player.add_to_field(tower1)
tower2 = Tower("Cow2", 10, 'assets\maps\cow.png')
tower2.set_position(map1.tiles[5][6])
player.add_to_field(tower2)
