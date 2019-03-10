#include "I2Cdev.h"
#include <string.h>
#include <Metro.h> 
#include "MPU6050_6Axis_MotionApps20.h"
#include <SoftwareSerial.h>

Metro Metro1 = Metro(100);
Metro Metro2 = Metro(0);

// IN 1-4 继电器 
#define IN1 2
#define IN2 3
#define IN3 4
#define IN4 5

// BT 8-9  RX and TX
#define BTRX 9
#define BTTX 8

// Single LED
#define LED 13

// 加速度
int16_t ax, ay, az;
// 重力加速度
int16_t gx, gy, gz;
// 加速度计比例系数
float AcceRatio = 16384.0;

char msg[20];
int msgIndex;

// 实例化mpu对象
MPU6050 mpu;
//实例化 BT对象
SoftwareSerial BT(BTRX, BTTX);


void setup() {
    // put your setup code here, to run once:
    // 小车继电器控制输出  IN1  --->  IN4
    pinMode(IN1,OUTPUT);
    pinMode(IN2,OUTPUT);
    pinMode(IN3,OUTPUT);
    pinMode(IN4,OUTPUT);
    pinMode(LED,OUTPUT);
    //  MPU6050 加速度传感器
    Wire.begin();   
    mpu.initialize();
    BT.begin(9600);
}

void BTread()
{
    if ( BT.available() ) {
      digitalWrite(LED,HIGH);
      char var = BT.read();
      if ( var != '/' ) {
        msg[msgIndex++] = var;
        msg[msgIndex] = 0;
      } else {
        if ( strcmp(msg,"UP") == 0 ) {
            Up();
        } else if ( strcmp(msg,"DOWN") == 0 ) {
            Down();
        } else if ( strcmp(msg,"LEFT") == 0 ) {
            Left();
        } else if ( strcmp(msg,"RIGHT") == 0 ) {
            Right();
        } else {
            Stop();  
        }
        msg[0] = 0;
        msgIndex = 0;
      }
      delay(200);
      digitalWrite(LED,LOW );
    }
}

void MPUread()
{
      mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
      float acceleration_X = ax / AcceRatio - 1.00;//偏移
      float acceleration_Y = ay / AcceRatio + 0.01;
      float acceleration_Z = az / AcceRatio + 0.03;
      BT.print(acceleration_X);
      BT.print("\t");
      BT.print(acceleration_Y);
      BT.print("\t");
      BT.println(acceleration_Z);
      // BT.print("gx");BT.print("---->");BT.println(gx);
      // BT.print("gy");BT.print("---->");BT.println(gy);
      // BT.print("gz");BT.print("---->");BT.println(gz);
}

void loop() {
  if ( Metro2.check() )
       BTread();
  if ( Metro1.check() )
       MPUread();
}

void Up() {
  // 小车方向控制   --->   向前
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
}

void Down() {
  // 小车方向控制   --->   向后
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH);
}

void Left() {
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,LOW);
}

void Right() {
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
}

void Stop() {
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,LOW);
}
