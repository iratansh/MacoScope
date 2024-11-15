from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    def get_queryset(self, request):
        # Force the admin to use the 'authentication' database
        return super().get_queryset(request).using('authentication')

    def save_model(self, request, obj, form, change):
        # Save the user to the 'authentication' database
        obj.save(using='authentication')

    def delete_model(self, request, obj):
        # Delete the user from the 'authentication' database
        obj.delete(using='authentication')

    def get_form(self, request, obj=None, **kwargs):
        # Ensure the form also uses the 'authentication' database
        form = super().get_form(request, obj, **kwargs)
        form.using = 'authentication'
        return form




