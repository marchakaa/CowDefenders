from enum import Enum
import pygame
import yaml
import os
from src.settings import RARITY_COLORS, FONT_URL
from copy import deepcopy

class Rarity(Enum):
    EMPTY = 0
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5

class Card:
    # Class-level font cache
    _font = None
    
    def __init__(self, cow_name: str, rarity: Rarity, damage: float, attack_speed: float, traits=None, image_size=(222, 150)):
        self.cow_name = cow_name
        self.traits = traits
        self.damage = damage
        self.attack_speed = attack_speed
        self.rarity = rarity
        self.image_size = image_size
        self.button_rect = None
        self.is_hovered = False

        # Initialize the class font if not already done
        if Card._font is None:
            Card._font = pygame.font.Font(FONT_URL, 24)

        self.image_path = f'{BASE_URL_CARDS}{self.cow_name.lower().replace(" ", "_")}_card.png'
        if os.path.exists(self.image_path):
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, self.image_size)
            # Pre-create hover image
            self.hover_image = self.image.copy()
            hover_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            hover_surface.fill((255, 255, 255, 30))
            self.hover_image.blit(hover_surface, (0, 0))
        else:
            self.image = None
            self.hover_image = None

        # Pre-render text
        self.text_surface = Card._font.render(self.cow_name, True, (255, 255, 255))

    def render(self, screen, pos):
        self.button_rect = pygame.Rect(pos[0], pos[1], self.image_size[0], self.image_size[1] + 61 + 2)
        
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.button_rect.collidepoint(mouse_pos) and not self.cow_name == "Empty"
        
        if self.image:
            rect = self.image.get_rect(topleft=pos)
            if self.is_hovered:
                screen.blit(self.hover_image, rect)
            else:
                screen.blit(self.image, rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), (*pos, *self.image_size))

        rarity_rect = pygame.Rect(pos[0], pos[1] + 152, 222, 61)
        rarity_color = RARITY_COLORS[self.rarity.value]
        if self.is_hovered:
            rarity_color = tuple(min(c + 30, 255) for c in rarity_color)
        
        pygame.draw.rect(screen, rarity_color, rarity_rect)

        text_rect = self.text_surface.get_rect(center=rarity_rect.center)
        screen.blit(self.text_surface, text_rect)
        
    def is_clicked(self, mouse_pos):
        return self.button_rect and self.button_rect.collidepoint(mouse_pos)
    
    def __repr__(self):
        return f"Card(cow_name='{self.cow_name}', rarity={self.rarity.name}, traits={self.traits})"

    def __str__(self):
        return f"{self.rarity.name} Card: {self.cow_name}"

    def clone(self):
        new_card = Card(
            cow_name=self.cow_name,
            rarity=self.rarity,
            damage=self.damage,
            attack_speed=self.attack_speed,
            traits=deepcopy(self.traits) if self.traits is not None else None,
            image_size=self.image_size
        )
        return new_card
    

def load_cards_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    cards = {}
    for name, attrs in data.items():
        cards[name] = Card(
            cow_name= name,
            rarity= Rarity[attrs['rarity']],
            damage= attrs['damage'],
            attack_speed= attrs['attack_speed'],
            traits= attrs.get('traits', [])
        )
    return cards



BASE_URL_CARDS = "assets/cards/"
cards = load_cards_from_yaml("assets/towers.yaml")
