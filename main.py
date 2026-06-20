"""
Princess Game - Main Entry Point
A 2D top-down adventure game where you rescue a princess
"""

import pygame
import sys
from game import Game


def main():
    """Initialize and run the game"""
    pygame.init()
    
    # Game configuration
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60
    
    # Create game instance
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, FPS)
    
    # Run the game
    game.run()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
