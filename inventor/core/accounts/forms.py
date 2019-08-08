from django.contrib.auth.models import Permission, Group
from crispy_forms.bootstrap import FormActions, InlineRadios, PrependedAppendedText, AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Row, HTML
from django import forms
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

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
