from django.core.management import call_command
from django.core.management.base import BaseCommand

from inventor.core.listings.models.general import Location, Category


class Command(BaseCommand):
    help = 'Loads sample data from fixtures'

    def handle(self, *args, **options):
        print('Loading fixtures...')
        call_command('loaddata', 'categories.json', 'features.json', 'locations.json', 'listings.json')
        print('Fixtures loaded.')
        print('Rebuilding MPTT trees...')
        Category.objects.rebuild()
        Location.objects.rebuild()
        print('MPTT trees rebuilded.')
