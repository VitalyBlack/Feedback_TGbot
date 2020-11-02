import requests
from requests_toolbelt.adapters import host_header_ssl

from API.config import BASE_URL, CERT_PATH, HEADERS


def getGroups(groupNumber) -> list:
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'groups/' + groupNumber, verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json()


def getTeachers(searchPhraze) -> list:
    namePattern = "%" + searchPhraze + "%"
    namePattern.replace(' ', '%')

    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'teachers/' + namePattern, verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json()


def setTeacherChatId(teacherId, chatId) -> bool:
    data = {
        "id": teacherId,
        "telegram_id": chatId
    }

    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.patch(BASE_URL + 'teachers', data=data, verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return False
    return True


def getAllStudents() -> list:
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'students', verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return []
    return response.json()


def createNewStudent(groupId, telegramId, login="") -> bool:
    if len(login) == 0:
        studentData = {
            "group_id": groupId,
            "telegram_id": telegramId
        }
    else:
        studentData = {
            "login": login,
            "group_id": groupId,
            "telegram_id": telegramId
        }

    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.post(BASE_URL + 'students', data=studentData, verify=CERT_PATH, headers=HEADERS)
    if response.status_code != 200:
        return False
    return True
