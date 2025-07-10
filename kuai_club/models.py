from django.db import models
from django.utils.text import slugify # Import slugify
from datetime import date

# 1. Homepage & Site Configuration
class SiteConfig(models.Model):
    """
    Model for general site-wide configuration and homepage content.
    This model should ideally only have one instance.
    """
    site_name = models.CharField(max_length=200, default="Kabale University AI Club")
    main_tagline = models.CharField(max_length=255, blank=True, help_text="A catchy tagline for the homepage hero section.")
    featured_announcement = models.TextField(blank=True, help_text="A short announcement to display prominently on the homepage.")
    homepage_background_image = models.ImageField(upload_to='site_config/backgrounds/', blank=True, null=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def __str__(self):
        return self.site_name

# 2. About Us Page Content
class AboutPageContent(models.Model):
    """
    Model for the main About Us page content.
    This model should ideally only have one instance.
    """
    mission = models.TextField()
    vision = models.TextField()
    objectives = models.TextField(help_text="Provide a general overview of objectives. Specific objectives can be broken down if needed.")

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"

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

# 4. Executive Board/Leaders (for the main KUAI Club)
class ExecutivePosition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField(default=0, help_text="Order in which positions are displayed.")

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Executive Position"
        verbose_name_plural = "Executive Positions"

    def __str__(self):
        return self.name

class ExecutiveLeader(models.Model):
    name = models.CharField(max_length=100)
    position = models.ForeignKey(ExecutivePosition, on_delete=models.SET_NULL, null=True, blank=True)
    photo = models.ImageField(upload_to='kuai_club_leaders/', blank=True, null=True)
    bio = models.TextField(blank=True)
    term_start = models.DateField(default=date.today)
    term_end = models.DateField(null=True, blank=True) # Null for current leaders

    def is_current(self):
        return self.term_end is None or self.term_end >= date.today()

    def __str__(self):
        return f"{self.name} ({self.position or 'No Position'})"

    class Meta:
        ordering = ['position__order', '-term_start', 'name']
        verbose_name = "Executive Board Member"
        verbose_name_plural = "Executive Board Members"


# 5. News/Announcements
class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True, help_text="A unique slug for the URL, auto-generated if left blank.") # Added blank=True
    author = models.CharField(max_length=100, blank=True, help_text="Name of the author or posting entity.")
    content = models.TextField()
    featured_image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "News Post"
        verbose_name_plural = "News Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug: # Only auto-generate if slug is not already set
            base_slug = slugify(self.title)
            slug_candidate = base_slug
            counter = 1
            # Ensure slug is unique
            while NewsPost.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)


# 6. Club Events (General KUAI Club Events)
class ClubEventType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ClubEvent(models.Model):
    title = models.CharField(max_length=255)
    event_type = models.ForeignKey(ClubEventType, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    date = models.DateField()
    time = models.CharField(max_length=50, blank=True, help_text="e.g., 10:00 AM - 12:00 PM")
    location = models.CharField(max_length=255, blank=True)
    registration_link = models.URLField(blank=True, null=True)
    event_image = models.ImageField(upload_to='club_events/', blank=True, null=True)
    is_upcoming = models.BooleanField(default=True, help_text="Uncheck for past events manually or update automatically.")

    class Meta:
        ordering = ['-date', '-time'] # Order by latest date first
        verbose_name = "Club Event"
        verbose_name_plural = "Club Events"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Basic logic to set is_upcoming based on date. Can be more sophisticated.
        self.is_upcoming = self.date >= date.today()
        super().save(*args, **kwargs)

# 7. Research & Projects
class ResearchArea(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True, help_text="A unique identifier for the URL, auto-generated if left blank.") 
    order = models.IntegerField(default=0, help_text="Order in which research areas are displayed.")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug: # Only auto-generate if slug is not already set
            base_slug = slugify(self.name)
            slug_candidate = base_slug
            counter = 1
            # Ensure slug is unique
            while ResearchArea.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)


class ClubProject(models.Model):
    title = models.CharField(max_length=255)
    research_area = models.ForeignKey(ResearchArea, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    status_choices = [
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Planned', 'Planned'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Ongoing')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    project_image = models.ImageField(upload_to='club_projects/', blank=True, null=True)
    is_featured = models.BooleanField(default=False, help_text="Check to feature this project on the homepage or dedicated section.")

    class Meta:
        ordering = ['status', '-start_date', 'title']
        verbose_name = "Club Project"
        verbose_name_plural = "Club Projects"

    def __str__(self):
        return self.title

# 8. Communities (to link to sub-apps like IndabaX)
class Community(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100, blank=True, help_text="Unique URL identifier (e.g., 'indabax').") # Added blank=True
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='communities/', blank=True, null=True)
    website_url = models.URLField(blank=True, null=True, help_text="URL to the community's section/app (e.g., /communities/indabax/).")
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Order in which communities are displayed.")

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Communities"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug: # Only auto-generate if slug is not already set
            base_slug = slugify(self.name)
            slug_candidate = base_slug
            counter = 1
            # Ensure slug is unique
            while Community.objects.filter(slug=slug_candidate).exists():
                slug_candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

# 9. Resource Links
class ResourceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, max_length=100, blank=True) # <-- ADD THIS
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first.") # <-- ADD THIS

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Resource Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ResourceLink(models.Model):
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True) # <-- ADD THIS
    display_order = models.IntegerField(default=0, help_text="Lower numbers appear first within their category.") # <-- ADD THIS

    class Meta:
        ordering = ['category__display_order', 'display_order', 'title'] # Order by category, then link order
        unique_together = ('category', 'title') # A link title should be unique within a category

    def __str__(self):
        return self.title
