from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

col_black = ('#383838')
col_gray = ('#4d4d4d')
col_lime = ('#83be9a')

Wind = QWidget()
Wind.setWindowTitle('Menu')

question_text = QLabel(' Введіть запитання: ')
answear_text = QLabel(' Введіть вірну відповідь: ')
wrong_ans_text1 = QLabel(' Введіть 1 хибну відповідь: ')
wrong_ans_text2 = QLabel(' Введіть 2 хибну відповідь: ')
wrong_ans_text3 = QLabel(' Введіть 3 хибну відповідь: ')
stat_title = QLabel(' Статистика поточного запитання: ')
stat_text = QLabel()

add_question_btn = QPushButton(' Додати запитання ')
clear_btn = QPushButton(' Очистити ')
back_btn = QPushButton('Назад')

question_lineEdit = QLineEdit()
answear_lineEdit = QLineEdit()
wrong_Ans_lineEdit1 = QLineEdit()
wrong_Ans_lineEdit2 = QLineEdit()
wrong_Ans_lineEdit3 = QLineEdit()

def menu_style():
    obj = [question_text, answear_text, wrong_ans_text1, wrong_ans_text2, wrong_ans_text3, stat_title, stat_text, add_question_btn, clear_btn, back_btn]
    for objs in obj:
        objs.setFont(QFont('Comfortaa'))
    qlineedits = [question_lineEdit, answear_lineEdit, wrong_Ans_lineEdit1, wrong_Ans_lineEdit2, wrong_Ans_lineEdit3]
    for obj in qlineedits:
        obj.setStyleSheet(f"background-color: {col_lime}; font-size:21pt; ")
    Wind.setStyleSheet(f'background-color: {col_black}')
    back_btn.setStyleSheet(f"background-color: {col_lime}; font-size:33pt; ")
    clear_btn.setStyleSheet(f"background-color: {col_lime}; font-size:24pt; ")
    add_question_btn.setStyleSheet(f"background-color: {col_lime}; font-size:24pt; ")
    stat_text.setStyleSheet(f"background-color: {col_gray}; color: {col_lime}; font-size:27pt; ")
    stat_title.setStyleSheet(f"background-color: {col_gray}; color: {col_lime}; font-size:27pt; ")
    wrong_ans_text3.setStyleSheet(f"background-color: {col_gray}; color: {col_lime}; font-size:24pt; ")
    wrong_ans_text2.setStyleSheet(f"background-color: {col_gray}; color: {col_lime}; font-size:24pt; ")
    wrong_ans_text1.setStyleSheet(f"background-color: {col_gray}; color: {col_lime}; font-size:24pt; ")
    answear_text.setStyleSheet(f"background-color: {col_gray}; color: {col_lime}; font-size:27pt; ")
    question_text.setStyleSheet(f"background-color: {col_gray}; color: {col_lime}; font-size:33pt; ")

LayoutH1 = QHBoxLayout()
LayoutH2 = QHBoxLayout()

LayoutV1 = QVBoxLayout()
LayoutV2 = QVBoxLayout()
LayoutV3 = QVBoxLayout()

LayoutV1.addWidget(question_text)
LayoutV1.addWidget(answear_text)
LayoutV1.addWidget(wrong_ans_text1)
LayoutV1.addWidget(wrong_ans_text2)
LayoutV1.addWidget(wrong_ans_text3)

LayoutV2.addWidget(question_lineEdit)
LayoutV2.addWidget(answear_lineEdit)
LayoutV2.addWidget(wrong_Ans_lineEdit1)
LayoutV2.addWidget(wrong_Ans_lineEdit2)
LayoutV2.addWidget(wrong_Ans_lineEdit3)

LayoutH1.addLayout(LayoutV1)
LayoutH1.addLayout(LayoutV2)

LayoutH2.addWidget(add_question_btn)
LayoutH2.addWidget(clear_btn)

LayoutV3.addLayout(LayoutH1)
LayoutV3.addLayout(LayoutH2)
LayoutV3.addWidget(stat_title)
LayoutV3.addWidget(stat_text)
LayoutV3.addWidget(back_btn)

Wind.setLayout(LayoutV3)