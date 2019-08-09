import os
import shutil
from os.path import normpath, join

from django.core.management import call_command
from django.core.management.base import BaseCommand

from tenant.settings.common import SOURCE_ROOT


class Command(BaseCommand):
    help = 'Resets listings migrations'

    def handle(self, *args, **options):
        call_command('migrate')
        self.reset_app_migrations(['lexicons', 'listings'])
        call_command('load_fixtures')

    def reset_app_migrations(self, apps):
        for app in apps:
            joined = join(SOURCE_ROOT, 'inventor/core/{}/migrations/'.format(app))
            initial_migration_path = normpath(joined)

            if os.path.exists(initial_migration_path):
                print('Resetting migrations for app {}'.format(app))
                call_command('migrate', app, 'zero')

        for app in apps:
            print('Deleting migrations for app {}'.format(app))

            joined = join(SOURCE_ROOT, 'inventor/core/{}/migrations/'.format(app))
            initial_migration_path = normpath(joined)

            if os.path.exists(initial_migration_path):
                print('Deleting {}'.format(initial_migration_path))
                # os.remove(initial_migration_path)
                shutil.rmtree(initial_migration_path, ignore_errors=False, onerror=None)
            else:
                print('Migration {} does NOT exist!'.format(initial_migration_path))

        for app in apps:
            print('Setting migrations for app {}'.format(app))
            call_command('makemigrations', app)
            call_command('migrate', app)
