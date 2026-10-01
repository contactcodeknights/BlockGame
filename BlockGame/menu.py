import pygame
from settings import *

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 40, bold=True)
        self.buttons = [
            {"text": "Play Level", "action": "play", "y": 250},
            {"text": "Level Editor", "action": "editor", "y": 350},
            {"text": "Exit Game", "action": "quit", "y": 450}
        ]

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOURS)

            # Draw Title
            title_surf = self.font.render("CUBE PLATFORMER", True, (255, 215, 0))
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100)))

            button_rects = []
            for btn in self.buttons:
                button_colour = (100, 255, 100) if btn["y"] - 20 < mouse_pos[1] < btn["y"] + 20 else (200, 200, 200)
                text_surf = self.font.render(btn["text"], True, button_colour)
                rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, btn["y"]))
                self.screen.blit(text_surf, rect)
                button_rects.append((rect, btn["action"]))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, action in button_rects:
                        if rect.collidepoint(mouse_pos):
                            return action

            pygame.display.flip()