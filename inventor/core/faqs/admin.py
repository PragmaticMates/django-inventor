from django.contrib import admin
from modeltrans.admin import ActiveLanguageMixin
from inventor.core.faqs.models import FAQ


@admin.register(FAQ)
class FAQAdmin(ActiveLanguageMixin, admin.ModelAdmin):
    search_fields = ['question_i18n', 'answer_i18n']
    list_display = ('question_i18n', 'answer_i18n',)
    list_display_links = ('question_i18n',)
