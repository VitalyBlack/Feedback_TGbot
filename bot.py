import telebot
from config import TOKEN
from utils import QuestionType, Question, RegistrationKeyboard, Data, UserState, NumericKeyboard, teacher_keyboard, \
    group_keyboard
import API.university as api_uni
import API.quiz as api_quiz

bot = telebot.TeleBot(TOKEN)

user_data = {}

#TODO УБРАТЬ ПОЗЖЕ
testLessonId = 1

# @bot.message_handler(commands=['start'])


@bot.message_handler(commands=['register'])
def registration(message):
    if message.chat.id in user_data:
        bot.send_message(message.chat.id, "Вы не можете проходить регистрацию в данный момент.")
        return

    bot.send_message(message.chat.id, 'Вы студент?', reply_markup=RegistrationKeyboard.keyboard)
    data = Data()
    data.state = UserState.REG_1
    user_data[message.chat.id] = data


@bot.message_handler(commands=['test'])
def test(message):
    data = Data()
    user_data[message.chat.id] = data
    keyboard = telebot.types.InlineKeyboardMarkup()
    begin_quiz = telebot.types.InlineKeyboardButton(text="Начать опрос", callback_data="begin")
    keyboard.add(begin_quiz)
    bot.send_message(message.chat.id, ' Нажмите кнопку, чтобы начать опрос', reply_markup=keyboard)


@bot.message_handler(commands=['begin'])
def begin(message):
    if message.chat.id not in user_data:
        bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
        return

    data = user_data[message.chat.id]

    if data.state != UserState.WAITING:
        print('Error')
        return

    questions = api_quiz.getQuestions(testLessonId)
    questions.sort(key=lambda question: question.id)
    questions.reverse()
    first_question = data.start(questions)
    ask_question(message.chat.id, first_question)


def ask_question(chat_id, question):
    if QuestionType(question.type) is QuestionType.TEXT:
        bot.send_message(chat_id, question.text + ' (текстовый ответ)')

    if QuestionType(question.type) is QuestionType.NUMERIC:
        bot.send_message(chat_id, question.text + ' (1-10)',
                         reply_markup=NumericKeyboard.keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        handle(call.message, call.data)


@bot.message_handler(content_types=['text'])
def handle(message, callback_data=None):
    if message.chat.id not in user_data:
        bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
        return

    data = user_data[message.chat.id]

    # if data.state != UserState.ASKING:
    #     print('Error')
    #     bot.send_message(message.chat.id, 'Ожидайте следующий опрос')
    #     return

    if data.state == UserState.WAITING:
        # TODO кнопку для начала опроса
        if callback_data:
            if callback_data == "begin":
                begin(message)
                return

        bot.send_message(message.chat.id, 'Нажмите на кнопку для начала опроса')
        return

    if data.state == UserState.REG_1:
        if callback_data:
            if (callback_data == 'Нет'):
                data.state = UserState.TEACHER_1
                bot.send_message(message.chat.id, 'Введите ФИО или часть ФИО')
            else:
                data.state = UserState.STUDENT_1
                bot.send_message(message.chat.id, 'Введите Группу')
        else:
            bot.send_message(message.chat.id, 'Нужно ответить на вопрос в предыдущем сообщении')
        return

    if data.state == UserState.TEACHER_1:
        if callback_data and data.teachers:
            id = callback_data
            for teacher in data.teachers:
                #TODO Пофиксить потом
                print(id)
                print(teacher['id'])
                if teacher['id'] == str(id):
                    isSuccess = api_uni.setTeacherChatId(id, message.chat.id)
                    if isSuccess:
                        bot.send_message(message.chat.id, 'Успешно зарегистрирован.')
                        del user_data[message.chat.id]
                        return
            bot.send_message(message.chat.id,
                             'Ошибка при сохранении пользователя. Обратитесь к администратору.')
            del user_data[message.chat.id]
            return


        fullname = message.text
        teachers = api_uni.getTeachers(fullname)
        if len(teachers) == 0:
            bot.send_message(message.chat.id, 'Преподавателей по данному запросу не найдено. Попробуйте ещё раз.')
            return

        if len(teachers) == 1:
            isSuccess = api_uni.setTeacherChatId(teachers[0]['id'], message.chat.id)
            if isSuccess:
                bot.send_message(message.chat.id, 'Успешно зарегистрирован.')
                del user_data[message.chat.id]
                return
            else:
                bot.send_message(message.chat.id, 'Ошибка при сохранении пользователя. Обратитесь к администратору.')
                del user_data[message.chat.id]
                return

        if len(teachers) > 1:
            bot.send_message(message.chat.id,
                             'Уточните запрос, найдено несколько преподавателей:',
                             reply_markup=teacher_keyboard(teachers))
            data.teachers = teachers

            return
        return

    if data.state == UserState.STUDENT_1:
        if callback_data and data.groups:
            id = callback_data
            for group in data.groups:
                # TODO Пофиксить потом
                print(id)
                print(group['id'])
                if group['id'] == str(id):
                    isSuccess = api_uni.createNewStudent(id, message.chat.id)
                    if isSuccess:
                        bot.send_message(message.chat.id, 'Успешно зарегистрирован.')
                        del user_data[message.chat.id]
                        return
            bot.send_message(message.chat.id,
                             'Ошибка при сохранении пользователя. Обратитесь к администратору.')
            del user_data[message.chat.id]
            # TODO юзер уже выбрал группу
            return

        groupNumber = message.text
        groups = api_uni.getGroups(groupNumber)
        if len(groups) == 0:
            bot.send_message(message.chat.id, 'Групп по данному запросу не найдено. Попробуйте ещё раз.')
            return

        if len(groups) == 1:
            isSuccess = api_uni.createNewStudent(groups[0]['id'], message.chat.id)
            if isSuccess:
                bot.send_message(message.chat.id, 'Успешно зарегистрирован.')
                del user_data[message.chat.id]
                return
            else:
                bot.send_message(message.chat.id, 'Ошибка при сохранении пользователя. Обратитесь к администратору.')
                del user_data[message.chat.id]
                return

        if len(groups) > 1:
            bot.send_message(message.chat.id, 'Уточните запрос, найдено несколько групп:',
                             reply_markup=group_keyboard(groups))
            data.groups = groups
            return
        return

    if data.state == UserState.ASKING:
        if callback_data:
            next_question = data.next_question(callback_data)
        else:
            next_question = data.next_question(message.text)

        if next_question is None:
            bot.send_message(message.chat.id, 'Спасибо за опрос!')
            for answer in data.answers:
                api_quiz.postAnswer(testLessonId, answer.type, answer.answer, answer.question_id)
            del user_data[message.chat.id]

        else:
            ask_question(message.chat.id, next_question)
        return

    # до 10 кнопок. варианты для нового студента и препода (две кнопки при регистрации - студент или преподаватель).


# у студента нужно узнать группу. дедлайн - до вторника.

bot.polling()
