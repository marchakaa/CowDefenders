import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE
from src.map import Tile, map1
from src.ui import hud
from src.wave import Wave, wave_announcement
from src.enemy import enemies_on_map
from src.player import player

class Game:
    def __init__(self):
        display_info = pygame.display.Info()

        # self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen_width = display_info.current_w
        self.screen_height = display_info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN  | pygame.HWSURFACE)

        pygame.display.set_caption("Cow Defenders")
        self.running = True

        
        self.current_wave, enemies_info = Wave.create_wave(1)
        self.wave_number = 1
        wave_announcement.show_announcement(1, enemies_info)

        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000

            self.handle_events()

            self.update(delta_time)

            self.render()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    if not self.current_wave.is_active:
                        self.current_wave.start()
                        wave_announcement.show_announcement(self.wave_number, "Wave Starting!")
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #Leftclick
                    pass
                if event.button == 3:
                    #RightClick
                    pass
                hud.handle_click_events(event.pos)
                player.handle_click_event(event)
            if event.type == pygame.MOUSEMOTION:
                player.mouse_move_event(event.pos)
            if event.type == pygame.QUIT:
                self.running = False
        
    def update(self, delta_time):
        #Update enemies
        enemies_on_map.update(delta_time)
        #Update player
        player.update(delta_time)
        hud.update(delta_time)
        
        wave_announcement.update(delta_time)
        
        if self.current_wave.update(delta_time):
            self.wave_number += 1
            self.current_wave, enemies_info = Wave.create_wave(self.wave_number)
            self.current_wave.start()
            wave_announcement.show_announcement(self.wave_number, enemies_info)

    def render(self):
        self.screen.fill((0, 100, 0))
        hud.render(self.screen)
        map1.render_map(self.screen)
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
            
            #Create text to display FPS
        font = pygame.font.Font(None, 20)  #None uses default font, 36 is size
        fps_color = (255 - 255 * (fps/60), 255 * (fps/60), 0);
        fps_text = font.render(f'FPS: {fps}', True, fps_color)
            

        self.current_wave.render_debug(self.screen)
        self.current_wave.render(self.screen)
        wave_announcement.render(self.screen)

            #Draw the FPS in the corner of the screen
        self.screen.blit(fps_text, (1870, 0))
        pygame.display.flip()
        
