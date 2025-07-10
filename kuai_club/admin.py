# kuai_club/admin.py

from django.contrib import admin
from .models import (
    SiteConfig, AboutPageContent, Partner, ExecutivePosition,
    ExecutiveLeader, NewsPost, ClubEventType, ClubEvent,
    ResearchArea, ClubProject, Community, ResourceCategory,
    ResourceLink
)

# Register your models here.

# Simple registrations (no custom admin needed for these for now)
admin.site.register(SiteConfig)
admin.site.register(AboutPageContent)
admin.site.register(ResearchArea)
admin.site.register(Community)



# Add or update this block for ClubProject for better admin experience
@admin.register(ClubProject) # This decorator automatically registers the model
class ClubProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'research_area', 'status', 'is_featured', 'start_date', 'end_date')
    list_filter = ('status', 'research_area', 'is_featured')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date' # Adds date-based navigation
    fieldsets = (
        (None, {
            'fields': ('title', 'research_area', 'description', 'project_image')
        }),
        ('Project Details', {
            'fields': ('status', 'start_date', 'end_date', 'github_link', 'is_featured'),
            'classes': ('collapse',), # Makes this section collapsible in the admin
        }),
    )


@admin.register(ExecutivePosition)
class ExecutivePositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',) # Allows changing order directly in the list view
    ordering = ('order',)

# Register ExecutiveLeader with custom admin for better display
@admin.register(ExecutiveLeader)
class ExecutiveLeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_current', 'term_start', 'term_end')
    list_filter = ('position', 'term_start', 'term_end')
    search_fields = ('name', 'bio')
    date_hierarchy = 'term_start'
    raw_id_fields = ('position',) # Useful if you have many positions
    fieldsets = (
        (None, {
            'fields': ('name', 'position', 'photo', 'bio')
        }),
        ('Term Details', {
            'fields': ('term_start', 'term_end'),
            'classes': ('collapse',),
        }),
    )


@admin.register(ClubEventType)
class ClubEventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ClubEvent)
class ClubEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'time', 'location', 'is_upcoming')
    list_filter = ('event_type', 'is_upcoming', 'date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('title', 'event_type', 'description', 'event_image')
        }),
        ('Event Details', {
            'fields': ('date', 'time', 'location', 'registration_link', 'is_upcoming'),
            'classes': ('collapse',),
        }),
    )


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_published', 'author')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content', 'author')
    date_hierarchy = 'published_date'
    prepopulated_fields = {'slug': ('title',)} # Auto-fill slug from title
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'news_image', 'author')
        }),
        ('Publication Information', {
            'fields': ('published_date', 'is_published'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_link', 'is_active', 'partner_type', 'display_order')
    list_filter = ('is_active', 'partner_type')
    search_fields = ('name', 'description')
    list_editable = ('display_order', 'is_active') # Allows quick editing from list
    ordering = ('display_order', 'name') # Order by custom order then name
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'description')
        }),
        ('Contact & Type', {
            'fields': ('website_link', 'partner_type'),
        }),
        ('Display Settings', {
            'fields': ('is_active', 'display_order'),
            'classes': ('collapse',),
        }),
    )


# For ResourceCategory
@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order')
    list_editable = ('display_order',)
    search_fields = ('name',)
    ordering = ('display_order', 'name')
    prepopulated_fields = {'slug': ('name',)} # Add slug for cleaner URLs if needed later

# For ResourceLink
@admin.register(ResourceLink)
class ResourceLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'is_active', 'display_order')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'url')
    list_editable = ('is_active', 'display_order')
    ordering = ('category__display_order', 'category__name', 'display_order', 'title') # Order by category order, then link order
    raw_id_fields = ('category',) # Use a raw ID field for category selection if many categories

