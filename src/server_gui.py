from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from requests import Session
from threading import Thread
from time import sleep
import server


# GUI:
app = QApplication([])
message = QLineEdit()
layout = QVBoxLayout()


text_area1 = QPlainTextEdit()
text_area1.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(text_area1)

text_area2 = QPlainTextEdit()
text_area2.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(text_area2)

text_area3 = QPlainTextEdit()
text_area3.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(text_area3)

text_area4 = QPlainTextEdit()
text_area4.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(text_area4)

text_area5 = QPlainTextEdit()
text_area5.setFocusPolicy(Qt.ClickFocus)
layout.addWidget(text_area5)

layout.addWidget(message)
window = QWidget()
window.setLayout(layout)
window.show()

# Event handlers:



def display_new_messages():
    text_area1.clear()
    text_area2.clear()
    text_area3.clear()
    text_area4.clear()
    text_area5.clear()
    text_area1.setPlainText(server.slot[0])
    text_area2.setPlainText(server.slot[1])
    text_area3.setPlainText(server.slot[2])
    text_area4.setPlainText(server.slot[3])
    text_area5.setPlainText(server.screen)

def send_message():
    server.command = message.text()
    server.command_signal = 1
    message.clear()

# Signals:
server.server_start()
message.returnPressed.connect(send_message)
timer = QTimer()
timer.timeout.connect(display_new_messages)
timer.start(1000)

app.exec_()