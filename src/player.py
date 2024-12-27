from src.tower import Tower
from src.shop import Shop
from src.tower import Tower
from src.settings import BENCH_SIZE, FONT_URL
from pygame import sprite, font
from src.map import map1
class Player:
    def __init__(self):
        self.bench: list[Tower] = [None, None, None, None, None, None, None, None]
        self.field = sprite.Group()
        self.chances: list[int] = [0,0,0,0,0]
        self.gold: int = 100
        self.hp: int = 100
        self.shop: Shop = Shop()
        self.cow_on_hold = None

    def add_to_bench(self, tower:Tower):
        for index, slot in enumerate(self.bench):
            if not slot:
                tower.set_position_bench(index)
                self.bench[index] = tower
                return True
        print("Bench is full!")
        return False

    def remove_from_bench(self, tower:Tower):
        for index, cow in enumerate(self.bench):
            if cow == tower:
                self.bench[index] = None

    def add_to_field(self, tower:Tower):
        if tower in self.bench:
            self.remove_from_bench(tower)
        self.field.add(tower)

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
            if cow: cow.render(screen)
        for cow in self.field:
            cow.render(screen)
        if self.cow_on_hold:
            self.cow_on_hold.render(screen)
        #Render money
        self.render_gold(screen)
            

    def buy_card_from_shop(self, card_index:int):
        card = self.shop.content[card_index]
        if card.cow_name != "Empty":
            if self.gold >= card.rarity.value:
                tower = Tower(card.cow_name, card.damage, f'assets\maps\{card.cow_name.lower().replace(" ", "_")}.png')
                added_to_bench = self.add_to_bench(tower)
                if added_to_bench:
                    self.remove_gold(card.rarity.value)
                    self.shop.remove_from_shop(card_index)
                    self.check_for_upgrade(tower)
            else:
                print("Not enough gold")

    def handle_click_event(self, mouse_click_event):
        if mouse_click_event.button == 1:
            #Ckick and buy the card
            card_index = self.shop.handle_click_event(mouse_click_event.pos)
            if card_index >= 0:
                self.buy_card_from_shop(card_index)
                
            #Reroll shop
            if self.shop.reroll_button_rect.collidepoint(mouse_click_event.pos):
                if self.gold >= 2:
                    self.shop.refresh_shop()
                    self.remove_gold(2)

            #Place cow on tile
            if self.cow_on_hold and map1.get_tile_by_pos(mouse_click_event.pos):
                self.check_for_upgrade(self.cow_on_hold)
                tile = map1.get_tile_by_pos(mouse_click_event.pos)
                if tile and tile.available:
                    self.cow_on_hold.set_position(tile)
                    self.add_to_field(self.cow_on_hold)
                    self.cow_on_hold = None
                    tile.available = False
            #Pick cow from the bench
            if self.cow_on_hold == None:
                for cow in self.bench:
                    if cow:
                        clicked_cow = cow.handle_left_click(mouse_click_event.pos)
                        if clicked_cow:
                            self.cow_on_hold = clicked_cow
                            break
        
        if mouse_click_event.button == 3:
            pass    
    def mouse_move_event(self, pos):
        if self.cow_on_hold:
            self.cow_on_hold.set_pos(pos)
    def __str__(self):
        pass
    def __repr__(self):
        pass

    def check_for_upgrade(self, tower: Tower) -> bool:
        fielded_match = [cow for cow in self.field if cow.name == tower.name and cow.level == tower.level]

        benched_match = [cow for cow in self.bench if cow and cow.name == tower.name and cow.level == tower.level]

        if len(fielded_match) >= 3:
            fielded_match[0].star_up()
            self.remove_from_field(fielded_match[1])
            self.remove_from_field(fielded_match[2])
            print(f"Upgraded {tower.name} from three towers on the field!")
            self.check_for_upgrade(fielded_match[0])
            return True

        if len(fielded_match) == 2 and len(benched_match) > 1:
            fielded_match[0].star_up()
            self.remove_from_field(fielded_match[1])
            self.remove_from_bench(tower)
            print(f"Upgraded {tower.name} on the field!")
            self.check_for_upgrade(fielded_match[0])
            return True

        if len(fielded_match) == 1 and len(benched_match) >= 2:
            fielded_match[0].star_up()
            self.remove_from_bench(benched_match[0])
            self.remove_from_bench(tower)
            print(f"Upgraded {tower.name} using one from the bench!")
            self.check_for_upgrade(fielded_match[0])
            return True

        if len(benched_match) >= 3:
            benched_match[0].star_up()
            self.remove_from_bench(benched_match[1])
            self.remove_from_bench(tower)
            print(f"Upgraded {tower.name} on the bench!")
            self.check_for_upgrade(benched_match[0])
            return True

        print(f"No upgrades available for {tower.name}.")
        return False

    def render_gold(self, screen) -> None:
        screen.blit(MONEY_TEXT.render(str(self.gold), True, (0,0,0)) , (1800, 30))

        

player = Player()
MONEY_TEXT = font.Font(FONT_URL, 32)