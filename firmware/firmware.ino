#include<Wire.h>
#include <SimpleKalmanFilter.h>
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;
SimpleKalmanFilter mpuKalmanFilter(2, 2, 0.01);
const int MPU_addr=0x68;
int16_t AcX,AcY,AcZ,Tmp,GyX,GyY,GyZ;
#define L1 36
#define L2 35
#define L3 25
#define L4 14
#define L5 13
#define B1 27
#define B2 33
#define B3 32
int minVal=265;
int maxVal=402;
int l1,l2,l3,l4,l5,b1,b2,b3;
double x;
double y;

 
void setup(){
Wire.begin();
Wire.beginTransmission(MPU_addr);
Wire.write(0x6B);
Wire.write(0);
Wire.endTransmission(true);
Serial.begin(115200);
SerialBT.begin("ESP32test"); //Bluetooth device name
pinMode(B1,INPUT_PULLUP);
pinMode(B2,INPUT_PULLUP);
pinMode(B3,INPUT_PULLUP);
}

void loop(){
readSensor();
readIMU();
Serial.print(l1);
Serial.print("\t");

Serial.print(l2);
Serial.print("\t");

Serial.print(l3);
Serial.print("\t");

Serial.print(l4);
Serial.print("\t");

Serial.print(l5);
Serial.print("\t");

Serial.print(int(x));
Serial.print("\t");
Serial.print(int(y));
Serial.print("\t");

Serial.print(b1);
Serial.print("\t");

Serial.print(b2);
Serial.print("\t");

Serial.print(b3);
Serial.println();
/////////////////////////////
SerialBT.print(l1);
SerialBT.print("\t");

SerialBT.print(l2);
SerialBT.print("\t");

SerialBT.print(l3);
SerialBT.print("\t");

SerialBT.print(l4);
SerialBT.print("\t");

SerialBT.print(l5);
SerialBT.print("\t");

SerialBT.print(int(x));
SerialBT.print("\t");
SerialBT.print(int(y));
SerialBT.print("\t");

SerialBT.print(b1);
SerialBT.print("\t");

SerialBT.print(b2);
SerialBT.print("\t");

SerialBT.print(b3);
SerialBT.println();


delay(500);
}
void readSensor()
{
  l1 = mpuKalmanFilter.updateEstimate(analogRead(L1));
  l2 = mpuKalmanFilter.updateEstimate(analogRead(L2));
  l3 = mpuKalmanFilter.updateEstimate(analogRead(L3));
  l4 = mpuKalmanFilter.updateEstimate(analogRead(L4));
  l5 = mpuKalmanFilter.updateEstimate(analogRead(L5));
  b1 = digitalRead(B1);
  b2 = digitalRead(B2);
  b3 = digitalRead(B3);
}
void readIMU(){
  Wire.beginTransmission(MPU_addr);
Wire.write(0x3B);
Wire.endTransmission(false);
Wire.requestFrom(MPU_addr,14,true);
AcX=Wire.read()<<8|Wire.read();
AcY=Wire.read()<<8|Wire.read();
AcZ=Wire.read()<<8|Wire.read();
int xAng = map(AcX,minVal,maxVal,-90,90);
int yAng = map(AcY,minVal,maxVal,-90,90);
int zAng = map(AcZ,minVal,maxVal,-90,90);
 
x= RAD_TO_DEG * (atan2(-yAng, -zAng)+PI);
y= RAD_TO_DEG * (atan2(-xAng, -zAng)+PI);
//x=mpuKalmanFilter.updateEstimate(x);
//y=mpuKalmanFilter.updateEstimate(y);

if(x<45 || x>320) x =0;
else if(x>45&&x<135) x= 90;
else if(x>135&&x<230) x = 180;
else if(x>230 && x<320) x =270;

if(y<45 || y>320) y =0;
else if(y>45&&y<135) y= 90;
else if(y>135&&y<230) y = 180;
else if(y>230 && y<320) y =270;

}
