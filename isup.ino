

#define LEDPIN 13

#define NBLED 4

#define LEDA 12
#define LEDB 11
#define LEDC 10
#define LEDD 9

char sensorValue = 0;  // variable to store the value coming from the sensor
char outputValue = 0;  // value output to the PWM (analog out)

int leds[NBLED] = {LEDA, LEDB, LEDC, LEDD};


unsigned int bitfield = 0;


void setup() {
  
  Serial.begin(9600);
  pinMode(LEDPIN, OUTPUT);
  
  for(int i = 0; i < NBLED; i++){
     Serial.print("Setup = ");
     Serial.println(i);
     pinMode(leds[i], OUTPUT);
  }
}

void toggleLed(unsigned int bits){
   
  for(int i = 0; i < NBLED; i++){
     Serial.print("Bit read: ");
     unsigned int isOn = bitRead(bits, i);
     Serial.println(isOn);
     
     if (isOn){
       digitalWrite(leds[i], HIGH); 
     }else{
       digitalWrite(leds[i], LOW); 
     }
  }
}

void loop() {
  if (Serial.available() > 0) {
    
    outputValue = Serial.read();

    /*
     * if the "string" starts with V, read the next char.
     * The next char represents a bitfield to toggle each led.
     */
    if (outputValue == 'V'){
        bitfield = Serial.read();
        
        Serial.print("bitfield = ");
        Serial.println(bitfield);
        toggleLed(bitfield);
    }
  }
  delay(100);
}
