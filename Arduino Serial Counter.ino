int counter = 0;

void setup() {
    Serial.begin(9600);
    Serial.setTimeout(50);
    Serial.println("Comms Started");
}

void loop() {   
  if(Serial.available() > 0 && Serial.readString() == "Button Pressed\n"){
    counter++;
    Serial.println(counter);
  }  
}