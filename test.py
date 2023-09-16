import time
import serial
import datetime
import threading
import sys

arduino = serial.Serial(port='COM8', baudrate=9600, timeout=0)  # Set timeout to 0 for non-blocking read

def get_time():
    print("\nGetting Time...\n")
    # Your code to handle getting time from Arduino goes here

def set_time():
    formatted_time = get_formatted_time()
    print(f"\nSending: {formatted_time}")
    arduino.write(formatted_time.encode())
    time.sleep(0.5)
    
    # Read the response from Arduino
    response = arduino.readline().decode().strip()
    print(f"Received response from Arduino: {response}\n")

def read_serial():
    try:
        while not done_flag.is_set():
            data = arduino.readline().decode().strip()
            if data:
                print(f"Received data from Arduino: {data}")
            time.sleep(0.001)  # Sleep for 1 millisecond (adjust as needed)
    except serial.SerialException:
        pass

def get_formatted_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("SD %d/%m/%Y/%H/%M/%S")
    return formatted_time

if __name__ == "__main__":
    done_flag = threading.Event()  # Flag to signal when to stop reading from the serial port

    arduino.flushInput()  # Clear any existing data in the input buffer
    arduino.flushOutput()  # Clear any existing data in the output buffer

    # Create a separate thread to continuously read from the serial port
    serial_thread = threading.Thread(target=read_serial)
    serial_thread.daemon = True
    serial_thread.start()

    try:
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
            elif choice == '3':
                done_flag.set()  # Set the flag to signal the serial reading thread to stop
                serial_thread.join()  # Wait for the serial reading thread to finish
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
    except KeyboardInterrupt:
        done_flag.set()  # Set the flag to signal the serial reading thread to stop
        serial_thread.join()  # Wait for the serial reading thread to finish
        arduino.close()  # Close the serial port when done
        sys.exit(0)
