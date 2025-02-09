from src.logger import Logger
logger = Logger()

import pygame
from src.settings import FONT_URL
from typing import Tuple

class MainMenu:
    @Logger.log_method()
    def __init__(self) -> None:
        display_info = pygame.display.Info()

        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN | pygame.HWSURFACE)

        pygame.display.set_caption("Cow Defenders")
        self.exit_status = None

        self.running = True
        
        self.x, self.y = self.screen_width // 2, self.screen_height // 3
        
        self.font = pygame.font.Font(FONT_URL, 36)
        self.font_menu = pygame.font.Font(FONT_URL, 50)
        
        self.menu_text = self.font_menu.render("Menu", True, (255, 255, 255))
        
        button_width, button_height = 300, 60
        self.start_button = pygame.Rect(self.x - button_width // 2, self.y, button_width, button_height)
        self.continue_button = pygame.Rect(self.x - button_width // 2, self.y + 100, button_width, button_height)
        self.exit_button = pygame.Rect(self.x - button_width // 2, self.y + 200, button_width, button_height)
        
    def run(self) -> str:
        while self.running:
            self.handle_events()
            self.render()
        return self.exit_status

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    logger.info("Game Stopped")
                    self.running = False
                    self.exit_status = "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.collidepoint(mouse_pos):
                        self.running = False
                        self.exit_status = "start"
                    elif self.continue_button.collidepoint(mouse_pos):
                        self.running = False
                        self.exit_status = "continue"
                    elif self.exit_button.collidepoint(mouse_pos):
                        self.running = False
                        self.exit_status = "exit"
        return None
        

    def render(self) -> None:
        self.screen.fill((68, 45, 39))

        menu_text_x = self.x - self.menu_text.get_width() // 2
        self.screen.blit(self.menu_text, (menu_text_x, self.y - 100))
        
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(self.start_button, "Start Game", mouse_pos)
        self.draw_button(self.continue_button, "Continue Game", mouse_pos)
        self.draw_button(self.exit_button, "Exit Game", mouse_pos)

        pygame.display.flip()
        
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

