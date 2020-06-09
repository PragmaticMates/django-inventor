from allauth.account.forms import SignupForm as AllAuthSignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from crispy_forms.bootstrap import FormActions, InlineRadios, PrependedAppendedText, AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Row, HTML
from django import forms
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget
from internationalflavor.countries import CountryFormField
from internationalflavor.vat_number import VATNumberFormField

from permissions_widget.forms import PermissionSelectMultipleField
from permissions_widget.layout import PermissionWidget
from inventor.core.accounts.models import User


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


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        fields = (
            'first_name', 'last_name', 'email', 'phone', 'avatar'
        )
        model = User

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
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
                    css_class='col-md-7'
                ),
                Fieldset(
                    _('Contact details'),
                    PrependedText('email', '<i class="fas fa-at"></i>'),
                    PrependedText('phone', '<i class="far fa-mobile"></i>'),
                    css_class='col-md-5'
                ),
            ),
            FormActions(
                Submit('submit', _('Submit'), css_class='btn-secondary')
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
    # TODO: settings for required fields
    first_name = forms.CharField(label=_('first name'), max_length=30)
    last_name = forms.CharField(label=_('last name'), max_length=30)
    phone = forms.CharField(label=_('phone'), max_length=30)
    street = forms.CharField(label=_('street and number'), max_length=200)
    postcode = forms.CharField(label=_('postcode'), max_length=30)
    city = forms.CharField(label=_('city'), max_length=50)
    country = CountryFormField(label=_('Country'), initial='SK')
    reg_id = forms.CharField(label=_('Reg. No'), max_length=30, required=False)
    tax_id = forms.CharField(label=_('TAX ID'), max_length=30, required=False)
    vat_id = VATNumberFormField(label=_('VAT ID'), required=False)
    date_of_birth = forms.DateField(label=_('date of birth'))  # TODO: datepicker / multiwidget
    gender = forms.ChoiceField(label=_('gender'), choices=get_user_model().GENDERS)
    team = forms.CharField(label=_('team/club'), max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['is_staff'].disabled = True

        # placeholders
        USE_PLACEHOLDERS = True

        if USE_PLACEHOLDERS:
            print(self.fields)
            for field_name, field in self.fields.items():
                if isinstance(field, forms.CharField) or \
                        isinstance(field, forms.ChoiceField) or \
                        isinstance(field, forms.DateField):
                    asterisk = '*' if field.required else ''
                    field.widget.attrs['placeholder'] = f'{field.label.capitalize()}{asterisk}'
                    field.label = ''

        self.helper = FormHelper()
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
                Fieldset(
                    _('Address'),
                    'street',
                    'postcode',
                    'city',
                    'country',
                ),
                Fieldset(
                    _('Date of birth'),
                    'date_of_birth',
                ),
                Fieldset(
                    _('Other'),
                    InlineRadios('gender'),
                    'team',
                    'password1',
                ),
            # ),
            FormActions(
                Submit('submit', _('Submit'), css_class='btn-primary')
            )
        )

    def custom_signup(self, request, user):
        field_names = [f.name for f in get_user_model()._meta.get_fields()]
        attrs_to_save = []

        for attr, value in self.cleaned_data.items():
            if attr in field_names:
                setattr(user, attr, value)
                attrs_to_save.append(attr)

        user.save(update_fields=attrs_to_save)
