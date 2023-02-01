
class EyeMovement:

    def __init__(
        self, type, start_pos, end_pos,
        amplitude, velocity, duration
    ) -> None:

        self.type = type
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.amplitude = amplitude
        self.velocity = velocity
        self.duration = duration

    def addTimestamps(self, timestamps):
        """
        Add timestamps for the stimulus.
        """

        self.timestamps = timestamps

        return
    
    def addPositions(self, positions):
        """
        Add stimulus successive positions.
        """

        self.positions = positions

        return
