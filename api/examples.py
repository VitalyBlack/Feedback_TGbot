import api.university as apiUni
import api.quiz as apiQuiz

# json = apiUni.getGroups('3')
# for element in json:
#     print(element)
#
# json = apiUni.getTeachers(firstname="ма")
# for element in json:
#     print(element)
#
# json = apiUni.getAllStudents()
# for element in json:
#     print("student" + str(element))
#
# bool = apiUni.createNewStudent(28055, 666)

testLessonId = 1
json = apiQuiz.getQuestions(testLessonId)
for element in json:
    print(element)

# if len(json) > 0:
#     print(apiQuiz.getAnswers(testLessonId))
#     testQuestionId = json[0]["question"]['id']
#     apiQuiz.postAnswer(testLessonId, 'numeric', '5', testQuestionId)
#     print(apiQuiz.getAnswers(testLessonId))
