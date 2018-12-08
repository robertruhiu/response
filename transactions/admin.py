from django.contrib import admin
from transactions.models import Candidate, Transaction
from classroom.models import Quiz,Student,TakenQuiz,Question,Answer,StudentAnswer,Subject
from frontend.models import candidatesprojects

# Register your models here.

class CandidateAdmin(admin.ModelAdmin):
    pass


class CandidateInline(admin.TabularInline):
    model = Candidate


admin.site.register(Candidate, CandidateAdmin)


class TransactionAdmin(admin.ModelAdmin):
    inlines = [
        CandidateInline,
    ]


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(candidatesprojects)
admin.site.register(Quiz)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(TakenQuiz)
admin.site.register(Question)
admin.site.register(Answer)