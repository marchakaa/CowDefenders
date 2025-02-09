from src.logger import Logger
logger = Logger()

import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE, FONT_URL
from src.map import Tile, map1
from src.ui import hud, PauseMenu
from src.wave import Wave, wave_announcement
from src.enemy import enemies_on_map
from src.player import player
import json
import os

class Game:
    @Logger.log_method()
    def __init__(self, game_file: str="") -> None:
        display_info = pygame.display.Info()

        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN  | pygame.HWSURFACE)
        self.pause_menu = PauseMenu(self.screen)

        pygame.display.set_caption("Cow Defenders")

        self.running = True
        
        self.current_wave, enemies_info = Wave.create_wave(1)
        self.wave_number = 1
        wave_announcement.show_announcement(1, enemies_info)

        self.clock = pygame.time.Clock()
        self.paused = False

        enemies_on_map.empty()
        if game_file:
            self.load_game(game_file)
            logger.info(f"Loaded game from {game_file}")
            player.shop.update_chances(self.wave_number)
            print(player.shop.chances)
        else:
            self.current_wave, enemies_info = Wave.create_wave(1)
            self.wave_number = 1
            wave_announcement.show_announcement(1, enemies_info)
            hud.reset_time()
            player.reset()

        self.show_save_dialog = False
        self.save_dialog_surface = pygame.Surface((400, 200))
        self.save_dialog_surface.fill((255, 255, 255))
        self.save_dialog_rect = self.save_dialog_surface.get_rect(center=(self.screen_width//2, self.screen_height//2))
        
        self.dialog_font = pygame.font.Font(FONT_URL, 24)
        
        self.save_filename = ""
        self.input_active = False
    def run(self) -> None:
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000

            self.handle_events()

            if not self.paused:
                self.update(delta_time)

            self.render()


    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if self.show_save_dialog:
                    if event.key == pygame.K_RETURN:
                        self.save_game_with_name()
                    elif event.key == pygame.K_BACKSPACE:
                        self.save_filename = self.save_filename[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.show_save_dialog = False
                    else:
                        self.save_filename += event.unicode
                else:
                    if event.key == pygame.K_ESCAPE: # Press ESCAPE to quit game
                        self.paused = not self.paused
                        if self.paused:
                            logger.info("Game Paused")
                        else:
                            logger.info("Game Unpaused")
                    if event.key == pygame.K_SPACE and not self.paused: # Press SPACE to start the wave
                        if not self.current_wave.is_active:
                            self.current_wave.start()
                            wave_announcement.show_announcement(self.wave_number, "Wave Starting!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_save_dialog:
                    dialog_mouse_pos = (
                        event.pos[0] - self.save_dialog_rect.x,
                        event.pos[1] - self.save_dialog_rect.y
                    )
                    
                    if self.save_button_rect.collidepoint(dialog_mouse_pos):
                        self.save_game_with_name()
                    elif self.close_button_rect.collidepoint(dialog_mouse_pos):
                        self.show_save_dialog = False
                else:
                    if event.button == 1:
                        #Pause menu handling
                        if self.paused:
                            result = self.pause_menu.handle_click_events(event.pos)
                            match result:
                                case "resume": self.paused = not self.paused
                                case "exit": self.running = False
                                case "save": 
                                    self.show_save_dialog = True
                                    self.save_filename = ""
                            logger.info(f"Clicked: '{result}' button in the menu")
                    if event.button == 3:
                        #RightClick
                        pass
                    if hud.handle_click_events(event.pos) and not self.paused:
                        self.paused = not self.paused
                        logger.info("Game Paused")

                    player.handle_click_event(event)
            if event.type == pygame.MOUSEMOTION:
                player.mouse_move_event(event.pos)
                hud.handle_mouse_move(event.pos)
            if event.type == pygame.QUIT:
                self.running = False
        
    def update(self, delta_time: float) -> None:
        if player.health == 0:
            self.running = False
        #Update enemies
        enemies_on_map.update(delta_time)
        #Update player
        player.update(delta_time)
        hud.update(delta_time)
        #Announce wave
        wave_announcement.update(delta_time)
        #Update wave
        if self.current_wave.update(delta_time):
            self.wave_number += 1
            self.current_wave, enemies_info = Wave.create_wave(self.wave_number)
            self.current_wave.start()
            wave_announcement.show_announcement(self.wave_number, enemies_info)

    def render(self) -> None:
        self.screen.fill((0, 100, 0))
        hud.render(self.screen)
        map1.render_map(self.screen)
        if not self.paused: # If the game is paused don't light the tiles
            mouse_pos = pygame.mouse.get_pos()
            x_index = (mouse_pos[0] - 225) // TILE_SIZE
            y_index = (mouse_pos[1] - 121) // TILE_SIZE
            if 0 <= x_index < len(map1.tiles) and 0 <= y_index < len(map1.tiles[0]):
                map1.tiles[x_index][y_index].update(self.screen)

        #Render player
        player.render(self.screen)
        #Render enemies
        for enemy in enemies_on_map:
            enemy.set_player(player)
            enemy.render(self.screen)

        
        fps = int(self.clock.get_fps())
            
            # Create text to display FPS
        font = pygame.font.Font(None, 20)
        fps_color = (255 - 255 * (fps/63), 255 * (fps/63), 0);
        fps_text = font.render(f'FPS: {fps}', True, fps_color)
            

        # self.current_wave.render_debug(self.screen)
        self.current_wave.render(self.screen)
        wave_announcement.render(self.screen)

        # Draw the FPS in the corner of the screen
        self.screen.blit(fps_text, (1870, 0))

        # Draw pause menu overlay if paused
        if self.paused:
            pause_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            pause_surface.fill((0, 0, 0, 128))
            self.screen.blit(pause_surface, (0, 0))
            
            mouse_pos = pygame.mouse.get_pos()
            self.pause_menu.render(mouse_pos)

        if self.show_save_dialog:
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))
            
            self.save_dialog_surface.fill((68, 45, 39))
            
            title_text = self.dialog_font.render("Save Game", True, (255, 255, 255))
            self.save_dialog_surface.blit(title_text, (20, 20))
            
            pygame.draw.rect(self.save_dialog_surface, (200, 200, 200), (20, 60, 360, 40))
            input_text = self.dialog_font.render(self.save_filename, True, (0, 0, 0))
            self.save_dialog_surface.blit(input_text, (25, 70))
            
            self.save_button_rect = pygame.Rect(220, 140, 80, 40)
            self.close_button_rect = pygame.Rect(310, 140, 80, 40)
            
            pygame.draw.rect(self.save_dialog_surface, (0, 200, 100), self.save_button_rect)
            pygame.draw.rect(self.save_dialog_surface, (128, 128, 128), self.close_button_rect)
            
            save_text = self.dialog_font.render("Save", True, (255, 255, 255))
            close_text = self.dialog_font.render("Close", True, (255, 255, 255))
            
            self.save_dialog_surface.blit(save_text, (235, 150))
            self.save_dialog_surface.blit(close_text, (320, 150))
            
            if hasattr(self, 'error_message'):
                error_text = self.dialog_font.render(self.error_message, True, (255, 0, 0))
                self.save_dialog_surface.blit(error_text, (20, 110))
            
            self.screen.blit(self.save_dialog_surface, self.save_dialog_rect)

        pygame.display.flip()
        
    def save_game(self, filename: str) -> None:
        data = {
            'wave_number': self.wave_number,
            'player_file': f"{filename}_player.json",
            'game_time': hud.get_time()
        }
        
        os.makedirs("saves", exist_ok=True)
        player.serialize(data['player_file'])
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Game saved to {filename}")

    def save_game_with_name(self) -> None:
        if not self.save_filename:
            return
            
        filename = f"saves/{self.save_filename}"
        if not filename.endswith('.json'):
            filename += '.json'
            
        if os.path.exists(filename):
            self.error_message = "File already exists!"
            return
            
        self.save_game(filename)
        self.show_save_dialog = False
        self.running = False

    def load_game(self, filename: str) -> None:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        player.deserialize(data['player_file'])
        
        self.wave_number = data['wave_number']
        self.current_wave, enemies_info = Wave.create_wave(self.wave_number)
        wave_announcement.show_announcement(self.wave_number, enemies_info)
        
        if 'game_time' in data:
            hud.set_time(data['game_time'])
        else:
            hud.reset_time()

        logger.info(f"Game loaded from {filename}")