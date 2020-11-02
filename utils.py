import telebot
from enum import Enum


class QuestionType(Enum):
    TEXT = 'text'
    NUMERIC = 'numeric'


class Question:
    def __init__(self, id, text, type):
        self.id = id
        self.text = text
        self.type = type

class Answer:
    def __init__(self, question_id, answer, type):
        self.question_id = question_id
        self.answer = answer
        self.type = type


class UserState(Enum):
    WAITING = 1
    ASKING = 2
    REG_1 = 3
    TEACHER_1 = 4
    STUDENT_1 = 7
    STUDENT_2 = 8
    STUDENT_3 = 9

class Data:
    def __init__(self):
        self.state = UserState.WAITING
        self.questions = []
        self.answers = []
        self.current_question = 0
        self.teacher = None
        self.groups = None
        self.lessonId = None

    def next_question(self, answer_text):
        self.answers.append(
            Answer(
                self.current_question.id,
                answer_text,
                self.current_question.type
            )
        )

        if len(self.questions) == 0:
            return None

        self.current_question = self.questions.pop()
        return self.current_question

    def start(self, questions, lessonId):
        self.state = UserState.ASKING
        self.lessonId = lessonId
        self.questions = questions.copy()
        self.current_question = self.questions.pop()
        return self.current_question


class NumericKeyboard:
    keyboard = telebot.types.InlineKeyboardMarkup()
    numeric1 = telebot.types.InlineKeyboardButton(text="1", callback_data="1")
    numeric2 = telebot.types.InlineKeyboardButton(text="2", callback_data="2")
    numeric3 = telebot.types.InlineKeyboardButton(text="3", callback_data="3")
    numeric4 = telebot.types.InlineKeyboardButton(text="4", callback_data="4")
    numeric5 = telebot.types.InlineKeyboardButton(text="5", callback_data="5")
    numeric6 = telebot.types.InlineKeyboardButton(text="6", callback_data="6")
    numeric7 = telebot.types.InlineKeyboardButton(text="7", callback_data="7")
    numeric8 = telebot.types.InlineKeyboardButton(text="8", callback_data="8")
    numeric9 = telebot.types.InlineKeyboardButton(text="9", callback_data="9")
    numeric10 = telebot.types.InlineKeyboardButton(text="10", callback_data="10")
    keyboard.add(numeric1)
    keyboard.add(numeric2)
    keyboard.add(numeric3)
    keyboard.add(numeric4)
    keyboard.add(numeric5)
    keyboard.add(numeric6)
    keyboard.add(numeric7)
    keyboard.add(numeric8)
    keyboard.add(numeric9)
    keyboard.add(numeric10)


class RegistrationKeyboard:
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb_yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="Да")
    kb_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    keyboard.add(kb_yes)
    keyboard.add(kb_no)