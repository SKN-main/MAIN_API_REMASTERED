import sys
import threading
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
            self._serial.flushInput()
            self._serial.flushOutput()
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            self._serial = None

        self.sensor_data = [0, 0, 0, 0, 0, 0]  # car has 6 sensors

        if output is not None:
            threading.Thread(target=self.read, daemon=True).start()

    @property
    def turn(self):
        return self._current_wheel_rotation

    @turn.setter
    def turn(self, angle):
        """
        Turn the robot by the specified angle. Positive is counter-clockwise.
        """
        if angle == self._current_wheel_rotation:
            return

        turn_level_per_degree = 100 / MAX_WHEEL_ROTATION
        wheel_rotation = int(abs(angle) * turn_level_per_degree)
        wheel_rotation = min(wheel_rotation, MAX_WHEEL_ROTATION)

        self._current_wheel_rotation = min(max(wheel_rotation, -MAX_WHEEL_ROTATION), MAX_WHEEL_ROTATION)

        self.send()

    @property
    def speed(self):
        return self._current_speed

    @speed.setter
    def speed(self, value):
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
            packet = f'{self._current_speed};{self._current_wheel_rotation};'
            try:
                self._serial.write(bytes(packet, 'utf-8'))
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
        return f'Car(turn={self.turn}, speed={self.speed}, sensors={self.sensor_data})'


if __name__ == '__main__':
    controller = Controller()
    controller.turn = 21
    controller.speed = -10
    controller.speed = 10
