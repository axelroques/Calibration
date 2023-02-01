
from gui import Button, Text
from __init__ import CONFIG

import pygame


class Menu:

    def __init__(self, screen) -> None:

        # Exit parameter
        self.exit_condition = False

        # Screen parameters
        self.screen = screen
        self.w = CONFIG['global']['width']
        self.h = CONFIG['global']['height']

    def getChoice(self):
        """
        Return button clicked.
        """
        return self.button_id

    def _awaitSelection(self):
        """
        Wait for the user to click on one of the buttons.
        """

        # Game clock
        clock = pygame.time.Clock()

        click = False
        self.running = True
        while self.running:

            # Mouse control
            mx, my = pygame.mouse.get_pos()

            # Detect clicks on menu buttons
            for i, button in enumerate(self.buttons):
                if button.rect.collidepoint((mx, my)):
                    if click:
                        return i

            click = False
            # Event queue
            for event in pygame.event.get():

                # Exit conditions
                self._catchExit(event)

                # Mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            # Draw
            self._draw()

            # 10 fps
            clock.tick(10)

        return

    def _catchExit(self, event):
        """
        Exit handler.
        """

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.exit_condition = True
        if event.type == pygame.QUIT:
            self.running = False
            self.exit_condition = True

        return

    def _draw(self):
        """
        Draw function.
        """

        # Draw background
        self.screen.fill(CONFIG['global']['bg_color'])

        # Draw buttons
        for button in self.buttons:
            self.screen.blit(button.surf, button.rect)

        # Draw texts
        for text in self.texts:
            self.screen.blit(text.surf, text.rect)

        # Display
        pygame.display.flip()

        return


class MainMenu(Menu):

    def __init__(self, screen) -> None:
        super().__init__(screen)

        # Layout
        self.buttons = [
            Button(x, y)
            for x, y in zip(
                [self.w/2-self.w/8, self.w/2-self.w/8],
                [self.h/2-self.h/7-self.h/18, self.h/2+self.h/18]
            )
        ]
        self.texts = [
            Text(text, button) for text, button
            in zip(
                ['Binary calibration', 'Ternary calibration'],
                self.buttons
            )
        ]

        # Await user input
        self.button_id = self._awaitSelection()


class ExportMenu(Menu):

    def __init__(self, screen) -> None:
        super().__init__(screen)

        # Layout
        self.buttons = [
            Button(
                self.w/2-self.w/8,
                self.h/2-self.h/7/2
            )
        ]

        self.texts = [
            Text('Export results', self.buttons[0])
        ]

        # Await user input
        self.button_id = self._awaitSelection()
