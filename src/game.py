import pygame
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE
from src.map import Tile, map1
from src.enemy import enemytest

class Game:
    def __init__(self):
        display_info = pygame.display.Info()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # self.screen_width = display_info.current_w
        # self.screen_height = display_info.current_h
        # self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

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
            if event.type == pygame.QUIT:
                self.running = False
        
    def update(self):
        enemytest.update()

    def render(self):
        self.screen.fill((0, 100, 0))
        map1.render_map(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        if(mouse_pos[0] <TILE_SIZE*20 and mouse_pos[1] < TILE_SIZE*15):
            map1.tiles[mouse_pos[0]//32][mouse_pos[1]//32].update(self.screen)
        enemytest.render(self.screen)
        pygame.display.flip()
