from django.db.models.signals import post_save
from django.dispatch import receiver

from inventor.core.lexicons.models import Category


@receiver(post_save, sender=Category)
# @apm_custom_context('signals')
def update_children_listing_type(sender, instance, **kwargs):
    listing_type = instance.listing_type
    instance.get_descendants().update(listing_type=listing_type)
