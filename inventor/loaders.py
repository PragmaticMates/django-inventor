from django.conf import settings
from django.template.loaders.filesystem import Loader as FilesystemLoader
from django.template.utils import get_app_template_dirs


class ThemeLoader(FilesystemLoader):
    def get_dirs(self):
        return get_app_template_dirs(f'{settings.ULTRALIST_THEME}/templates')
