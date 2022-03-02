from django.contrib import admin

from users.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "date_joined", "is_superuser", "is_staff")
    list_filter = ("email", "date_joined", "is_superuser")

admin.site.register(CustomUser, CustomUserAdmin)
