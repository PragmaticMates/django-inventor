from django.db import models


class BookingQuerySet(models.QuerySet):
    def of_traveler(self, user):
        return self.filter(traveler=user)

    def of_listing(self, listing):
        return self.filter(listing=listing)
