"""
Enemy Characters
"""

import pygame
import math


class ExBoyfriend:
    """The princess's ex-boyfriend - main antagonist of Level 1"""
    
    def __init__(self, x, y, speed=2):
        """
        Initialize the ex-boyfriend enemy
        
        Args:
            x (int): Starting x position
            y (int): Starting y position
            speed (float): Movement speed
        """
        self.x = x
        self.y = y
        self.width = 35
        self.height = 35
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (139, 69, 19)  # Brown
        
        # AI state
        self.target = None
        self.alert_range = 300
        self.lost_player = False
        self.lost_cooldown = 0
    
    def update(self, player):
        """
        Update enemy behavior
        
        Args:
            player (Knight): The player knight
        """
        distance = self.distance_to(player.x, player.y)
        
        # Check if player is in alert range and not hidden
        if distance < self.alert_range and not player.is_hidden:
            self.lost_player = False
            self.lost_cooldown = 0
            self.target = player
            self.chase_player(player)
        elif self.target and player.is_hidden:
            # Player used town clothes - lose the player
            self.lost_player = True
            self.lost_cooldown = 120  # 2 seconds at 60 FPS
            self.target = None
        elif self.lost_cooldown > 0:
            self.lost_cooldown -= 1
            if self.lost_cooldown <= 0:
                self.lost_player = False
        
        # Update rect position
        self.rect.x = self.x
        self.rect.y = self.y
    
    def chase_player(self, player):
        """Chase the player"""
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize and apply speed
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def distance_to(self, x, y):
        """Calculate distance to a point"""
        dx = self.x - x
        dy = self.y - y
        return math.sqrt(dx**2 + dy**2)
    
    def get_threat_level(self, player):
        """
        Get threat level (0.0 to 1.0)
        Based on distance from player
        """
        distance = self.distance_to(player.x, player.y)
        threat = max(0, 1 - (distance / self.alert_range))
        
        # Extra threat if pursuing
        if self.target and not self.lost_player:
            threat = min(1.0, threat * 1.5)
        
        return min(1.0, threat)
    
    def draw(self, screen):
        """Draw the enemy"""
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        
        # Draw eyes
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 10, self.y + 10), 3)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 25, self.y + 10), 3)
