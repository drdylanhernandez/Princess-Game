"""
Level 1 - The Town
"""

import pygame
from enemy import ExBoyfriend
from tools import ToolBox, DiceRoller


class Level1:
    """Level 1 implementation - Escape the town"""
    
    def __init__(self, game, knight):
        """
        Initialize Level 1
        
        Args:
            game (Game): Main game instance
            knight (Knight): Player character
        """
        self.game = game
        self.knight = knight
        self.width = game.screen.get_width()
        self.height = game.screen.get_height()
        
        # Level elements
        # Enemy spawns at top-right, far from player
        self.enemy = ExBoyfriend(self.width - 100, 50)
        self.tool_box = ToolBox(self.width // 2, self.height // 2)
        self.dice_roller = DiceRoller()
        
        # Level state
        self.threat_level = 0.0
        self.max_threat = 1.0
        self.game_over = False
        self.won = False
        self.level_complete = False
        
        # UI
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Escape area (bottom of screen)
        self.escape_zone = pygame.Rect(0, self.height - 100, self.width, 100)
    
    def handle_event(self, event):
        """Handle input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not self.dice_roller.rolling:
                # Roll dice at tool box
                if self.knight.rect.colliderect(self.tool_box.rect):
                    self.dice_roller.start_roll()
            
            if event.key == pygame.K_ESCAPE:
                # Return to main menu
                from game_states import CharacterSelectionState
                self.game.change_state(CharacterSelectionState(self.game))
    
    def update(self):
        """Update level logic"""
        if self.game_over or self.won:
            return
        
        # Handle player input
        keys = pygame.key.get_pressed()
        self.knight.handle_input(keys)
        
        # Keep player in bounds
        self.knight.x = max(0, min(self.knight.x, self.width - self.knight.width))
        self.knight.y = max(0, min(self.knight.y, self.height - self.knight.height))
        
        # Update enemy
        self.enemy.update(self.knight)
        
        # Update threat level
        self.threat_level = self.enemy.get_threat_level(self.knight)
        
        # Check if player caught
        if self.knight.rect.colliderect(self.enemy.rect) and not self.knight.is_hidden:
            self.game_over = True
        
        # Update dice roller
        roll_complete = self.dice_roller.update()
        if roll_complete:
            # Apply the tool
            tool = self.dice_roller.current_tool
            self.knight.use_tool(tool)
        
        # Check if player escaped
        if self.knight.rect.colliderect(self.escape_zone):
            self.won = True
            self.level_complete = True
    
    def draw(self, screen):
        """Draw level"""
        # Background
        screen.fill((100, 150, 100))  # Green grass
        
        # Town area
        pygame.draw.rect(screen, (200, 180, 140), pygame.Rect(0, 0, self.width, 400))
        
        # Forest area (escape zone)
        pygame.draw.rect(screen, (34, 139, 34), self.escape_zone)
        
        # Draw level elements
        self.tool_box.draw(screen)
        self.enemy.draw(screen)
        self.knight.draw(screen)
        
        # Draw HUD
        self._draw_hud(screen)
        
        # Draw game over/win message
        if self.game_over:
            self._draw_game_over(screen)
        elif self.won:
            self._draw_win(screen)
    
    def _draw_hud(self, screen):
        """Draw heads-up display"""
        # Threat meter
        meter_width = 300
        meter_height = 30
        meter_x = 20
        meter_y = 20
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(meter_x, meter_y, meter_width, meter_height))
        
        # Threat bar
        threat_width = meter_width * self.threat_level
        threat_color = (255, int(255 * (1 - self.threat_level)), 0)  # Red to yellow
        pygame.draw.rect(screen, threat_color, pygame.Rect(meter_x, meter_y, threat_width, meter_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(meter_x, meter_y, meter_width, meter_height), 2)
        
        # Label
        label = self.font_small.render("THREAT", True, (255, 255, 255))
        screen.blit(label, (meter_x, meter_y - 30))
        
        # Instructions
        instructions = self.font_small.render("ARROW KEYS: Move | UP: Roll Dice at Box | ESC: Menu", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(topleft=(20, self.height - 30))
        screen.blit(instructions, instructions_rect)
        
        # Status
        if self.knight.is_hidden:
            status = self.font_small.render("STATUS: HIDDEN", True, (0, 255, 0))
        else:
            status = self.font_small.render("STATUS: VISIBLE", True, (255, 0, 0))
        status_rect = status.get_rect(topright=(self.width - 20, 20))
        screen.blit(status, status_rect)
        
        # Draw dice roller if active
        if self.dice_roller.rolling or self.dice_roller.current_tool:
            self.dice_roller.draw(screen, self.width // 2, 100)
    
    def _draw_game_over(self, screen):
        """Draw game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("CAUGHT!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        
        # Retry text
        retry_text = self.font_medium.render("Press ESC to return to menu", True, (255, 255, 255))
        retry_rect = retry_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(retry_text, retry_rect)
    
    def _draw_win(self, screen):
        """Draw win screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Win text
        win_text = self.font_large.render("ESCAPED!", True, (0, 255, 0))
        win_rect = win_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        screen.blit(win_text, win_rect)
        
        # Continue text
        continue_text = self.font_medium.render("Press ESC to return to menu", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(self.width // 2, self.height // 2 + 50))
        screen.blit(continue_text, continue_rect)
