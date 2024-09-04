from django.contrib import admin
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.using('authentication')

    def save_model(self, request, obj, form, change):
        obj.save(using='authentication')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
