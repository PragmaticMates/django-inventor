from django.contrib.postgres.operations import HStoreExtension, UnaccentExtension, CreateExtension
from django.db import migrations


class Migration(migrations.Migration):
    # unaccent, pg_trgm, hstore;

    operations = [
        UnaccentExtension(),
        CreateExtension('pg_trgm'),
        HStoreExtension(),
    ]
