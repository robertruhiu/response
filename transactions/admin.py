from django.contrib import admin
from transactions.models import Candidate, Transaction


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
