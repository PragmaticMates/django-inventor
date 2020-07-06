from django.contrib import admin, messages
from django.contrib.admin.sites import NotRegistered
from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from mapwidgets import GooglePointFieldWidget
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from sorl.thumbnail.admin import AdminImageMixin

from inventor import settings
from inventor.core.bookings.admin import BookingMixinAdmin
from inventor.core.listings.models.general import Album, Video, Photo, Listing
from inventor.helpers import get_listing_types_classes


class PhotoInline(NestedStackedInline):
    model = Photo
    extra = 1


class AlbumInline(NestedStackedInline):
    model = Album
    extra = 1
    inlines = [PhotoInline]


class VideoInline(admin.StackedInline):
    model = Video
    extra = 1
    inlines = []


def make_convert_to_type_action(listing_type):
    def convert_to_type(modeladmin, request, queryset):
        for listing in queryset:
            listing.convert(listing_type)
            messages.info(request, "Listing {0} converted to {1}".format(listing, listing.get_listing_type_display()))

    listing_type_display = listing_type._meta.verbose_name
    convert_to_type.short_description = _("Convert to {0}").format(listing_type_display)
    # We need a different '__name__' for each action - Django
    # uses this as a key in the drop-down box.
    listing_type_identifier = listing_type.__name__.lower()
    convert_to_type.__name__ = 'convert_to_type_{0}'.format(listing_type_identifier)

    return convert_to_type


class ListingAdmin(AdminImageMixin, NestedModelAdmin):
    date_hierarchy = 'created'
    search_fields = ['id', 'title_i18n', 'description']
    list_display = ('id', 'title_i18n', 'slug_i18n', 'get_categories', 'address', 'locality', 'get_price_display', 'published', 'created')
    list_display_links = ('title_i18n',)
    list_filter = ('published', 'promoted', 'awaiting')
    autocomplete_fields = ['author', 'locality']
    list_select_related = ['locality']
    filter_vertical = ['categories', 'features']  # TODO: filter categories for selected listing type only
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }

    class Media:
        js = (
            'js/map-widget-utils.js',
        )

    def get_actions(self, request):
        actions = super().get_actions(request)

        for listing_type in Listing.__subclasses__():
            action = make_convert_to_type_action(listing_type)
            actions[action.__name__] = (action,
                                        action.__name__,
                                        action.short_description)

        return actions

    def get_categories(self, obj):
        return ", ".join(obj.categories.values_list('title', flat=True))
    get_categories.admin_order_field = 'categories'
    get_categories.short_description = _('Categories')

    def get_price_display(self, obj):
        return obj.get_price_display()
    get_price_display.admin_order_field = 'price'
    get_price_display.short_description = _('Price')

    @property
    def fieldsets(self):
        fieldsets_definition = {
            'DEFINITION': (_('Definition'), {'fields': ('title_i18n', 'slug_i18n', 'description_i18n',)}),
            'MANAGEMENT': (_('Management'), {'fields': ('author', 'published', 'promoted')}),
            'SPECIFICATION': (_('Specification'), {'fields': (('categories', 'features'),)}),
            'PRICE': (_('Price'), {'fields': (('price_starts_at', 'price', 'price_unit', 'price_per_person', 'in_stock', 'awaiting'),)}),
            'LOCATION': (_('Location'), {'fields': ('locality', 'country', 'address', 'point')}),
            'PREVIEWS': (_('Previews'), {'fields': (('image', 'banner'),)}),
            'CONTACT': (_('Contact information'), {'fields': ('person', 'phone', 'email', 'website')}),
            'SOCIAL': (_('Social connections'), {'fields': ('social_networks',)}),
        }

        fieldsets = ()
        sections = settings.SECTIONS or fieldsets_definition.keys()

        for section in sections:
            fieldsets += fieldsets_definition[section],

        return fieldsets

    # @property
    # def inlines(self):
    #     inlines = []
    #     if settings.VIDEOS_ENABLED:
    #         inlines.append(VideoInline)
    #     if settings.GALLERY_ENABLED:
    #         inlines.append(AlbumInline)
    #     # add comments?
    #     return inlines


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1


if settings.GALLERY_ENABLED:
    @admin.register(Album)
    class AlbumAdmin(admin.ModelAdmin):
        search_fields = ['listing__title', 'title', 'description']
        list_display = ('listing', 'title', 'description')
        raw_id_fields = ['listing']
        inlines = [PhotoInline]


# Listing types
@admin.register(*get_listing_types_classes())
class ListingTypeAdmin(ListingAdmin):
    pass


try:
    from inventor.core.listings.models.listing_types import Accommodation
    admin.site.unregister(Accommodation)
    @admin.register(Accommodation)
    class AccommodationAdmin(ListingAdmin):
        fieldsets = ListingTypeAdmin.fieldsets + BookingMixinAdmin.fieldsets + (
            (_('Specific'), {'fields': ('amenities', 'star_rating', 'rooms')}),
        )
except (NotRegistered, ImportError, TypeError):
    pass


try:
    from inventor.core.listings.models.listing_types import Race
    admin.site.unregister(Race)
    @admin.register(Race)
    class RaceAdmin(ListingAdmin):
        list_display = ListingTypeAdmin.list_display + ('distance_display', 'elevation_display')
        list_filter = ListingTypeAdmin.list_filter + ('distance', 'elevation')

        def distance_display(self, obj):
            return obj.get_distance_display()
        distance_display.admin_order_field = 'distance'
        distance_display.short_description = _('Distance')

        def elevation_display(self, obj):
            return obj.get_elevation_display()
        elevation_display.admin_order_field = 'elevation'
        elevation_display.short_description = _('Elevation')

        @property
        def fieldsets(self):
            return super().fieldsets + (
                (_('Specific'), {'fields': ('distance', 'elevation', 'medal')}),
            )
except (NotRegistered, ImportError):
    pass


try:
    from inventor.core.listings.models.listing_types import Exercise
    admin.site.unregister(Exercise)
    @admin.register(Exercise)
    class ExerciseAdmin(ListingAdmin):
        list_display = ListingTypeAdmin.list_display + ('difficulty', 'duration_display',)
        list_filter = ListingTypeAdmin.list_filter + ('difficulty', 'duration', )

        def duration_display(self, obj):
            return obj.get_duration_display()
        duration_display.admin_order_field = 'duration'
        duration_display.short_description = _('Duration')

        @property
        def fieldsets(self):
            return super().fieldsets + (
                (_('Specific'), {'fields': ('duration', 'difficulty')}),
            )
except (NotRegistered, ImportError):
    pass


try:
    from inventor.core.listings.models.listing_types import Product
    admin.site.unregister(Product)
    @admin.register(Product)
    class ProductAdmin(ListingAdmin):
        list_display = ListingTypeAdmin.list_display + ('options_display',)
        list_filter = ListingTypeAdmin.list_filter + ('options', )

        def options_display(self, obj):
            return ', '.join([str(option) for option in obj.options.all()])
        options_display.short_description = _('Options')

        @property
        def fieldsets(self):
            return super().fieldsets + (
                (_('Specific'), {'fields': ('options',)}),
            )
except (NotRegistered, ImportError):
    pass


for model in get_listing_types_classes():
    model_admin = admin.site._registry[model].__class__
    admin.site.unregister(model)

    if settings.VIDEOS_ENABLED and not VideoInline in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [VideoInline]
    if settings.GALLERY_ENABLED and not AlbumInline in model_admin.inlines:
        model_admin.inlines = list(model_admin.inlines)[:] + [AlbumInline]

    admin.site.register(model, model_admin)
