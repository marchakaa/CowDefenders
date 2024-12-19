import pygame
from src.settings import TILE_SIZE


class Tile:
    def __init__(self, startPos, empty=True, available=True):
        self.empty = empty
        self.available = available
        self.size = 64
        self.pos_top_left = startPos
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
    def update(self, screen):
        pygame.draw.rect(self.surface, (255, 255, 255, 64), (0, 0, self.size, self.size))
        screen.blit(self.surface, self.pos_top_left)
    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()
    


class Map:
    def __init__(self, pattern, image):
        self.tiles = pattern
        self.map_image = pygame.image.load(image)
        self.map_points = []
    def render_map(self, screen):
        screen.blit(self.map_image, [MAP_START[0], MAP_START[1]])
    def draw(screen):
        pass
    
    def __str__(self):
        return super().__str__()
    def __repr__(self):
        return super().__repr__()
    def create_mapPoints(self, indices):
        last_point = (MAP_START[0], MAP_START[1])
        self.map_points.extend(
        [(last_point := (last_point[0] + x * TILE_SIZE, last_point[1] + y * TILE_SIZE))
            for (x, y) in indices]
    )
        
MAP_START = (225, 121)
tiles = []
for i in range(23):
    row = []
    for j in range(10):
        coords = (225 + i*64, 121 + j*64)
        row.append(Tile(coords))
    tiles.append(row)

map1 = Map(tiles, "assets\maps\map1.png")
map1Points = ((0, 8), (4, 0), (0, -4), (3, 0), (0, -2), (3, 0), (0, 6), (4, 0), (0, -3), (6, 0), (0, -3), (3, 0))
map1.create_mapPoints(map1Points)