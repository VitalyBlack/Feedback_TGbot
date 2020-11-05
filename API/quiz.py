import requests
from requests_toolbelt.adapters import host_header_ssl

from API.config import BASE_URL, CERT_PATH, HEADERS
from utils import Question


def getQuestions(lessonId) -> list:
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'quiz/' + str(lessonId), verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return []
    questions = []
    for element in response.json():
        questions.append(
            Question(
                element['question']['id'],
                element['question']['text'],
                element['question']['type']
            )
        )
    return questions


def postAnswer(lessonId, type, answer, questionId, studentId=None) -> bool:
    if studentId == None:
        answerData = {
            "answer_type": type,
            "answer": answer,
            "question_id": questionId
        }
    else:
        answerData = {
            "answer_type": type,
            "answer": answer,
            "question_id": questionId,
            "student_id": 0
        }

    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.post(BASE_URL + 'quiz/' + str(lessonId), data=answerData, verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return False
    return True


def postNewQuestion(lessonId, text) -> bool:
    answerData = {
        "answer_type": 'questions',
        "answer": text
    }

    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.post(BASE_URL + 'quiz/' + str(lessonId), data=answerData, verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return False
    return True


def getAnswers(lessonId) -> list:
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'quiz/' + str(lessonId) + '/answers', verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json()
