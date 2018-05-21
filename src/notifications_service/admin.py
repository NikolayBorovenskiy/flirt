from django.contrib import admin

from .models import Notification, NotificationDelivery


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['uuid', ]

    class Meta:
        model = Notification


class NotificationDeliveryAdmin(admin.ModelAdmin):
    list_display = ['notification', ]

    class Meta:
        model = NotificationDelivery


admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationDelivery, NotificationDeliveryAdmin)
