import requests
from requests_toolbelt.adapters import host_header_ssl

from API.config import BASE_URL, CERT_PATH, HEADERS


def getQuestions(lessonId) -> list:
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'quiz/' + str(lessonId), verify=CERT_PATH, headers=HEADERS)
    if response.status_code == 400:
        return []
    return response.json()


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
    if response.status_code == 400:
        return False
    return True


def getAnswers(lessonId) -> list:
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'quiz/' + str(lessonId) + '/answers', verify=CERT_PATH, headers=HEADERS)
    if response.status_code == 400:
        return []
    return response.json()
