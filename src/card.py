from enum import Enum
import pygame
import yaml

class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5

class Card:
    def __init__(self, cow_name: str, rarity: Rarity, damage:float, attack_speed:float, traits=None, image_size=(100, 150)):
        self.cow_name = cow_name
        self.traits = traits
        self.damage = damage
        self.attack_speed = attack_speed
        self.rarity = rarity
        self.image_size = image_size

        self.image = pygame.image.load(f'{BASE_URL_CARDS}{self.cow_name.lower()}_card.png')
        self.image = pygame.transform.scale(self.image, self.image_size)

    def render(self, screen, pos):
        if self.image:
            rect = self.image.get_rect(topleft=pos)
            screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (*pos, *self.image_size))

    def __repr__(self):
        return f"Card(cow_name='{self.cow_name}', rarity={self.rarity.name})"

    def __str__(self):
        return f"{self.rarity.name} Card: {self.cow_name}"


def load_cards_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    cards = {}
    for name, attrs in data.items():
        cards[name] = Card(
            cow_name=name,
            rarity=Rarity[attrs['rarity']],
            damage=attrs['damage'],
            attack_speed=attrs['attack_speed']
        )
    return cards

BASE_URL_CARDS = "assets/cards/"
cards = load_cards_from_yaml("assets/towers.yaml")
print(cards)
