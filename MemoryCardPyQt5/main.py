from PyQt5.QtWidgets import QApplication
from random import choice, shuffle
from time import sleep

col_pink = ('#ff6496')

app = QApplication([])

from main_widnow import *
from menu_window import *

main_style()
menu_style()

class Question():
    def __init__(self, question=None, answer=None, wrong_ans1=None, wrong_ans2=None, wrong_ans3=None):
        self.question = question
        self.answer = answer
        self.wrong_answer1 = wrong_ans1
        self.wrong_answer2 = wrong_ans2
        self.wrong_answer3 = wrong_ans3
        self.actual = True
        self.count_asked = 0
        self.count_right = 0
    def got_right(self):
        self.count_asked += 1
        self.count_right += 1
    def got_wrong(self):
        self.count_asked += 1

q1 = Question('  Яблуко  ', ' apple ', ' application ', ' pinapple ', ' apply ')
q2 = Question('  Дім  ', ' house ', ' horse ', ' hurry ', ' hour ')
q3 = Question('  Миша  ', ' mouse ', ' mouth' , 'mose ', ' museum ')
q4 = Question('  Число  ', ' number ', ' digit ', ' amount ', ' summary ')

questions_list = [q1, q2, q3, q4]
radio_list = [rb_ans1, rb_ans2, rb_ans3, rb_ans4]
answer, wrong_answer1, wrong_answer2, wrong_answer3 = radio_list[0], radio_list[1], radio_list[2], radio_list[3]


def new_question():
    global cur_q
    cur_q = choice(questions_list)
    lb_question1.setText(cur_q.question)
    lb_right_answer.setText(cur_q.answer)
    shuffle(radio_list)

    radio_list[0].setText(cur_q.wrong_answer1)
    radio_list[1].setText(cur_q.wrong_answer2)
    radio_list[2].setText(cur_q.wrong_answer3)
    radio_list[3].setText(cur_q.answer)
new_question()

def check_result():
    RadioGroup.setExclusive(False)
    for answer in radio_list:
        if answer.isChecked():
            if answer.text() == lb_right_answer.text():
                cur_q.got_right()
                lb_result.setStyleSheet(f"background-color: {col_lime}; font-size:44pt;")
                lb_result.setText(' Вірно! ')
                answer.setChecked(False)
                break
            else:
                lb_result.setStyleSheet(f"background-color: {col_pink}; font-size:44pt;")
                lb_result.setText(' Неправильно ')
                cur_q.got_wrong()

    RadioGroup.setExclusive(True)

def switch_screen():
    if btn_next.text() == ' Відповісти ':
        check_result()
        gb_question.hide()
        gb_answer.show()

        btn_next.setText(' Наступне запитання ')
    else:
        new_question()
        gb_question.show()
        gb_answer.hide()

        btn_next.setText(' Відповісти ')

def back_screen():
    Wind.hide()
    window.show()

def rest():
    window.hide()
    Time = sp_rest.value() * 60
    sleep(Time)
    window.show()

def menu_generate():
    if cur_q.count_asked == 0:
        c = 0
    else:
        c = (cur_q.count_right / cur_q.count_asked)*100
    text_cur = f' Разів відповіли: {cur_q.count_asked}\n'\
                f' Вірних відповідей: {cur_q.count_right}\n'\
                f' Успішність: {c}%'
    stat_text.setText(text_cur)
    window.hide()
    Wind.show()

def add_question():
    Q = question_lineEdit.text()
    Ans = answear_lineEdit.text()
    Wro_ans1 = wrong_Ans_lineEdit1.text()
    Wro_ans2 = wrong_Ans_lineEdit2.text()
    Wro_ans3 = wrong_Ans_lineEdit3.text()
    q0 = Question(Q, Ans, Wro_ans1, Wro_ans2, Wro_ans3)
    questions_list.append(q0)
    
def clear_lineEdit():
    question_lineEdit.clear()
    answear_lineEdit.clear()
    wrong_Ans_lineEdit1.clear()
    wrong_Ans_lineEdit2.clear()
    wrong_Ans_lineEdit3.clear()

btn_menu.clicked.connect(menu_generate)
btn_rest.clicked.connect(rest)
btn_next.clicked.connect(switch_screen)
clear_btn.clicked.connect(clear_lineEdit)
back_btn.clicked.connect(back_screen)
add_question_btn.clicked.connect(add_question)

window.show()
app.exec_()