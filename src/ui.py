import pygame
from src.settings import FONT_URL, FPS

pygame.init()

class Hud:
    def __init__(self, image_url):
        # Load and convert image for faster blitting
        self.image = pygame.image.load(image_url)
        self.money_text = 50
        self.font = pygame.font.Font(FONT_URL, 32)
        self.pause_button_rect = pygame.Rect(16, 16, 32, 32)
        self.cards = []
        
        # Pre-render static text
        self.bench_text = self.font.render('Bench', True, (0, 0, 0))
        self.cached_money_text = {}  # Cache for money text surfaces
        
        # Pre-render static elements to a surface
        self.ui_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.ui_surface.blit(self.image, (0, 0))
        pygame.draw.rect(self.ui_surface, (200, 0, 0), self.pause_button_rect)
        self.ui_surface.blit(self.bench_text, (70, 120))

    def update(self):
        self.money_text += 1

    def render(self, screen):
        # Blit pre-rendered UI surface
        screen.blit(self.ui_surface, (0, 0))
        
        # Cache and render money text
        money_value = str(self.money_text // FPS)
        if money_value not in self.cached_money_text:
            self.cached_money_text[money_value] = self.font.render(money_value, True, (0, 0, 0))
        screen.blit(self.cached_money_text[money_value], (30, 30))

    def handle_click_events(self, mouse_pos):
        if self.pause_button_rect.collidepoint(mouse_pos):
            print("Pause Clicked")

hud = Hud("assets\\maps\\ui.png")
