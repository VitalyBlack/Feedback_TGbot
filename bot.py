import telebot
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

question = ('Интересная пара была?')
options = ['Да', 'Нет']
welcome = ('Введите /poll, чтобы начать опрос')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, welcome)


class Poll(question, options):
    @bot.message_handler (commands= ['poll'])
    def send_poll(self, message):
        bot.send_poll(message.chat.id, Poll.question, Poll.options)












