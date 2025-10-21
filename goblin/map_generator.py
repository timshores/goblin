"""
Procedural map generation for Goblin game
"""
import random
from typing import List, Tuple
from enum import Enum


class Tile(Enum):
    """Different types of terrain tiles"""
    EMPTY = ' '
    GRASS = '.'
    FOREST = 'T'
    MOUNTAIN = '^'
    WATER = '~'
    DESERT = ':'


class MapGenerator:
    """Generates procedural maps using various algorithms"""

    def __init__(self, width: int = 50, height: int = 25, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed if seed is not None else random.randint(0, 1000000)
        random.seed(self.seed)

    def generate(self) -> List[List[Tile]]:
        """
        Generate a procedural map using cellular automata
        Returns a 2D list of Tile objects
        """
        # Initialize with random tiles
        map_grid = [[self._random_tile() for _ in range(self.width)]
                    for _ in range(self.height)]

        # Apply cellular automata for smoother terrain
        for _ in range(3):
            map_grid = self._smooth_terrain(map_grid)

        return map_grid

    def _random_tile(self) -> Tile:
        """Generate a random tile with weighted probabilities"""
        weights = {
            Tile.GRASS: 40,
            Tile.FOREST: 20,
            Tile.MOUNTAIN: 15,
            Tile.WATER: 15,
            Tile.DESERT: 10,
        }
        tiles = list(weights.keys())
        probabilities = list(weights.values())
        return random.choices(tiles, probabilities)[0]

    def _smooth_terrain(self, map_grid: List[List[Tile]]) -> List[List[Tile]]:
        """Apply cellular automata to smooth terrain"""
        new_grid = [[Tile.GRASS for _ in range(self.width)]
                    for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                # Count neighbor tiles
                neighbor_counts = self._count_neighbors(map_grid, x, y)

                # Most common neighbor becomes the tile (with some randomness)
                if neighbor_counts and random.random() > 0.3:
                    most_common = max(neighbor_counts, key=neighbor_counts.get)
                    new_grid[y][x] = most_common
                else:
                    new_grid[y][x] = map_grid[y][x]

        return new_grid

    def _count_neighbors(self, map_grid: List[List[Tile]], x: int, y: int) -> dict:
        """Count the types of neighboring tiles"""
        counts = {}

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                nx, ny = x + dx, y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    tile = map_grid[ny][nx]
                    counts[tile] = counts.get(tile, 0) + 1

        return counts
