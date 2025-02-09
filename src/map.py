import pygame
from src.settings import TILE_SIZE
from src.logger import Logger
from typing import List, Tuple

class Tile:
    def __init__(self, startPos, available=True) -> None:
        self.available = available
        self.size = 64
        self.pos_top_left = startPos
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
    def update(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(self.surface, (255, 255, 255, 64), (0, 0, self.size, self.size))
        screen.blit(self.surface, self.pos_top_left)
    def __str__(self) -> str:
        return super().__str__()
    def __repr__(self) -> str:
        return super().__repr__()
    


class Map:
    def __init__(self, pattern, image: str) -> None:
        self.tiles = pattern
        self.map_image = pygame.image.load(image)
        self.map_points = []
    def render_map(self, screen: pygame.Surface):
        screen.blit(self.map_image, [MAP_START[0], MAP_START[1]])
    # def draw(screen):
    #     pass
    def get_tile_by_pos(self, pos:tuple) -> Tile:
        if pos[0] >= 225 and pos[0] <= 1697 and pos[1] >= 121 and pos[1] <= 761:
            col = int((pos[0] - 225) // 64)
            row = int((pos[1] - 121) // 64)
            return self.tiles[col][row]
    
    @Logger.log_method()
    def make_tile_unavailable(self, tile:Tile) -> None:
        tile.available = False
    @Logger.log_method()
    def make_tile_available(self, tile:Tile) -> None:
        tile.available = True

    @Logger.log_method()
    def make_tiles_unavailable(self, mappoints: List[Tuple[int, int]]) -> None:
        curr_row, curr_col = mappoints[0][1], mappoints[0][0]

        for i in range(1, len(mappoints)):
            next_col = curr_col + mappoints[i][0]
            next_row = curr_row + mappoints[i][1]

            if curr_row == next_row:
                step = 1 if curr_col < next_col else -1
                for col in range(curr_col, next_col + step, step):
                    if col > 22: break
                    self.tiles[col][curr_row].available = False
                    self.tiles[col][curr_row - 1].available = False

            elif curr_col == next_col:
                step = 1 if curr_row < next_row else -1
                for row in range(curr_row, next_row + step, step):
                    if row > 9: return
                    if row == next_row: self.tiles[curr_col - 1][row - 1].available = False
                    self.tiles[curr_col][row].available = False
                    self.tiles[curr_col - 1][row].available = False

            curr_col, curr_row = next_col, next_row



    def __str__(self) -> str:
        return super().__str__()
    def __repr__(self) -> str:
        return super().__repr__()
    def create_mapPoints(self, indices: List[Tuple[int, int]]) -> None:
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
map1Points = [(0, 8), (4, 0), (0, -4), (3, 0), (0, -2), (3, 0), (0, 6), (4, 0), (0, -3), (6, 0), (0, -3), (3, 0)]
map1.create_mapPoints(map1Points)
map1.make_tiles_unavailable(map1Points)