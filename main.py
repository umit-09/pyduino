import serial

ser = serial.Serial('COMX', 9600, timeout=1)  # Replace 'COMX' with your Arduino's serial port

def set_arduino_time():
    try:
        date_time_str = input("Enter the new date and time (YYYY-MM-DD HH:MM:SS): ")
        new_date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        new_timestamp = int(new_date_time.timestamp())
        
        # Send the "SD <timestamp>" command to Arduino
        ser.write(f"SD {new_timestamp}\n".encode())
        
        response = ser.readline().decode().strip()  # Read the response from Arduino
        print(response)
    except ValueError:
        print("Invalid date and time format. Use YYYY-MM-DD HH:MM:SS format.")

def get_arduino_time():
    ser.write(b"GD\n")  # Send the "GD" command to Arduino
    response = ser.readline().decode().strip()  # Read the time from Arduino
    return response

while True:
    print("\nMenu:")
    print("1. Set Date and Time (SD)")
    print("2. Get Date and Time (GD)")
    print("3. Exit")
    
    choice = input("Select an option: ").strip().lower()
    
    if choice == "1" or choice == "sd":
        set_arduino_time()
    elif choice == "2" or choice == "gd":
        arduino_time = get_arduino_time()
        print(f"Time from Arduino: {arduino_time}")
    elif choice == "3" or choice == "exit":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
