import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE
from src.map import Tile, map1
from src.ui import hud
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


        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            self.handle_events()

            self.update()

            self.render()

            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
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
        
    def update(self):
        #Update enemies
        enemies_on_map.update()
        #Update player
        player.update()
        hud.update()

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
            enemy.render(self.screen)

        
        fps = int(self.clock.get_fps())
            
            # Create text to display FPS
        font = pygame.font.Font(None, 36)  # None uses default font, 36 is size
        fps_text = font.render(f'FPS: {fps}', True, (0,0,0))  # White color
            
            # Draw the FPS in the corner of the screen
        self.screen.blit(fps_text, (10, 10))
        pygame.display.flip()
        
