from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.account.models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
    )

    def get_password(self, instance):
        return instance.password

    get_password.short_description = "Password"


admin.site.register(User, UserAdmin)
