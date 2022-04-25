from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import QObject, QThread, Signal
import serial.tools.list_ports
import sys, serial

class Serial_Reader(QObject):
    message_received = Signal(str)
    
    def __init__(self, serial):
        super(Serial_Reader, self).__init__()
        self.serial = serial
        self.comms_open = False

    def read_comm(self):
        while self.comms_open:
            #print("Reading...")
            command = self.serial.readline().decode('UTF-8')
            self.message_received.emit(command)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.comms = serial.Serial()
        self.comms.baudrate=9600


        self.setWindowTitle("Threaded Serial Comms")
        self.thread = QThread()
        self.reader = Serial_Reader(self.comms)
        self.reader.moveToThread(self.thread)

        self.commConnect = QPushButton("Connect")        
        self.commSelect = QLineEdit("COM3")
        self.countdownButton = QPushButton("Start Timer")        
        self.countdown = QLineEdit("0")
        self.led_On = QPushButton("Led On")        
        self.led_Off = QPushButton("Led Off")
        
        self.commSelect.setStyleSheet("QLineEdit {min-width: 100px;}")
        self.countdown.setStyleSheet("QLineEdit {min-width: 100px;}")
        self.commConnect.setStyleSheet("QPushButton {min-width: 100px; max-width: 100px;}")
        self.countdownButton.setStyleSheet("QPushButton {min-width: 100px; max-width: 100px;}")
        self.led_On.setStyleSheet("QPushButton {border-radius: 5px; border-style: outset;border-color: beige; background-color: green;  font: bold 12px; min-width: 100px;padding-top: 6px;padding-bottom: 6px;}")
        self.led_Off.setStyleSheet("QPushButton {background-color: red; border-radius: 5px; border-style: outset;border-color: beige; font: bold 12px; min-width: 100px;padding-top: 6px;padding-bottom: 6px;}")

        self.thread.started.connect(self.reader.read_comm)
        self.reader.message_received.connect(self.on_message)
        self.countdownButton.clicked.connect(self.startCountdown)
        self.commConnect.clicked.connect(self.connect_serial)
        self.led_On.clicked.connect(self.Led_on)
        self.led_Off.clicked.connect(self.Led_off)
        
        layout = QVBoxLayout()
        line0 = QHBoxLayout()
        line1 = QHBoxLayout()
        line2 = QHBoxLayout()

        line0.addWidget(self.commConnect)
        line0.addWidget(self.commSelect)
        line1.addWidget(self.countdownButton)
        line1.addWidget(self.countdown)
        line2.addWidget(self.led_On)
        line2.addWidget(self.led_Off)

        layout.addLayout(line0)
        layout.addLayout(line1)
        layout.addLayout(line2)
        
        container = QWidget()
        container.setLayout(layout)
 
        self.setCentralWidget(container)


    def Led_on(self):    
        self.comms.write(b'Led On\n')
        #print("Led Opened")

    def Led_off(self):
        self.comms.write(b'Led Off\n')
        #print("Led Closed")
        
    def connect_serial(self):
        if self.reader.comms_open:
            self.reader.comms_open = False
            self.comms.close()
            self.commConnect.setText("Connect")
            self.commSelect.setEnabled(True)
            #print(self.comms.port + " closed")
            self.thread.quit()
        else:
            port = self.commSelect.text()
            self.comms.port = port
            self.comms.open()
            self.comms.readline()
            self.commConnect.setText("Disconnect")
            self.commSelect.setEnabled(False)
            #print(port + " opened")
            self.reader.comms_open = True
            self.thread.start()

    def startCountdown(self):
        if self.countdown.isEnabled():
            self.countdownButton.setText("Stop Timer")
            self.countdown.setEnabled(False)
            self.comms.write(self.countdown.text().encode("UTF-8"))
        else:
            self.countdownButton.setText("Start Timer")
            self.comms.write(b'Stop\n')
            self.countdown.setEnabled(True)
            self.countdown.setText("0")

    def on_message(self, data):
        data = data.strip()
        if data.isnumeric():
            if data == "0":
                self.countdownButton.setText("Start Timer")
                self.countdown.setEnabled(True)
            self.countdown.setText(data)
            
def run():
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()
