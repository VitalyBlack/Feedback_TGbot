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
        self.teachers = None
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
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(*[telebot.types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in [1, 2, 3, 4, 5]])
    keyboard.add(*[telebot.types.InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in [6, 7, 8, 9, 10]])


class RegistrationKeyboard:
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        *[telebot.types.InlineKeyboardButton(text=str(name), callback_data=str(name)) for name in ['Да', 'Нет']])


def teacher_keyboard(teachers):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    counter = 0
    for teacher in teachers:
        counter += 1
        if counter == 6:
            break
        original_name = teacher['full_name']
        splited = original_name.split()
        new_name = splited[0] + ' '
        for other in splited[1:]:
            new_name += other[1].upper() + '.'
        chair = teacher['chair']
        id = teacher['id']
        keyboard.add(telebot.types.InlineKeyboardButton(text=f'{new_name}\n{chair}', callback_data=id))
    return keyboard


def group_keyboard(groups):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    counter = 0
    for group in groups:
        counter += 1
        if counter == 6:
            break
        group_id = group['id']
        group_name = group['name']
        keyboard.add(telebot.types.InlineKeyboardButton(text=f'{group_name}', callback_data=group_id))
    return keyboard


class NoQuestionsMarkup:
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb_button = telebot.types.InlineKeyboardButton(text="Не хочу ничего добавлять", callback_data="no_questions")
    keyboard.add(kb_button)
