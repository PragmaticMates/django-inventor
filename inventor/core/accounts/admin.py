from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Permission
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import ugettext_lazy as _
from inventor.core.accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    add_fieldsets = (
        (_('Password'), {'fields': ('password1', 'password2')}),
        (_('Login'), {'fields': ('email',)}),
    )
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        (_('Contact'), {'fields': ('phone',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # (_('Notifications'), {'fields': ('notices_settings',)}),
    )
    ordering = ('last_name', 'first_name')


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'model_display', 'app_label', 'codename')
    search_fields = ('name', 'codename')
    list_select_related = ('content_type',)

    def app_label(self, obj):
        return obj.content_type.app_label

    def model_display(self, obj):
        return obj.content_type.model
