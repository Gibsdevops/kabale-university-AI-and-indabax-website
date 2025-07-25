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
                     HeroBackgroundImage,)

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

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'term_start', 'term_end')
    list_filter = ('position',)
    search_fields = ('name',)


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