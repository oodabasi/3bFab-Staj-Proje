int start_time;
int countdown;
bool countdown_active = 0;

void setup() {
    pinMode(LED_BUILTIN, OUTPUT);   
    Serial.begin(9600);
    Serial.setTimeout(50);
    Serial.println("Comms Connected");
}

void loop() {   
  int current_time = millis();
  if(countdown_active && (current_time - start_time) >= 1000){    
    Serial.println(countdown);
    countdown--;
    if(countdown == -1){
      countdown_active = 0;
    }
    else{
      start_time = current_time;      
    }    
  }
    
  if(Serial.available() > 0){    
    String command = Serial.readString();    
    if(command == "Led On\n"){
      digitalWrite(LED_BUILTIN, HIGH);
    }
    else if(command == "Led Off\n"){
      digitalWrite(LED_BUILTIN, LOW);
    }
    else if(command == "Stop\n"){
      countdown = 0;
      countdown_active = 0;
    }
    else{
      countdown = command.toInt();
      countdown_active = 1;
            
    }  
  }     
}

  
