import asyncio
import flask
from flask_cors import cross_origin

from rest import app
from bot.bot import startPollForUsers, sendResultsToTeacher, joinStudents


@app.route('/bot/start_poll', methods=['POST'])
@cross_origin()
def start_poll():
    json = flask.request.json
    if json is None:
        return "Wrong JSON format", 400
    print(json)
    if 'user_ids' not in json:
        return "Wrong JSON format - no 'chatIds' key", 400
    if 'lesson_id' not in json:
        return "Wrong JSON format - no 'lesson_id' key", 400

    userIds = json['user_ids']
    lessonId = json['lesson_id']
    asyncio.run(startPollForUsers(userIds, lessonId))

    return "OK", 200


# TODO по апишке доп. параметры
@app.route('/bot/send_results', methods=['POST'])
@cross_origin()
def send_results():
    json = flask.request.json
    if json is None:
        return "Wrong JSON format", 400
    print(json)
    if 'teacher_telegram_id' not in json:
        return "Wrong JSON format - no 'teacher_telegram_id' key", 400
    if 'lesson_id' not in json:
        return "Wrong JSON format - no 'lesson_id' key", 400

    teacher_telegram_id = json['teacher_telegram_id']
    lessonId = json['lesson_id']
    asyncio.run(sendResultsToTeacher(teacher_telegram_id, lessonId))

    return "OK", 200


@app.route('/bot/join_students', methods=['POST'])
@cross_origin()
def join_students():
    json = flask.request.json
    if json is None:
        return "Wrong JSON format", 400
    print(json)
    if 'high_chat_id' not in json:
        return "Wrong JSON format - no 'high_chat_id' key", 400
    if 'low_chat_id' not in json:
        return "Wrong JSON format - no 'low_chat_id' key", 400

    high_chat_id = json['high_chat_id']
    low_chat_id = json['low_chat_id']
    asyncio.run(joinStudents(high_chat_id, low_chat_id))

    return "OK", 200
