import pygame
from src.settings import FONT_URL, FPS

pygame.init()

class Hud:
    def __init__(self, image_url):
        # Load and convert image for faster blitting
        self.image = pygame.image.load(image_url)
        self.font = pygame.font.Font(FONT_URL, 32)
        self.pause_button_rect = pygame.Rect(16, 16, 32, 32)
        self.time = 0
        
        # Pre-render static text
        self.bench_text = self.font.render('Bench', True, (0, 0, 0))
        
        # Pre-render static elements to a surface
        self.ui_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.ui_surface.blit(self.image, (0, 0))
        pygame.draw.rect(self.ui_surface, (200, 0, 0), self.pause_button_rect)
        self.ui_surface.blit(self.bench_text, (70, 120))

    def update(self, delta_time):
        self.time += delta_time

    def render(self, screen):
        screen.blit(self.ui_surface, (0, 0))

        # Format elapsed time as MM:SS
        total_seconds = int(self.time)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_text = f"{minutes:02}:{seconds:02}"
        
        # Render time text
        time_surface = self.font.render(time_text, True, (0, 0, 0))
        screen.blit(time_surface, (820, 40))

    def handle_click_events(self, mouse_pos):
        if self.pause_button_rect.collidepoint(mouse_pos):
            print("Pause Clicked")

hud = Hud("assets\\maps\\ui.png")
