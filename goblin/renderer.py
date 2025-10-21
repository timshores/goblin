"""
ASCII rendering system for Goblin
"""
from typing import List
from goblin.map_generator import Tile
from goblin.entities import Entity


class Renderer:
    """Handles rendering the game state to ASCII"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.camera_x = 0
        self.camera_y = 0

    def render(self, map_grid: List[List[Tile]], entities: List[Entity],
               selected_entity: Entity = None) -> str:
        """
        Render the game state to an ASCII string
        """
        # Create a copy of the map for rendering
        render_buffer = [[tile.value for tile in row] for row in map_grid]

        # Draw entities on top of the map
        for entity in entities:
            if 0 <= entity.y < len(render_buffer) and 0 <= entity.x < len(render_buffer[0]):
                symbol = entity.get_symbol()
                if entity.selected:
                    symbol = symbol.upper()  # Highlight selected entities
                render_buffer[entity.y][entity.x] = symbol

        # Convert to string
        output = []
        output.append("=" * (self.width + 2))
        output.append(" GOBLIN - Procedural Strategy Game")
        output.append("=" * (self.width + 2))

        for row in render_buffer:
            output.append("|" + "".join(row) + "|")

        output.append("=" * (self.width + 2))

        # Add legend
        output.append("\nTerrain: . grass | T forest | ^ mountain | ~ water | : desert")
        output.append("Units: g goblin | W warrior | S settler | s scout")
        output.append("\nControls: arrow keys to move cursor | SPACE to select | m to move | q to quit")

        if selected_entity:
            output.append(f"\nSelected: {selected_entity.type.name} at ({selected_entity.x}, {selected_entity.y})")

        return "\n".join(output)

    def render_simple(self, map_grid: List[List[Tile]]) -> str:
        """Simple rendering without entities (for testing)"""
        output = []
        for row in map_grid:
            output.append("".join(tile.value for tile in row))
        return "\n".join(output)
