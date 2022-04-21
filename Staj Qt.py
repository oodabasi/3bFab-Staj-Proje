from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton ,QLabel, QVBoxLayout, QHBoxLayout, QLineEdit
from PySide6.QtCore import QTimer, QSize
import serial.tools.list_ports
import sys, serial

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.comms = serial.Serial()
     
        #self.setFixedSize(QSize(165,110))
        self.setWindowTitle("My App")

        self.timer = QTimer()
        self.commConnect = QPushButton("Connect")
        self.commSelect = QLineEdit("COM7")
        self.counterButton = QPushButton("Counter")
        self.counterButton.setEnabled(False)
        self.counter = QLabel("0")
        self.timerButton = QPushButton("Start Timer")
        self.countdown = QLineEdit("0")

        self.timer.timeout.connect(self.updateCountdown)
        self.counterButton.clicked.connect(self.serial_comm)
        self.timerButton.clicked.connect(self.changeCountdownName)
        self.commConnect.clicked.connect(self.connect_port)

        layout = QVBoxLayout()
        line0 = QHBoxLayout()
        line1 = QHBoxLayout()
        line2 = QHBoxLayout()
        
        line0.addWidget(self.commConnect)
        line0.addWidget(self.commSelect)
        line1.addWidget(self.counterButton)
        line1.addWidget(self.counter)
        line2.addWidget(self.timerButton)
        line2.addWidget(self.countdown)

        layout.addLayout(line0)
        layout.addLayout(line1)
        layout.addLayout(line2)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def updateCountdown(self):
        currentCounter = int(self.countdown.text())
        if currentCounter > 1:
            currentCounter -= 1
            self.countdown.setText(str(currentCounter))
            self.startCountdown()
        else:
            self.timer_stop()

    def startCountdown(self):
        self.timer.start(1000)
        self.countdown.setReadOnly(True)
    
    def changeCountdownName(self):
        if self.timerButton.text() == "Start Timer":
            self.timerButton.setText("Stop Timer")
            self.startCountdown()
        else:
            self.timer_stop()

    def serial_comm(self):
        self.comms.write(b'Button Pressed\n')
        a = self.comms.readline()
        a = int(a.strip())
        self.counter.setNum(a)

    def connect_port(self):
        if(self.commConnect.text() == "Connect"):
            self.comms.baudrate=9600
            self.comms.port = self.commSelect.text()
            self.comms.open()
            self.comms.readline()
            self.commConnect.setText("Disconnect")
            self.counterButton.setEnabled(True)
        else:
            self.comms.close()
            self.commConnect.setText("Connect")
            self.counter.setText("0")
            self.timer_stop()
            self.counterButton.setEnabled(False)

    def timer_stop(self):
        self.timerButton.setText("Start Timer")
        self.countdown.setText("0")
        self.timer.stop()
        self.countdown.setReadOnly(False)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()