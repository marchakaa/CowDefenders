import pygame
from src.settings import FONT_URL, FPS
from src.logger import Logger
from typing import Optional, Tuple

logger = Logger()
pygame.init()

class Hud:
    def __init__(self, image_url: str) -> None:
        # Load and convert image for faster blitting
        self.image = pygame.image.load(image_url)
        self.font = pygame.font.Font(FONT_URL, 32)
        self.pause_button_rect = pygame.Rect(16, 16, 64, 64)
        self.time = 0
        self.pause_button_image = pygame.image.load("assets\\ui\\pause_button.png")
        
        # Pre-render static text
        self.bench_text = self.font.render('Bench', True, (0, 0, 0))
        
        # Pre-render static elements to a surface
        self.ui_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        self.ui_surface.blit(self.image, (0, 0))
        self.ui_surface.blit(self.bench_text, (70, 120))

    def update(self, delta_time: float) -> None:
        self.time += delta_time

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.ui_surface, (0, 0))
        screen.blit(self.pause_button_image, self.pause_button_rect)
        # MM:SS time
        total_seconds = int(self.time)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        time_text = f"{minutes:02}:{seconds:02}"
        
        # Render time text
        time_surface = self.font.render(time_text, True, (0, 0, 0))
        screen.blit(time_surface, (820, 40))

    def handle_mouse_move(self, mouse_move: Tuple[int, int]) -> None:
        if self.pause_button_rect.collidepoint(mouse_move):
            self.pause_button_image = pygame.image.load("assets/ui/pause_button_hover.png")
        else:
            self.pause_button_image = pygame.image.load("assets/ui/pause_button.png")

    def handle_click_events(self, mouse_pos: Tuple[int, int]) -> bool:
        if self.pause_button_rect.collidepoint(mouse_pos):
            logger.info("Pause Clicked")
            return True
        
    
    def set_time(self, time: float) -> None:
        self.time = time
        
    def reset_time(self) -> None:
        self.time = 0
        
    def get_time(self) -> float:
        return self.time

class PauseMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.background_color = (68, 45, 39)
        self.width, self.height = 600, 720
        self.x, self.y = (screen.get_width() - self.width) // 2, (screen.get_height() - self.height) // 2
        
        self.font = pygame.font.Font(FONT_URL, 36)
        
        self.menu_text = self.font.render("Menu", True, (255, 255, 255))
        self.resume_button = pygame.Rect(self.x + 150, self.y + 200, 300, 60)
        self.save_button = pygame.Rect(self.x + 150, self.y + 300, 300, 60)
        self.exit_button = pygame.Rect(self.x + 150, self.y + 400, 300, 60)
        
    def render(self, mouse_pos: Tuple[int, int]) -> None:
        
        pygame.draw.rect(self.screen, self.background_color, (self.x, self.y, self.width, self.height))
        self.screen.blit(self.menu_text, (self.x + (self.width - self.menu_text.get_width()) // 2, self.y + 50))
        
        self.draw_button(self.resume_button, "Resume(ESC)", mouse_pos)
        self.draw_button(self.exit_button, "Exit Game", mouse_pos)
        self.draw_button(self.save_button, "Save Game", mouse_pos)
        
    def draw_button(self, button_rect: pygame.Rect, text: str, mouse_pos: Tuple[int, int]) -> None:
        is_hovered = button_rect.collidepoint(mouse_pos)
        button_color = (255, 255, 255) if is_hovered else (68, 45, 39)
        text_color = (68, 45, 39) if is_hovered else (255, 255, 255)
        
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        text_surface = self.font.render(text, True, text_color)
        text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
        text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))
    
    def handle_click_events(self, mouse_pos: Tuple[int, int]) -> Optional[str]:
        
        if self.resume_button.collidepoint(mouse_pos):
            return "resume"
        elif self.exit_button.collidepoint(mouse_pos):
            return "exit"
        elif self.save_button.collidepoint(mouse_pos):
            return "save"
        return None


hud = Hud("assets\\ui\\ui.png")
