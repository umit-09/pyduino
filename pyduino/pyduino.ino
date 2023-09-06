#include <Wire.h>
#include <RTClib.h>

RTC_DS3231 rtc;

void setup() {
  Serial.begin(9600);
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    if (input.startsWith("SD ")) {
      // Extract the timestamp from the command
      unsigned long newTimestamp = input.substring(3).toULong();
      
      // Set the RTC time with the new timestamp
      rtc.adjust(DateTime(newTimestamp));
      
      Serial.println("RTC time has been set.");
    }
    else if (input.equals("GD")) {
      // Get the current time from the RTC
      DateTime now = rtc.now();
      String timeStr = now.timestamp(DateTime::TIMESTAMP_TIME);
      Serial.println(timeStr);
    }
  }
  // Add your other loop logic here
}
