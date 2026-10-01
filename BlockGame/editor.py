
import pygame
import json
import os
from settings import *

class LevelEditor:
    def __init__(self, screen, save_file="map_data.json"):
        self.screen = screen
        self.save_file = save_file
        self.level_data = {}
        self.tile_types = ["blue", "green", "yellow", "red", "start", "exit"]
        self.current_type_index = 0
        
        # Camera implementation for larger maps
        self.scroll = [0, 0]
        self.scroll_speed = 10
        
        # Warning message state
        self.warning_message = ""
        self.warning_timer = 0
        
        self.load_map()

    def load_map(self):
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f: 
                self.level_data = json.load(f)

    def save_map(self): 
        with open(self.save_file, "w") as f: 
            json.dump(self.level_data, f, indent=4)

    def draw_grid(self):
        # Offsets the grid lines based on the camera scroll
        offset_x = -self.scroll[0] % SCALED_TILE
        offset_y = -self.scroll[1] % SCALED_TILE
        
        for x in range(offset_x, SCREEN_WIDTH, SCALED_TILE):
            pygame.draw.line(self.screen, (60, 60, 75), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(offset_y, SCREEN_HEIGHT, SCALED_TILE):
            pygame.draw.line(self.screen, (60, 60, 75), (0, y), (SCREEN_WIDTH, y))

    def run(self):
        running = True
        font = pygame.font.SysFont('Arial', 20)
        warning_font = pygame.font.SysFont('Arial', 40, bold=True)
        clock = pygame.time.Clock()
        
        while running:
            self.screen.fill(BG_COLOURS)
            
            # Input Handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]: self.scroll[1] -= self.scroll_speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]: self.scroll[1] += self.scroll_speed
            if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.scroll[0] -= self.scroll_speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.scroll[0] += self.scroll_speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_MINUS:
                        self.level_data.clear()
                    if event.key == pygame.K_ESCAPE:
                        # Validation check to make sure both start and exit points exist before saving
                        has_start = "start" in self.level_data.values()
                        has_exit = "exit" in self.level_data.values()
                        
                        if not has_start and not has_exit:
                            self.warning_message = "Start and Exit points not set!"
                            self.warning_timer = pygame.time.get_ticks()
                        elif not has_start:
                            self.warning_message = "Start point not set!"
                            self.warning_timer = pygame.time.get_ticks()
                        elif not has_exit:
                            self.warning_message = "Exit point not set!"
                            self.warning_timer = pygame.time.get_ticks()
                        else:
                            # Both exist, safe to save and leave
                            self.save_map()
                            return
                            
                    if event.key == pygame.K_SPACE:
                        self.current_type_index = (self.current_type_index + 1) % len(self.tile_types)

            # Mouse logic for placing and removing tiles
            mouse_position = pygame.mouse.get_pos()
            grid_x = (mouse_position[0] + self.scroll[0]) // SCALED_TILE
            grid_y = (mouse_position[1] + self.scroll[1]) // SCALED_TILE
            position_key = f"{grid_x},{grid_y}"
            
            if pygame.mouse.get_pressed()[0]: # Left click to place
                self.level_data[position_key] = self.tile_types[self.current_type_index]
            elif pygame.mouse.get_pressed()[2]: # Right click to remove
                if position_key in self.level_data:
                    del self.level_data[position_key]

            self.draw_grid()

            # Render Placed Tiles (Account for camera scroll)
            for position_key, tile_type in self.level_data.items():
                gx, gy = map(int, position_key.split(','))
                screen_x = gx * SCALED_TILE - self.scroll[0]
                screen_y = gy * SCALED_TILE - self.scroll[1]
                
                # Only draw tiles visible on the screen
                if -SCALED_TILE < screen_x < SCREEN_WIDTH and -SCALED_TILE < screen_y < SCREEN_HEIGHT:
                    rect = (screen_x, screen_y, SCALED_TILE, SCALED_TILE)
                    pygame.draw.rect(self.screen, COLOURS[tile_type], rect)

            # --- Draw Warning Message ---
            if self.warning_message:
                if pygame.time.get_ticks() - self.warning_timer < 2500: # Flash for 2.5 seconds
                    warn_surf = warning_font.render(self.warning_message, True, (255, 50, 50)) # Bright red text
                    warn_rect = warn_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    
                    # Draw a solid black background box behind the text so it stands out over tiles
                    bg_rect = warn_rect.inflate(30, 20) 
                    pygame.draw.rect(self.screen, (0, 0, 0), bg_rect)
                    pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 3) # White border
                    
                    self.screen.blit(warn_surf, warn_rect)
                else:
                    self.warning_message = "" # Clear the message after the timer ends

            # UI Text
            current_type = self.tile_types[self.current_type_index].upper()
            ui_text = font.render(f"[SPACE] Toggle Tile: {current_type} | [WASD] Move Camera | [-] Delete All | [ESC] Save & Exit", True, (255, 255, 255))
            
            # Add a small background so the UI text doesn't blend into tiles
            pygame.draw.rect(self.screen, (0, 0, 0), (5, 5, ui_text.get_width() + 10, ui_text.get_height() + 10))
            self.screen.blit(ui_text, (10, 10))

            pygame.display.flip()
            clock.tick(60)