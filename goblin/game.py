"""
Main game logic and state management for Goblin
"""
import sys
import os
import platform
from typing import List, Optional
from goblin.map_generator import MapGenerator, Tile
from goblin.renderer import Renderer
from goblin.entities import Entity, EntityType, Player

# Platform-specific imports for keyboard input
if platform.system() == 'Windows':
    import msvcrt
else:
    import tty
    import termios


class GameState:
    """Manages the overall game state"""

    def __init__(self, width: int = 50, height: int = 25, seed: int = None):
        self.width = width
        self.height = height
        self.seed = seed

        # Generate the map
        generator = MapGenerator(width, height, seed)
        self.map = generator.generate()

        # Initialize renderer
        self.renderer = Renderer(width, height)

        # Game entities
        self.players = []
        self.entities = []
        self.current_player_idx = 0

        # Cursor position
        self.cursor_x = width // 2
        self.cursor_y = height // 2

        # Selected entity
        self.selected_entity: Optional[Entity] = None

        # Game mode
        self.mode = "normal"  # normal, move

    def initialize_game(self):
        """Set up initial game state with players and entities"""
        # Create player
        player1 = Player(0, "Player 1", "blue")
        self.players.append(player1)

        # Spawn initial entities
        self._spawn_initial_entities(player1)

    def _spawn_initial_entities(self, player: Player):
        """Spawn initial entities for a player"""
        # Find a good spawn location (grass tile)
        spawn_x, spawn_y = self._find_spawn_location()

        # Create starting units
        goblin1 = Entity(EntityType.GOBLIN, spawn_x, spawn_y, player.id)
        goblin2 = Entity(EntityType.GOBLIN, spawn_x + 1, spawn_y, player.id)
        warrior = Entity(EntityType.WARRIOR, spawn_x, spawn_y + 1, player.id)

        self.entities.extend([goblin1, goblin2, warrior])
        player.add_entity(goblin1)
        player.add_entity(goblin2)
        player.add_entity(warrior)

    def _find_spawn_location(self) -> tuple:
        """Find a suitable spawn location on grass"""
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == Tile.GRASS:
                    return (x, y)
        # Fallback to center
        return (self.width // 2, self.height // 2)

    def move_cursor(self, dx: int, dy: int):
        """Move the cursor"""
        self.cursor_x = max(0, min(self.width - 1, self.cursor_x + dx))
        self.cursor_y = max(0, min(self.height - 1, self.cursor_y + dy))

    def select_entity_at_cursor(self):
        """Select an entity at the cursor position"""
        for entity in self.entities:
            if entity.x == self.cursor_x and entity.y == self.cursor_y:
                if self.selected_entity:
                    self.selected_entity.selected = False
                self.selected_entity = entity
                entity.selected = True
                return

        # Deselect if nothing at cursor
        if self.selected_entity:
            self.selected_entity.selected = False
            self.selected_entity = None

    def move_selected_entity(self, dx: int, dy: int):
        """Move the selected entity"""
        if self.selected_entity:
            new_x = max(0, min(self.width - 1, self.selected_entity.x + dx))
            new_y = max(0, min(self.height - 1, self.selected_entity.y + dy))

            # Check if position is occupied
            if not self._is_position_occupied(new_x, new_y):
                self.selected_entity.move_to(new_x, new_y)

    def _is_position_occupied(self, x: int, y: int) -> bool:
        """Check if a position is occupied by an entity"""
        for entity in self.entities:
            if entity.x == x and entity.y == y:
                return True
        return False

    def render(self) -> str:
        """Render the current game state"""
        return self.renderer.render(self.map, self.entities, self.selected_entity)


class Game:
    """Main game controller"""

    def __init__(self, width: int = 50, height: int = 25, seed: int = None):
        self.state = GameState(width, height, seed)
        self.running = False

    def start(self):
        """Start the game"""
        self.state.initialize_game()
        self.running = True
        self.game_loop()

    def game_loop(self):
        """Main game loop"""
        while self.running:
            # Clear screen and render
            self._clear_screen()
            print(self.state.render())

            # Get input
            key = self._get_key()
            self._handle_input(key)

    def _clear_screen(self):
        """Clear the terminal screen (cross-platform)"""
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def _get_key(self) -> str:
        """Get a single keypress from the user (cross-platform)"""
        if platform.system() == 'Windows':
            # Windows implementation using msvcrt
            ch = msvcrt.getch()

            # Handle special keys (arrow keys return 2 bytes on Windows)
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                if ch2 == b'H':
                    return 'UP'
                elif ch2 == b'P':
                    return 'DOWN'
                elif ch2 == b'M':
                    return 'RIGHT'
                elif ch2 == b'K':
                    return 'LEFT'

            # Decode regular keys
            try:
                return ch.decode('utf-8')
            except:
                return ''
        else:
            # Unix implementation using termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)

                # Handle arrow keys (escape sequences)
                if ch == '\x1b':
                    ch = sys.stdin.read(2)
                    if ch == '[A':
                        return 'UP'
                    elif ch == '[B':
                        return 'DOWN'
                    elif ch == '[C':
                        return 'RIGHT'
                    elif ch == '[D':
                        return 'LEFT'

                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _handle_input(self, key: str):
        """Handle user input"""
        if key == 'q':
            self.running = False
            print("\nThanks for playing Goblin!")

        elif key == 'UP':
            if self.state.mode == "move" and self.state.selected_entity:
                self.state.move_selected_entity(0, -1)
            else:
                self.state.move_cursor(0, -1)

        elif key == 'DOWN':
            if self.state.mode == "move" and self.state.selected_entity:
                self.state.move_selected_entity(0, 1)
            else:
                self.state.move_cursor(0, 1)

        elif key == 'LEFT':
            if self.state.mode == "move" and self.state.selected_entity:
                self.state.move_selected_entity(-1, 0)
            else:
                self.state.move_cursor(-1, 0)

        elif key == 'RIGHT':
            if self.state.mode == "move" and self.state.selected_entity:
                self.state.move_selected_entity(1, 0)
            else:
                self.state.move_cursor(1, 0)

        elif key == ' ':
            self.state.select_entity_at_cursor()

        elif key == 'm':
            if self.state.selected_entity:
                if self.state.mode == "move":
                    self.state.mode = "normal"
                else:
                    self.state.mode = "move"
