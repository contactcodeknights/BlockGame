import pygame
from settings import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, SCALED_TILE, SCALED_TILE)
        self.colour = (255, 165, 0) # Orange Cube
        
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = -10
        self.bounce_power = -18 # Higher jump for yellow tiles
        self.gravity = 0.5
        
        self.on_ground = False

    def update(self, tiles, start_position):
        keys = pygame.key.get_pressed()
        self.vel_x = 0
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel_y = self.jump_power

        self.vel_y += self.gravity

        # X Collision
        self.rect.x += self.vel_x
        for tile, t_type in tiles:
            if t_type == "red":
                if self.rect.colliderect(tile):
                    self.reset_player(start_position)
                    return
            elif self.rect.colliderect(tile):
                if self.vel_x > 0:
                    self.rect.right = tile.left
                elif self.vel_x < 0:
                    self.rect.left = tile.right

        # Y Collision
        self.rect.y += self.vel_y
        self.on_ground = False
        
        for tile, t_type in tiles:
            if t_type == "red":
                if self.rect.colliderect(tile):
                    self.reset_player(start_position)
                    return
            elif self.rect.colliderect(tile):
                if self.vel_y > 0:
                    self.rect.bottom = tile.top
                    # Check if landing on a yellow trampoline tile
                    if t_type == "yellow":
                        self.vel_y = self.bounce_power
                    else:
                        self.vel_y = 0
                        self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = tile.bottom
                    self.vel_y = 0

    def reset_player(self, start_position):
        # Reset position and momentum
        self.rect.topleft = start_position
        self.vel_x = 0
        self.vel_y = 0

    def draw(self, surface, scroll):
        # Draw offset by camera
        screen_x = self.rect.x - scroll[0]
        screen_y = self.rect.y - scroll[1]
        pygame.draw.rect(surface, self.colour, (screen_x, screen_y, self.rect.width, self.rect.height))