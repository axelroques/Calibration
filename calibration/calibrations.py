
from __init__ import CONFIG
from target import Target

from itertools import cycle
import pygame


class Calibration:

    def __init__(self, screen) -> None:

        # Exit condition
        self.early_break = False

        self.screen = screen
        self.running = True
        self.fps = 100

        # Initialize time series data structure for export
        self.data = {
            't': [],
            'x': [],
            'y': []
        }

    def getStimulusMovements(self):
        """
        Return stimulus movements.
        """
        return self.movement_queue

    def _run(self):
        """
        Launch experiment.
        """

        # Initialize target
        self.target = Target()

        # Generate an event queue
        self.movement_queue = self._generateMovementQueue()

        # Game clock
        self.clock = pygame.time.Clock()

        while self.running:

            for movement in self.movement_queue:

                # Get appropriate target behavior
                try:
                    self._updateTargetBehavior(movement)

                except RuntimeWarning:
                    self.early_break = True
                    break

                # Update time series data
                self.data['t'] += movement.timestamps
                self.data['x'] += movement.positions['x']
                self.data['y'] += movement.positions['y']

            # Once all movements are done, exit
            self.running = False

        return

    def _catchExit(self, event):
        """
        Exit handler.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                return RuntimeWarning
        if event.type == pygame.QUIT:
            self.running = False
            raise RuntimeWarning

    def _draw(self):
        """
        Draw function.
        """

        # Draw background
        self.screen.fill(CONFIG['global']['bg_color'])

        # Draw target
        self.screen.blit(self.target.surf, self.target.rect)

        # Display
        pygame.display.flip()

        return

    def _updateTargetBehavior(self, movement):
        """
        Deal with movement types.
        """

        updates = {
            'fixation': self._handleFixation,
            'saccade': self._handleSaccade,
            'pursuit': self._handlePursuit
        }

        # Update target position
        updates[movement.type](movement)

        return

    def _handleFixation(self, movement):
        """
        Deal with fixation movement.

        A fixation does not move so nothing to do
        here really.
        """

        # Initialize output variables
        timestamps = []
        positions = {
            'x': [],
            'y': []
        }

        time = 0
        duration = movement.duration*1000
        # print(
        #     f'Fixation: t={duration/1000}s, amplitude={movement.amplitude}, start={movement.start_pos}, end={movement.end_pos}, vel={movement.velocity}'
        # )
        while time < duration:

            # Draw
            self._draw()

            # Catch exit
            for event in pygame.event.get():
                self._catchExit(event)

            # Get timestamp
            timestamps.append(time)

            # Get position
            positions['x'].append(self.target.x)
            positions['y'].append(self.target.y)

            # Update clock
            self.clock.tick(self.fps)

            # Increment time
            time += self.clock.get_time()

        # Populate movement info
        movement.addTimestamps(timestamps)
        movement.addPositions(positions)

        return

    def _handleSaccade(self, movement):
        """
        Deal with saccade movement.

        At half of the saccade's duration, actually
        move the saccade towards its destination.
        """

        # Initialize output variables
        timestamps = []
        positions = {
            'x': [],
            'y': []
        }

        time = 0
        duration = movement.duration*1000
        # print(
        #     f'Saccade: t={duration/1000}s, amplitude={movement.amplitude}, start={movement.start_pos}, end={movement.end_pos}, vel={movement.velocity}'
        # )
        while time < duration:

            # Draw
            self._draw()

            # Catch exit
            for event in pygame.event.get():
                self._catchExit(event)

            # Get timestamp
            timestamps.append(time)

            # Get position
            positions['x'].append(self.target.x)
            positions['y'].append(self.target.y)

            # Move the target towards its destination
            if time >= duration/2:
                self.target.updatePos(*movement.end_pos)

            # Update clock
            self.clock.tick(self.fps)

            # Increment time
            time += self.clock.get_time()

        # Populate movement info
        movement.addTimestamps(timestamps)
        movement.addPositions(positions)

        return

    def _handlePursuit(self, movement):
        """
        Default function that will be overwitten if 
        necessary.
        """
        return


class BinaryCalibration(Calibration):

    def __init__(self, screen) -> None:
        super().__init__(screen)

        self.type = 'binary_calibration'

        self._run()

    def _generateMovementQueue(
        self,
        t_max=CONFIG['global']['exp_duration']
    ):
        """
        Generate stimulus movements until the total 
        duration reaches the maxmimum experiment time
        (3 minutes by default).
        """

        # Start with a fixation
        start_pos = self.target._getPos()
        movement_queue = [
            self.target._generateFixation(start_pos)
        ]
        total_duration = movement_queue[-1].duration

        # Cycle over saccade and fixation movements until
        # the duration criteria is respected
        for generateMovement in cycle([
            self.target._generateSaccade,
            self.target._generateFixation
        ]):

            if total_duration >= t_max*60:
                break

            # Generate and store the new movement
            movement = generateMovement(start_pos)
            movement_queue.append(movement)

            # Starting position of the next movement
            # is the end_pos of the previous one
            start_pos = movement.end_pos

            # Update total movement duration
            total_duration += movement.duration

        return movement_queue


class TernaryCalibration(Calibration):

    def __init__(self, screen) -> None:
        super().__init__(screen)

        self.type = 'ternary_calibration'

        self._run()

    def _generateMovementQueue(
        self,
        t_max=CONFIG['global']['exp_duration']
    ):
        """
        Generate stimulus movements until the total 
        duration reaches the maxmimum experiment time
        (3 minutes by default).
        """

        # Start with a fixation
        start_pos = self.target._getPos()
        movement_queue = [
            self.target._generateFixation(start_pos)
        ]
        total_duration = movement_queue[-1].duration

        # Cycle over saccade and fixation movements until
        # the duration criteria is respected
        for generateMovement in cycle([
            self.target._generateSaccade,
            self.target._generateFixation,
            self.target._generatePursuit,
            self.target._generateFixation
        ]):

            if total_duration >= t_max*60:
                break

            # Generate and store the new movement
            movement = generateMovement(start_pos)
            movement_queue.append(movement)

            # Starting position of the next movement
            # is the end_pos of the previous one
            start_pos = movement.end_pos

            # Update total movement duration
            total_duration += movement.duration

        return movement_queue

    def _handlePursuit(self, movement):
        """
        Deal with pursuit movement.
        """

        # Initialize output variables
        timestamps = []
        positions = {
            'x': [],
            'y': []
        }

        time = 0
        duration = movement.duration*1000
        # print(
        #     f'Pursuit: t={duration/1000}s, amplitude={movement.amplitude}, start={movement.start_pos}, end={movement.end_pos}, vel={movement.velocity}'
        # )
        while time < duration:

            # Draw
            self._draw()

            # Catch exit
            for event in pygame.event.get():
                self._catchExit(event)

            # Get timestamp
            timestamps.append(time)

            # Get position
            positions['x'].append(self.target.x)
            positions['y'].append(self.target.y)

            # Move the target towards its destination
            deltaT = self.clock.get_time()/1000
            x_increment = deltaT * movement.velocity[0]
            y_increment = deltaT * movement.velocity[1]
            self.target.updatePos(
                self.target.x + x_increment,
                self.target.y + y_increment
            )

            # Update clock
            self.clock.tick(self.fps)

            # Increment time
            time += self.clock.get_time()

        # Final movement
        self.target.updatePos(*movement.end_pos)
        timestamps.append(time)
        positions['x'].append(self.target.x)
        positions['y'].append(self.target.y)

        # Populate movement info
        movement.addTimestamps(timestamps)
        movement.addPositions(positions)

        return
