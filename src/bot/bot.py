import telebot
import src.api.quiz as api_quiz
import src.api.university as api_uni
from src.bot.utils import QuestionType, RegistrationKeyboard, Data, UserState, NumericKeyboard, NoQuestionsMarkup, \
    teacher_keyboard, group_keyboard

from src.resources.bot_token import BOT_TOKEN
import src.resources.text as txt

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

# TODO УБРАТЬ ПОЗЖЕ
testLessonId = 1
testUserId = 176664413


@bot.message_handler(commands=['start'])
def stop(message):
    bot.send_message(message.chat.id, txt.ABOUT, parse_mode='Markdown')
    bot.send_message(message.chat.id, txt.HELP, parse_mode='Markdown')


@bot.message_handler(commands=['stop'])
def stop(message):
    if message.chat.id not in user_data:
        return
    data = user_data[message.chat.id]
    if data.state == UserState.ASKING:
        data.answers = None
        data.questions = None
        data.current_question = None
        data.state = UserState.WAITING
    else:
        del user_data[message.chat.id]
    return


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, txt.HELP, parse_mode='Markdown')
    return


@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, txt.ABOUT, parse_mode='Markdown')
    return


@bot.message_handler(commands=['register'])
def registration(message):
    if message.chat.id in user_data:
        bot.send_message(message.chat.id, txt.CANNOT_REGISTER_NOW)
        return

    bot.send_message(message.chat.id, txt.ARE_YOU_A_STUDENT, reply_markup=RegistrationKeyboard.keyboard)
    data = Data()
    data.state = UserState.REG_1
    user_data[message.chat.id] = data


@bot.message_handler(commands=['test'])
def test(message):
    startPoll(message.chat.id, testLessonId)


def startPoll(chatId, lessonId):
    data = Data(lessonId)
    user_data[chatId] = data
    keyboard = telebot.types.InlineKeyboardMarkup()
    begin_quiz = telebot.types.InlineKeyboardButton(text="Начать опрос", callback_data="begin")
    keyboard.add(begin_quiz)
    bot.send_message(chatId, txt.PRESS_TO_BEGIN, reply_markup=keyboard)


@bot.message_handler(commands=['begin'])
def begin(message):
    if message.chat.id not in user_data:
        bot.send_message(message.chat.id, txt.WAIT_FOR_NEXT_POLL)
        return

    data = user_data[message.chat.id]

    if data.state != UserState.WAITING:
        print('Error')
        return

    first_question = data.start()
    ask_question(message.chat.id, first_question)


def ask_question(chat_id, question):
    if QuestionType(question.type) is QuestionType.TEXT:
        bot.send_message(chat_id, question.text + txt.TEXT_ANSWER, parse_mode='Markdown')

    if QuestionType(question.type) is QuestionType.NUMERIC:
        bot.send_message(chat_id, question.text + txt.NUMBER_ANSWER,
                         reply_markup=NumericKeyboard.keyboard, parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        handle(call.message, call.data)


def ask_for_questions(id):
    bot.send_message(id,
                     txt.ADDITIONAL_QUESTIONS,
                     reply_markup=NoQuestionsMarkup.keyboard, parse_mode='Markdown')
    pass


@bot.message_handler(content_types=['text'])
def handle(message, callback_data=None):
    if message.chat.id not in user_data:
        bot.send_message(message.chat.id, txt.WAIT_FOR_NEXT_POLL)
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

        bot.send_message(message.chat.id, txt.PRESS_TO_BEGIN)
        return

    if data.state == UserState.REG_1:
        if callback_data:
            if (callback_data == 'Нет'):
                data.state = UserState.TEACHER_1
                bot.send_message(message.chat.id, txt.ENTER_FIO)
            else:
                data.state = UserState.STUDENT_1
                bot.send_message(message.chat.id, txt.ENTER_GROUP)
        else:
            bot.send_message(message.chat.id, txt.ANSWER_LAST_QUESTION)
        return

    if data.state == UserState.TEACHER_1:
        if callback_data and data.teachers:
            id = callback_data
            print(id)
            print(int(id))
            for teacher in data.teachers:
                if teacher['id'] == int(id):
                    bot.send_message(message.chat.id, 'Найден 1 преподаватель: ' + teacher['full_name'])
                    isSuccess = api_uni.setTeacherChatId(int(id), message.chat.id)
                    if isSuccess:
                        bot.send_message(message.chat.id, 'Успешно зарегистрирован.')
                        del user_data[message.chat.id]
                        return
            bot.send_message(message.chat.id,
                             txt.SAVE_USER_ERROR)
            del user_data[message.chat.id]
            return


        fullname = message.text
        teachers = api_uni.getTeachers(fullname)
        if len(teachers) == 0:
            bot.send_message(message.chat.id, txt.NO_TEACHERS_FOUND)
            return

        if len(teachers) == 1:
            bot.send_message(message.chat.id, 'Найден 1 преподаватель: ' + teachers[0]['full_name'])
            isSuccess = api_uni.setTeacherChatId(teachers[0]['id'], message.chat.id)
            if isSuccess:
                bot.send_message(message.chat.id, txt.SUCCESS_REGISTER)
                del user_data[message.chat.id]
                return
            else:
                bot.send_message(message.chat.id, txt.SAVE_USER_ERROR)
                del user_data[message.chat.id]
                return

        if len(teachers) > 1:
            bot.send_message(message.chat.id,
                             txt.TOO_MUCH_TEACHERS,
                             reply_markup=teacher_keyboard(teachers))
            data.teachers = teachers

            return
        return

    if data.state == UserState.STUDENT_1:
        if callback_data and data.groups:
            id = callback_data
            for group in data.groups:
                if group['id'] == int(id):
                    bot.send_message(message.chat.id, 'Найдена 1 группа: ' + group['name'])
                    isSuccess = api_uni.createNewStudent(int(id), message.chat.id)
                    if isSuccess:
                        bot.send_message(message.chat.id, 'Успешно зарегистрирован.')
                        del user_data[message.chat.id]
                        return
            bot.send_message(message.chat.id,
                             txt.SAVE_USER_ERROR)
            del user_data[message.chat.id]
            # TODO юзер уже выбрал группу
            return

        groupNumber = message.text
        groups = api_uni.getGroups(groupNumber)
        if len(groups) == 0:
            bot.send_message(message.chat.id, txt.NO_GROUPS_FOUND)
            return

        if len(groups) == 1:
            bot.send_message(message.chat.id, 'Найдена 1 группа: ' + groups[0]['name'])
            isSuccess = api_uni.createNewStudent(groups[0]['id'], message.chat.id)
            if isSuccess:
                bot.send_message(message.chat.id, txt.SUCCESS_REGISTER)
                del user_data[message.chat.id]
                return
            else:
                bot.send_message(message.chat.id, txt.SAVE_USER_ERROR)
                del user_data[message.chat.id]
                return

        if len(groups) > 1:
            bot.send_message(message.chat.id, txt.TOO_MUCH_GROUPS,
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
            data.state = UserState.ADDITIONAL_QUESTIONS
            ask_for_questions(message.chat.id)
            for answer in data.answers:
                api_quiz.postAnswer(data.lessonId, answer.type, answer.answer, answer.question_id)
            data.questions = None
            data.answers = None
        else:
            ask_question(message.chat.id, next_question)
        return

    if data.state == UserState.ADDITIONAL_QUESTIONS:
        if callback_data:
            bot.send_message(message.chat.id, txt.THANKS_FOR_POLL)
            del user_data[message.chat.id]
        else:
            api_quiz.postNewQuestion(data.lessonId, message.text)
            ask_for_questions(message.chat.id)


def runBot():
    print("bot start polling")
    bot.polling()
    print("bot start polling 2")


async def startPollForUsers(userIds, lessonId):
    for userId in userIds:
        startPoll(userId, lessonId)


# TODO
async def sendResultsToTeacher(teacherId, lessonId):
    print(f"sendResultsToTeacher: {teacherId}, {lessonId}")
    return

# TODO
async def joinStudents(high_id, low_id):
    print(f"joinStudents: {high_id}, {low_id}")
    return
