from django.contrib import admin

from projects.models import Project, Framework, Language


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)


class FrameworkAdmin(admin.ModelAdmin):
    pass


admin.site.register(Framework, FrameworkAdmin)


class LanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
