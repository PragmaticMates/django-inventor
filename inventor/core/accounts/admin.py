from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from inventor.core.accounts.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    add_fieldsets = (
        (_('Password'), {'fields': ('password1', 'password2')}),
        (_('Login'), {'fields': ('email',)}),
    )
    fieldsets = (
        (None, {'fields': ('password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'avatar')}),
        (_('Contact'), {'fields': ('email', 'phone',)}),
        (_('Address'), {'fields': ('street', 'postcode', 'city', 'country')}),
        (_('Other'), {'fields': ('date_of_birth', 'gender', 'team', 'preferred_language')}),
        (_('Agreements'), {'fields': ('agree_terms_and_conditions', 'agree_privacy_policy', 'agree_marketing_purposes', 'agree_social_networks_sharing')}),
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
