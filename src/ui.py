import pygame
from src.settings import FONT_URL, FPS

pygame.init()

class Hud:
    def __init__(self, image_url):
        self.image = pygame.image.load(image_url)
        self.money_text = 50
        self.font = pygame.font.Font(FONT_URL, 32)
        self.pause_button_rect = pygame.Rect(16, 16, 32, 32)
        self.cards = []

    def update(self):
        self.money_text += 1

    def render(self, screen):
        screen.blit(self.image, [0, 0])
    
        pygame.draw.rect(screen, (200, 0, 0), self.pause_button_rect)    
        money_surface = self.font.render(str(self.money_text//FPS), True, (0, 0, 0))
        bench_text = self.font.render('Bench', True, (0,0,0))
        screen.blit(bench_text, (70, 120))
        screen.blit(money_surface, (30, 30))

    def handle_click_events(self, mouse_pos):
        if self.pause_button_rect.collidepoint(mouse_pos):
            print("Pause Clicked")
        else:
            print(mouse_pos)

hud = Hud("assets\\maps\\ui.png")