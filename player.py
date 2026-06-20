"""
Player Character - Knight
"""

import pygame


class Knight:
    """Player-controlled knight character"""
    
    COLOR_MAP = {
        'pink': (255, 192, 203),
        'orange': (255, 165, 0),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
    }
    
    def __init__(self, color, x, y):
        """
        Initialize a knight
        
        Args:
            color (str): Knight color (pink, orange, red, green)
            x (int): Starting x position
            y (int): Starting y position
        """
        self.color = color.lower()
        self.color_value = self.COLOR_MAP.get(self.color, (255, 255, 255))
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # State
        self.is_hidden = False  # Whether wearing town clothes
        self.current_tool = None
        self.health = 100
        
    def handle_input(self, keys):
        """Handle player input"""
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
    
    def use_tool(self, tool):
        """Use a tool from the dice roll"""
        self.current_tool = tool
        
        if tool == 'town_clothes':
            self.is_hidden = True
        elif tool == 'shovel':
            # Dig mechanic - increase speed temporarily
            pass
        elif tool == 'sword':
            # Combat mechanic
            pass
    
    def stop_hiding(self):
        """Stop hiding/remove town clothes"""
        self.is_hidden = False
    
    def draw(self, screen):
        """Draw the knight"""
        if self.is_hidden:
            # Draw as town clothes (different appearance)
            pygame.draw.rect(screen, (200, 150, 100), self.rect)
            pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        else:
            # Draw as colored knight
            pygame.draw.rect(screen, self.color_value, self.rect)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
    
    def get_position(self):
        """Get current position"""
        return (self.x, self.y)
    
    def distance_to(self, x, y):
        """Calculate distance to a point"""
        dx = self.x - x
        dy = self.y - y
        return (dx**2 + dy**2)**0.5
