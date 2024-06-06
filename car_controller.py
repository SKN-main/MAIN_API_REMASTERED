import sys
import threading
from time import sleep

import serial

MAX_SPEED = 100
MIN_SPEED = -100

MAX_WHEEL_ROTATION = 100
MIN_WHEEL_ROTATION = -100


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
            print("Init completed")
            self._serial.flushInput()
            self._serial.flushOutput()
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            self._serial = None

        self.sensor_data = [0, 0, 0, 0, 0, 0]  # car has 6 sensors

        if output is not None:
            threading.Thread(target=self.read, daemon=True).start()

    def turn(self, rotation):
        """
        Turn the robot by the specified angle. Positive is counter-clockwise.
        In percentage, 100 is full speed counter-clockwise, -100 is full speed clockwise.
        """
        if rotation == self._current_wheel_rotation:
            return
        print(f"Turning by {rotation}")

        if rotation < MIN_WHEEL_ROTATION:
            rotation = MIN_WHEEL_ROTATION
        elif rotation > MAX_WHEEL_ROTATION:
            rotation = MAX_WHEEL_ROTATION

        self._current_wheel_rotation = rotation

        print(f"Setting wheel rotation to {self._current_wheel_rotation}")
        self.send()

    def set_speed(self, value):
        """
        Set the speed of both wheels.
        """
        if value == self._current_speed:
            return
        self._current_speed = min(max(value, -MAX_SPEED), MAX_SPEED)
        self.send()

    def send(self):
        """
        Send a packet to the controller directly. Low-level.
        """
        if self._serial:
            print(f"Sending speed: {self._current_speed}, wheel rotation: {self._current_wheel_rotation}")
            packet = f'{self._current_speed};{self._current_wheel_rotation};\n'
            try:
                self._serial.write(bytes(packet, 'utf-8'))
                print("message sent")
            except serial.SerialException as e:
                print(f"Error writing to serial: {e}")

    def read(self):
        """
        Read the serial port and parse incoming packets.
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
        self.reset_car()

    def reset_car(self):
        self._current_speed = 0
        self._current_wheel_rotation = 0
        self.send()


if __name__ == '__main__':
    controller = Controller()
    print(controller)

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
