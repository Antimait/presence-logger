#include <LiquidCrystal.h>;

LiquidCrystal lcd(12, 11, 2, 3, 4, 5);
const int PIR = 8;
bool presence;
int value_read;
String msg;
 
void setup() { 
    Serial.begin(9600);    
    pinMode(PIR, INPUT);
    presence = false;
    lcd.begin(16, 2); 
}

void update_lcd(String msg) {
    lcd.setCursor(0, 0);
    lcd.clear();
    lcd.print(msg);
}
 
void loop() {
    value_read = digitalRead(PIR);
    if(value_read == HIGH && !presence) {
        Serial.println("on");
        presence = true;
    } else if (value_read == LOW && presence) {
        Serial.println("off");
        presence = false;
    }

    if(Serial.available()) {
        msg = Serial.readString();
        update_lcd(msg);
    }
    delay(100);    
}
