"""
Level 1 - The Town
"""

import pygame
from enemy import ExBoyfriend
from tools import ToolBox, DiceRoller


class Building:
    """A building that blocks movement"""
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (139, 69, 19)  # Brown
        self.outline_color = (101, 50, 14)  # Darker brown
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, self.outline_color, self.rect, 3)
        # Draw windows
        window_size = 15
        for wx in range(self.rect.x + 10, self.rect.x + self.rect.width - 10, 25):
            for wy in range(self.rect.y + 10, self.rect.y + self.rect.height - 10, 25):
                pygame.draw.rect(screen, (255, 255, 100), (wx, wy, window_size, window_size))


class Level1:
    """Level 1 implementation - Escape the town maze"""
    
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
        
        # Create town buildings (Pac-Man style maze)
        self.buildings = self._create_town_layout()
        
        # Level elements
        # Enemy spawns at opposite end of town
        self.enemy = ExBoyfriend(self.width - 100, self.height - 100)
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
        
        # Escape area (right side of town)
        self.escape_zone = pygame.Rect(self.width - 80, 0, 80, self.height)
    
    def _create_town_layout(self):
        """Create a Pac-Man style town layout with buildings"""
        buildings = []
        
        # Block size and spacing
        block_width = 80
        block_height = 80
        street_width = 50
        
        # Create grid of buildings with streets
        for row in range(0, self.height, block_height + street_width):
            for col in range(0, self.width, block_width + street_width):
                # Skip some positions to create varied maze
                if (row // (block_height + street_width) + col // (block_width + street_width)) % 3 == 0:
                    continue
                
                # Skip right edge (escape zone) and top-left (starting area)
                if col > self.width - 200:
                    continue
                if row < 100 and col < 100:
                    continue
                
                buildings.append(Building(col, row, block_width, block_height))
        
        return buildings
    
    def check_collision(self, rect):
        """Check if a rectangle collides with any building"""
        for building in self.buildings:
            if rect.colliderect(building.rect):
                return True
        return False
    
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
        old_x, old_y = self.knight.x, self.knight.y
        
        self.knight.handle_input(keys)
        
        # Check collision with buildings - revert if collision
        if self.check_collision(self.knight.rect):
            self.knight.x, self.knight.y = old_x, old_y
            self.knight.rect.x = self.knight.x
            self.knight.rect.y = self.knight.y
        
        # Keep player in bounds
        self.knight.x = max(0, min(self.knight.x, self.width - self.knight.width))
        self.knight.y = max(0, min(self.knight.y, self.height - self.knight.height))
        self.knight.rect.x = self.knight.x
        self.knight.rect.y = self.knight.y
        
        # Update enemy
        self.enemy.update(self.knight)
        
        # Check enemy collision with buildings
        if self.check_collision(self.enemy.rect):
            # Revert enemy movement
            self.enemy.x -= (self.enemy.x - self.enemy.rect.x)
            self.enemy.y -= (self.enemy.y - self.enemy.rect.y)
            self.enemy.rect.x = self.enemy.x
            self.enemy.rect.y = self.enemy.y
        
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
        # Background (streets)
        screen.fill((180, 180, 180))  # Gray streets
        
        # Draw buildings
        for building in self.buildings:
            building.draw(screen)
        
        # Draw escape zone
        pygame.draw.rect(screen, (34, 139, 34), self.escape_zone)
        escape_text = self.font_small.render("FOREST", True, (255, 255, 255))
        escape_text_rect = escape_text.get_rect(center=(self.width - 40, self.height // 2))
        screen.blit(escape_text, escape_text_rect)
        
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
