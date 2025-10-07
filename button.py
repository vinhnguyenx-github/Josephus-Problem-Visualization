import pygame
from config import *

class Button:
    def __init__(self, x, y, w, h, label, action):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.action = action
        self.font = pygame.font.SysFont(FONT_NAME, 28, bold=True)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(mouse)
        bg = BUTTON_BG_HOVER if hover else BUTTON_BG
        pygame.draw.rect(screen, bg, self.rect, border_radius=8)
        pygame.draw.rect(screen, BUTTON_BORDER, self.rect, 2, border_radius=8)
        text = self.font.render(self.label, True, BUTTON_TEXT)
        screen.blit(text, text.get_rect(center=self.rect.center))

    def handle_event(self, event, callback_map):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                func = callback_map.get(self.action)
                if func:
                    func()
                return True
        return False