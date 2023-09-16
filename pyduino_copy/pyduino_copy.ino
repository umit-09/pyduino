#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RTClib.h>

DS1302 rtc;  // Create an RTC object

LiquidCrystal_I2C lcd(0x27, 20, 4);  // Set the LCD address to 0x27 for a 4x20 display

int day, month, year, hour, minute, second;

void setup() {
  Serial.begin(9600);             // Initialize serial communication
  lcd.init();                     // Initialize the LCD
  lcd.backlight();                // Turn on the backlight
  lcd.setCursor(0, 0);            // Set the cursor to the top-left corner
  lcd.print("Arduino LCD Demo");  // Display a welcome message

  rtc.begin();  // Initialize the RTC module
}

void loop() {
  for (int i = 0; i < 1000; i++) {
    serial_check();
    delay(1);
  }

  DateTime now = rtc.now();
  char buf[100];
  strncpy(buf, "YYYY.MM.DD hh:mm:ss", 100);

  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print(now.format(buf));
}

void serial_check() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');  // Read a line from the serial port
    inputString.trim();                                 // Remove leading and trailing whitespace

    // Check if the inputString starts with "SD "
    if (inputString.startsWith("SD ")) {
      String datetimeString = inputString.substring(3);  // Remove the "SD " prefix
      
      sscanf(datetimeString.c_str(), "%2d/%2d/%4d/%2d/%2d/%2d", &day, &month, &year, &hour, &minute, &second);

      // Set the RTC time using the received date and time components
      DateTime newTime(year, month, day, hour, minute, second);
      
      rtc.adjust(newTime);

      // Clear the LCD and print the received date and time
      lcd.clear();
      lcd.setCursor(0, 1);
      lcd.print(datetimeString);

      // Send acknowledgment back to Python
      Serial.println("ACK");
      delay(2000);
    }
  }
}