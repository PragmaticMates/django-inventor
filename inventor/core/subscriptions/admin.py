from copy import deepcopy

from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from inventor.core.subscriptions.models import UserPlan, Plan, PlanQuota, Quota, Pricing


class UserLinkMixin(object):
    def user_link(self, obj):
        user_model = get_user_model()
        app_label = user_model._meta.app_label
        model_name = user_model._meta.model_name
        change_url = reverse('admin:%s_%s_change' % (app_label, model_name), args=(obj.user.id,))
        return format_html('<a href="{}">{}</a>', change_url, obj.user.username)

    user_link.short_description = 'User'
    user_link.allow_tags = True


class PlanQuotaInline(admin.TabularInline):
    model = PlanQuota


class PricingInline(admin.TabularInline):
    model = Pricing


class QuotaAdmin(admin.ModelAdmin):
    list_display = [
        'codename', 'name', 'description', 'unit',
        'is_boolean',
        #'move_up_down_links',
    ]

    list_display_links = list_display


def copy_plan(modeladmin, request, queryset):
    """
    Admin command for duplicating plans preserving quotas and pricings.
    """
    for plan in queryset:
        plan_copy = deepcopy(plan)
        plan_copy.id = None
        plan_copy.is_available = False
        plan_copy.is_default = False
        plan_copy.trial_duration = 0
        plan_copy.created = None
        plan_copy.save(force_insert=True)

        for pricing in plan.pricing_set.all():
            pricing.id = None
            pricing.plan = plan_copy
            pricing.save(force_insert=True)

        for quota in plan.planquota_set.all():
            quota.id = None
            quota.plan = plan_copy
            quota.save(force_insert=True)


copy_plan.short_description = _('Make a plan copy')


class PlanAdmin(admin.ModelAdmin):
    search_fields = ('name',
                     # 'customized__username', 'customized__email',
                     )
    list_filter = ('is_available', 'is_visible')
    list_display = [
        'title',
        # 'description',
        # 'customized',
        'trial_duration',
        'is_default', 'is_available',
        'created',
        # 'move_up_down_links'
    ]
    inlines = (
        PricingInline,
        PlanQuotaInline,
    )
    list_select_related = True
    # raw_id_fields = ('customized',)
    actions = [copy_plan, ]

    # def queryset(self, request):
    #     return super(PlanAdmin, self).queryset(request).select_related(
    #         'customized'
    #     )


# class RecurringPlanInline(admin.StackedInline):
#     model = RecurringUserPlan
#     extra = 0


class PricingAdmin(admin.ModelAdmin):
    list_select_related = ['plan']
    list_display = [
        'id',
        'plan',
        'duration', 'period',
        'price',
        'timedelta',
    ]


class UserPlanAdmin(UserLinkMixin, admin.ModelAdmin):
    actions = ['send_reminder']
    list_filter = (
        #'is_active',
        'expiration', 'plan__title', 'plan__is_available', 'plan__is_visible', 'modified', 'pricing')
    search_fields = ('user__email', 'plan__title',)
    list_display = ('id', 'user', 'plan', 'pricing', 'expiration',  # 'is_active',
                    # 'recurring__automatic_renewal', 'recurring__pricing'
                    'modified')
    list_select_related = True
    readonly_fields = ['user_link', ]
    # inlines = (RecurringPlanInline,)
    fields = ('user', 'user_link', 'plan', 'pricing', 'expiration', )  #'is_active')
    autocomplete_fields = ['user', 'plan', ]

    def recurring__automatic_renewal(self, obj):
        return obj.recurring.has_automatic_renewal
    recurring__automatic_renewal.admin_order_field = 'recurring__has_automatic_renewal'
    recurring__automatic_renewal.boolean = True

    def recurring__pricing(self, obj):
        return obj.recurring.pricing
    recurring__automatic_renewal.admin_order_field = 'recurring__pricing'

    def send_reminder(self, request, queryset):
        for obj in queryset:
            if obj.is_expired():
                messages.error(request, _('Userplan %s already expired') % obj)
            else:
                messages.success(request, _('Reminder sent (%s)') % obj)
                obj.send_reminder()
    send_reminder.short_description = _('Send reminder')


admin.site.register(Quota, QuotaAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Pricing, PricingAdmin)
admin.site.register(UserPlan, UserPlanAdmin)
