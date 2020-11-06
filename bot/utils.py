import telebot
from enum import Enum
import api.quiz as api_quiz


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
    ADDITIONAL_QUESTIONS = 10

class Data:
    def __init__(self, lessonId=None):
        self.state = UserState.WAITING
        self.questions = []
        self.answers = []
        self.current_question = 0
        self.teacher = None
        self.groups = None
        self.lessonId = lessonId

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

    def start(self):
        questions = api_quiz.getQuestions(self.lessonId)
        questions.sort(key=lambda question: question.id)
        questions.reverse()

        self.state = UserState.ASKING
        self.questions = questions.copy()
        self.current_question = self.questions.pop()
        return self.current_question


class NumericKeyboard:
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(1, 11):
        keyboard.add(
            telebot.types.InlineKeyboardButton(text=str(i), callback_data=str(i))
        )


class RegistrationKeyboard:
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb_yes = telebot.types.InlineKeyboardButton(text="Да", callback_data="Да")
    kb_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    keyboard.add(kb_yes)
    keyboard.add(kb_no)


class NoQuestionsMarkup:
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb_button = telebot.types.InlineKeyboardButton(text="Не хочу ничего добавлять", callback_data="no_questions")
    keyboard.add(kb_button)