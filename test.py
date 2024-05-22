import sys
import threading
import json
import time

MAX_SPEED = 1
MIN_SPEED = -1

class Controller:
    def __init__(self, output=sys.stdout):
        self._current_turn = 0
        self._current_speed = 0
        self._output = output


        self.turn = 0
        self.speed = 0
        self.sensor_data = [0, 0, 0]

        """This code creates a new thread that will run the self.read method in the background.
        The main program will continue execution without waiting for the self.read method to finish.
        The daemon=True flag ensures that the program can exit even if the self.read method is still.
        running in the background thread."""
        if output is not None:
            threading.Thread(target=self.read, daemon=True).start()

    def help(self):
        """Print the car's help message to the output."""
        self.send('help\n')

    def test(self):
        """Run self test. Will move the wheels at full speed!"""
        self.send('selftest\n')

    
    @property
    def turn(self):
        return self._current_turn

    @turn.setter
    def turn(self, angle):
        """Turn the robot by the specified angle. Positive is counter-clockwise."""
        if angle == self._current_turn:
            return
        turn_direction = 'L' if angle > 0 else 'R'
        max_angle = 30
        turn_level_per_degree = 100 / max_angle
        turn_level = int(abs(angle) * turn_level_per_degree)
        turn_level = min(turn_level, 100)

        self._current_turn = min(max(angle, -max_angle), max_angle)

        json_message = json.dumps({
            'turn_direction': turn_direction,
            'turn_level': self._current_turn
            }
        )
        self.send(json_message)

    @property
    def speed(self):
        return self._current_speed

    @speed.setter
    def speed(self, value):
        """Set the speed of both wheels."""
        if value == self._current_speed:
            return
        if value == 0:
            self.stop()
            return
        move_direction = 'F' if value > 0 else 'R'
    
        speed_level = int(abs(value))
        speed_level = min(speed_level, MAX_SPEED)

        # Constraint the speed to the [-max_speed; max_speed] range
        self._current_speed = min(max(value, -MAX_SPEED), MAX_SPEED)

        json_message = json.dumps({
            'move_direction': move_direction,
            'speed_level': self._current_speed
            }
        )
        self.send(json_message)

    def stop(self):
        """Stop the car."""
        self._current_speed = 0

        json_message = json.dumps({
            'direction': 'S',
            'speed_level': 0
            }
        )
        self.send(json_message)

    def send(self, packet):
        """Send a packet to the controller directly. Low-level."""
        print(f'Sent: ')
        self._output.write(packet)
        print(f'\n')

    def read(self):
        """Read the serial port and parse incoming packets."""
        while True:
            # example data
            time.sleep(1)
            data = {
                'speed': controller.speed,
                'turn': controller.turn,
                'distance_sensors': [3, 4, 5],
                'accelerometer': 123
            }
            if data:
                speed = data['speed']
                turn = data['turn']
                distance_sensors = data['distance_sensors']
                accelerometer = data['accelerometer']
                print(f'speed: {speed}, turn: {turn}, '
                    f'distance_sensors[0]: {distance_sensors[0]}, '
                    f'distance_sensors[1]: {distance_sensors[1]}, '
                    f'distance_sensors[2]: {distance_sensors[2]}, '
                    f'accelerometer: {accelerometer}\n')

    def __repr__(self):
        return f'Controller(turn={self.turn}, speed={self.speed})'


if __name__ == '__main__':
    controller = Controller()
    controller.turn = 21
    controller.speed = -0.1
    controller.speed = 0.2