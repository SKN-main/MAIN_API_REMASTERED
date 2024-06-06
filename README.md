# MAIN_API_REMASTERED

This project is a Python-based car controller that communicates with a car via a serial port.

## Controller Class

The `Controller` class in `car_controller.py` is the main entry point of the application. It can be used to control the car's speed and wheel rotation.

### Methods

- `__init__(self, output=sys.stdout, port='/dev/ttyACM0')`: Initializes the controller with serial communication and default values. Starts a background thread to read data from the car if an output is provided.

- `turn(self, rotation)`: Turns the wheels of the car by a specified rotation. The rotation is expressed in percentage, where 100 is full counter-clockwise and -100 is full clockwise.

- `set_speed(self, value)`: Sets the speed of the car. The speed is expressed in percentage, where 100 is full speed forward and -100 is full speed backward.

- `send(self)`: Sends a packet to the controller directly. It sends the information about speed and wheel rotation which the user wants to apply to the car.

- `read(self)`: Reads the serial port and parses incoming packets. The incoming data format is "speed;wheel_rotation;sensor1;sensor2;...;sensor6;\n".

- `__repr__(self)`: Returns a string representation of the `Controller` object.

- `__del__(self)`: Resets the car to default values (speed = 0, wheel_rotation = 0) when the controller is closed.

- `reset_car(self)`: Resets the car to its default values (speed = 0, wheel_rotation = 0) and sends this information to the car.

### Values

- `speed`: The speed of the car, expressed in percentage. 100 is full speed forward, -100 is full speed backward, and 0 is stopped.
- `wheel_rotation`: The rotation of the wheels, expressed in percentage. 100 is full counter-clockwise, -100 is full clockwise, and 0 is straight.

## Requirements

- Python
- pyserial~=3.5

## Installation

1. Clone the repository
2. Install the required Python packages using pip:

```bash
pip install -r requirements.txt