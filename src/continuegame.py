import os
import pygame
from typing import List, Tuple
from src.logger import Logger
from src.settings import FONT_URL
from src.game import Game

SAVES_FOLDER = "saves"
logger = Logger()
class ContinueGameMenu:
    @Logger.log_method()
    def __init__(self) -> None:
        display_info = pygame.display.Info()
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN | pygame.HWSURFACE)
        pygame.display.set_caption("Cow Defenders")

        self.running = True
        self.x, self.y = self.screen_width // 2, self.screen_height // 5
        self.font = pygame.font.Font(FONT_URL, 15)
        self.font_menu = pygame.font.Font(FONT_URL, 50)
        self.font_back_button = pygame.font.Font(FONT_URL, 35)
        self.menu_text = self.font_menu.render("Games", True, (255, 255, 255))
        
        self.games = self.load_games()
        self.back_button = pygame.Rect(50, self.screen_height - 100, 150, 60)
        self.delete_confirm = None
        
    def load_games(self) -> List[str]:
        games = []
        if not os.path.exists(SAVES_FOLDER):
            os.makedirs(SAVES_FOLDER)
        
        for file in os.listdir(SAVES_FOLDER):
            if file.endswith(".yaml") or file.endswith(".json") and not file.endswith(".json_player.json"):
                games.append(file)
        return games

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.render()

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.delete_confirm:
                    if self.delete_confirm["yes"].collidepoint(mouse_pos):
                        self.delete_game(self.delete_confirm["game"])
                        self.delete_confirm = None
                    elif self.delete_confirm["no"].collidepoint(mouse_pos):
                        self.delete_confirm = None
                    return
                
                if self.back_button.collidepoint(mouse_pos):
                    self.running = False
                    
                for i, game in enumerate(self.games):
                    delete_rect = pygame.Rect(100 + 150*i, self.y + 35, 100, 70)
                    start_rect = pygame.Rect(100 + 150*i, self.y + 110, 100, 30)
                    if delete_rect.collidepoint(mouse_pos):
                        self.delete_confirm = self.confirm_delete_popup(game, delete_rect)
                        return
                    if start_rect.collidepoint(mouse_pos):
                        self.start_game(game)
                        return

    def delete_game(self, game_name: str) -> None:
        file_path = os.path.join(SAVES_FOLDER, game_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        player_file_path = file_path + "_player.json"
        if os.path.exists(player_file_path):
            os.remove(player_file_path)
        self.games = self.load_games()

    def start_game(self, game_name: str) -> None:
        logger.info(f"Starting game: {game_name}")
        self.running = False
        game = Game(f'saves/{game_name}')
        game.run()

    def confirm_delete_popup(self, game_name: str, rect: pygame.Rect):
        return {
            "game": game_name,
            "rect": pygame.Rect(rect.x - 50, rect.y - 40, 300, 120),
            "yes": pygame.Rect(rect.x, rect.y + 50, 80, 40),
            "no": pygame.Rect(rect.x + 100, rect.y + 50, 80, 40)
        }

    def draw_button(self, button_rect: pygame.Rect, text: str, mouse_pos: Tuple[int, int], is_delete_button: bool = False) -> None:
        if button_rect == self.back_button:
            is_hovered = button_rect.collidepoint(mouse_pos)
            button_color = (255, 255, 255) if is_hovered else (68, 45, 39)
            text_color = (68, 45, 39) if is_hovered else (255, 255, 255)
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
            text_surface = self.font_back_button.render(text, True, text_color)
            text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
            text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
            self.screen.blit(text_surface, (text_x, text_y))
            return
        
        is_hovered = button_rect.collidepoint(mouse_pos)
        button_color = (255, 255, 255) if is_hovered else (68, 45, 39)
        text_color = (68, 45, 39) if is_hovered else (255, 255, 255)
        
        if is_delete_button:
            button_color = (200, 0, 0) if is_hovered else (150, 0, 0)
            text = "Delete" if is_hovered else text
            text_color = (255, 255, 255)
        
        pygame.draw.rect(self.screen, button_color, button_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), button_rect, 2)
        
        text_surface = self.font.render(text, True, text_color)
        text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
        text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

    def render(self) -> None:
        self.screen.fill((68, 45, 39))
        menu_text_x = self.x - self.menu_text.get_width() // 2
        self.screen.blit(self.menu_text, (menu_text_x, self.y - 100))
        
        mouse_pos = pygame.mouse.get_pos()
        self.draw_button(self.back_button, "Back", mouse_pos)
        
        for i, game in enumerate(self.games):
            game_name = os.path.splitext(game)[0].replace("_", " ")
            delete_rect = pygame.Rect(100 + 150*i, self.y + 35, 100, 70)
            start_rect = pygame.Rect(100 + 150*i, self.y + 110, 100, 30)
            self.draw_button(delete_rect, "", mouse_pos, True)
            if len(game_name) >= 8:
                game_name = game_name[:6] + "..."
            self.draw_button(start_rect, game_name, mouse_pos)

        if self.delete_confirm:
            popup = self.delete_confirm["rect"]
            pygame.draw.rect(self.screen, (68, 45, 39), popup)
            pygame.draw.rect(self.screen, (255, 255, 255), popup, 2)
            text_surface = self.font.render(f'Delete "{self.delete_confirm['game'].split('.')[0].replace("_", " ")}"?', True, (255, 255, 255))
            self.screen.blit(text_surface, (popup.x + 10, popup.y + 10))
            self.draw_button(self.delete_confirm["yes"], "Yes", mouse_pos)
            self.draw_button(self.delete_confirm["no"], "No", mouse_pos)

        pygame.display.flip()
