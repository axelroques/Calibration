
from __init__ import CONFIG

import pygame


class Button:

    def __init__(self, x, y):
        self.surf = pygame.Surface(
            (CONFIG['global']['window_width']/4,
             CONFIG['global']['window_height']/7)
        )
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y

        # Moves the button's rect at x and y
        self.rect.x = x
        self.rect.y = y


class Text:

    def __init__(self, text, button):

        self.surf = pygame.font.SysFont(
            'Lato', 25).render(text, True, CONFIG['global']['bg_color'])
        self.rect = self.surf.get_rect(center=button.rect.center)
