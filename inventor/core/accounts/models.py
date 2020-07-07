from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
# from whistle.mixins import UserNotificationsMixin
from internationalflavor.countries import CountryField
from inventor.core.accounts.managers import UserManager, UserQuerySet
from inventor.core.accounts.utils import avatar_path_handler, avatar_thumbnail_exists, create_avatar_thumbnail


class User(AbstractBaseUser, PermissionsMixin):  # UserNotificationsMixin
    MAX_USERNAME_LENGTH = 30
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    GENDER_MALE = 'MALE'
    GENDER_FEMALE = 'FEMALE'
    GENDERS = [
        (GENDER_MALE, _('male')),
        (GENDER_FEMALE, _('female')),
    ]

    # Name
    first_name = models.CharField(_('first name'), max_length=30, blank=True, db_index=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, db_index=True)
    
    # Contact details
    email = models.EmailField(_('email'), unique=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True)

    # Address
    street = models.CharField(_('street and number'), max_length=200, blank=True)
    postcode = models.CharField(_('postcode'), max_length=30, blank=True)
    city = models.CharField(_('city'), max_length=50, blank=True)
    country = CountryField(verbose_name=_('Country'), db_index=True, blank=True)

    # Date of birth
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True, default=None)

    # Other
    gender = models.CharField(_('gender'), choices=GENDERS, max_length=6, blank=True)
    team = models.CharField(_('team/club'), max_length=50, blank=True)

    # Management
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=now)
    last_seen = models.DateTimeField(_('last seen'),
        blank=True, null=True, default=None)
    avatar = models.ImageField(
        verbose_name=_('avatar'),
        help_text=_('photo, image or icon'),
        max_length=1024,
        upload_to=avatar_path_handler,
        blank=True,
    )
    preferred_language = models.CharField(_('language'), max_length=5, choices=settings.LANGUAGES)

    # agreements / GDPR
    agree_terms_and_conditions = models.BooleanField(_('Terms and conditions'), default=True)
    agree_privacy_policy = models.BooleanField(_('Privacy policy'), default=True)
    agree_marketing_purposes = models.BooleanField(_('Marketing purposes'), default=True)
    agree_social_networks_sharing = models.BooleanField(_('Sharing on social networks'), default=True)

    objects = UserManager()
    qs = UserQuerySet.as_manager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('first_name', 'last_name', 'email')
        default_permissions = settings.DEFAULT_PERMISSIONS

    def __str__(self):
        return self.get_full_name() or self.email

    def get_absolute_url(self):
        return reverse('inventor:accounts:user_update_profile')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_avatar_url(self, size):
        if self.avatar:
            if not avatar_thumbnail_exists(self, size):
                create_avatar_thumbnail(self, size)

            return self.avatar.storage.url(self.avatar_name(size))
        return settings.AVATAR_DEFAULT_URL

    def avatar_name(self, size):
        def find_extension(format):
            format = format.lower()

            if format == 'jpeg':
                format = 'jpg'

            return format

        ext = find_extension(settings.AVATAR_THUMB_FORMAT)

        return avatar_path_handler(
            instance=self,
            size=size,
            ext=ext
        )
