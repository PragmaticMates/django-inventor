import logging
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from inventor.core.subscriptions.querysets import PlanQuerySet

accounts_logger = logging.getLogger('accounts')


class Plan(models.Model):
    title = models.CharField(unique=True, max_length=50)
    order = models.PositiveSmallIntegerField(verbose_name=_('ordering'), help_text=_('to set order in pricing'), unique=True, default=1)
    trial_duration = models.PositiveSmallIntegerField(verbose_name=_('trial duration'), help_text=_('in days'), default=0)
    is_default = models.BooleanField(
        help_text=_('Default plan for user'),
        default=False,
        db_index=True,
    )
    is_available = models.BooleanField(
        _('available'), default=False, db_index=True,
        help_text=_('Is still available for purchase')
    )
    is_visible = models.BooleanField(
        _('visible'), default=True, db_index=True,
        help_text=_('Is visible in current offer')
    )
    quotas = models.ManyToManyField('Quota', through='PlanQuota')
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = PlanQuerySet.as_manager()

    class Meta:
        verbose_name = _(u'plan')
        verbose_name_plural = _(u'plans')
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('inventor:subscriptions:plans')

    @classmethod
    def get_default_plan(cls):
        try:
            return_value = cls.objects.get(is_default=True)
        except cls.DoesNotExist:
            return_value = None
        return return_value

    @classmethod
    def get_current_plan(cls, user):
        """ Get current plan for user. If userplan is expired, return None """
        # We need to handle both default plan (new user -> TRIAL) and expired plan -> None
        if not user or user.is_anonymous or not hasattr(user, 'subscription') or user.subscription.is_expired():
            return None
            # default_plan = Plan.get_default_plan()
            # if default_plan is None or not default_plan.is_free():
            #     raise ValidationError(_('User plan has expired'))
            # return default_plan
        return user.subscription.plan

    def get_quotas(self):
        quota_dic = {}
        for plan_quota in PlanQuota.objects.filter(plan=self).select_related('quota'):
            quota_dic[plan_quota.quota.codename] = plan_quota.value
        return quota_dic

    def is_free(self):
        return not self.pricing_set.exists()
    is_free.boolean = True


class Pricing(models.Model):
    PERIOD_DAY = 'DAY'
    PERIOD_MONTH = 'MONTH'
    PERIOD_YEAR = 'YEAR'
    PERIODS = [
        (PERIOD_DAY, _('day')),
        (PERIOD_MONTH, _('month')),
        (PERIOD_YEAR, _('year')),
    ]
    PERIODS_PLURALIZE = [
        (PERIOD_DAY, (_('day'), _('days'))),
        (PERIOD_MONTH, (_('month'), _('months'))),
        (PERIOD_YEAR, (_('year'), _('years'))),
    ]

    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    period = models.CharField(_('period'), choices=PERIODS, max_length=5, blank=True)
    duration = models.PositiveSmallIntegerField(verbose_name=_('duration'), help_text=_('in period'),
                                           blank=True, null=True, default=None)
    price = models.DecimalField(_('price'), help_text=settings.INVENTOR_CURRENCY, max_digits=10, decimal_places=2, db_index=True, validators=[MinValueValidator(0.01)],
                                blank=True, null=True, default=None)
    # is_default = models.BooleanField(
    #     help_text=_('Default plan for user'),
    #     default=False,
    #     db_index=True,
    # )
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)
    objects = PlanQuerySet.as_manager()

    class Meta:
        verbose_name = _(u'pricing plan')
        verbose_name_plural = _(u'pricing plans')
        ordering = ['price']

    def __str__(self):
        return f'{self.plan} ({self.get_duration_display()})'

    def get_absolute_url(self):
        return reverse('inventor:subscriptions:plans')

    def get_duration_display(self):
        period_localize = dict(self.PERIODS_PLURALIZE).get(self.period)
        preiod_display = period_localize[0] if self.duration == 1 else period_localize[1]  # TODO: i18n
        return f'{self.duration} {preiod_display}'

    def get_price_display(self):
        return f'{self.price} {settings.INVENTOR_CURRENCY}'

    def get_add_to_cart_url(self):  # TODO: move to ProductMixin
        content_type = ContentType.objects.get_for_model(self)
        return reverse('commerce:add_to_cart', args=(content_type.id, self.id))

    @property
    def price_per_month(self):
        if self.period == self.PERIOD_DAY:
            return self.price * 30 / self.duration  # approximately

        if self.period == self.PERIOD_MONTH:
            return self.price / self.duration

        if self.period == self.PERIOD_YEAR:
            return self.price / 12 / self.duration

    def get_price_per_month_display(self):
        return f'{self.price_per_month} {settings.INVENTOR_CURRENCY}'

    @property
    def timedelta(self):
        if self.period == self.PERIOD_DAY:
            return timedelta(days=self.duration)

        if self.period == self.PERIOD_MONTH:
            return relativedelta(months=self.duration)

        if self.period == self.PERIOD_YEAR:
            return relativedelta(years=self.duration)


class UserPlan(models.Model):
    """
    Currently selected plan for user account.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_('user'),
        on_delete=models.CASCADE, related_name='subscription', related_query_name='subscription'
    )
    plan = models.ForeignKey('Plan', verbose_name=_('plan'), on_delete=models.CASCADE)
    pricing = models.ForeignKey('Pricing', help_text=_('pricing'), default=None,
                                null=True, blank=True, on_delete=models.CASCADE)
    expiration = models.DateField(_('Expires'), default=None, blank=True, null=True, db_index=True)
    # is_active = models.BooleanField(_('active'), default=True, db_index=True)
    # is_recurring = models.BooleanField(_('active'), default=True, db_index=True)  # TODO: can be turned on/turned off
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _("User plan")
        verbose_name_plural = _("Users plans")

    def __str__(self):
        return "%s [%s]" % (self.user, self.plan)

    # def is_active(self):
    #     return self.active

    def is_expired(self):
        if self.expiration is None:
            return False
        else:
            return self.expiration < date.today()

    def days_left(self):
        if self.expiration is None:
            return None
        else:
            return (self.expiration - date.today()).days

    # def clean_activation(self):
    #     errors = plan_validation(self.user)
    #     if not errors['required_to_activate']:
    #         plan_validation(self.user, on_activation=True)
    #         self.activate()
    #     else:
    #         self.deactivate()
    #     return errors
    #
    # def activate(self):
    #     if not self.active:
    #         self.active = True
    #         self.save()
    #         account_activated.send(sender=self, user=self.user)
    #
    # def deactivate(self):
    #     if self.active:
    #         self.active = False
    #         self.save()
    #         account_deactivated.send(sender=self, user=self.user)

    # def initialize(self):
    #     """
    #     Set up user plan for first use
    #     """
    #     if not self.is_active():
    #         # Plans without pricings don't need to expire
    #         if self.expiration is None and self.plan.pricing_set.count():
    #             self.expiration = now() + timedelta(
    #                 days=getattr(settings, 'PLANS_DEFAULT_GRACE_PERIOD', 30))
    #         self.activate()  # this will call self.save()

    def get_plan_extended_from(self, plan):
        if plan.is_free():
            return None
        if not self.is_expired() and self.expiration is not None and self.plan == plan:
            return self.expiration
        return date.today()

    def get_plan_extended_until(self, plan, pricing):
        if plan.is_free():
            return None
        if not self.plan.is_free() and self.expiration is None:
            return None
        if pricing is None:
            return self.expiration
        return self.get_plan_extended_from(plan) + pricing.timedelta
        # from_date = self.get_plan_extended_from(plan)
        # return from_date + self.plan.timedelta

    def plan_autorenew_at(self):
        """
        Helper function which calculates when the plan autorenewal will occur
        """
        if self.expiration:
            plans_autorenew_before_days = getattr(settings, 'PLANS_AUTORENEW_BEFORE_DAYS', 0)
            plans_autorenew_before_hours = getattr(settings, 'PLANS_AUTORENEW_BEFORE_HOURS', 0)
            return self.expiration - timedelta(days=plans_autorenew_before_days, hours=plans_autorenew_before_hours)

    # def set_plan_renewal(self, order, has_automatic_renewal=True, **kwargs):
    #     """
    #     Creates or updates plan renewal information for this userplan with given order
    #     """
    #     if hasattr(self, 'recurring'):
    #         # Delete the plan to populate with default values
    #         # We don't want to mix the old and new values
    #         self.recurring.delete()
    #     recurring = RecurringUserPlan.objects.create(
    #         user_plan=self,
    #         pricing=order.pricing,
    #         amount=order.amount,
    #         tax=order.tax,
    #         currency=order.currency,
    #         has_automatic_renewal=has_automatic_renewal,
    #         **kwargs,
    #     )
    #     return recurring

    def extend_account(self, plan, pricing):
        """
        Manages extending account after plan or pricing order
        :param plan:
        :param pricing: if pricing is None then account will be only upgraded
        :return:
        """

        if pricing and pricing.plan != plan:
            raise ValueError(f'Extending by plan {plan} by invalid pricing {pricing}!')

        status = False  # flag; if extending account was successful?
        new_expiration = self.get_plan_extended_until(plan, pricing)

        print('new_expiration', new_expiration)
        if pricing is None:
            # Process a plan change request (downgrade or upgrade)
            # No account activation or extending at this point
            self.plan = plan

            # if self.expiration is not None and not plan.pricing_set.count():
            #     # Assume no expiry date for plans without pricing.
            #     self.expiration = None

            self.expiration = new_expiration
            self.save()

            account_change_plan.send(sender=self, user=self.user)
            # if getattr(settings, 'PLANS_SEND_EMAILS_PLAN_CHANGED', True):
            #     mail_context = {'user': self.user, 'userplan': self, 'plan': plan}
            #     send_template_email([self.user.email], 'mail/change_plan_title.txt', 'mail/change_plan_body.txt',
            #                         mail_context, get_user_language(self.user))
            accounts_logger.info("Account '%s' [id=%d] plan changed to '%s' [id=%d]" % (self.user, self.user.pk, plan, plan.pk))
            status = True

        else:
            # Processing standard account extending procedure
            if self.plan == plan:
                status = True
            else:
                # This should not ever happen (as this case should be managed by plan change request)
                # but just in case we consider a case when user has a different plan
                if not self.plan.is_free() and self.expiration is None:
                    status = True
                elif not self.plan.is_free() and self.expiration > date.today():
                    status = False
                    accounts_logger.warning("Account '%s' [id=%d] plan NOT changed to '%s' [id=%d]" % (
                        self.user, self.user.pk, plan, plan.pk))
                else:
                    status = True
                    account_change_plan.send(sender=self, user=self.user)
                    self.plan = plan

            if status:
                self.expiration = new_expiration
                self.save()
                accounts_logger.info("Account '%s' [id=%d] has been extended by %d days using plan '%s' [id=%d]" % (
                    self.user, self.user.pk, pricing.timedelta.days, plan, plan.pk))
                # if getattr(settings, 'PLANS_SEND_EMAILS_PLAN_EXTENDED', True):
                    # mail_context = {'user': self.user,
                    #                 'userplan': self,
                    #                 'plan': plan,
                    #                 'pricing': pricing}
                    # send_template_email([self.user.email], 'mail/extend_account_title.txt',
                    #                     'mail/extend_account_body.txt',
                    #                     mail_context, get_user_language(self.user))

        # if status:
        #     self.clean_activation()

        return status

    def expire_account(self):
        """manages account expiration"""

        self.deactivate()

        accounts_logger.info(
            "Account '%s' [id=%d] has expired" % (self.user, self.user.pk))

        mail_context = {'user': self.user, 'userplan': self}
        send_template_email([self.user.email], 'mail/expired_account_title.txt', 'mail/expired_account_body.txt',
                            mail_context, get_user_language(self.user))

        account_expired.send(sender=self, user=self.user)

    def remind_expire_soon(self):
        """reminds about soon account expiration"""

        mail_context = {
            'user': self.user,
            'userplan': self,
            'days': self.days_left()
        }
        send_template_email([self.user.email], 'mail/remind_expire_title.txt', 'mail/remind_expire_body.txt',
                            mail_context, get_user_language(self.user))

    @classmethod
    def create_for_user(cls, user, pricing=None):
        if pricing:
            plan = pricing.plan
            expiration = now() + pricing.timedelta
        else:
            plan = Plan.get_default_plan()

            # check if default plan is available
            if not plan:
                return
    
            expiration = None if plan.is_free() else now() + timedelta(days=plan.trial_duration)

        return UserPlan.objects.create(
            user=user,
            plan=plan,
            pricing=pricing,
            # active=False,
            expiration=expiration,
        )

    @classmethod
    def create_for_users_without_plan(cls):
        userplans = get_user_model().objects.filter(subscription=None)
        for user in userplans:
            UserPlan.create_for_user(user)
        return userplans


# class RecurringUserPlan(models.Model):
#     """
#     OneToOne model associated with UserPlan that stores information about the plan recurrence.
#     More about recurring payments in docs.
#     """
#     user_plan = models.OneToOneField('UserPlan', on_delete=models.CASCADE, related_name='recurring')
#     token = models.CharField(
#         _('recurring token'),
#         help_text=_('Token, that will be used for payment renewal. Depends on used payment provider'),
#         max_length=255,
#         default=None,
#         null=True,
#         blank=True,
#     )
#     payment_provider = models.CharField(
#         _('payment provider'),
#         help_text=_('Provider, that will be used for payment renewal'),
#         max_length=255,
#         default=None,
#         null=True,
#         blank=True,
#     )
#     pricing = models.ForeignKey('Pricing', help_text=_('Recurring pricing'), default=None,
#                                 null=True, blank=True, on_delete=models.CASCADE)
#     amount = models.DecimalField(
#         _('amount'), max_digits=7, decimal_places=2, db_index=True, null=True, blank=True)
#     tax = models.DecimalField(_('tax'), max_digits=4, decimal_places=2, db_index=True, null=True,
#                               blank=True)  # Tax=None is when tax is not applicable
#     currency = models.CharField(_('currency'), max_length=3)
#     has_automatic_renewal = models.BooleanField(
#         _('has automatic plan renewal'),
#         help_text=_(
#             'Automatic renewal is enabled for associated plan. '
#             'If False, the plan renewal can be still initiated by user.',
#         ),
#         default=False,
#     )
    # card_expire_year = models.IntegerField(null=True, blank=True)
    # card_expire_month = models.IntegerField(null=True, blank=True)
    # card_masked_number = models.CharField(null=True, blank=True, max_length=255)
    #
    # def create_renew_order(self):
    #     """
    #     Create order for plan renewal
    #     """
    #     userplan = self.user_plan
    #     return Order.objects.create(
    #         user=userplan.user,
    #         plan=userplan.plan,
    #         pricing=userplan.recurring.pricing,
    #         amount=userplan.recurring.amount,
    #         tax=userplan.recurring.tax,
    #         currency=userplan.recurring.currency,
    #     )


# class Pricing(models.Model):
#     """
#     Type of plan period that could be purchased (e.g. 10 days, month, year, etc)
#     """
#     name = models.CharField(_('name'), max_length=100)
#     period = models.PositiveIntegerField(
#         _('period'), default=30, null=True, blank=True, db_index=True)
#     url = models.URLField(max_length=200, blank=True, help_text=_(
#         'Optional link to page with more information (for clickable pricing table headers)'))
#
#     class Meta:
#         ordering = ('period',)
#         verbose_name = _("Pricing")
#         verbose_name_plural = _("Pricings")
#
#     def __str__(self):
#         return "%s (%d " % (self.name, self.period) + "%s)" % _("days")
#
#
class Quota(models.Model):
    """
    Single countable or boolean property of system (limitation).
    """
    codename = models.CharField(_('codename'), max_length=50, unique=True, db_index=True)
    name = models.CharField(_('name'), max_length=100)
    unit = models.CharField(_('unit'), max_length=100, blank=True)
    description = models.TextField(_('description'), blank=True)
    is_boolean = models.BooleanField(_('is boolean'), default=False)

    class Meta:
        ordering = ('name',)  # TODO: custom ordering
        verbose_name = _("Quota")
        verbose_name_plural = _("Quotas")

    def __str__(self):
        return "%s" % (self.codename, )


# class PlanPricingManager(models.Manager):
#     def get_query_set(self):
#         return super(PlanPricingManager, self).get_query_set().select_related('plan', 'pricing')


# class PlanPricing(models.Model):
#     plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
#     pricing = models.ForeignKey('Pricing', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=7, decimal_places=2, db_index=True)
#     order = models.IntegerField(default=0, null=False, blank=False)
#     has_automatic_renewal = models.BooleanField(
#         _('has automatic renewal'),
#         help_text=_('Use automatic renewal if possible?'),
#         default=False,
#     )
#
#     objects = PlanPricingManager()
#
#     class Meta:
#         ordering = ('order', 'pricing__period', )
#         verbose_name = _("Plan pricing")
#         verbose_name_plural = _("Plans pricings")
#
#     def __str__(self):
#         return "%s %s" % (self.plan.name, self.pricing)


class PlanQuotaManager(models.Manager):
    def get_query_set(self):
        return super(PlanQuotaManager, self).get_query_set().select_related('plan', 'quota')


class PlanQuota(models.Model):
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    quota = models.ForeignKey('Quota', on_delete=models.CASCADE)
    value = models.IntegerField(default=1, null=True, blank=True)
    objects = PlanQuotaManager()

    class Meta:
        verbose_name = _("Plan quota")
        verbose_name_plural = _("Plans quotas")


from .signals import *
