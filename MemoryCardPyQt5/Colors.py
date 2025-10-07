from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import * 
import sys
class Windows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('colors')
        self.setGeometry(400, 200, 400, 200)
        layoutH1 = QHBoxLayout()
        layoutV1 = QVBoxLayout()
        self.button1 = QPushButton('Темний фон')
        self.button1.setStyleSheet('''
                                    font-size:20pt;
                                    background-color: #383838
                                    ''')
        self.button2 = QPushButton('Відділеня від фону')
        self.button2.setStyleSheet('''
                                    font-size:20pt;
                                    background-color: #4d4d4d
                                    ''')
        self.button3 = QPushButton('Шрифт')
        self.button3.setStyleSheet('''
                                    font-size:20pt;
                                    background-color: #83be9a
                                    ''')
        self.button5 = QPushButton('Розовенький')
        self.button5.setStyleSheet('''
                                    font-size:20pt;
                                    background-color: #ff6496
                                    ''')
        self.button7 = QPushButton('Акцентний')
        self.button7.setStyleSheet('''
                                    font-size:20pt;
                                    background-color: #64be83;
                                    ''')
        self.button_list = [self.button1, self.button2, self.button3, self.button5, self.button7]
        for buttons in self.button_list:
            buttons.setFont(QFont('Comfortaa'))
        layoutV1.addWidget(self.button1, alignment=Qt.AlignCenter)
        layoutV1.addWidget(self.button2, alignment=Qt.AlignCenter)
        layoutV1.addWidget(self.button7, alignment=Qt.AlignCenter)
        layoutV1.addWidget(self.button3, alignment=Qt.AlignCenter)
        layoutV1.addWidget(self.button5, alignment=Qt.AlignCenter)
        layoutH1.addLayout(layoutV1)
        central_widget = QWidget()
        central_widget.setLayout(layoutH1)
        self.setCentralWidget(central_widget)
app = QApplication([])
window = Windows()
window.show()
sys.exit(app.exec_())