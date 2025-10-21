# Goblin

A procedurally generated ASCII text-based strategy game. Move your pieces around an abstract world with terrain, plan your strategy, and eventually engage in multiplayer cooperative and competitive gameplay.

## Features

- **Procedural Map Generation**: Each game generates a unique map using cellular automata
- **ASCII Graphics**: Classic text-based rendering with different terrain types
- **Strategic Gameplay**: Control different unit types with unique roles
- **Abstract Design**: Focus on strategic piece movement and positioning
- **Cross-Platform**: Works on Windows, Linux, and macOS

## Terrain Types

- `.` Grass - Common open terrain
- `T` Forest - Wooded areas
- `^` Mountain - Elevated terrain
- `~` Water - Rivers and lakes
- `:` Desert - Arid regions

## Unit Types

- `g` Goblin - Basic unit
- `W` Warrior - Combat unit
- `S` Settler - Expansion unit
- `s` Scout - Fast reconnaissance unit

## Controls

- **Arrow Keys**: Move cursor / Move selected unit (in move mode)
- **SPACE**: Select/deselect unit at cursor
- **m**: Toggle move mode for selected unit
- **q**: Quit game

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd goblin

# No dependencies needed - uses only Python standard library
# On Linux/macOS:
python3 main.py

# On Windows:
python main.py
```

## Usage

```bash
# Start with default settings (50x25 map)
python3 main.py  # Linux/macOS
python main.py   # Windows

# Custom map size
python3 main.py --width 80 --height 40

# Use a specific seed for reproducible maps
python3 main.py --seed 12345
```

**Note for Windows users**: Use `python` instead of `python3` in all commands.

## Gameplay

1. Use arrow keys to move the cursor around the map
2. Press SPACE when the cursor is over a unit to select it
3. Press 'm' to enter move mode
4. Use arrow keys to move the selected unit
5. Press 'm' again to exit move mode
6. Explore the procedurally generated terrain!

## Future Enhancements

- Multiplayer support (networked gameplay)
- Diplomacy system for cooperative play
- Resource management
- Combat system
- More unit types and abilities
- Fog of war
- Larger maps with scrolling camera
- Save/load game state

## Development

The project structure:

```
goblin/
├── goblin/
│   ├── __init__.py
│   ├── map_generator.py    # Procedural map generation
│   ├── renderer.py          # ASCII rendering
│   ├── entities.py          # Game pieces and players
│   └── game.py              # Main game logic
├── main.py                  # Entry point
└── README.md
```

## License

See LICENSE file for details.
