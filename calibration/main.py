
from calibrations import TernaryCalibration
from calibrations import BinaryCalibration
from menus import MainMenu, ExportMenu
from __init__ import CONFIG

from datetime import datetime
import pandas as pd
import pickle
import pygame


class Experiment:

    def __init__(self) -> None:

        # Monitor info
        # TO DO

        # Initiate PyGame
        pygame.init()
        pygame.display.set_caption('Calibration')
        self.screen = pygame.display.set_mode(
            (CONFIG['global']['width'], CONFIG['global']['height'])
        )

        completed = False
        while not completed:

            # Main menu
            self._main_menu = MainMenu(self.screen)
            self.calibration_id = self._main_menu.getChoice()

            # Exit condition
            if self._main_menu.exit_condition:
                return

            # Calibration experiment
            self.calibration = self._launchCalibration(
                self.calibration_id, self.screen
            )

            completed = not self.calibration.early_break

        # Export menu
        self._export_menu = ExportMenu(self.screen)

        # Exit condition
        if self._export_menu.exit_condition:
            return
            # Otherwise export the data
        else:
            self._exportData()

    @staticmethod
    def _launchCalibration(calibration_id, screen):
        """
        Launch binary or ternary calibration depending
        on which button was pressed.
        """

        calibrations = {
            0: BinaryCalibration,
            1: TernaryCalibration
        }

        try:
            return calibrations[calibration_id](screen)

        except KeyError:
            raise RuntimeError('How did that happen?!')

        return

    def _exportData(self):
        """
        Export data from the calibration
        """

        # Get time series data
        data = pd.DataFrame(data=self.calibration.data)

        # Get stimulus movements
        movements = self.calibration.getStimulusMovements()

        # Export them...
        now = datetime.now()
        date = now.strftime("%Y_%m_%d-%H_%M_%S")
        filename = f'{date}-{self.calibration.type}'

        # ... as a csv file ...
        data.to_csv(f'results/{filename}.csv', index=False)

        # ... and as a pickle file
        with open(f'results/{filename}.pkl', 'wb') as f:
            pickle.dump(movements, f)

        return


if __name__ == '__main__':

    exp = Experiment()
