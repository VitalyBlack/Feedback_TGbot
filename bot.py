import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
welcome = ('Введите /poll, чтобы начать опрос')

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


bot.polling()










