#include <SharpIR.h>
#include <DualVNH5019MotorShield.h>
#include <Streaming.h>

#include <RunningMedian.h>

DualVNH5019MotorShield md;

/////////////// Motor Encoder Read
#define m1EncA 3 //Microcontroller pin 5, PORTD, PCINT2_vect, PCINT19
#define m1EncB 5 //Microcontroller pin 11, PORTD,PCINT2_vect, PCINT21
#define m2EncA 13 //Microcontroller pin 17, PORTB, PCINT0_vect, PCINT3
#define m2EncB 11 //Microcontroller pin 19, PORTB, PCINT0_vect, PCINT5

#define BLOCK_SIZE_CM 10 // CM

volatile int mCounter[2]; //0: RIGHT, 1: LEFT //M1: RIGHT, M2: LEFT
volatile int num = 0;
int turnRightTicks = 0;
volatile int setSpeeds[2] = {0, 0}; // 0: LEFT, 1: RIGHT
//Variables for PID to work
int lastTicks[2] = {0, 0};
int lastError;
int totalErrors;

long lastTime = millis();
int breakingI = 0;

long lastSensorTime = millis();

const int ONE_BLOCK = 1080 ; //1128
const int TWO_BLOCK = 1140 ; //1128
const int THREE_BLOCK = 1140 ; //1128
const int FOUR_BLOCK = 1145 ; //1128
const int FIVE_BLOCK = 1155 ; //1128
const int SIX_BLOCK = 1160 ; //1128
const int SEVEN_BLOCK = 1160 ; //1128
const int EIGHT_BLOCK = 1165 ; //1128
const int NINE_BLOCK = 1170 ; //1128
const int TEN_BLOCK = 1170 ; //1128
const int MORE_THAN_ONE_BLOCK = 1128; //1128

#define SPEED_EXPLORE 300
#define SPEED_ROTATION 200

/////////////// Motor Encoder Read

// Message Queue for FW,L,R operations
#define INPUT_SIZE 30


// SharpIR Sensor START
int irPinRF = A0; //PS1
int irPinRB = A1; //PS2
int irPinFF = A2; //PS3
int irPinFR = A3; //PS4
int irPinLL = A4; //PS5
int irPinFL = A5; //PS6

SharpIR FL(irPinFL, 1080);
SharpIR FF(irPinFF, 1080);
SharpIR FR(irPinFR, 1080);
SharpIR RF(irPinRF, 1080);
SharpIR LL(irPinLL, 1080);
SharpIR RB(irPinRB, 20150);
// SharpIR Sensor END

// declaration for encoder, encoder pulse interupt and rpm calculation
unsigned long cPulse1 = 0;
unsigned long cPulse2 = 0;
unsigned long prevT1 = 0;
unsigned long prevT2 = 0;
long cTime = 0;
long pTime = 0;

long ticks1 = 0;
long ticks2 = 0;

long tCount1 = 0;
long tCount2 = 0;
//number of samples
int sample1 = 0;
int sample2 = 0;
int count = 0;


//movement declaration
int moveCounter;
bool startRun;

char inputString[INPUT_SIZE + 1];
bool stringComplete = false;


volatile int oneSecondTimer = 0;

//flag
bool isMotorMoving = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); // serial
  Serial.setTimeout(50);
  setupMovement();

  // Setup Interrupt Timers
  // https://www.instructables.com/id/Arduino-Timer-Interrupts/
  // http://maxembedded.com/2011/06/avr-timers-timer0/
  // Use Excel to compute the required timer count for OCR#A
  // compare match register = [ 16,000,000 / (prescaler * desired interrupt frequency) ] - 1
  // Remember that when you use timers 0 and 2 this number must be less than 256, and less than 65536 for timer1
  noInterrupts();
  //  //  // Trigger every 1ms
  //  TCCR0A = 0;                          // Reset TCCR0A to 0
  //  TCCR0B = 0;                          // Reset TCCR0B to 0
  //  TCNT0 = 0;                           // initialize counter value to 0
  //  OCR0A = 249;                         // 16,000,000 / (64 * 249)
  //  TCCR0A |= (1 << WGM01);              // Enable CTC mode
  //  TCCR0B |= (1 << CS01) | (1 << CS00); // Enable 64 prescaler
  //  TIMSK0 |= (1 << OCIE0A);             // Enable Timer Compare Interrupt

  //
  // Trigger every 1s
  //http://maxembedded.com/2011/06/avr-timers-timer1/
  //  TCCR1B |= (1 << CS11);
  //  TCNT1 = 0;
  //  TIMSK1 |= (1 << TOIE1);
  //  OCR1A = 15625;
  //  oneSecondTimer = 0;
  //http://maxembedded.com/2011/06/avr-timers-timer1/
  //
  interrupts();

  // END Setup Interrupt Timers
}

void loop() {
  // put your main code here, to run repeatedly:
  if (stringComplete)
  {
    receiveMessage();
    memset(inputString, 0, sizeof(inputString));
    stringComplete = false;
  }
  MovementRoutine();
}

// Processing incoming data
void serialEvent()
{
  while (Serial.available())
  {
    byte size = Serial.readBytesUntil('\n', inputString, INPUT_SIZE);
    if (size > 0)
    {
      stringComplete = true;
    }
  }
}

// Message Handling from RPi
// NOTE: We read in leftSpeed and rightSpeed, the speed setting for md
// The model is created in the RPi, and the
double leftSpeed, leftRPM, rightSpeed, rightRPM = 0;
char *separator;

// https://arduino.stackexchange.com/a/3994
// Maximum number of commandParameters substrings expected
const int MAX_SUBSTRINGS = 5;
// Array of pointers to each substring after displayString() has been called
static char *commandParameters[MAX_SUBSTRINGS];
void parseParameters(char *s)
{
  // First clear the array of substrings
  for (int i = 0; i < MAX_SUBSTRINGS; i++)
    commandParameters[i] = 0;
  // Now split the input string
  char *text = strtok(s, ":");
  int i = 0;
  while (text != 0 && i < MAX_SUBSTRINGS)
  {
    // A token was found: append it to the array of substrings
    commandParameters[i++] = text;
    text = strtok(0, ":");
  }
}
// https://arduino.stackexchange.com/a/3994
void readSensors(bool rawValues = false) {
  int data[6];
  data[0] = cmToBlocks(medianMulti(FL, 3) - 4);
  data[1] = cmToBlocks(medianMulti(FF, 9) - 4);
  data[2] = cmToBlocks(medianMulti(FR, 9) - 5);
  data[3] = cmToBlocks(medianMulti(LL, 5) - 3);
  data[4] = cmToBlocks(medianMulti(RB, 9) - 15);
  data[5] = cmToBlocks(medianMulti(RF, 5) - 4);
  
  Serial.print("SDATA,");
  Serial.print(data[0]);
  Serial.print(",");
  Serial.print(data[1]);
  Serial.print(",");
  Serial.print(data[2]);
  Serial.print(",");
  Serial.print(data[3]);
  Serial.print(",");
  Serial.print(data[4]);
  Serial.print(",");
  Serial.print(data[5]);
  Serial.print("\n");
  Serial.flush();

  isMotorMoving = false;
}

// returns the median value of the sensor data
int medianMulti(SharpIR sensor, int count) {
  RunningMedian sample = RunningMedian(count);
  for (int i = 0; i < count; i++) {
    sample.add(sensor.distance());
  }
  return sample.getMedian();
}

int cmToBlocks(int distance) {
  return (floor)(distance / BLOCK_SIZE_CM);
}

void receiveMessage()
{
  char *command = strtok(inputString, '\n');
  int count = 0;
  while (command != NULL)
  {
    switch (command[count])
    {
      //Read sensor
      case 'I':
        pushQueue('I');
        break;

      // Calibration
      case 'C':
        pushQueue('C');
        break;

      // Directionals
      case 'F': // Move forward 1 block
      case '1':
        pushQueue('F');
        break;
      case '2': // Move forward 2 block
        pushQueue('2');
        break;
      case '3': // Move forward 3 block
        pushQueue('3');
        break;
      case '4': // Move forward 4 block
        pushQueue('4');
        break;
      case '5': // Move forward 5 block
        pushQueue('5');
        break;
      case '6': // Move forward 6 block
        pushQueue('6');
        break;
      case '7': // Move forward 7 block
        pushQueue('7');
        break;
      case '8': // Move forward 8 block
        pushQueue('8');
        break;
      case '9': // Move forward 9 block
        pushQueue('9');
        break;
      case '0': // Move forward 10 block
        pushQueue('0');
        break;

      case 'B':
        pushQueue('B');
        break;

      case 'L':
        pushQueue('L');
        break;

      case 'R':
        pushQueue('R');
        break;

      default:
        Serial.print("Unrecognised Character: ");
        Serial.print(command[0]);
        Serial.println();

        memset(inputString, 0, sizeof(inputString));
        stringComplete = false;
        break;
    }

    if (command[count+1] != NULL) {
      count++;
    } else {
      command = strtok(0, '; ');
    }
  }
}

//---------------------------------------------------------------------Movement Function Start---------------------------------------------------------------------//

volatile int angle = 0;
volatile int distance = 0;
volatile int currentDirection = 0;

#define MOVEMENT_QUEUE_SIZE 24 //12

char movementQueue[MOVEMENT_QUEUE_SIZE];
int readQueue = 0;
int writeQueue = 0;

void pushQueue(char direction) {
  movementQueue[writeQueue] = direction;
  writeQueue = (writeQueue + 1) % MOVEMENT_QUEUE_SIZE;
}

bool queueHasNewValue() {
  if (movementQueue[((readQueue) % MOVEMENT_QUEUE_SIZE)] != 0) {
    return true;
  }
  return false;
}

bool queueHasNextValue() {
  if (movementQueue[((readQueue + 1) % MOVEMENT_QUEUE_SIZE)] == 0) {
    return false;
  }

  return true;
}

void popQueue() {
  switch (movementQueue[readQueue]) {
    case 'I':
      isMotorMoving = true;
      readSensors();
      break;
    case 'F':
      currentDirection = 1;
      movementForward(1);
      break;

    case '2':
      currentDirection = 1;
      movementForward(2);
      break;
    case '3':
      currentDirection = 1;
      movementForward(3);
      break;
    case '4':
      currentDirection = 1;
      movementForward(4);
      break;
    case '5':
      currentDirection = 1;
      movementForward(5);
      break;
    case '6':
      currentDirection = 1;
      movementForward(6);
      break;
    case '7':
      currentDirection = 1;
      movementForward(7);
      break;
    case '8':
      currentDirection = 1;
      movementForward(8);
      break;
    case '9':
      currentDirection = 1;
      movementForward(9);
      break;
    case '0':
      currentDirection = 1;
      movementForward(10);
      break;

    case 'C':
      calibrateMovement();
      break;

    case 'B':
      currentDirection = 4;
      movementBackward(1);
      break;

    case 'L':
      currentDirection = 2;
      movementRotateLeft(89);
      break;

    case 'R':
      movementRotateRight(89);
      break;
  }
  movementQueue[readQueue] = 0;
  readQueue = (readQueue + 1) % MOVEMENT_QUEUE_SIZE;
}

void setupMovement()
{
  md.init();           //motor init

  pinMode(m1EncA, INPUT); //Microcontroller pin 5, PORTD, PCINT2_vect, PCINT19
  pinMode(m1EncB, INPUT); //Microcontroller pin 11, PORTD,PCINT2_vect, PCINT21
  pinMode(m2EncA, INPUT); //Microcontroller pin 17, PORTB, PCINT0_vect, PCINT3
  pinMode(m2EncB, INPUT);

  pciSetup(m1EncA); //Microcontroller pin 5, PORTD, PCINT2_vect, PCINT19
  pciSetup(m1EncB); //Microcontroller pin 11, PORTD,PCINT2_vect, PCINT21
  pciSetup(m2EncA); //Microcontroller pin 17, PORTB, PCINT0_vect, PCINT3
  pciSetup(m2EncB);
}

void resetMotorCounters() {
  // Reset Motor
  currentDirection = 0;
  turnRightTicks = 0;
  resetMCounters();
  lastError = 0;
  totalErrors = 0;
  lastTicks[0] = 0;
  lastTicks[1] = 0;
}

void movementForward(int numBlocks)
{
  // Movement Forward
  distance = blockToTicks(numBlocks);

  setSpeeds[0] = SPEED_EXPLORE; // LEFT
  setSpeeds[1] = SPEED_EXPLORE; // RIGHT

  resetMotorCounters();

  md.setSpeeds(setSpeeds[1], setSpeeds[0]);
  lastTime = -1;
  breakingI = 0;

  // set Motor Direction
  currentDirection = 1;

  isMotorMoving = true;
}

void movementBackward(int numBlocks)
{
  // Movement Forward
  distance = blockToTicks(numBlocks);

  setSpeeds[0] = -SPEED_EXPLORE; // LEFT
  setSpeeds[1] = -SPEED_EXPLORE; // RIGHT

  resetMotorCounters();

  md.setSpeeds(setSpeeds[1], setSpeeds[0]);
  lastTime = -1;
  breakingI = 0;

  // set Motor Direction
  currentDirection = 4;

  isMotorMoving = true;
}

void movementRotateLeft(int numGivenAngle)
{
  // Turn Left
  angle = angleToTicksLeft(numGivenAngle);

  setSpeeds[0] = -SPEED_ROTATION; // LEFT
  setSpeeds[1] = SPEED_ROTATION; // RIGHT

  resetMotorCounters();

  // set Motor Direction
  currentDirection = 2;

  md.setSpeeds(setSpeeds[1], setSpeeds[0]); // RIGHT, LEFT

  lastTime = -1;
  breakingI = 0;

  isMotorMoving = true;
}

void movementRotateRight(int numGivenAngle)
{
  // Turn Right
  angle = angleToTicksRight(numGivenAngle);

  setSpeeds[0] = SPEED_ROTATION; // LEFT
  setSpeeds[1] = -SPEED_ROTATION; // RIGHT

  resetMotorCounters();

  // set Motor Direction
  currentDirection = 3;

  md.setSpeeds(setSpeeds[1], setSpeeds[0]); // RIGHT, LEFT
  lastTime = -1;
  breakingI = 0;

  isMotorMoving = true;
}

// Calibrate to blocks in directly in front of top left and right sensors
void calibrateMovement() {
  float sensor_left = FL.distance();
  float sensor_right = FR.distance();
  char prevTurn, curTurn;
  bool firstTime = true;
    while ((sensor_left < 8.60 || sensor_left > 8.66) || (sensor_right < 9.82 || sensor_right > 9.88)){
    //left side
    if (sensor_left > 8.66) {
      md.setM2Speed(SPEED_EXPLORE);
      delay(5);
      md.setM2Brake(350);
      delay(15);
    } else if (sensor_left < 8.60) {
      md.setM2Speed(-SPEED_EXPLORE);
      delay(6);
      md.setM2Brake(350);
      delay(15);
    }
    //right side
    if (sensor_right > 9.88) {
      md.setM1Speed(SPEED_EXPLORE);
      delay(5);
      md.setM1Brake(350);
      delay(15);
    } else if (sensor_right < 9.82) {
      md.setM1Speed(-SPEED_EXPLORE);
      delay(6);
      md.setM1Brake(350);
      delay(15);
    }
    sensor_left = FL.distance();
    sensor_right = FR.distance();
    delay(10);
  }
  delay(200);
}

//---------------------------------------------------------------------Movement Function END-----------------------------------------------------------------------//

//---------------------------------------------------------------------PID Function Start-------------------------------------------------------------------------//

void readSensorRoutine() {
  if (millis() - lastSensorTime > 200) {
    readSensors();
    lastSensorTime = millis();
  }
}

void MovementRoutine() {

  if (!isMotorMoving && queueHasNewValue()) {
    popQueue();
    return;
  }

  if (isMotorMoving) {
    switch (currentDirection) {
      case 1: // FORWARD
        if (mCounter[0] < distance && mCounter[1] < distance) {
          PIDControl(&setSpeeds[1], &setSpeeds[0], 200, 3.3, 17, 0.5); //By block 50, 0, 80, 0
          md.setSpeeds(setSpeeds[1], setSpeeds[0]);
          delay(5);
        } else {
          md.setBrakes(400, 373);
          delay(200);
          isMotorMoving = false;
          resetMCounters();
        }
        break;

      case 2: // LEFT
        if (mCounter[0] < angle && mCounter[1] < angle ) {
          PIDControl(&setSpeeds[1], &setSpeeds[0], 200, 0, 14.9, -1); //150 ,6 ,15 , -1
          md.setSpeeds(setSpeeds[1], setSpeeds[0]);
          delay(5);
        } else {
          md.setBrakes(400, 375);
          delay(200);
          isMotorMoving = false;
          resetMCounters();
        }
        break;

      case 3:// RIGHT
        if (mCounter[0] < angle && mCounter[1] < angle ) {
          PIDControl(&setSpeeds[1], &setSpeeds[0], 300, 0.9, 5.6, 1); //300, 0 , 5.6
          md.setSpeeds(setSpeeds[1], setSpeeds[0]);
          delay(5);
        } else {
          md.setBrakes(375, 375);
          delay(200);
          isMotorMoving = false;
          resetMCounters();
        }
        break;

      case 4: // BACKWARD
        if (mCounter[0] < distance && mCounter[1] < distance) {
//           PIDControl(&setSpeeds[1], &setSpeeds[0], 100, 0, 0, 0); //By block 50, 0, 80, 0
          md.setSpeeds(setSpeeds[1], setSpeeds[0]);
          breakingI = 0;

        } else {
          md.setBrakes(400, 400);
          isMotorMoving = false;
          resetMCounters();
        }
        break;

      default:
        // Nothing should happen
        break;
    }
  } else {
    if (queueHasNextValue()) {
      popQueue();
    }
  }
}

void PIDControl(int *setSpdR, int *setSpdL, int kP, int kI, int kD, int dr) {
  int adjustment;
  int error = (mCounter[1] - lastTicks[1]) - (mCounter[0] - lastTicks[0]);            //Proportional
  int errorRate = error - lastError;                                                  //Differential
  lastError = error;
  lastTicks[0] = mCounter[0];
  lastTicks[1] = mCounter[1];
  //totalErrors += 2;
  totalErrors += error;   //Integration, Add up total number  of errors (for Ki)

  adjustment = ((kP * error) + (kI * totalErrors) + (kD * errorRate)) / 100;   //Main PID calculation
  if (dr == 1 || dr == -1) {          //Go left or right
    *setSpdR += -adjustment * dr;
    *setSpdL -= adjustment * dr;
  }
  else {                              //Go forward
    *setSpdR += adjustment;           //Adjustments made here. Original speed + adjustment
    *setSpdL -= adjustment;

    if (*setSpdR > 400) {             //Limiter, to not go above 400
      *setSpdR = 400;
    }
    if (*setSpdL > 400) {
      *setSpdL = 400;
    }
  }
}

void resetMCounters() {
  mCounter[0] = 0;
  mCounter[1] = 0;
}

int blockToTicks(int blocks) {
  switch (blocks) {
    case 1:
      return ONE_BLOCK * 1;
    case 2:
      return TWO_BLOCK * 2;
    case 3:
      return THREE_BLOCK * 3;
    case 4:
      return FOUR_BLOCK * 4;
    case 5:
      return FIVE_BLOCK * 5;
    case 6:
      return SIX_BLOCK * 6;
    case 7:
      return SEVEN_BLOCK * 7;
    case 8:
      return EIGHT_BLOCK * 8;
    case 9:
      return NINE_BLOCK * 9;
    case 10:
      return TEN_BLOCK * 10;
  }
}

int angleToTicksRight(long angle)
{
  if (angle == 90)
    return 17330 * angle / 1000;
  else
    return (17330 * angle / 1000);
}

int angleToTicksLeft(long angle)
{
  if (angle == 90)
    return 17290 * angle / 1000;
  else
    return (17290 * angle / 1000);
}
//---------------------------------------------------------------------PID Function END---------------------------------------------------------------------//

//---------------------------------------------------------------------Encoder Function Start---------------------------------------------------------------------//

//ISR for Motor 1 (Right) Encoders
ISR(PCINT2_vect) {
  mCounter[0]++;
}

//ISR for Motor 2 (Left) Encoders
ISR(PCINT0_vect) {
  mCounter[1]++;
}

//Standard function to enable interrupts on any pins
void pciSetup(byte pin) {
  *digitalPinToPCMSK(pin) |= bit (digitalPinToPCMSKbit(pin));  // enable pin
  PCIFR  |= bit (digitalPinToPCICRbit(pin)); // clear any outstanding interrupt
  PCICR  |= bit (digitalPinToPCICRbit(pin)); // enable interrupt for the group
}


void fwdCorrection() {
  int pullDist = ((mCounter[0] - mCounter[1]) * 1) / 2;
  resetMCounters();

  if (pullDist > 0) {
    if (mCounter[0] < abs(pullDist)) {
      md.setM1Speed(-350);
    }
  }

  md.setBrakes(400, 400);
}
//---------------------------------------------------------------------Encoder Function END---------------------------------------------------------------------//
