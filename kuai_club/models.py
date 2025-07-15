from django.db import models
from django.utils.text import slugify # Import slugify
from datetime import date
from django.utils.timezone import now



class SiteSettings(models.Model):
    """Global settings for the site."""

    # Basic Info
    site_name = models.CharField(max_length=100, default="Education Platform")
    site_description = models.TextField(default="Welcome to our education platform where learning meets innovation.")
    site_keywords = models.CharField(max_length=255, blank=True)
    site_tagline = models.CharField(max_length=255, default="Empowering Minds, Transforming Futures")

    #QUICKLINKS
    quick_links = models.JSONField(default=list, blank=True, help_text="List of quick links in JSON format. Example: [{'name': 'Home', 'url': '/home'}, {'name': 'About Us', 'url': '/about'}]")  # FIXED: changed from CharField to JSONField for better structure

    # Logos and Branding
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text="Recommended size: 200x200px")
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True, help_text="Recommended size: 32x32px")
    primary_color = models.CharField(max_length=7, default="#1e3a8a", help_text="Hex color code for primary theme color")  # FIXED typo: CahrField → CharField
    secondary_color = models.CharField(max_length=7, default="#f59e0b", help_text="Hex color code for secondary theme color")  # FIXED typo: CahrField → CharField

    # Contact
    contact_email = models.EmailField(max_length=254, default="info@example.com", help_text="Primary contact email")
    contact_phone = models.CharField(max_length=20, default="+256-456-7890", help_text="Primary phone number")
    contact_address = models.TextField(default="Kampala, Uganda", help_text="Physical address")  # FIXED: added 'default' instead of wrongly placed argument
    portal_url = models.URLField(max_length=200, blank=True, null=True, help_text="User portal URL")

    # Social Media
    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    twitter_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)
    youtube_url = models.URLField(max_length=200, blank=True, null=True)
    github_url = models.URLField(max_length=200, blank=True, null=True)
    tiktok_url = models.URLField(max_length=200, blank=True, null=True)
    whatsapp_url = models.URLField(max_length=200, blank=True, null=True)
    telegram_url = models.URLField(max_length=200, blank=True, null=True)

    # Hours
    working_hours = models.CharField(max_length=100, default="Mon-Fri: 9:00 AM - 5:00 PM")

    # Legal
    privacy_policy_url = models.URLField(max_length=200, blank=True, null=True)
    terms_of_service_url = models.URLField(max_length=200, blank=True, null=True)

    # Feature Toggles
    enable_sitemap = models.BooleanField(default=True)
    enable_cookies = models.BooleanField(default=True)
    enable_captcha = models.BooleanField(default=True)
    enable_social_login = models.BooleanField(default=True)
    enable_two_factor_auth = models.BooleanField(default=False)
    enable_dark_mode = models.BooleanField(default=False)
    enable_search = models.BooleanField(default=True)
    enable_search_suggestions = models.BooleanField(default=True)
    enable_user_profiles = models.BooleanField(default=True)
    enable_user_roles = models.BooleanField(default=True)
    enable_content_moderation = models.BooleanField(default=True)

    # SEO & Integrations
    google_analytics_id = models.CharField(max_length=20, blank=True, null=True)
    google_tag_manager_id = models.CharField(max_length=20, blank=True, null=True)
    google_adsense_id = models.CharField(max_length=20, blank=True, null=True)
    google_maps_api_key = models.CharField(max_length=50, blank=True, null=True)

    # Maintenance Mode
    is_maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True, null=True)
    maintenance_image = models.ImageField(upload_to='maintenance/', blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
        ordering = ['-created_at']

    def __str__(self):
        return self.site_name
    def save(self, *args, **kwargs):
      """Ensure only one SiteSettings instance exists."""
      if not self.pk and SiteSettings.objects.exists():
        raise ValueError("Only one instance of SiteSettings is allowed.")
    
      super().save(*args, **kwargs)

    # Delete any other instances if they exist
      SiteSettings.objects.exclude(pk=self.pk).delete()


from django.db import models
from django.utils.text import slugify

# ===========================
# About Us
# ===========================
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from PIL import Image

class Aboutus(models.Model):
    """Model for the About Us page content."""
    title = models.CharField(max_length=100, default="About Us")
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField(default="Welcome to our education platform. We are dedicated to empowering minds and transforming futures through innovative learning solutions.")
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    mission = models.TextField()
    mission_image = models.ImageField(upload_to='about/', blank=True, null=True)
    vision = models.TextField()
    vision_image = models.ImageField(upload_to='about/', blank=True, null=True)
    objectives = models.TextField(help_text="Provide a general overview of objectives.")
    who_we_are_title = models.CharField(max_length=100, default="Who We Are")
    who_we_are_description = models.TextField(blank=True, null=True)
    who_we_are_image = models.ImageField(upload_to='about/', blank=True, null=True)
    why_exist_title = models.CharField(max_length=100, default="Why We Exist")
    why_exist_description = models.TextField(blank=True, null=True)

    COLUMN_CHOICES = (
        ('left', 'Left'),
        ('right', 'Right'),
    )
    column_position = models.CharField(max_length=5, choices=COLUMN_CHOICES, default='left')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Us"
        verbose_name_plural = "About Us"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Enforce singleton (only one instance allowed)
        if not self.pk and Aboutus.objects.exists():
            raise ValidationError("Only one About Us entry is allowed.")

        super().save(*args, **kwargs)

        # Resize images if they exist
        max_width, max_height = 800, 600
        for image_field in [self.image, self.mission_image, self.vision_image, self.who_we_are_image]:
            if image_field and image_field.path:
                img = Image.open(image_field.path)
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height))
                    img.save(image_field.path)

    def __str__(self):
        return self.title


from django.db import models
from PIL import Image
from datetime import timedelta
from django.utils.timezone import now

class Leader(models.Model):
    CATEGORY_CHOICES = [
        ('student', 'Student Leader'),
        ('executive', 'Executive Board'),
        ('faculty', 'Faculty Mentor'),
    ]

    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, help_text="e.g., President, Technical Lead")
    bio = models.TextField(blank=True, help_text="Short description about the leader")
    photo = models.ImageField(upload_to='leaders_photos/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    personal_website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='student',
        help_text="Select group type"
    )

    # Leadership duration
    start_date = models.DateField(help_text="Start of leadership period", default=date.today)
    end_date = models.DateField(help_text="End of leadership period (auto-calculates 6 months if left empty)", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Leader"
        verbose_name_plural = "Leaders"

    def save(self, *args, **kwargs):
        # Auto-calculate end_date as 6 months later if not set
        if self.start_date and not self.end_date:
            self.end_date = self.start_date + timedelta(days=180)

        super().save(*args, **kwargs)

        # Resize uploaded photo if needed
        max_width, max_height = 800, 600
        if self.photo and self.photo.path:
            img = Image.open(self.photo.path)
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height))
                img.save(self.photo.path)

    def __str__(self):
        return f"{self.full_name} - {self.position}"

    def is_current(self):
        today = now().date()
        return self.start_date <= today <= self.end_date

    def is_past(self):
        today = now().date()
        return today > self.end_date


class News(models.Model):
    """Comprehensive News model for all site content: news, announcements, updates, academic info, etc."""

    title = models.CharField(max_length=150, unique=True, help_text="Headline or title of the news item")
    slug = models.SlugField(max_length=160, unique=True, blank=True, help_text="URL-friendly slug")
    summary = models.TextField(blank=True, help_text="Short summary or excerpt")
    content = models.TextField(blank=True, help_text="Full detailed content for the news")
    url = models.URLField(max_length=300, blank=True, help_text="Optional external link for news or resource")

    image = models.ImageField(upload_to='news_images/', blank=True, null=True, help_text="Optional image for the news item")

    is_published = models.BooleanField(default=True, help_text="Show or hide this news item on the site")
    publish_date = models.DateTimeField(null=True, blank=True, help_text="Date when news was published or will be published")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.publish_date:
            from django.utils.timezone import now
            self.publish_date = now()
        super().save(*args, **kwargs)



# ===========================
# Events
# ===========================

from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from PIL import Image

class Event(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    background_image = models.ImageField(upload_to='events_section_bg/', blank=True, null=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    event_url = models.URLField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    event_start = models.DateTimeField(null=True, blank=True)
    event_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['event_start']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.event_start:
            self.event_start = now()
        super().save(*args, **kwargs)

        # Resize images if they exist
        max_width = 800
        max_height = 600

        for img_field in [self.background_image, self.image]:
            if img_field and img_field.path:
                img = Image.open(img_field.path)
                if img.width > max_width or img.height > max_height:
                    img.thumbnail((max_width, max_height))
                    img.save(img_field.path)

    def is_upcoming(self):
        return self.event_start and self.event_start >= now()

    def is_past(self):
        return self.event_end and self.event_end < now()

    def time_until_start(self):
        delta = self.event_start - now()
        if delta.total_seconds() > 0:
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f"{days}d {hours}h {minutes}m remaining"
        return "Started"


# ===========================
# Research Links
# ===========================

from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now

class Research(models.Model):
    """Professional Research model for all research projects, papers, teams, and initiatives."""

    title = models.CharField(max_length=150, unique=True, help_text="Title of the research project or paper")
    slug = models.SlugField(max_length=160, unique=True, blank=True, help_text="URL-friendly slug")
    summary = models.TextField(blank=True, help_text="Short summary or abstract of the research")
    content = models.TextField(blank=True, help_text="Full research description, findings, goals, etc.")
    
    researchers = models.CharField(max_length=255, blank=True, help_text="Names of lead researchers or contributors")
    category = models.CharField(max_length=100, blank=True, help_text="E.g. AI, Robotics, Agriculture, Climate, etc.")
    institution = models.CharField(max_length=150, blank=True, help_text="Institution or faculty involved")
    document_url = models.URLField(max_length=300, blank=True, help_text="Optional external link to PDF or documentation")
    
    image = models.ImageField(upload_to='research_images/', blank=True, null=True, help_text="Main image or thumbnail")
    is_published = models.BooleanField(default=True, help_text="Show or hide this research on the site")
    publish_date = models.DateTimeField(null=True, blank=True, help_text="Date the research was published or announced")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Research"
        verbose_name_plural = "Research"
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.publish_date:
            self.publish_date = now()
        super().save(*args, **kwargs)



# ===========================
# Resources
# ===========================
class Resource(models.Model):
    """Professional model to manage downloadable tools and learning materials."""

    RESOURCE_TYPES = [
        ('learning', 'Learning Resource'),
        ('tool', 'Tool / Download'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Brief summary or purpose of the resource")
    file = models.FileField(upload_to='resources/files/', blank=True, null=True, help_text="Optional downloadable file")
    external_url = models.URLField(blank=True, null=True, help_text="Optional link to external resource")

    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES, default='learning')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



# ===========================
# Community Outreach
# ===========================

class CommunityOutreach(models.Model):
    """Model for community outreach links."""
    title = models.CharField(max_length=50, default='Community Outreach')
    url = models.URLField(max_length=200, blank=True, null=True, help_text="URL for the community outreach link")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Community Outreach"
        verbose_name_plural = "Community Outreaches"

    def __str__(self):
        return self.title


# ===========================
# Projects
# ===========================
from django.utils.text import slugify
from PIL import Image
import os

class Project(models.Model):
    # your existing fields ...
    title = models.CharField(max_length=100, help_text="Project or Initiative title")
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    summary = models.TextField(blank=True, help_text="Short summary of the project")
    description = models.TextField(help_text="Full details or body content")
    contact_email = models.EmailField(blank=True, null=True, help_text="Email to reach out about this project")
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text="Phone number if applicable")
    url = models.URLField(blank=True, null=True, help_text="External or internal project link")
    image = models.ImageField(upload_to='project_images/', blank=True, null=True, help_text="Project image or banner")
    is_published = models.BooleanField(default=True)
    publish_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-publish_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        # Resize image after saving
        if self.image:
            img_path = self.image.path
            img = Image.open(img_path)

            max_width = 800
            max_height = 600

            # Only resize if larger than max dimensions
            if img.width > max_width or img.height > max_height:
                img.thumbnail((max_width, max_height))
                img.save(img_path)
    
    def __str__(self):
        return self.title




from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image  # Pillow library
import os

class HeroSlide(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='hero_slides/')
    button1_text = models.CharField(max_length=50, default='Apply Now')
    button1_url = models.CharField(max_length=255, default='/apply/')
    button1_style = models.CharField(max_length=50, default='primary')
    button2_text = models.CharField(max_length=50, default='Virtual Tour')
    button2_url = models.CharField(max_length=255, default='/virtual-tour/')
    button2_style = models.CharField(max_length=50, default='outline-light')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = _('Hero Slide')
        verbose_name_plural = _('Hero Slides')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            image_path = self.image.path
            try:
                img = Image.open(image_path)

                # Resize while maintaining aspect ratio
                max_size = (1920, 800)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save optimized image
                img.save(image_path, format='JPEG', quality=85)
            except Exception as e:
                print(f"Error resizing image: {e}")
































# 3. Partners/Affiliations
class Partner(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='partners/', help_text="Upload partner logo (recommended size: 150x150 pixels)")
    website_link = models.URLField(blank=True, null=True, help_text="Link to the partner's website.")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0, help_text="Order in which partners are displayed.")


    PARTNER_TYPES = (
        ('sponsor', 'Sponsor'),
        ('collaborator', 'Collaborator'),
        ('academic', 'Academic Partner'),
        ('other', 'Other'),
    )
    partner_type = models.CharField(max_length=50, choices=PARTNER_TYPES, default='collaborator')
    is_active = models.BooleanField(default=True) # To easily toggle visibility on the frontend
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first on the page.")

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name

