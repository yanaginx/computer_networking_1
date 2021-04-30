import threading
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import Session
from threading import Thread
from time import sleep
import ipaddress
import client
import os
import subprocess

# p = subprocess.Popen("OpenHardwareMonitor.exe", shell=True)

first = 1
ip = ""

# GUI:
app = QApplication([])
message = QLineEdit()
layout = QVBoxLayout()

text_area = QPlainTextEdit()
text_area.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(text_area)

error_area = QPlainTextEdit()
error_area.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(error_area)



layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()

# Event handlers:



def display_new_messages():
    global first
    error_area.setPlainText(client.err)
    if first:
        text_area.clear()
        text_area.setPlainText("Please input Server IP address: \n")
    else:
        text_area.clear()
        text_area.setPlainText(client.screen+client.confirm)
    if (client.exit_confirmed):
        p.terminate()
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
            # print("This is ip connection" + client.SERVER)
            client.client_start()
        if client.client_restart:
            first = 1
            client.client_restart = 0
        else :
            if client.reg_succeeded:
                # print("sadmlakskmd\n")
                first = 0
        message.clear()

    else:
        client.command = message.text()
        client.command_signal = 1
        message.clear()
        
message.returnPressed.connect(send_message)
timer = QTimer()
timer.timeout.connect(display_new_messages)
timer.start(200)
app.exec_()

