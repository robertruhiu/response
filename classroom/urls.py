from django.urls import include, path

from .views import students, teachers

urlpatterns = [


    path('students/', include(([
        path('', students.quizlist, name='quiz_list'),
        path('taken/', students.taken_quizlist, name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take, name='take'),
        path('tests/', students.student_registration, name='tests'),
        path('retake/<int:quizid>/<int:studentid>',students.retake, name='retake')
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.quizlist, name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.updatequiz, name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.quizresults, name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
    ], 'classroom'), namespace='teachers')),
]
