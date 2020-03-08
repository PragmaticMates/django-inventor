from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import BaseCommand

from inventor.core.listings.models.general import Location, Category


class Command(BaseCommand):
    help = 'Loads sample data from fixtures'

    def handle(self, *args, **options):
        print('Loading fixtures...')
        call_command('loaddata',
                     'categories.json',  # TODO: update with values from deprecated accommodation and property types
                     'features.json',
                     'locations.json',
                     'accommodation_amenities.json',
                     #'accommodation_types.json',
                     #'property_types.json',
                     'listings.json'
                     )
        print('Fixtures loaded.')
        print('Setting lorem descriptions.')

        lexicons = ContentType.objects.filter(app_label__in=['lexicons', 'listings'])

        for lexicon in lexicons:
            model = lexicon.model_class()

            if hasattr(model, 'description'):
                model.objects.update(description={
                    'lexicons': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed nec enim condimentum, ullamcorper nulla consequat, ullamcorper enim. Nulla hendrerit ex a lacus finibus pulvinar. Sed sit amet urna tortor. Praesent efficitur mauris faucibus tempus hendrerit. Duis semper ipsum semper nibh ultricies, in posuere ex condimentum.',
                    'listings': "Aliquam malesuada luctus mauris, non ultrices purus consectetur vel. Mauris nulla sem, semper ut dui et, pulvinar elementum nisi. Sed sit amet sagittis ante. Duis porta velit eu congue gravida. Phasellus vehicula tortor arcu, quis fermentum purus placerat quis. In hac habitasse platea dictumst. Sed nisl orci, mattis et semper vel, facilisis et mi. Nulla faucibus libero vel velit aliquam finibus. Sed sollicitudin fringilla velit, a commodo turpis commodo eu.\n\nEtiam vulputate placerat magna. Nunc non sodales diam, malesuada auctor nisl. Ut lorem quam, auctor quis auctor nec, condimentum in purus. Donec aliquet tristique imperdiet. Duis rhoncus interdum lectus eget iaculis. Morbi elementum sapien libero, sed lacinia diam gravida in. Suspendisse in nibh magna. Aenean ex ex, viverra et neque ac, volutpat pharetra purus. Sed vel neque turpis. Phasellus eu hendrerit arcu, et rutrum magna. Nunc gravida, justo sed mollis feugiat, elit purus rutrum metus, at sagittis purus magna non purus. In hac habitasse platea dictumst."
                }.get(lexicon.app_label))

        print('Rebuilding MPTT trees...')
        Category.objects.rebuild()
        Location.objects.rebuild()
        print('MPTT trees rebuilded.')
