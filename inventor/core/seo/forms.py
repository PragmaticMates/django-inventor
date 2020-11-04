from django import forms

from .models import Seo


class SeoForm(forms.ModelForm):
    class Meta:
        model = Seo
        fields = ['title_i18n', 'description_i18n', 'keywords_i18n']
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
