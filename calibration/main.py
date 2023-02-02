
from calibrations import TernaryCalibration
from calibrations import BinaryCalibration
from menus import MainMenu, ExportMenu
from __init__ import CONFIG

from datetime import datetime
import pandas as pd
import numpy as np
import pickle
import pygame


class Experiment:

    def __init__(self) -> None:

        # Monitor info
        self.pixel_size = CONFIG['monitor']['monitor_width'] / \
            CONFIG['monitor']['horizontal_pixel_resolution']
        self.viewing_distance = CONFIG['monitor']['viewing_distance']

        # Initiate PyGame
        pygame.init()
        pygame.display.set_caption('Calibration')
        self.screen = pygame.display.set_mode(
            (CONFIG['global']['window_width'],
             CONFIG['global']['window_height'])
        )

        # Main loop
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

        # Generate export data from the calibration experiment
        self._generateData()

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

    def _generateData(self):
        """
        Generate data from the stimulus movements.
        """

        # Initialize time series data structure for export
        self.data = {
            't': [],
            'x': [],
            'y': []
        }

        time_offset = 0
        for i, movement in enumerate(self.calibration.getStimulusMovements()):

            if i == 0:
                self.data['t'] += movement.timestamps
                self.data['x'] += movement.positions['x']
                self.data['y'] += movement.positions['y']

            # First time and position is a duplicate from the previous movement
            else:
                self.data['t'] += [
                    t + time_offset for t in movement.timestamps[1:]
                ]
                self.data['x'] += movement.positions['x'][1:]
                self.data['y'] += movement.positions['y'][1:]

            time_offset += movement.timestamps[-1]

        return

    def _exportData(self):
        """
        Export data from the calibration
        """

        # Get time series data
        data = pd.DataFrame(data={
            't': self.data['t'],
            'x': self._pixToDeg(self.data['x']),
            'y': self._pixToDeg(self.data['y'])
        })

        # Get stimulus movements
        experiment = {key: val for key, val in CONFIG.items()}
        movements = self.calibration.getStimulusMovements()
        experiment['movements'] = [movement.__dict__ for movement in movements]

        # Export them...
        now = datetime.now()
        date = now.strftime("%Y_%m_%d-%H_%M_%S")
        filename = f'{date}-{self.calibration.type}'

        # ... as a csv file ...
        data.to_csv(f'results/{filename}.csv', index=False)

        # ... and as a pickle file
        with open(f'results/{filename}.pkl', 'wb') as f:
            pickle.dump(experiment, f)

        return

    def _pixToDeg(self, distance):
        """
        Convert pixels to degrees of visual angle.
        """
        return np.arctan2(
            (np.array(distance)*self.pixel_size), self.viewing_distance
        ) * 180 / np.pi


if __name__ == '__main__':

    exp = Experiment()
