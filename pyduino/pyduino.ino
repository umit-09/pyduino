#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <TimeLib.h>
#include <RTClib.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);  // Set the LCD address to 0x27 for a 4x20 display

DS1302 rtc(8, 6, 7);

void setup() {
  Serial.begin(9600);             // Initialize serial communication
  lcd.init();                     // Initialize the LCD
  lcd.backlight();                // Turn on the backlight
  lcd.setCursor(0, 0);            // Set the cursor to the top-left corner
  lcd.print("Arduino LCD Demo");  // Display a welcome message
  setTime(0);                     // Initialize the Time library (start from epoch)
  if (!rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    // following line sets the RTC to the date & time this sketch was compiled
    rtc.adjust(DateTime(__DATE__, __TIME__));
  }
}

void loop() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');  // Read a line from the serial port
    inputString.trim();                                 // Remove leading and trailing whitespace

    // Check if the inputString starts with "SD "
    if (inputString.startsWith("SD ")) {
      String timestamp = inputString.substring(3);  // Remove the "SD " prefix

      // Convert timestamp to a long integer
      long timestampLong = atol(timestamp.c_str());

      // Set the system time using the received Unix timestamp
      setTime(timestampLong);

      // Create a formatted date and time string
      char datetimeString[20];  // Buffer for date and time string
      sprintf(datetimeString, "%02d/%02d/%04d %02d:%02d:%02d", month(), day(), year(), hour(), minute(), second());

      // Clear the LCD and print the formatted date and time
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(datetimeString);

      // Send acknowledgment back to Python
      Serial.println("ACK");
    }
  }
}
