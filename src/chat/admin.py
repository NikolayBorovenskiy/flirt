from django.contrib import admin

from chat.models import Thread


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['uuid', ]

    class Meta:
        model = Thread


admin.site.register(Thread, ThreadAdmin)
