#!/usr/bin/env python3
"""
Main entry point for Goblin game
"""
import sys
import argparse
from goblin.game import Game


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Goblin - Procedural ASCII Strategy Game')
    parser.add_argument('--width', type=int, default=50, help='Map width (default: 50)')
    parser.add_argument('--height', type=int, default=25, help='Map height (default: 25)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for map generation')

    args = parser.parse_args()

    print("Starting Goblin...")
    print(f"Map size: {args.width}x{args.height}")
    if args.seed:
        print(f"Seed: {args.seed}")
    print("\nPress any key to begin...")
    input()

    game = Game(width=args.width, height=args.height, seed=args.seed)
    game.start()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
