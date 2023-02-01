
from __init__ import CONFIG
from calibrations import TernaryCalibration
from calibrations import BinaryCalibration
from gui import Button, Text

import pandas as pd
import pygame


class Experiment:

    def __init__(self) -> None:

        # Monitor info
        # TO DO

        # Initiate PyGame
        pygame.init()
        pygame.display.set_caption('Calibration')

        # Main menu display
        width = CONFIG['global']['width']
        height = CONFIG['global']['height']
        self.screen = pygame.display.set_mode((width, height))
        self.buttons = [
            Button(x, y)
            for x, y in zip(
                [width/2-width/8, width/2-width/8],
                [height/2-height/7-height/18, height/2+height/18]
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
        self._awaitSelection()

    def getStimulusMovements(self):
        """
        Return stimulus movements.
        """
        return self.calibration.getStimulusMovements()

    def getData(self):
        """
        Return stimulus movements as a pandas DataFrame.
        """
        return pd.DataFrame(data=self.calibration.data)

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
                        self.calibration = self._launchCalibration(
                            i, self.screen
                        )

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
        if event.type == pygame.QUIT:
            self.running = False

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

    @staticmethod
    def _launchCalibration(button_id, screen):
        """
        Launch binary or ternary calibration depending
        on which button was pressed.
        """

        calibrations = {
            0: BinaryCalibration,
            1: TernaryCalibration
        }

        try:
            return calibrations[button_id](screen)

        except KeyError:
            raise RuntimeError('How did that happen?!')


if __name__ == '__main__':

    exp = Experiment()
    movements = exp.getStimulusMovements()
    data = exp.getData()
    print(data)
