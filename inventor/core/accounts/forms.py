from allauth.account.forms import SignupForm as AllAuthSignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from crispy_forms.bootstrap import FormActions, InlineRadios, PrependedAppendedText, AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Row, HTML
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import HiddenInput
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from internationalflavor.countries import CountryFormField
from internationalflavor.vat_number import VATNumberFormField

from permissions_widget.forms import PermissionSelectMultipleField
from permissions_widget.layout import PermissionWidget

from flatpages_i18n.models import FlatPage_i18n
from inventor.core.accounts.models import User
from inventor import settings as inventor_settings


class UserWidget(ModelSelect2Widget):
    queryset = User.objects.all()
    search_fields = ['first_name__icontains', 'last_name__icontains']
    # data_view = 'accounts:user_select2'

    # def __init__(self, *args, **kwargs):
    #     defaults = {'data_view': self.data_view}
    #     defaults.update(kwargs)
    #     super().__init__(*args, **defaults)

    def filter_queryset(self, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        if term.isdigit():
            return queryset.filter(pk=term).distinct()
        return super().filter_queryset(term, queryset, **dependent_fields)


class UsersWidget(ModelSelect2MultipleWidget):
    queryset = User.objects.all()
    search_fields = ['first_name__icontains', 'last_name__icontains']
    # data_view = 'accounts:user_select2'

    # def __init__(self, *args, **kwargs):
    #     defaults = {'data_view': self.data_view}
    #     defaults.update(kwargs)
    #     super().__init__(*args, **defaults)

    def filter_queryset(self, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = self.get_queryset()
        if term.isdigit():
            return queryset.filter(pk=term).distinct()
        return super().filter_queryset(term, queryset, **dependent_fields)


class ProfileForm(forms.ModelForm):
    class Meta:
        fields = (
            'first_name', 'last_name', 'email', 'phone',
            'avatar',
            'street', 'postcode', 'city', 'country',
            'date_of_birth', 'gender', 'team', 'preferred_language',
            'agree_terms_and_conditions', 'agree_privacy_policy', 'agree_marketing_purposes', 'agree_social_networks_sharing',
        )
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print('USER_REQUIRED_FIELDS', inventor_settings.USER_REQUIRED_FIELDS)
        for required_field_name in inventor_settings.USER_REQUIRED_FIELDS:
            self.fields[required_field_name].required = True

        print('USER_HIDDEN_FIELDS', inventor_settings.USER_HIDDEN_FIELDS)
        for hidden_field_name in inventor_settings.USER_HIDDEN_FIELDS:
            if self.fields[hidden_field_name].required:
                raise ValueError(f'Field {hidden_field_name} can not be hidden, because it is required')
            self.fields[hidden_field_name].widget = HiddenInput()

        address_fields = ['street', 'postcode', 'city', 'country']
        address_label = '' if set(address_fields) <= set(inventor_settings.USER_HIDDEN_FIELDS) else _('Address')
        dob_fields = ['date_of_birth']
        dob_label = '' if set(dob_fields) <= set(inventor_settings.USER_HIDDEN_FIELDS) else _('Date of birth')

        # placeholders
        if inventor_settings.USE_PLACEHOLDERS:
            for field_name, field in self.fields.items():
                if isinstance(field, forms.CharField) or \
                        isinstance(field, forms.ChoiceField) or \
                        isinstance(field, forms.DateField):
                    asterisk = '*' if field.required else ''
                    field.widget.attrs['placeholder'] = f'{field.label.capitalize()}{asterisk}'
                    field.label = ''

        self.helper = FormHelper()

        if inventor_settings.USER_FORM_COLUMNS:
            column_class = 'col-md-6'
        else:
            column_class = 'col-md-6 offset-md-3'

        self.helper.layout = Layout(
            Div(
                Div(
                    Fieldset(
                        _('Name and surname'),
                        Row(
                            Div('first_name', css_class='col-md-5'),
                            Div('last_name', css_class='col-md-7'),
                        ),
                    ),
                    Fieldset(
                        _('Contact details'),
                        PrependedText('email', '<i class="fas fa-at"></i>'),
                        PrependedText('phone', '<i class="far fa-mobile"></i>')
                    ),
                    Fieldset(address_label, *address_fields),
                    Fieldset(dob_label, *dob_fields),
                    # Fieldset(
                    #     _('Address'),
                    #     'street',
                    #     Row(
                    #         Div('postcode', css_class='col-md-5'),
                    #         Div('city', css_class='col-md-7'),
                    #     ),
                    #     'country',
                    # ),
                    # Fieldset(
                    #     _('Date of birth'),
                    #     'date_of_birth',
                    # ),
                    css_class=column_class
                ),
                Div(
                    Fieldset(
                        _('Other'),
                        InlineRadios('gender'),
                        'team',
                        'avatar',
                    ),
                    Fieldset(
                        _('Preferred language'),
                        'preferred_language'
                    ),
                    Fieldset(
                        _('Agreements'),
                        # agreements / GDPR
                        'agree_terms_and_conditions',
                        'agree_privacy_policy',
                        'agree_marketing_purposes',
                        'agree_social_networks_sharing',
                    ),
                    css_class=column_class
                ),
            css_class='row'),
            FormActions(
                Submit('submit', _('Submit'), css_class='btn-lg btn-primary'),
                css_class='text-center'
            )
        )


class UserForm(forms.ModelForm):
    user_permissions = PermissionSelectMultipleField(required=False)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone', 'avatar',
            'is_active', 'is_superuser', 'is_staff',
            'groups', 'user_permissions',
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        groups_permissions = []
        if self.instance and self.instance.pk:
            groups_permissions = Permission.objects.filter(group__user=self.instance)

        self.fields['is_superuser'].disabled = True
        self.fields['is_staff'].disabled = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    _('Personal details'),
                    Row(
                        Div('first_name', css_class='col-md-5'),
                        Div('last_name', css_class='col-md-7'),
                    ),
                    'avatar',
                    css_class='col-md-4'
                ),
                Fieldset(
                    _('Contact details'),
                    PrependedText('email', '<i class="fas fa-at"></i>'),
                    PrependedText('phone', '<i class="far fa-mobile"></i>'),
                    css_class='col-md-3'
                ),
                Fieldset(
                    _('Classification'),
                    'groups',
                    css_class='col-md-3'
                ),
                Fieldset(
                    _('Status'),
                    'is_active',
                    'is_superuser',
                    'is_staff',
                    css_class='col-md-5'
                ),
            ),
            Row(
                Fieldset(
                    _('Permissions'),
                    PermissionWidget('user_permissions', groups_permissions=groups_permissions),
                    css_class='col-md-12'
                )
            ),
            FormActions(
                Submit('submit', _('Submit'), css_class='btn-secondary')
            )
        )


class SignupForm(AllAuthSignupForm):
    # TODO: settings for required and visible fields
    first_name = forms.CharField(label=_('first name'), max_length=30)
    last_name = forms.CharField(label=_('last name'), max_length=30)
    phone = forms.CharField(label=_('phone'), max_length=30, required=False)
    street = forms.CharField(label=_('street and number'), max_length=200, required=False)
    postcode = forms.CharField(label=_('postcode'), max_length=30, required=False)
    city = forms.CharField(label=_('city'), max_length=50, required=False)
    country = CountryFormField(label=_('Country'), required=False)  # TODO: initial country
    reg_id = forms.CharField(label=_('Reg. No'), max_length=30, required=False)
    tax_id = forms.CharField(label=_('TAX ID'), max_length=30, required=False)
    vat_id = VATNumberFormField(label=_('VAT ID'), required=False)
    date_of_birth = forms.DateField(label=_('date of birth'), required=False)  # TODO: datepicker / multiwidget
    gender = forms.ChoiceField(label=_('gender'), choices=get_user_model().GENDERS, required=False)
    team = forms.CharField(label=_('team/club'), max_length=50, required=False)
    agree_terms_and_conditions = forms.BooleanField(label=_('I agree terms and conditions'), required=True, initial=False)
    agree_privacy_policy = forms.BooleanField(label=_('I agree privacy policy'), required=True, initial=False)
    agree_marketing_purposes = forms.BooleanField(label=_("I agree with marketing purposes"), required=False, initial=True)
    agree_social_networks_sharing = forms.BooleanField(label=_("I agree with publishing of my photos on social media channels of the organizer"), required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print('USER_REQUIRED_FIELDS', inventor_settings.USER_REQUIRED_FIELDS)
        for required_field_name in inventor_settings.USER_REQUIRED_FIELDS:
            self.fields[required_field_name].required = True

        print('USER_HIDDEN_FIELDS', inventor_settings.USER_HIDDEN_FIELDS)
        for hidden_field_name in inventor_settings.USER_HIDDEN_FIELDS:
            if self.fields[hidden_field_name].required:
                raise ValueError(f'Field {hidden_field_name} can not be hidden, because it is required')
            self.fields[hidden_field_name].widget = HiddenInput()

        address_fields = ['street', 'postcode', 'city', 'country']
        address_label = '' if set(address_fields) <= set(inventor_settings.USER_HIDDEN_FIELDS) else _('Address')
        dob_fields = ['date_of_birth']
        dob_label = '' if set(dob_fields) <= set(inventor_settings.USER_HIDDEN_FIELDS) else _('Date of birth')

        # placeholders
        if inventor_settings.USE_PLACEHOLDERS:
            for field_name, field in self.fields.items():
                if isinstance(field, forms.CharField) or \
                        isinstance(field, forms.ChoiceField) or \
                        isinstance(field, forms.DateField):
                    asterisk = '*' if field.required else ''
                    field.widget.attrs['placeholder'] = f'{field.label.capitalize()}{asterisk}'
                    field.label = ''

        # agreements
        try:
            terms = FlatPage_i18n.objects.get(machine_name='terms')
            self.fields['agree_terms_and_conditions'].label = _('I agree <a href="%s" target="_blank">terms and conditions</a>') % terms.get_absolute_url()
        except ObjectDoesNotExist:
            pass

        try:
            privacy = FlatPage_i18n.objects.get(machine_name='privacy')
            self.fields['agree_privacy_policy'].label = _('I agree <a href="%s" target="_blank">privacy policy</a>') % privacy.get_absolute_url()
        except ObjectDoesNotExist:
            pass

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # Row(
                Fieldset(
                    _('Name and surname'),
                    Row(
                        Div('first_name', css_class='col-md-5'),
                        Div('last_name', css_class='col-md-7'),
                    ),
                ),
                Fieldset(
                    _('Contact details'),
                    Row(
                        Div(PrependedText('email', '<i class="fas fa-at"></i>'), css_class='col-md-7'),
                        Div(PrependedText('phone', '<i class="far fa-mobile"></i>'), css_class='col-md-5'),
                    ),
                ),
                Fieldset(address_label, *address_fields),
                Fieldset(dob_label, *dob_fields),
                Fieldset(
                    _('Other'),
                    InlineRadios('gender'),
                    'team',
                    'password1',
                ),
                Fieldset(
                    _('Agreements'),
                    'agree_terms_and_conditions',
                    'agree_privacy_policy',
                    'agree_marketing_purposes',
                    'agree_social_networks_sharing',
                ),
            # ),
            FormActions(
                Submit('submit', _('Sign up'), css_class='btn-primary')
            )
        )

    def custom_signup(self, request, user):
        field_names = [f.name for f in get_user_model()._meta.get_fields()]
        attrs_to_save = []

        for attr, value in self.cleaned_data.items():
            if attr.startswith('dont_'):
                attr = attr.replace('dont_', '')
                value = not value

            if attr in field_names:
                setattr(user, attr, value)
                attrs_to_save.append(attr)

        user.save(update_fields=attrs_to_save)
