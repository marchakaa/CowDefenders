import pygame
class Tile:
    def __init__(self, startPos, empty=True, available=True):
        self.empty = empty
        self.available = available
        self.size = 32
        self.posTopLeft = startPos
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
    def update(self, screen):
        pygame.draw.rect(self.surface, (255, 255, 255, 64), (0, 0, self.size, self.size))
        screen.blit(self.surface, self.posTopLeft)
class Map:
    def __init__(self, pattern, image):
        self.tiles = pattern
        self.map_image = pygame.image.load(image)
    def render_map(self, screen):
        screen.blit(self.map_image, [0, 0])
    def draw(screen):
        pass
tiles = []
for i in range(20):
    row = []
    for j in range(15):
        coords = (i*32, j*32)
        row.append(Tile(coords))
    tiles.append(row)
map1 = Map(tiles, "assets\maps\map1.png")

mapPoints = ((0, 13*32), (5*32, 13*32), (5*32, 5*32), (9*32, 5*32), (9*32, 11*32),
             (13*32, 11*32), (13*32, 4*32), (20*32, 4*32))