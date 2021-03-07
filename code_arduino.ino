/*****************************************************
*        Arduino example for MD25 and LCD03          *
*    MD25 is controlled using I2C and the LCD03      *
*            is controlled using serial              *
*                                                    *
*              By James Henderson 2012               *
*****************************************************/

#include <SoftwareSerial.h>
#include <Wire.h>

#define CMD                 (byte)0x00                        // Values of 0 eing sent using write have to be cast as a byte to stop them being misinterperted as NULL
                                                              // This is a but with arduino 1
#define MD25ADDRESS         0x58                              // Address of the MD25
#define SOFTWAREREG         0x0D                              // Byte to read the software version
#define SPEED1              (byte)0x00                        // Byte to send speed to first motor
#define SPEED2              0x01                              // Byte to send speed to second motor
#define ENCODERONE          0x02                              // Byte to read motor encoder 1
#define ENCODERTWO          0x06                              // Byte to read motor encoder 2
#define VOLTREAD            0x0A                              // Byte to read battery volts
#define RESETENCODERS       0x20
#define ACCELERATIONRATE       0x14
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int x1=0;                                                    // int x stores a value to be used as speed data for the motors
int x2=0;
//------------------PL
long result1 =0;
float ecart1= 0;
int correction1 =0;
float objectif1 = 0;                                        //360=1tour:: 1028= 1 tour robot
float ramp=0.197;
long result2 =0;
float ecart2= 0;
int correction2 =0;
float objectif2 = -0;
int LIM = 300;
int Vmin = 10;
bool hear=false;
float cont=100000;
float value=0;
float value1=0;
float value2=0;
bool go=false;
int steep=0;
int ajustementAsserv = 0;
bool stateAjustement = false;
  int message=1;
void setup(){
//  acceleration();
  Wire.begin();
  Serial.begin(9600);
  delay(100);
// Wait for everything to power up

//    encodeReset();                                            // Cals a function that resets the encoder values to 0

}

int debut;
int arr[100];
int ct;
int ct_prec=ct;
int new_value;
int compter=0;
int dec=0;
void loop(){                                       //Sinon
       
        if (message==1){
          debut=encoder1();
          message=2;}
        else if (message==2){
          
        
          Wire.beginTransmission(MD25ADDRESS);                    // Drive motor 1 at speed value stored in x
          Wire.write(SPEED1);
          Wire.write(128+correction1);
          Wire.endTransmission();
      
          Wire.beginTransmission(MD25ADDRESS);                    // Drive motor 1 at speed value stored in x
          Wire.write(SPEED2);
          Wire.write(128+correction1);
          Wire.endTransmission();
        }
        new_value=encoder1();
        
        ct=abs(new_value-debut);
        
        if (ct==ct_prec){
          compter+=1;
        }
        else {
          compter=0;
          ct_prec=ct;
        }
        if (compter==100){
          Serial.println(ct);
          compter=0;
        }
        
        correction1=asserv(ct,2000);
        if (ct>=1997 and message==2){
          Wire.beginTransmission(MD25ADDRESS);                    // Drive motor 1 at speed value stored in x
          Wire.write(SPEED1);
          Wire.write(128);
          Wire.endTransmission();
      
          Wire.beginTransmission(MD25ADDRESS);                    // Drive motor 1 at speed value stored in x
          Wire.write(SPEED2);
          Wire.write(128);
          Wire.endTransmission();
          dec=1;
//          for (int i=0; i<99;i+=1){
//            Serial.println(arr[i]);
//            }
          message=0;
          }
//        if (abs(debut-encoder1())>3000){
//               Serial.println(debut);
//               Serial.println(encoder1());
//
//            Wire.beginTransmission(MD25ADDRESS);
//          Wire.write(SPEED2);
//          Wire.write(128);                                           // Sends a value of 128 to motor 2 this value stops the motor
//          Wire.endTransmission();
//          
//          Wire.beginTransmission(MD25ADDRESS);
//          Wire.write(SPEED1);
//          Wire.write(128);
//          Wire.endTransmission();
//          Serial.println("fin"); 
//        }

        
 
    }

int asserv(int x,float value){
  int Vmin=10;
  float ramp=0.197;
  float Vmax=Vmin+ramp*value/3;
  if (Vmax>80){
    Vmax=80;
  }
  float V=0;
  if (x<value/3){
    V=Vmin+ramp*x;
    if (V>Vmax ){
      V=Vmax;
      if (stateAjustement == false){
      ajustementAsserv = value/3 -(80-Vmin)/ramp;
      stateAjustement = true;}
      
    }
  }
  else if (x<2*value/3){
    V=Vmax;
  }
  else{
    if(ajustementAsserv-(x-2*value/3) > 0){
      V = Vmax;
      }
      else{
      
    V=Vmax-ramp*(x-(2*value/3+ajustementAsserv));

    
    }
  }
  V= (int) V;
  return V;
}
  
byte getSoft(){                                              // Function that gets the software version
  Wire.beginTransmission(MD25ADDRESS);                      // Send byte to read software version as a single byte
  Wire.write(SOFTWAREREG);
  Wire.endTransmission();
  
  Wire.requestFrom(MD25ADDRESS, 1);                         // request 1 byte form MD25
  while(Wire.available() < 1);                              // Wait for it to arrive
  byte software = Wire.read();                            // Read it in
  
  return(software);
}

void encodeReset(){                                        // This function resets the encoder values to 0
  Wire.beginTransmission(MD25ADDRESS);
  Wire.write(CMD);
  Wire.write(0x20);                                         // Putting the value 0x20 to reset encoders
  Wire.endTransmission(); 
}

long encoder1(){                                            // Function to read and display value of encoder 1 as a long
  Wire.beginTransmission(MD25ADDRESS);                      // Send byte to get a reading from encoder 1
  Wire.write(ENCODERONE);
  Wire.endTransmission();
 
  Wire.requestFrom(MD25ADDRESS, 4);                         // Request 4 bytes from MD25
  while(Wire.available() < 4);                              // Wait for 4 bytes to arrive
  long poss1 = Wire.read();                                 // First byte for encoder 1, HH.
  poss1 <<= 8;
  poss1 += Wire.read();                                     // Second byte for encoder 1, HL
  poss1 <<= 8;
  poss1 += Wire.read();                                     // Third byte for encoder 1, LH
  poss1 <<= 8;
  poss1  +=Wire.read();                                     // Fourth byte for encoder 1, LL

//  delay(10);                                                // Wait for everything to make sure everything is sent
  
  return(poss1);
}

long encoder2(){                                            // Function to read and display velue of encoder 2 as a long
  Wire.beginTransmission(MD25ADDRESS);           
  Wire.write(ENCODERTWO);
  Wire.endTransmission();
  
  Wire.requestFrom(MD25ADDRESS, 4);                         // Request 4 bytes from MD25
  while(Wire.available() < 4);                              // Wait for 4 bytes to become available
  long poss2 = Wire.read();
  poss2 <<= 8;
  poss2 += Wire.read();                
  poss2 <<= 8;
  poss2 += Wire.read();                
  poss2 <<= 8;
  poss2  +=Wire.read();               
  
  delay(50);                                                // Wait to make sure everything is sent
   
  return(poss2);
}

void acceleration(){
  Wire.beginTransmission(MD25ADDRESS);
  Wire.write(ACCELERATIONRATE);
  Wire.write(10);                                           // Sends a value of 128 to motor 2 this value stops the motor
  Wire.endTransmission();
  
}
void stopMotor(){                                           // Function to stop motors
  Wire.beginTransmission(MD25ADDRESS);
  Wire.write(SPEED2);
  Wire.write(128);                                           // Sends a value of 128 to motor 2 this value stops the motor
  Wire.endTransmission();
  
  Wire.beginTransmission(MD25ADDRESS);
  Wire.write(SPEED1);
  Wire.write(128);
  Wire.endTransmission();
}  
