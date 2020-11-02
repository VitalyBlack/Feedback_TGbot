import telebot
from config import TOKEN
from enum import Enum

bot = telebot.TeleBot(TOKEN)


class QuestionType(Enum):
    TEXT = 'text'
    NUMERIC = 'numeric'


class Question:
    def __init__(self, id, text, type):
        self.id = id
        self.text = text
        self.type = type


class Userstate(Enum):
    WAITING = 1
    QUESTIONING = 2
    REGISTRATION = 3

class Data:
    def __init__(self):
        self.state = Userstate.WAITING
        self.questions = []
        self.answers = {}
        self.current_question = 0

    def next_question(self, answer):
        self.answers[self.current_question.id] = answer

        if len(self.questions) == 0:
            return ''

        self.current_question = self.questions.pop()
        return self.current_question

    def start(self, questions):
        self.state = Userstate.QUESTIONING
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


user_data = {}
test_questions = [
    Question(1, 'Kak dela?', QuestionType.TEXT),
    Question(2, 'Kak para?', QuestionType.NUMERIC),
    Question(3, 'Kak?', QuestionType.TEXT),
]


@bot.message_handler(commands=['start'])
def registration(message):
    bot.send_message(message.chat.id, 'Вы студент?', reply_markup=RegistrationKeyboard.keyboard)


@bot.message_handler(commands=['test'])
def test(message):
    data = Data()
    user_data[message.chat.id] = data
    bot.send_message(message.chat.id, 'Напишите /begin, чтобы начать')


@bot.message_handler(commands=['begin'])
def begin(message):

    if message.chat.id not in user_data:
        bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
        return

    data = user_data[message.chat.id]

    if data.state != Userstate.WAITING:
        print('Error')
        return

    first_question = data.start(test_questions)
    ask_question(message.chat.id, first_question)


def ask_question(chat_id, question):
    if question.type == QuestionType.TEXT:
        bot.send_message(chat_id, question.text + ' (текстовый ответ)')

    if question.type == QuestionType.NUMERIC:
        bot.send_message(chat_id, question.text + ' (выберите ответ по 10-балльной шкале)', reply_markup=NumericKeyboard.keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        handle(call.message, call.data)


@bot.message_handler(content_types = ['text'])
def handle(message, callback_data=None):
    print(message.chat.id)

    if message.chat.id not in user_data:
        bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
        return

    data = user_data[message.chat.id]

    if data.state != Userstate.QUESTIONING:
        print('Error')
        bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
        return

    if callback_data:
        next_question = data.next_question(callback_data)

    else:
        next_question = data.next_question(message.text)

    if next_question == '':
        bot.send_message(message.chat.id, 'Спасибо за опрос!')
        print(data.answers)
        del user_data[message.chat.id]

    else:
        ask_question(message.chat.id, next_question)

#до 10 кнопок. варианты для нового студента и препода (две кнопки при регистрации - студент или преподаватель).
#у студента нужно узнать группу. дедлайн - до вторника.

bot.polling()
