import threading

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QComboBox, QLabel, QLineEdit
from serial_manager import SerialManager
from serial.tools import list_ports


class DataReceiver(QObject):
    data_received = pyqtSignal(str)

    def __init__(self, serial_manager):
        super(DataReceiver, self).__init__()
        self.serial_manager = serial_manager
        self.running = False

    def start(self):
        self.running = True
        threading.Thread(target=self.receive_data_thread, daemon=True).start()

    def stop(self):
        self.running = False

    def receive_data_thread(self):
        while self.running and self.serial_manager.serial_port.is_open:
            received_data = self.serial_manager.receive_data()
            if received_data:
                self.data_received.emit(received_data)


class Terminal(QWidget):
    def __init__(self):
        super(Terminal, self).__init__()
        self.layout = QVBoxLayout()
        self.serial_manager = SerialManager()

        self.com_port_label = QLabel("COM Port:")
        self.com_port_combobox = QComboBox()
        self.layout.addWidget(self.com_port_label)
        self.layout.addWidget(self.com_port_combobox)

        self.baud_rate_label = QLabel("Baud Rate:")
        self.baud_rate_combobox = QComboBox()
        self.baud_rate_combobox.addItems(["9600", "115200"])
        self.layout.addWidget(self.baud_rate_label)
        self.layout.addWidget(self.baud_rate_combobox)

        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_serial_port)
        self.layout.addWidget(self.open_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close_serial_port)
        self.layout.addWidget(self.close_button)

        self.line_ending_label = QLabel("Line Ending:")
        self.line_ending_combobox = QComboBox()
        self.line_ending_combobox.addItems(["CR", "LF", "CR/LF"])
        self.layout.addWidget(self.line_ending_label)
        self.layout.addWidget(self.line_ending_combobox)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        self.input_line = QLineEdit()
        self.layout.addWidget(self.input_line)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_data)
        self.layout.addWidget(self.send_button)

        self.fill_com_ports()

        self.data_receiver = DataReceiver(self.serial_manager)
        self.data_receiver.data_received.connect(self.handle_received_data)

        self.setLayout(self.layout)

    def fill_com_ports(self):
        available_ports = [port.device for port in list_ports.comports()]
        self.com_port_combobox.clear()
        self.com_port_combobox.addItems(available_ports)

    def open_serial_port(self):
        selected_com_port = self.com_port_combobox.currentText()
        selected_baud_rate = int(self.baud_rate_combobox.currentText())

        if self.serial_manager.open_serial_port(selected_com_port, selected_baud_rate):
            print(f"COM port {selected_com_port} opened successfully.")
            self.data_receiver.start()
        else:
            print(f"Failed to open COM port {selected_com_port}.")

    def close_serial_port(self):
        self.data_receiver.stop()
        self.serial_manager.close_serial_port()
        print("COM port closed.")

    def send_data(self):
        data_to_send = self.input_line.text()
        line_ending = self.get_line_ending_bytes(self.get_line_ending())

        self.serial_manager.send_data(data_to_send, line_ending)
        self.text_edit.append(f"Sent: {data_to_send.strip()}")

    def get_line_ending(self):
        return self.line_ending_combobox.currentText()

    @staticmethod
    def get_line_ending_bytes(line_ending):
        if line_ending == "CR":
            return b'\r'
        elif line_ending == "LF":
            return b'\n'
        elif line_ending == "CR/LF":
            return b'\r\n'
        else:
            return b''

    def handle_received_data(self, data):
        self.text_edit.append(f"Received: {data.strip()}")
