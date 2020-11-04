from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _

from .models import Seo


class SeoInlineForm(forms.ModelForm):
    class Meta:
        model = Seo
        fields = ['title_i18n', 'description_i18n', 'keywords_i18n', 'robots']
        widgets = {
            'title_i18n': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
            'description_i18n': forms.Textarea(attrs={'cols': 50, 'rows': 2}),
            'keywords_i18n': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title_i18n'].required = True
        self.fields['description_i18n'].required = True
        self.fields['keywords_i18n'].required = True


class SeoForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        path = cleaned_data.get('path_i18n', None)
        content_type = cleaned_data.get('content_type', None)

        if path in EMPTY_VALUES and content_type in EMPTY_VALUES:
            raise ValidationError(_('Either path or content type is required'))

    def clean_content_type(self):
        path = self.cleaned_data.get('path_i18n', None)
        content_type = self.cleaned_data.get('content_type', None)

        if path not in EMPTY_VALUES and content_type not in EMPTY_VALUES:
            raise ValidationError(_('Content type can not be set if path is specified'))

        return content_type

    def clean_object_id(self):
        content_type = self.cleaned_data.get('content_type', None)
        object_id = self.cleaned_data.get('object_id', None)

        if content_type not in EMPTY_VALUES and object_id in EMPTY_VALUES:
            raise ValidationError(_('Object id has to be set if content type is specified'))

        return object_id
