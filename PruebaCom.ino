
int A = 0; 
#include <Servo.h>
Servo Popo;
Servo Popo2;
Servo Popo3;
Servo Popo4;
Servo Popo5;
void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  Popo.attach(3);
  Popo2.attach(4);
  Popo3.attach(5);
  Popo4.attach(6);
  Popo5.attach(7);  
}

void loop() {
  
  if (Serial.available()>0){
    String Mensaje = Serial.readStringUntil("\n");
    Serial.print("Recibido: " );
    Serial.println(Mensaje);
    A = Mensaje.toInt();
    if (A == 1){
      digitalWrite(2, HIGH);
      Popo.write(60);
    
    }
    else if (A == 2){
      Popo2.write(45);
    }
    else if (A== 3){
      Popo3.write(150);
    }
    else if (A == 4){
      Popo4.write(150);
    }
    else if (A == 5){
      Popo5.write(60);
    }

    else if (A == 0){
      digitalWrite(2,0);
     
      
      Popo.write (180);
      Popo2.write(180);
      Popo3.write(0);
      Popo4.write(0);
      Popo5.write(180);
      }

  }
  delay(100);
}
