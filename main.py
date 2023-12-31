import time, serial, datetime
from time import gmtime, strftime

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1) 

def get_time():
    print("GD\n")
    print("response")

def set_time():
    timestamp_utc = datetime.datetime.now(datetime.timezone.utc).timestamp()
    timestamp = str(int(timestamp_utc))  # Convert to integer for seconds since epoch
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
