from django import forms

from inventor.core.listings.models.general import Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file', 'description_i18n']
        widgets = {
            'description_i18n': forms.Textarea(attrs={'cols': 50, 'rows': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description_i18n'].required = True
