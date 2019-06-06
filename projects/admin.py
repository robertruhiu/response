from django.contrib import admin

from projects.models import Project, Framework, Language,Projecttype,Devtype


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

class ProjecttypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Projecttype, ProjecttypeAdmin)

class DevtypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Devtype, DevtypeAdmin)
