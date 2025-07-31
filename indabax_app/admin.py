from django.contrib import admin
from .models import ( EventImage, 
                     TutorialCategory, 
                     Tutorial, 
                     Leader, 
                     AboutContent, 
                     HomePageContent, 
                     Pillar,
                     Event, 
                     Partner,
                     GalleryImage, 
                     HeroBackgroundImage,
                     Album,
                     Session, 
                     SessionImage,
                    SiteSettings )

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('contact_email', 'phone_number',)
    # You might want to limit to a single instance from admin directly too
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

admin.site.register(Album)

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('main_heading',)

@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'is_upcoming', 'location')
    list_filter = ('is_upcoming', 'date')
    search_fields = ('title', 'description')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'order')
    list_editable = ('order',)


@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_uploaded')
    search_fields = ('title',)

@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_posted')
    list_filter = ('category',)
    search_fields = ('title',)

class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'term_start', 'is_current') # Corrected list_display
    list_filter = ('is_current', 'position')
    search_fields = ('name', 'position')

admin.site.register(Leader, LeaderAdmin)


# Register AboutContent and its inlines
class ObjectiveInline(admin.TabularInline):
    model = AboutContent.Objective
    extra = 1 # Number of empty forms to display

class AffiliationLinkInline(admin.TabularInline):
    model = AboutContent.AffiliationLink
    extra = 1

@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    inlines = [ObjectiveInline, AffiliationLinkInline]
    fieldsets = (
        (None, {
            'fields': ('main_heading', 'main_paragraph')
        }),
        ('Purpose & Objectives', {
            'fields': ('purpose_heading', 'purpose_paragraph')
        }),
        ('Affiliations & Contact', {
            'fields': ('affiliations_heading', 'affiliations_paragraph', 'contact_email')
        }),
    )


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'image')
    list_editable = ('order',)
    search_fields = ('title',)

admin.site.register(HeroBackgroundImage)


admin.site.register(SessionImage)

class SessionImageInline(admin.TabularInline):
    model = SessionImage
    extra = 3 # Number of empty forms to display

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    # This inline is for SessionImage, not directly for speakers.
    class SessionImageInline(admin.TabularInline):
        model = SessionImage
        extra = 3 # Number of empty forms to display

    inlines = [SessionImageInline]
    list_display = (
        'title',
        'session_date',
        'venue',
        'is_published',
        'google_photos_link'
    )
    list_filter = ('is_published', 'session_date')
    search_fields = ('title', 'description', 'venue', 'guest_speakers_info')

    # Define the fields shown in the add/change form
    fieldsets = (
        (None, {
            'fields': ('title', 'tagline', 'description', 'is_published', 'google_photos_link')
        }),
        ('Session Details', {
            'fields': ('session_date', ('start_time', 'end_time'), 'venue')
        }),
        ('Speakers', { # NEW FIELDSET for speakers
            'fields': ('speakers', 'guest_speakers_info'), # Both fields here
            'description': 'Select existing leaders or add guest speakers manually.'
        }),
    )




