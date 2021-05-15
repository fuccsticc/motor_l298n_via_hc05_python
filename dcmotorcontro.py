// Control 2 DC motors (with L298N) via Bluetooth
// using RoboRemo app
// www.roboremo.com

// Hardware setup:
// BT module   Arduino
// GND ------- GND
// VCC ------- 5V
// TX-O ------ pin0
// RX-I ------ pin1


// L298N   Arduino pin
int IN_1A = 12;
int EN_1  = 11;
int IN_1B = 10;
int IN_2A = 4;
int EN_2  = 3;
int IN_2B = 2;


char cmd[100];
int cmdIndex;

int m1speed=0, m2speed=0;
int m1speedOld, m2speedOld;


boolean cmdStartsWith(const char *st) {
  for(int i=0; ; i++) {
    if(st[i]==0) return true;
    if(cmd[i]==0) return false;
    if(cmd[i]!=st[i]) return false;;
  }
  return false;
}


void onConnectionLost() {
  
  // stop motors
  
  analogWrite(EN_1, 0);
  digitalWrite(IN_1A, LOW);
  digitalWrite(IN_1B, LOW);
  analogWrite(EN_1, 255);

  analogWrite(EN_2, 0);
  digitalWrite(IN_2A, LOW);
  digitalWrite(IN_2B, LOW);
  analogWrite(EN_2, 255);
}

unsigned long lastCmdTime = 0;

void exeCmd() {

  lastCmdTime = millis();

  if(cmdStartsWith("m1 ") ) {
    m1speedOld = m1speed;
    m1speed = atoi(cmd+3);
    if(m1speed>0) {
      if(m1speedOld<0) {
        analogWrite(EN_1, 0);
      }
      // forward
      digitalWrite(IN_1A, HIGH);
      digitalWrite(IN_1B, LOW);
      analogWrite(EN_1, m1speed);
    }
    if(m1speed<0) {
      if(m1speedOld>0) {
        analogWrite(EN_1, 0);
      }
      // backward
      digitalWrite(IN_1A, LOW);
      digitalWrite(IN_1B, HIGH);
      analogWrite(EN_1, -m1speed);
    }
    if(m1speed==0) {
      analogWrite(EN_1, 0);
    }
  }


  if(cmdStartsWith("m2 ") ) {
    m2speedOld = m2speed;
    m2speed = atoi(cmd+3);
    if(m2speed>0) {
      if(m2speedOld<0) {
        analogWrite(EN_2, 0);
      }
      // forward
      digitalWrite(IN_2A, HIGH);
      digitalWrite(IN_2B, LOW);
      analogWrite(EN_2, m2speed);
    }
    if(m2speed<0) {
      if(m2speedOld>0) {
        analogWrite(EN_2, 0);
      }
      // backward
      digitalWrite(IN_2A, LOW);
      digitalWrite(IN_2B, HIGH);
      analogWrite(EN_2, -m2speed);
    }
    if(m2speed==0) {
      analogWrite(EN_2, 0);
    }
  }
}

void setup() {
  
  delay(500); // wait for bluetooth module to start

  Serial.begin(9600);
  // My Bluetooth default baud is 115200
  // for HC-05/06 it is usually 9600
  
  pinMode(EN_1, OUTPUT);
  analogWrite(EN_1, 0);
  pinMode(EN_2, OUTPUT);
  analogWrite(EN_1, 0);

  pinMode(IN_1A, OUTPUT);
  pinMode(IN_2A, OUTPUT);
  pinMode(IN_1B, OUTPUT);
  pinMode(IN_2B, OUTPUT);
  
  cmdIndex = 0;
}


void loop() {

  // if nothing received for 500ms
  if( millis() - lastCmdTime > 500) {
    onConnectionLost();
  }
  
  if(Serial.available()) {
    
    char c = (char)Serial.read();
    
    if(c=='\n') {
      cmd[cmdIndex] = 0;
      exeCmd();  // execute the command
      cmdIndex = 0; // reset the cmdIndex
    } else {      
      cmd[cmdIndex] = c;
      if(cmdIndex<99) cmdIndex++;
    } 
  }
}
