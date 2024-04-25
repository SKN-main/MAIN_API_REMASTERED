import sys
import threading

# import json

import serial


class Controller:
    def __init__(self, output=sys.stdout, port='/dev/ttyACM0'):
        self._current_turn = 0
        self._current_speed = 0
        self._output = output
        self._serial = serial.Serial(port=port, baudrate=115200, timeout=0.05)
        
        self._serial.flushInput()
        self._serial.flushOutput()
        
        self.turn = 0
        self.speed = 0

        """This code creates a new thread that will run the self.read method in the background. 
        The main program will continue execution without waiting for the self.read method to finish. 
        The daemon=True flag ensures that the program can exit even if the self.read method is still 
        running in the background thread."""
        if output is not None:
            threading.Thread(target=self.read, daemon=True).start()

    def help(self):
        """Print the car's help message to the output."""
        self.send('help\n')

    def test(self):
        """Run self test. Will move the wheels at full speed!"""
        self.send('selftest\n')


    """
    In Python, the @property decorator is used to create a property method. 
    A property method acts like an attribute but provides more control over how the 
    value is accessed and potentially modified.
    """
    @property
    def turn(self):
        return self._current_turn

    @turn.setter
    def turn(self, angle):
        """Turn the robot by the specified angle. Positive is counter-clockwise."""
        if angle == self._current_turn:
            return
        direction = 'L' if angle > 0 else 'R'
        max_angle = 30
        turn_level_per_degree = 100 / max_angle
        turn_level = int(abs(angle) * turn_level_per_degree)
        turn_level = min(turn_level, 100)

        self.send(f's{direction} {turn_level}\n')
        self._current_turn = min(max(angle, -max_angle), max_angle)

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
        direction = 'F' if value > 0 else 'R'
        max_speed = 100
        speed_level = int(abs(value) * 100 / max_speed)
        speed_level = min(speed_level, 100)

        self.send(f'm{direction} {speed_level}\n')
        self._current_speed = min(max(value, -max_speed), max_speed)

    def stop(self):
        self.send('mS 0\n')
        self._current_speed = 0

    def __del__(self):
        self._serial.close()

    def send(self, packet):
        """Send a packet to the controller directly. Low-level."""
        packet_bytes = bytes(packet, 'utf-8')
        self._serial.write(packet_bytes)

    def read(self):
        while True:
            data = self._serial.readline()
            if data:
                self._output.write(data.decode('utf-8'))

    def __repr__(self):
        return f'Controller(turn={self.turn}, speed={self.speed})'


if __name__ == '__main__':
    print()
