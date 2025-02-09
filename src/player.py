from src.tower import Tower
from src.shop import Shop
from src.tower import Tower
from src.card import Card, Rarity
from src.settings import BENCH_SIZE, FONT_URL
from pygame import sprite, font, draw, image, mouse, Surface
from src.map import map1
from src.logger import Logger
import json
from typing import Tuple

logger = Logger()
class Player:
    @Logger.log_method()
    def __init__(self) -> None:
        self.bench: list[Tower] = [None, None, None, None, None, None, None, None]
        self.field = sprite.Group()
        self.chances: list[int] = [0,0,0,0,0]
        self.gold: int = 2
        self.health: int = 100
        self.shop: Shop = Shop()
        self.cow_on_hold = None
        self.cow_on_hold_pos = 0
        self.clicked_cow = None
        self.health_color =self.transition_color_health_bar()
    @Logger.log_method()
    def add_to_bench(self, tower:Tower) -> bool:
        for index, slot in enumerate(self.bench):
            if not slot:
                tower.set_position_bench(index)
                self.bench[index] = tower
                return True
        logger.info("Bench is full!")
        return False

    @Logger.log_method()
    def remove_from_bench(self, tower:Tower) -> bool:
        for index, cow in enumerate(self.bench):
            if cow == tower:
                self.bench[index] = None
                return True
        return False

    @Logger.log_method()
    def add_to_field(self, tower:Tower) -> bool:
        if tower in self.bench:
            self.remove_from_bench(tower)
        self.field.add(tower)
        return True

    @Logger.log_method()
    def remove_from_field(self, tower:Tower) -> bool:
        self.field.remove(tower)
        return True
    
    @Logger.log_method()
    def add_gold(self, amount:int) -> None:
        self.gold += amount
        logger.info(f"Player gained {amount} money and now has {self.gold}")
    @Logger.log_method()
    def remove_gold(self, amount:int) -> None:
        self.gold -= amount
        logger.info(f"Player gave {amount} money and now has {self.gold}")
        
    @Logger.log_method()
    def add_health(self, amount:int) -> None:
        self.health += amount
        logger.info(f"Player gained {amount} health and now has {self.health}")
    @Logger.log_method()
    def remove_health(self, amount:int) -> None:
        self.health = 0 if self.health <= amount else self.health - amount
        logger.info(f"Player loss {amount} health and now has {self.health}")
        self.transition_color_health_bar()
    @Logger.log_method()
    def set_health(self, amount:int) -> None:
        self.health = amount
        logger.info(f"Player set it's health to {amount}")

    def update(self, delta_time: float) -> None:
        self.field.update(delta_time)
    def render(self, screen: Surface) -> None:
        self.shop.render(screen)
        for cow in self.bench:
            if cow: cow.render(screen)
        for cow in self.field:
            cow.render(screen)
        if self.cow_on_hold:
            self.cow_on_hold.render(screen)
        if self.clicked_cow:
            #Render range
            self.clicked_cow.render_range(screen)
            #Render cow card with stats
            self.render_cow_card(screen)

        #Render money
        self.render_gold(screen)
        #Render health
        self.render_health(screen)
    def render_cow_card(self, screen: Surface) -> None:
            #Icon
            cow_image = image.load(f"assets/cards/empty_card.png")
            screen.blit(cow_image, (1698, 213))
            #Fury
            percent = self.clicked_cow.current_fury / self.clicked_cow.max_fury
            x = 223 * percent
            draw.rect(screen, (255, 200, 0), (1697, 357, x, 5))
            draw.rect(screen, (0, 0, 0), (1697 + x, 357, 223 - x, 5))
            #Icons
            image_dmg = image.load("assets/icons/icon_dmg.png")
            image_fury = image.load("assets/icons/icon_fury.png")
            image_attack_speed = image.load("assets/icons/icon_attack_speed.png")
            image_attack_range = image.load("assets/icons/icon_attack_range.png")
            screen.blit(image_dmg, (1710, 370))
            screen.blit(image_fury, (1710, 410))
            screen.blit(image_attack_speed, (1710, 450))
            screen.blit(image_attack_range, (1710, 490))
            #Name
            name_surface = PLAYER_TEXT.render(str(self.clicked_cow.name), True, (255,255,255))
            card_left = 1697
            card_width = 223
            text_x = card_left + (card_width - name_surface.get_width()) // 2
            screen.blit(name_surface, (text_x, 317))
            #Stats
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.base_dmg), True, (255,255,255)) , (1750, 370))
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.base_fury_gain), True, (255,255,255)) , (1750, 410))
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.base_attack_speed), True, (255,255,255)) , (1750, 450))
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.base_range), True, (255,255,255)) , (1750, 490))
            #Bonus Stats
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.get_total_dmg()), True, (255,255,255)) , (1850, 370))
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.get_total_fury_gain()), True, (255,255,255)) , (1850, 410))
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.get_total_attack_speed()), True, (255,255,255)) , (1850, 450))
            screen.blit(PLAYER_TEXT.render(str(self.clicked_cow.get_total_range()), True, (255,255,255)) , (1850, 490))
            #Ability
            square_size = 40
            square_y = 530
            square_x = card_left + (card_width - square_size) // 2
            # Red square (template)
            draw.rect(screen, (255, 0, 0), (square_x, square_y, square_size, square_size))
            #Display ability info
            mouse_pos = mouse.get_pos()
            if (square_x <= mouse_pos[0] <= square_x + square_size and 
                square_y <= mouse_pos[1] <= square_y + square_size):
                ability_info = str(self.clicked_cow.ability).split('\n')
                line_height = INFO_TEXT.get_linesize()
                for i, line in enumerate(ability_info):
                    text_surface = INFO_TEXT.render(line, True, (255, 255, 255))
                    text_x = card_left + (card_width - text_surface.get_width()) // 2
                    text_y = square_y + square_size + 10 + (i * line_height)
                    screen.blit(text_surface, (text_x, text_y))
    def transition_color_health_bar(self) -> None:

        start_r, start_g, start_b = 172, 50, 50
        end_r, end_g, end_b = 72, 200, 117
        self.health_color = (int(start_r + (end_r - start_r) * self.health / 100),
                             int(start_g + (end_g - start_g) * self.health / 100),
                             int(start_b + (end_b - start_b) * self.health / 100),
                             )
    @Logger.log_method()
    def buy_card_from_shop(self, card_index:int) -> None:
        card = self.shop.content[card_index]
        if card.cow_name != "Empty":
            if self.gold >= card.rarity.value:
                tower = Tower(card.cow_name, card.damage, card.attack_speed, card.range, \
                              card.starting_fury, card.max_fury, card.fury_gain, card.fury_lock, card.target_type, \
                                f'assets\\towers\{card.cow_name.lower().replace(" ", "_")}.png')
                added_to_bench = self.add_to_bench(tower)
                if added_to_bench:
                    self.remove_gold(card.rarity.value)
                    self.shop.remove_from_shop(card_index)
                    self.check_for_upgrade(tower)
                    logger.info(f"Player bought the tower {tower} successfully")
            else:
                logger.info("Not enough gold")

    def handle_click_event(self, mouse_click_event) -> None:
        if mouse_click_event.button == 1:
            #Ckick and buy the card
            card_index = self.shop.handle_click_event(mouse_click_event.pos)
            if card_index >= 0:
                logger.info("Clicked buy from card")
                self.buy_card_from_shop(card_index)
                
            #Reroll shop
            if self.shop.handle_button_click(mouse_click_event.pos):
                logger.info("Clicked Reroll")
                if self.gold >= 2:
                    self.shop.refresh_shop()
                    self.remove_gold(2)

            #Place cow on tile
            if self.cow_on_hold and map1.get_tile_by_pos(mouse_click_event.pos):
                logger.info("Clicked to place cow")
                self.check_for_upgrade(self.cow_on_hold)
                tile = map1.get_tile_by_pos(mouse_click_event.pos)
                if tile and tile.available:
                    self.cow_on_hold.set_position(tile)
                    self.add_to_field(self.cow_on_hold)
                    self.cow_on_hold = None
                    self.clicked_cow = None
                    tile.available = False
                    return
            #Return the cow to the bench
            if self.cow_on_hold and not map1.get_tile_by_pos(mouse_click_event.pos):
                self.bench[self.cow_on_hold_pos] = self.cow_on_hold
                self.cow_on_hold.set_position_bench(self.cow_on_hold_pos)
                self.cow_on_hold = None
            #Pick cow from the bench
            if self.cow_on_hold == None:
                logger.info("Clicked to pick cow from bench")
                for i, cow in enumerate(self.bench):
                    if cow:
                        clicked_cow = cow.handle_left_click(mouse_click_event.pos)
                        if clicked_cow:
                            self.cow_on_hold = clicked_cow
                            self.cow_on_hold_pos = i
                            return

            #Select cow to draw range
            if self.clicked_cow == None:
                logger.info("Clicked do draw range")
                for cow in self.field:
                    if cow:
                        self.clicked_cow = cow.handle_left_click(mouse_click_event.pos)
                        if self.clicked_cow: return
            else: 
                logger.info("Clicked to stop showing range")
                self.clicked_cow = None
        
        if mouse_click_event.button == 3:
            pass    
    def mouse_move_event(self, pos: Tuple[int, int]) -> None:
        if self.cow_on_hold:
            self.cow_on_hold.set_pos(pos)
        self.shop.handle_mouse_move_event(pos)
    def __str__(self) -> str:
        pass
    def __repr__(self) -> str:
        pass

    def check_for_upgrade(self, tower: Tower) -> bool:
        if tower.level == 3: return
        fielded_match = [cow for cow in self.field if cow.name == tower.name and cow.level == tower.level]
        benched_match = [cow for cow in self.bench if cow and cow.name == tower.name and cow.level == tower.level]

        if len(fielded_match) >= 3:
            fielded_match[0].star_up()
            self.remove_from_field(fielded_match[1])
            self.remove_from_field(fielded_match[2])
            tile1 = map1.get_tile_by_pos(tuple(fielded_match[1].center_pos))
            tile2 = map1.get_tile_by_pos(tuple(fielded_match[2].center_pos))
            map1.make_tile_available(tile1)
            map1.make_tile_available(tile2)
            logger.info(f"Upgraded {tower.name} from three towers on the field!")
            self.check_for_upgrade(fielded_match[0])

            return True

        if len(fielded_match) == 2 and len(benched_match) >= 1:
            fielded_match[0].star_up()
            self.remove_from_field(fielded_match[1])
            tile2 = map1.get_tile_by_pos(tuple(fielded_match[1].center_pos))
            map1.make_tile_available(tile2)
            self.remove_from_bench(tower)
            logger.info(f"Upgraded {tower.name} on the field!")
            self.check_for_upgrade(fielded_match[0])
            return True

        if len(fielded_match) == 1 and len(benched_match) >= 2:
            fielded_match[0].star_up()
            self.remove_from_bench(benched_match[0])
            self.remove_from_bench(tower)
            logger.info(f"Upgraded {tower.name} using one from the bench!")
            self.check_for_upgrade(fielded_match[0])
            return True

        if len(benched_match) >= 3:
            benched_match[0].star_up()
            self.remove_from_bench(benched_match[1])
            self.remove_from_bench(tower)
            logger.info(f"Upgraded {tower.name} on the bench!")
            self.check_for_upgrade(benched_match[0])
            return True

        logger.info(f"No upgrades available for {tower.name}.")
        return False

    def render_health(self, screen: Surface) -> None:
        if not self.health_color:
            self.transition_color_health_bar()
        draw.polygon(screen, self.health_color, ((1619, 27), (1619 + 218*self.health/100, 27), (1647 + 218*self.health/100, 56), (1647, 56)))
        screen.blit(PLAYER_TEXT.render(str(self.health), True, (255,255,255)), (1800, 26))
        
    def render_gold(self, screen: Surface) -> None:
        screen.blit(PLAYER_TEXT.render(str(self.gold), True, (255,255,255)) , (1800, 57))

    def serialize(self, file: str) -> None:
        data = {
            'gold': self.gold,
            'health': self.health,
            'bench': [],
            'field': [],
            'shop_content': []
        }
        
        for tower in self.bench:
            if tower:
                data['bench'].append({
                    'name': tower.name,
                    'level': tower.level,
                    'current_fury': tower.current_fury,
                    'center_pos': tower.center_pos,
                    'dmg': tower.base_dmg,
                    'attack_speed': tower.base_attack_speed,
                    'range': tower.base_range,
                    'fury_gain': tower.base_fury_gain,
                    'max_fury': tower.max_fury,
                    'fury_lock': tower.fury_lock,
                    'target_type': tower.target_type.value
                })
            else:
                data['bench'].append(None)
        
        for tower in self.field:
            data['field'].append({
                'name': tower.name,
                'level': tower.level,
                'current_fury': tower.current_fury,
                'center_pos': tower.center_pos,
                'dmg': tower.base_dmg,
                'attack_speed': tower.base_attack_speed,
                'range': tower.base_range,
                'fury_gain': tower.base_fury_gain,
                'max_fury': tower.max_fury,
                'fury_lock': tower.fury_lock,
                'target_type': tower.target_type.value
            })
        
        for card in self.shop.content:
            data['shop_content'].append({
                'cow_name': card.cow_name,
                'rarity': card.rarity.value,
                'damage': card.damage,
                'attack_speed': card.attack_speed,
                'range': card.range,
                'starting_fury': card.starting_fury,
                'max_fury': card.max_fury,
                'fury_gain': card.fury_gain,
                'fury_lock': card.fury_lock,
                'target_type': card.target_type
            })
        
        with open(file, 'w') as f:
            json.dump(data, f, indent=2)

    def deserialize(self, file: str) -> None:
        with open(file, 'r') as f:
            data = json.load(f)
        
        self.gold = data['gold']
        self.health = data['health']
        
        self.bench = [None] * len(self.bench)
        self.field.empty()
        
        for i, tower_data in enumerate(data['bench']):
            if tower_data:
                tower = Tower(
                    name=tower_data['name'],
                    dmg=tower_data['dmg'],
                    attack_speed=tower_data['attack_speed'],
                    attack_range=tower_data['range'],
                    starting_fury=tower_data['current_fury'],
                    max_fury=tower_data['max_fury'],
                    fury_gain=tower_data['fury_gain'],
                    fury_lock=tower_data['fury_lock'],
                    target_type=tower_data['target_type'],
                    image_url=f'assets/towers/{tower_data["name"].lower().replace(" ", "_")}.png'
                )
                tower.level = tower_data['level']
                tower.center_pos = tower_data['center_pos']
                self.bench[i] = tower
        
        for tower_data in data['field']:
            tower = Tower(
                name=tower_data['name'],
                dmg=tower_data['dmg'],
                attack_speed=tower_data['attack_speed'],
                attack_range=tower_data['range'],
                starting_fury=tower_data['current_fury'],
                max_fury=tower_data['max_fury'],
                fury_gain=tower_data['fury_gain'],
                fury_lock=tower_data['fury_lock'],
                target_type=tower_data['target_type'],
                image_url=f'assets/towers/{tower_data["name"].lower().replace(" ", "_")}.png'
            )
            tower.level = tower_data['level']
            tower.center_pos = tower_data['center_pos']
            self.field.add(tower)
            
            from src.map import map1
            tile = map1.get_tile_by_pos(tuple(tower.center_pos))
            if tile:
                tile.available = False
        
        self.shop.content = []
        for card_data in data['shop_content']:
            card = Card(
                cow_name=card_data['cow_name'],
                rarity=Rarity(card_data['rarity']),
                damage=card_data['damage'],
                attack_speed=card_data['attack_speed'],
                attack_range=card_data['range'],
                starting_fury=card_data['starting_fury'],
                max_fury=card_data['max_fury'],
                fury_gain=card_data['fury_gain'],
                fury_lock=card_data['fury_lock'],
                target_type=card_data['target_type']
            )
            self.shop.content.append(card)
    
    def reset(self) -> None:
        self.bench = [None] * BENCH_SIZE
        self.field.empty()
        self.chances = [0, 0, 0, 0, 0]
        self.gold = 2
        self.health = 100
        self.shop = Shop()
        self.cow_on_hold = None
        self.cow_on_hold_pos = 0
        self.clicked_cow = None
        self.health_color = self.transition_color_health_bar()

player = Player()
PLAYER_TEXT = font.Font(FONT_URL, 28)
INFO_TEXT = font.Font(FONT_URL, 13)
ABILITY_TEXT = font.Font(FONT_URL, 18)