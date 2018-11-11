from django.contrib import admin

from testing.models import IpAddress, Snapshot


# Register your models here.

class IpAddressAdmin(admin.ModelAdmin):
    pass
admin.site.register(IpAddress, IpAddressAdmin)


class SnapshotAdmin(admin.ModelAdmin):
    pass
admin.site.register(Snapshot, SnapshotAdmin)
