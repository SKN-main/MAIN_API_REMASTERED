import sys
import threading

MAX_SPEED = 100
MIN_SPEED = -100


class Controller:
    def __init__(self, output=sys.stdout):
        self._current_turn = 0
        self._current_speed = 0
        self._output = output
        self.turn = 0
        self.speed = 0
        self.sensor_data = [0, 0, 0, 0, 0, 0]  # car has 6 sensors (2 front-left, 2 front, 2 front-right)

        """This code creates a new thread that will run the self.read method in the background.
        The main program will continue execution without waiting for the self.read method to finish.
        The daemon=True flag ensures that the program can exit even if the self.read method is still.
        running in the background thread."""
        if output is not None:
            threading.Thread(target=self.read, daemon=True).start()

    # def help(self):
    #     """Print the car's help message to the output."""
    #     self.send('help\n')
    #
    # def test(self):
    #     """Run self test. Will move the wheels at full speed!"""
    #     self.send('selftest\n')

    @property
    def turn(self):
        return self._current_turn

    @turn.setter
    def turn(self, angle):
        """Turn the robot by the specified angle. Positive is counter-clockwise."""
        if angle == self._current_turn:
            return

        max_angle = 30
        turn_level_per_degree = 100 / max_angle
        turn_level = int(abs(angle) * turn_level_per_degree)
        turn_level = min(turn_level, 100)

        self._current_turn = min(max(turn_level, -max_angle), max_angle)

        self.send(packet='data')

    @property
    def speed(self):
        return self._current_speed

    @speed.setter
    def speed(self, value):
        """Set the speed of both wheels."""
        if value == self._current_speed:
            return
        # Constraint the speed to the [-max_speed; max_speed] range
        self._current_speed = min(max(value, -MAX_SPEED), MAX_SPEED)
        self.send(packet='data')

    def send(self, packet='data'):
        """Send a packet to the controller directly. Low-level."""
        if packet == 'data':
            packet = (f'{self._current_speed};{self._current_turn};'
                      f'{self.sensor_data[0]};{self.sensor_data[1]};'
                      f'{self.sensor_data[2]};{self.sensor_data[3]};'
                      f'{self.sensor_data[4]};{self.sensor_data[5]};')

        self._output.write(packet)

    def read(self):
        """Read the serial port and parse incoming packets."""
        example_data = '-12;23;50;56;23;32;65;34'
        while True:
            self.speed = int(example_data.split(';')[0])
            self.turn = int(example_data.split(';')[1])
            self.sensor_data = [int(x) for x in example_data.split(';')[2:]]
            self.send()
            break

    def __repr__(self):
        return f'Car(turn={self.turn}, speed={self.speed})'


if __name__ == '__main__':
    controller = Controller()
    controller.read()
    controller.turn = 21
    controller.speed = -0.1
    controller.speed = 0.2
