
from __init__ import CONFIG
from movement import EyeMovement

import numpy as np
import pygame


class Target(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super(Target, self).__init__()

        # Aesthetics
        self.surf = pygame.image.load("assets/target.png")
        self.rect = self.surf.get_rect()

        # Initialize position at the center of the screen
        self.x = (CONFIG['global']['width']-self.surf.get_width())/2
        self.y = (CONFIG['global']['height']-self.surf.get_height())/2
        self.rect.x = self.x
        self.rect.y = self.y

    def _getCenteredPos(self):
        return np.array([
            self.x+self.surf.get_width()/2,
            self.y+self.surf.get_height()/2
        ])

    def _getPos(self):
        return np.array([self.x, self.y])

    def _generateFixation(self, start_pos):
        """
        Generate and return a fixation, of random 
        duration.
        """

        amplitude = 0
        velocity = np.array([0, 0])
        duration = np.random.uniform(
            CONFIG['fixation']['min_duration'],
            CONFIG['fixation']['max_duration']
        )
        end_pos = start_pos

        return EyeMovement(
            'fixation', start_pos, end_pos,
            amplitude, velocity, duration
        )

    def _generateSaccade(self, start_pos):
        """
        Generate and return a saccade, of 
            - random direction
            - random amplitude 
            - duration of 3 s.
        """

        end_pos = np.array([
            np.random.random()*(
                CONFIG['global']['width']-self.surf.get_width()
            ),
            np.random.random()*(
                CONFIG['global']['height']-self.surf.get_height()
            )
        ])
        distance = end_pos-start_pos
        amplitude = np.linalg.norm(distance)
        duration = np.random.uniform(
            CONFIG['saccade']['min_duration'],
            CONFIG['saccade']['max_duration']
        )
        velocity = distance / duration

        return EyeMovement(
            'saccade', start_pos, end_pos,
            amplitude, velocity, duration
        )

    def _generatePursuit(self, start_pos):
        """
        Generate and return a pursuit, of 
            - random direction
            - random amplitude 
            - random velocity 
            - random duration.
        """

        # Find an acceptable destination with respect
        # to the velocity constraints
        velocity_condition_respected = False
        while not velocity_condition_respected:
            end_pos = np.array([
                np.random.random()*(
                    CONFIG['global']['width']-self.surf.get_width()
                ),
                np.random.random()*(
                    CONFIG['global']['height']-self.surf.get_height()
                )
            ])
            duration = np.random.uniform(
                CONFIG['pursuit']['min_duration'],
                CONFIG['pursuit']['max_duration']
            )
            distance = end_pos-start_pos
            amplitude = np.linalg.norm(distance)
            velocity = distance / duration
            vel_norm = np.linalg.norm(velocity)
            if (CONFIG['pursuit']['min_vel'] <= vel_norm) \
                    and (CONFIG['pursuit']['max_vel'] >= vel_norm):
                velocity_condition_respected = True

        return EyeMovement(
            'pursuit', start_pos, end_pos,
            amplitude, velocity, duration
        )

    def updatePos(self, x, y):
        """
        Update target position.
        """

        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

        return
