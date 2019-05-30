#include <Eventually.h>

#define BTN1 5
#define BTN2 6
#define BUZZ 7

int status = 0;

EvtManager mgr;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(BTN1, INPUT);
  pinMode(BTN2, INPUT);

  mgr.addListener(new EvtPinListener(BTN1, (EvtAction)down));
}

bool down(){
   
  if(digitalRead(BTN2) == HIGH){

    status = !status;

    if(status){
      while(1){
        if(digitalRead(BTN1) == LOW || digitalRead(BTN2) == LOW){
          Serial.println("tmr_start");  
          break;
        }
      }
    }else{
      Serial.println("tmr_stop");
      delay(500);
    }
    
    //beep();    

  }
  return true;
}

void beep(){
    digitalWrite(BUZZ, HIGH);
    delay(500);
    digitalWrite(BUZZ, LOW);
}

USE_EVENTUALLY_LOOP(mgr);
