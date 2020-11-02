import requests
from requests_toolbelt.adapters import host_header_ssl

from API.config import BASE_URL, CERT_PATH, HEADERS


def getGroups(groupNumber):
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'groups/' + groupNumber, verify=CERT_PATH, headers=HEADERS)
    if response.status_code == 400:
        return []
    return response.json()


def getTeachers(lastname="", firstname="", midname=""):
    namePattern = "%" + lastname + "%" + firstname + "%" + midname + "%"

    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'teachers/' + namePattern, verify=CERT_PATH, headers=HEADERS)
    if response.status_code == 400:
        return []
    return response.json()


def getAllStudents():
    s = requests.Session()
    s.mount('https://', host_header_ssl.HostHeaderSSLAdapter())
    response = s.get(BASE_URL + 'students', verify=CERT_PATH, headers=HEADERS)
    if response.status_code == 400:
        return []
    return response.json()


def createNewStudent(groupId, telegramId, login=""):
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
    if response.status_code == 400:
        return False
    return True
