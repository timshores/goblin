"""
Game entities and pieces for Goblin
"""
from typing import Tuple
from enum import Enum


class EntityType(Enum):
    """Types of game entities"""
    GOBLIN = 'g'
    WARRIOR = 'W'
    SETTLER = 'S'
    SCOUT = 's'


class Entity:
    """Represents a game piece that can move on the map"""

    def __init__(self, entity_type: EntityType, x: int, y: int, player_id: int = 0):
        self.type = entity_type
        self.x = x
        self.y = y
        self.player_id = player_id
        self.selected = False

    def move(self, dx: int, dy: int):
        """Move the entity by a delta amount"""
        self.x += dx
        self.y += dy

    def move_to(self, x: int, y: int):
        """Move the entity to absolute coordinates"""
        self.x = x
        self.y = y

    def get_position(self) -> Tuple[int, int]:
        """Get the current position of the entity"""
        return (self.x, self.y)

    def get_symbol(self) -> str:
        """Get the ASCII symbol for rendering"""
        return self.type.value


class Player:
    """Represents a player in the game"""

    def __init__(self, player_id: int, name: str, color: str = 'white'):
        self.id = player_id
        self.name = name
        self.color = color
        self.entities = []

    def add_entity(self, entity: Entity):
        """Add an entity to the player's control"""
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        """Remove an entity from the player's control"""
        if entity in self.entities:
            self.entities.remove(entity)
