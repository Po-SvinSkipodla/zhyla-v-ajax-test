import serial


class SerialManager:
    def __init__(self):
        self.serial_port = None

    def open_serial_port(self, port, baudrate):
        try:
            self.serial_port = serial.Serial(port=port, baudrate=baudrate, timeout=1)
            return True
        except serial.SerialException as e:
            print(f"Error opening COM port: {e}")
            return False

    def close_serial_port(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

    def send_data(self, data, line_ending=''):
        if not self.serial_port or not self.serial_port.is_open:
            print("COM port is not open.")
            return

        data_to_send = data.encode("utf-8")
        data_to_send += line_ending
        print(data_to_send)

        try:
            self.serial_port.write(data_to_send)
        except serial.SerialException as e:
            print(f"Error sending data: {e}")

    def receive_data(self):
        if not self.serial_port or not self.serial_port.is_open:
            print("COM port is not open.")
            return None

        return self.serial_port.readline().decode("utf-8")
