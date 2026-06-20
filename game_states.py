"""
Game States - Character Selection and Levels
"""

import pygame
from player import Knight
from level1 import Level1


class GameState:
    """Base class for game states"""
    
    def handle_event(self, event):
        """Handle input events"""
        pass
    
    def update(self):
        """Update state logic"""
        pass
    
    def draw(self, screen):
        """Draw the state"""
        pass


class CharacterSelectionState(GameState):
    """Character selection screen"""
    
    KNIGHT_COLORS = {
        'pink': (255, 192, 203),
        'orange': (255, 165, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
    }
    
    def __init__(self, game):
        self.game = game
        self.selected_index = 0
        self.color_names = list(self.KNIGHT_COLORS.keys())
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
    
    def handle_event(self, event):
        """Handle character selection input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.color_names)
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.color_names)
            elif event.key == pygame.K_RETURN:
                # Start the game with selected color
                selected_color = self.color_names[self.selected_index]
                knight = Knight(selected_color, 600, 700)
                level1 = Level1(self.game, knight)
                self.game.change_state(level1)
    
    def draw(self, screen):
        """Draw character selection screen"""
        # Title
        title = self.font_large.render("Choose Your Knight", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = self.font_small.render("Use LEFT/RIGHT arrows to select, ENTER to confirm", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(screen.get_width() // 2, 200))
        screen.blit(instructions, instructions_rect)
        
        # Draw color options
        box_size = 120
        spacing = 250
        start_x = screen.get_width() // 2 - (spacing * 1.5)
        
        for i, color_name in enumerate(self.color_names):
            x = start_x + (i * spacing)
            y = 400
            color = self.KNIGHT_COLORS[color_name]
            
            # Draw knight rectangle
            rect = pygame.Rect(x, y, box_size, box_size)
            pygame.draw.rect(screen, color, rect)
            
            # Highlight selected
            if i == self.selected_index:
                pygame.draw.rect(screen, (255, 255, 255), rect, 5)
            else:
                pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            
            # Draw color name
            name_text = self.font_medium.render(color_name.capitalize(), True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(x + box_size // 2, y + box_size + 40))
            screen.blit(name_text, name_rect)


class Level1State(GameState):
    """Level 1 state - placeholder"""
    
    def __init__(self, game, knight):
        self.game = game
        self.knight = knight
        self.level = Level1(game, knight)
    
    def handle_event(self, event):
        self.level.handle_event(event)
    
    def update(self):
        self.level.update()
    
    def draw(self, screen):
        self.level.draw(screen)
