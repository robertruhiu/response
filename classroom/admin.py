from django.contrib import admin
from classroom.models import Quiz,Student,StudentAnswer,Answer,TakenQuiz,Subject,Question

admin.site.register(Quiz)
admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(Answer)
admin.site.register(TakenQuiz)
admin.site.register(Subject)
admin.site.register(Question)