import threading
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import Session
from threading import Thread
from time import sleep
import ipaddress
import client

first = 1
ip = ""

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
    global first
    if first:
        text_area.clear()
        text_area.setPlainText("Please input Server IP address: ")
    else:
        text_area.clear()
        text_area.setPlainText(client.screen+client.confirm)
        if (client.exit_confirmed):
            app.exit()



def send_message():
    global first
    global ip
    if first:
        try:
            client.SERVER=str(ipaddress.ip_address(message.text()))
        except ValueError:
            client.SERVER=""
        if client.SERVER:
            ip=message.text()
            print("This is ip connection" + client.SERVER)
            client.client_start()
            first = 0
            message.clear()

    else:
        client.command = message.text()
        client.command_signal = 1
        message.clear()
        
message.returnPressed.connect(send_message)
timer = QTimer()
timer.timeout.connect(display_new_messages)
timer.start(1000)
app.exec_()

