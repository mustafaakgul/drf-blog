from django.contrib import admin
from accounts.models import Profile


admin.site.register(Profile)


@admin.register(CustomUserModel)
class CustomAdmin(UserAdmin):
    list_display = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Avatar Değiştirme Alanı', {
            'fields': ['avatar']
        }),
    )
