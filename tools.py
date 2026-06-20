"""
Tool System - Dice Rolling and Tool Selection
"""

import pygame
import random


class ToolBox:
    """Magic box that contains tools and dice rolling"""
    
    TOOLS = [
        'town_clothes',
        'shovel',
        'sword',
        'fish',
        'people',
        'regular_clothes',
    ]
    
    TOOL_DESCRIPTIONS = {
        'town_clothes': 'Hide from enemies',
        'shovel': 'Dig under enemies',
        'sword': 'Combat weapon',
        'fish': '???',
        'people': '???',
        'regular_clothes': '???',
    }
    
    def __init__(self, x, y):
        """
        Initialize a tool box
        
        Args:
            x (int): Box x position
            y (int): Box y position
        """
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (255, 215, 0)  # Gold
        self.opened = False
    
    def draw(self, screen):
        """Draw the tool box"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (200, 170, 0), self.rect, 3)
        
        # Draw box pattern
        pygame.draw.line(screen, (200, 170, 0), (self.x, self.y), (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(screen, (200, 170, 0), (self.x + self.width, self.y), (self.x, self.y + self.height), 2)


class DiceRoller:
    """Dice rolling system for tool selection"""
    
    def __init__(self):
        self.rolling = False
        self.current_tool = None
        self.roll_duration = 0
        self.max_roll_duration = 60  # Frames to roll
        self.font = pygame.font.Font(None, 48)
    
    def start_roll(self):
        """Start a dice roll"""
        self.rolling = True
        self.roll_duration = self.max_roll_duration
    
    def update(self):
        """Update dice rolling animation"""
        if self.rolling:
            self.roll_duration -= 1
            
            if self.roll_duration <= 0:
                # Roll complete - select a random tool
                self.current_tool = random.choice(ToolBox.TOOLS)
                self.rolling = False
                return True  # Roll complete
        
        return False
    
    def get_current_display(self):
        """Get current tool to display during rolling"""
        if self.rolling:
            return random.choice(ToolBox.TOOLS)
        return self.current_tool
    
    def draw(self, screen, x, y):
        """Draw the dice roller UI"""
        if self.rolling or self.current_tool:
            # Draw rolling animation or result
            tool = self.get_current_display()
            text = self.font.render(tool.replace('_', ' ').title(), True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            
            # Draw background box
            box_rect = text_rect.inflate(20, 20)
            pygame.draw.rect(screen, (50, 50, 50), box_rect)
            pygame.draw.rect(screen, (200, 200, 200), box_rect, 2)
            
            screen.blit(text, text_rect)
            
            # Draw status
            if self.rolling:
                status = self.font.render("ROLLING...", True, (255, 200, 0))
            else:
                status = self.font.render("YOU GOT:", True, (0, 255, 0))
            
            status_rect = status.get_rect(center=(x, y - 60))
            screen.blit(status, status_rect)
