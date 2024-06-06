import sys
import threading
from time import sleep

import serial

MAX_SPEED = 100
MIN_SPEED = -100

MAX_WHEEL_ROTATION = 100
MIN_WHEEL_ROTATION = -100


def clamp(value, min_value, max_value):
    """
    Clamp a value between a minimum and maximum value.
    :param value: _current_speed / _current_wheel_rotation
    :param min_value: MIN_SPEED / MIN_WHEEL_ROTATION
    :param max_value: MAX_SPEED / MAX_WHEEL_ROTATION
    :return: constrained value
    """
    return max(min(max_value, value), min_value)


class Controller:
    def __init__(self, output=sys.stdout, port='/dev/ttyACM0'):
        """
        Initialize the controller with serial communication and default values.
        """
        self._current_wheel_rotation = 0
        self._current_speed = 0
        self._output = output

        try:
            self._serial = serial.Serial(port=port, baudrate=115200, timeout=0.05)
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            self._serial = None

        self.sensor_data = [0, 0, 0, 0, 0, 0]  # car has 6 sensors

        if output is not None:
            threading.Thread(target=self.read, daemon=True).start()

    def turn(self, rotation):
        """
        Turn the wheels by the specified rotation. Positive is counter-clockwise.
        The rotation is expressed in percentage, 100 is full counter-clockwise, -100 is full clockwise.
        """
        if rotation == self._current_wheel_rotation:
            return

        rotation = clamp(rotation, MIN_WHEEL_ROTATION, MAX_WHEEL_ROTATION)

        self._current_wheel_rotation = rotation

        self.send()

    def set_speed(self, value):
        """
        Set the speed of the car.
        Positive is forward, negative is backward.
        The speed is expressed in percentage, 100 is full speed forward, -100 is full speed backward.
        """
        if value == self._current_speed:
            return

        value = clamp(value, MIN_SPEED, MAX_SPEED)

        self._current_speed = value
        self.send()

    def send(self):
        """
        Send a packet to the controller directly. Low-level.
        Sends the information about speed and wheel rotation which user want to apply to car.
        """
        if self._serial:
            packet = f'{self._current_speed};{self._current_wheel_rotation};\n'
            try:
                self._serial.write(bytes(packet, 'utf-8'))
            except serial.SerialException as e:
                print(f"Error writing to serial: {e}")

    def read(self):
        """
        Read the serial port and parse incoming packets.
        The incoming data format:
        "speed;wheel_rotation;sensor1;sensor2;...;sensor6;\n"
        """
        while True:
            if not self._serial:
                return
            try:
                data = self._serial.readline()
                if data:
                    data_str = data.decode('utf-8').strip()
                    self._output.write(data_str + '\n')
                    data_parts = data_str.split(';')
                    if len(data_parts) >= 8:
                        self._current_speed = int(data_parts[0])
                        self._current_wheel_rotation = int(data_parts[1])
                        self.sensor_data = [int(x) for x in data_parts[2:8]]
            except serial.SerialException as e:
                print(f"Error reading from serial: {e}")
            except ValueError as e:
                print(f"Data conversion error: {e}")

    def __repr__(self):
        return f'Car(turn={self._current_wheel_rotation}, speed={self._current_speed}, sensors={self.sensor_data})'

    def __del__(self):
        """
        When we close the controller, the car is reseted to default values. (speed = 0, wheel_rotation = 0)
        """
        self.reset_car()

    def reset_car(self):
        self._current_speed = 0
        self._current_wheel_rotation = 0
        self.send()


if __name__ == '__main__':
    controller = Controller()
    print(controller)

    # Tests for the car controller
    while True:
        sleep(0.5)
        controller.turn(100)
        sleep(0.5)
        controller.set_speed(-30)
        sleep(0.5)
        controller.turn(-100)
        sleep(0.5)
        controller.set_speed(30)
        sleep(0.5)
