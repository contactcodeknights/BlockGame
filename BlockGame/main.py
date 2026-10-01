# https://www.pygame.org/docs/ref/color.html - link to pygame website for docs. 


import pygame
import sys
import json
import os
from settings import *
from menu import MainMenu
from editor import LevelEditor
from player import Player


def play_level(screen):
    clock = pygame.time.Clock()
    solid_tiles = []
    shaded_rects = []
    start_position = (100, 100)
    exit_rect = None

    # Load existing map data
    if os.path.exists("map_data.json"):
        with open("map_data.json", "r") as f:
            level_data = json.load(f)
            for position_key, tile_type in level_data.items():
                gx, gy = map(int, position_key.split(','))
                # The map dynamically reads SCALED_TILE from settings
                rect = pygame.Rect(gx * SCALED_TILE, gy * SCALED_TILE, SCALED_TILE, SCALED_TILE)
                
                if tile_type == "start":
                    start_position = (rect.x, rect.y)
                elif tile_type == "exit":
                    exit_rect = rect
                else:
                    solid_tiles.append((rect, tile_type)) 
                    shaded_rects.append((rect, COLOURS[tile_type]))

    player = Player(*start_position)
    
    # Camera setup, starts directly on the player's spawn point
    scroll = [start_position[0] - SCREEN_WIDTH//2, start_position[1] - SCREEN_HEIGHT//2]
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return # Exit back to menu

        # Updates player logic
        player.update(solid_tiles, start_position)

        # Smooth Camera Follow
        # Because we're calculate based on player.rect.centerx, the camera always focuses the middle of the player cube.
        scroll[0] += (player.rect.centerx - SCREEN_WIDTH / 2 - scroll[0]) / 10
        scroll[1] += (player.rect.centery - SCREEN_HEIGHT / 2 - scroll[1]) / 10
        int_scroll = [int(scroll[0]), int(scroll[1])]

        # Print statement to confirm the level is over.
        if exit_rect and player.rect.colliderect(exit_rect):
            print("Level Complete!")
            return 

        # Renders colours and tiles
        screen.fill(BG_COLOURS)
        
        # Draw start/exit tiles offset by camera
        if exit_rect:
            pygame.draw.rect(screen, COLOURS["exit"], (exit_rect.x - int_scroll[0], exit_rect.y - int_scroll[1], SCALED_TILE, SCALED_TILE))
        pygame.draw.rect(screen, COLOURS["start"], (start_position[0] - int_scroll[0], start_position[1] - int_scroll[1], SCALED_TILE, SCALED_TILE))

        # Draw environment offset by camera
        for rect, colour in shaded_rects:
            screen_x = rect.x - int_scroll[0]
            screen_y = rect.y - int_scroll[1]
            if -SCALED_TILE < screen_x < SCREEN_WIDTH and -SCALED_TILE < screen_y < SCREEN_HEIGHT:
                pygame.draw.rect(screen, colour, (screen_x, screen_y, SCALED_TILE, SCALED_TILE))

        player.draw(screen, int_scroll)
        
        pygame.display.flip()
        clock.tick(FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cube Platformer")

    app_running = True
    while app_running:
        menu = MainMenu(screen)
        choice = menu.run()

        if choice == "play":
            play_level(screen)
        elif choice == "editor":
            editor = LevelEditor(screen)
            editor.run()
        elif choice == "quit" or choice is None:
            app_running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()