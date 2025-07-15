# kuai_club/admin.py
from django.contrib import admin
from .models import SiteSettings,Aboutus,Leader,Event,Resource,CommunityOutreach,News,Research,Project
from .models import HeroSlide
from django.utils.html import format_html

# Register your models here.

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'is_maintenance_mode', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('site_name', 'site_tagline', 'site_description', 'site_keywords')
        }),
        ('Branding', {
            'fields': ('logo', 'favicon', 'primary_color', 'secondary_color')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'contact_address', 'portal_url')
        }),
        ('Social Media Links', {
            'fields': (
                'facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url',
                'youtube_url', 'github_url', 'tiktok_url', 'whatsapp_url', 'telegram_url'
            )
        }),
        ('Quick Links', {
            'fields': ('quick_links',)
        }),
        ('Business Info', {
            'fields': ('working_hours', 'privacy_policy_url', 'terms_of_service_url')
        }),
        ('Feature Toggles', {
            'fields': (
                'enable_sitemap', 'enable_cookies', 'enable_captcha', 'enable_social_login',
                'enable_two_factor_auth', 'enable_dark_mode', 'enable_search',
                'enable_search_suggestions', 'enable_user_profiles', 'enable_user_roles',
                'enable_content_moderation'
            )
        }),
        ('SEO & Integrations', {
            'fields': (
                'google_analytics_id', 'google_tag_manager_id', 'google_adsense_id', 'google_maps_api_key'
            )
        }),
        ('Maintenance Mode', {
            'fields': ('is_maintenance_mode', 'maintenance_message', 'maintenance_image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Aboutus)
class AboutusAdmin(admin.ModelAdmin):
    list_display = ('title', 'column_position', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

    def has_add_permission(self, request):
        # Only allow adding if no entry exists
        if Aboutus.objects.exists():
            return False
        return super().has_add_permission(request)

    fieldsets = (
        ('Content', {
            'fields': (
                'title', 'slug', 'content', 'column_position', 'image',
            )
        }),
        ('Who We Are Section', {
            'fields': (
                'who_we_are_title',
                'who_we_are_description',
                'who_we_are_image',
            ),
        }),
        ('Mission & Vision', {
            'fields': (
                'mission',
                'mission_image',
                'vision',
                'vision_image'
            ),
        }),
        ('Why We Exist Section', {
            'fields': (
                'why_exist_title',
                'why_exist_description',
            ),
        }),
        ('Objectives', {
            'fields': ('objectives',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )





@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 
        'position', 
        'category',         
        'email', 
        'start_date', 
        'end_date',      
        'created_at', 
        'updated_at'
    )
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('full_name', 'position', 'email')
    list_filter = ('category',)  
    ordering = ('-start_date', 'full_name') 


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish_date', 'is_published', 'created_at', 'updated_at', 'news_image_tag')
    readonly_fields = ('created_at', 'updated_at', 'news_image_preview', 'background_image_preview')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('is_published', 'publish_date')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'summary', 'content', 'url', 'is_published', 'publish_date')
        }),
        ('Images', {
            'fields': ('image', 'news_image_preview', 'background_image', 'background_image_preview')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def news_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="40" style="object-fit:cover;" />', obj.image.url)
        return "-"
    news_image_tag.short_description = "News Image"

    def news_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="object-fit:contain;" />', obj.image.url)
        return "No image"

    def background_image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" width="300" style="object-fit:contain;" />', obj.background_image.url)
        return "No background"



from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'background_image', 'event_start', 'event_end', 'is_published', 'is_upcoming', 'created_at')
    list_filter = ('is_published', 'event_start')
    search_fields = ('title', 'location', 'summary')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('event_start',)
    
    def is_upcoming(self, obj):
        return obj.is_upcoming()
    is_upcoming.boolean = True
    is_upcoming.admin_order_field = 'event_start'



@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'institution', 'is_published', 'publish_date')
    search_fields = ('title', 'category', 'researchers', 'institution')
    list_filter = ('category', 'is_published', 'institution')
    readonly_fields = ('created_at', 'updated_at', 'slug')



@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Resource Info', {
            'fields': ('title', 'slug', 'description', 'resource_type', 'file', 'external_url', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(CommunityOutreach)
class CommunityOutreachAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('title',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact_email', 'publish_date', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'summary', 'description', 'image')
        }),
        ('Contact Details', {
            'fields': ('contact_email', 'phone_number', 'url')
        }),
        ('Status & Timestamps', {
            'fields': ('is_published', 'created_at', 'updated_at')
        }),
    )

@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle', 'description')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('title', 'subtitle', 'description', 'image')
        }),
        ('Button 1', {
            'fields': ('button1_text', 'button1_url', 'button1_style')
        }),
        ('Button 2', {
            'fields': ('button2_text', 'button2_url', 'button2_style')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )



from .models import GalleryImage

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')
    search_fields = ('title', 'caption')
    list_filter = ('upload_date',)
    readonly_fields = ('upload_date',)
