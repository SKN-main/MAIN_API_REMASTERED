#include <Arduino.h>
#include <Servo.h>


const int MOTOR_PIN = 23; // Temporary - Yaw (mf 50 - slightly left, mr 50 - slightly right)
const int STEERING_PIN = 22; //Temporary - Pitch (sl 80 is front (NEVER GO ABOVE 90); sr 80 is up)

/*
src zaświecić
dać 0 
Zaczekać aż zaświeci

sterowanie z servo
*/

Servo steeringMotor;
Servo forwardMotor;

int m_zeroPWMSignalInMicroseconds = 1500;
int m_minimumPWMSignalLengthInMicroseconds = 1100; //1000
int m_maximumPWMSignalLengtoInMicroseconds = 1900; //2000

// trim wartosc dodana to kazdego paramteru zmieniajaca polozenie ale zakres dlaej nie moze przejsc powyzej lub ponizej maximum/minimum
// check sumy i znaki poczatku i konca

// void steer(int steer_value) {
//   steer_value =

// }

void setNeutral(){
  forwardMotor.writeMicroseconds(1500);
  steeringMotor.writeMicroseconds(1500);
}

bool isValidRange(int value) {
  return value >= -100 && value <= 100;
}

void parseCommand(String command) {
  command.trim();  // Remove any leading or trailing whitespace
  int separatorIndex = command.indexOf(';');

  if (separatorIndex == -1 || command.lastIndexOf(';') == separatorIndex) {
    Serial.println("Invalid command format. Please use speed;turn;");
    return;
  }

  String speedString = command.substring(0, separatorIndex);
  String turnString = command.substring(separatorIndex + 1, command.length() - 1);

  int speed = speedString.toInt();
  int turn = turnString.toInt();

  if (isValidRange(speed) && isValidRange(turn)) {
    
    int speedPWM = map(speed, -100, 100, 1000, 2000);
    int turnPWM = map(turn, -100, 100, 1000, 2000);
    Serial.println("-----------");
    Serial.print("Speed: ");
    Serial.println("");
    Serial.print(speedPWM);
    Serial.print("|");
    Serial.println(speed);
    Serial.print("Turn: ");
    Serial.println("");
    Serial.print(turnPWM);
    Serial.print("|");
    Serial.println(turn);
    Serial.println("-----------");
    forwardMotor.writeMicroseconds(speedPWM);
    steeringMotor.writeMicroseconds(turnPWM);
    // Add your code here to handle speed and turn values
  } else {
    Serial.println("Values out of range. Please use values between -100 and 100.");
  }
}

void setup() {
  // put your setup code here, to run once:
  steeringMotor.attach(STEERING_PIN);
  forwardMotor.attach(23);
  Serial.begin(115200);
  //m_steeringPWM.attach(m_PWMControlPin, m_minimumPWMSignalLengthInMicroseconds, m_maximumPWMSignalLengtoInMicroseconds);
  forwardMotor.writeMicroseconds(1500);
  steeringMotor.writeMicroseconds(1500);
  delay(1000);
}

String tekst = "brak";

void loop() {
  // put your main code here, to run repeatedly:
  // servoMotor.writeMicroseconds(1100);
  // delay(1000);
  // servoMotor.writeMicroseconds(1900);
  // delay(1000);

  // steeringMotor.writeMicroseconds(1100);
  // delay(1000);
  // steeringMotor.writeMicroseconds(1900);
  // delay(1000);

  // steeringMotor.writeMicroseconds(1400);
  // forwardMotor.writeMicroseconds(1500); Połączyć pin 5 voltowe
  // delay(1000); LARP
  // steeringMotor.writeMicroseconds(1600);
  // forwardMotor.writeMicroseconds(1500);
  // delay(1000);
  // steeringMotor.writeMicroseconds(1100);
  // forwardMotor.writeMicroseconds(1500);
  // delay(1000);

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the command from the serial
    parseCommand(command);
  }

}
