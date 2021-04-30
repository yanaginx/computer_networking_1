from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import Session
from threading import Thread
from time import sleep
import ipaddress
import client

first = 1

# GUI:
app = QApplication([])
message = QLineEdit()
layout = QVBoxLayout()

text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(text_area)



layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()

# Event handlers:



def display_new_messages():
    text_area.clear()
    text_area.setPlainText(client.screen+client.confirm)


def send_message():
    client.command = message.text()
    client.command_signal = 1
    message.clear()

client.SERVER ="192.168.43.79"
client.client_start()
message.returnPressed.connect(send_message)
timer = QTimer()
timer.timeout.connect(display_new_messages)
timer.start(1000)
app.exec_()

