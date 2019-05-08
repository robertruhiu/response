from django.contrib import admin
from transactions.models import Candidate, Transaction,OpenCall,Applications

from frontend.models import candidatesprojects,Report

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
admin.site.register(OpenCall)
admin.site.register(Applications)
admin.site.register(Report)