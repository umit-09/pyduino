import time, serial, datetime
from time import gmtime, strftime

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1) 

def get_time():
    print("GD\n")
    print("response")

def get_timezone_offset():
    current_time = datetime.datetime.now()
    utc_time = datetime.datetime.utcnow()
    
    # Calculate the timezone offset in seconds
    timezone_offset_seconds = (current_time - utc_time).total_seconds()
    
    # Calculate the offset in hours and minutes
    hours, remainder = divmod(int(timezone_offset_seconds), 3600)
    minutes = int(remainder / 60)
    
    return hours, minutes

def set_time():
    # Get the current timezone offset
    hours, minutes = get_timezone_offset()
    
    # Get the current time and add the offset
    current_time = datetime.datetime.now()
    adjusted_time = current_time + datetime.timedelta(hours=hours, minutes=minutes)
    
    # Convert the adjusted time to a Unix timestamp
    timestamp = str(int(adjusted_time.timestamp()))
    
    print(f"SD {timestamp}")
    arduino.write(str.encode(f"SD {timestamp}"))
    time.sleep(0.5)

if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Get Time")
        print("2. Set Time")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            get_time()
        elif choice == '2':
            set_time()
            response = arduino.readline().decode().strip()  # Read acknowledgment from Arduino
            print(f"Arduino says: {response}")
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
