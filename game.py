"""
Main Game Loop and State Management
"""

import pygame
from game_states import CharacterSelectionState, Level1State


class Game:
    """Main game controller"""
    
    def __init__(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Princess Game")
        
        # Game states
        self.current_state = CharacterSelectionState(self)
        self.running = True
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Pass events to current state
            self.current_state.handle_event(event)
    
    def update(self):
        """Update game logic"""
        self.current_state.update()
    
    def draw(self):
        """Render the game"""
        self.screen.fill((0, 0, 0))  # Black background
        self.current_state.draw(self.screen)
        pygame.display.flip()
    
    def change_state(self, new_state):
        """Change to a new game state"""
        self.current_state = new_state
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
