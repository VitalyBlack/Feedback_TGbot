import telebot
from config import TOKEN
from enum import Enum

bot = telebot.TeleBot(TOKEN)
welcome = ('Введите /poll, чтобы начать опрос')

user_data = {}
test_questions = {
    1: 'Понравилась пара?',
    2: 'Как дела?',
    3: 'Устал?',
}

class Poll():
    def __init__(self, question, options):
        self.question = question
        self.options = options


def send_poll(chat_id, poll):
    bot.send_poll(chat_id, poll.question, poll.options)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, welcome)


@bot.message_handler(commands=['poll'])
def send_opros(message):
    poll = Poll(
        'Интересная пара была?',
        ['Да', 'Нет']
    )
    send_poll(message.chat.id, poll)


class Userstate(Enum):
    WAITING = 1
    QUESTIONING = 2


# ch_id = 1
# quiz = {
#     ch_id: {q_id: o_id}
#
# }

# print(quiz[1])

class Data:
    def __init__(self):
        self.state = Userstate.WAITING
        self.questions = {}
        self.current_question = 0
        self.answers = {}

    def next_question(self, answer):
        self.answers[self.current_question] = answer

        if (len(self.questions) == 0):
            return ''

        next_question = self.questions.popitem()
        self.current_question = next_question[0]
        return next_question[1]

    def start(self, questions):
        self.state = Userstate.QUESTIONING
        self.questions = questions.copy()
        next_question = self.questions.popitem()
        self.current_question = next_question[0]
        return next_question[1]


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
    bot.send_message(message.chat.id, first_question)


@bot.message_handler(content_types = ['text'])
def handle(message):
    print(message.chat.id)

    if message.chat.id not in user_data:
        bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
        return


    data = user_data[message.chat.id]

    if data.state != Userstate.QUESTIONING:
        print('Error')
        bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
        return

    next_question = data.next_question(message.text)

    if next_question == '' :
        bot.send_message(message.chat.id, 'Спасибо за опрос!')
        print(data.answers)
        del user_data[message.chat.id]

    else:
        bot.send_message(message.chat.id, next_question)

#кнопка, класс вопроса из двух переменных question_text, question_type; не просто текст вопросов хранится
#в answers и questions, а хранится экземпляр класса вопроса. в Data новая переменная хранящая еще и тип вопроса



# state = Userstate.waiting
# def quiz(message):
#     state = Userstate.questioning
#     if(state == Userstate.questioning):
#             poll = Poll(q_id, o_id)
#             bot.send_poll(message.chat.id, poll)
#             state = Userstate.waiting
#
#     elif(state == Userstate.waiting):
#         def ignore(message):
#             bot.send_message(message.chat.id, 'Ожидайте новый опрос')


bot.polling()
