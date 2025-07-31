from django.db import models
from django.urls import reverse
from django.utils import timezone


class SiteSettings(models.Model):
    # Social Media Links
    facebook_url = models.URLField(blank=True, verbose_name="Facebook URL")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter URL")
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")
    github_url = models.URLField(blank=True, verbose_name="GitHub URL")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube URL")

    # Contact Info
    contact_email = models.EmailField(blank=True, verbose_name="Contact Email")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Phone Number")
    physical_address = models.CharField(max_length=255, blank=True, verbose_name="Physical Address")

    # Other Footer/Site Content (e.g., short club description)
    footer_description = models.TextField(blank=True, verbose_name="Footer Club Description", help_text="A short description for the footer.")

    def __str__(self):
        return "Site Settings"

    # Ensure only one instance can exist (singleton pattern)
    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            # If trying to create a second instance, get the existing one
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
            self.id = existing.id # For older Django versions
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"


class HomePageContent(models.Model):
    """
    Model to store general dynamic content for the Home page.
    Assumes a single instance for primary home page text.
    """
    main_heading = models.CharField(max_length=200, default="Welcome to IndabaX Kabale AI Club!")
    main_subheading = models.TextField(default="Your premier hub for Artificial Intelligence education, research, and community engagement in Kabale, Uganda.")
    
    # About Our Initiative Section
    about_home_heading = models.CharField(max_length=200, default="About Our Initiative")
    about_home_paragraph = models.TextField(default="IndabaX Kabale is part of the larger Deep Learning IndabaX movement, aimed at strengthening African Machine Learning. We foster a vibrant community, providing resources and opportunities for learning, collaboration, and innovation in AI.")
    about_home_image = models.ImageField(upload_to='home_content/', blank=True, null=True, help_text="Image for the 'About Our Initiative' section on homepage.")

    # Call to Action Section
    cta_heading = models.CharField(max_length=200, default="Get Involved!")
    cta_paragraph = models.TextField(default="Ready to dive into the world of AI? Join our upcoming events and connect with us.")
    cta_primary_button_text = models.CharField(max_length=50, default="Upcoming Events")
    cta_primary_button_url = models.URLField(blank=True, null=True, help_text="URL for the primary Call to Action button (e.g., Upcoming Events page).")
    cta_secondary_button_text = models.CharField(max_length=50, default="Contact Us")
    cta_secondary_button_url = models.URLField(blank=True, null=True, help_text="URL for the secondary Call to Action button (e.g., Contact page).")

    def __str__(self):
        return "Home Page General Content"

    class Meta:
        verbose_name_plural = "Home Page General Content"

class Pillar(models.Model):
    """
    Model for the 'Our Core Pillars' section on the Home page.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class (e.g., fas fa-graduation-cap)")
    #button_text = models.CharField(max_length=50, default="Learn More")
    #button_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which pillars are displayed.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Event(models.Model):
    """
    Model for Upcoming and Past Events.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 9:00 AM - 12:00 PM")
    location = models.CharField(max_length=200, blank=True, null=True)
    registration_url = models.URLField(blank=True, null=True, help_text="Google Form URL or similar registration link")
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_upcoming = models.BooleanField(default=True, help_text="Check if this is an upcoming event.")
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date'] # Order by most recent date first

class Partner(models.Model):
    """
    Model for dynamic Partners section.
    """
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='partners/')
    website_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which partners are displayed.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

#----home page: slider images ------
class EventImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='slider/')
    description = models.TextField(blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# -------- Tutorials Page --------
class TutorialCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE)
    video_url = models.URLField()
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# -------- Leaders Page --------
class Leader(models.Model):
    POSITION_CHOICES = [
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Technical Lead', 'Technical Lead'),
        ('Treasurer', 'Treasurer'),
        ('Secretary', 'Secretary'),
        ('Graphics Designer Lead', 'Graphics Designer Lead'),
        ('Social Media Manager', 'Social Media Manager'),
        ('Event Manger', 'Event Manager'),
        ('Mobilizer', 'Mobilizer'),
        ('Year One Representative', 'Year One Representative'),
        ('Year Two Representative', 'Year Two Representative'),
        ('Presidential Advisor', 'Presidential Advisor'),
        
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    photo = models.ImageField(upload_to='leaders/')
    term_start = models.DateField()
    #term_end = models.DateField(null=True, blank=True)

    # --- The updated `is_current` field ---
    is_current = models.BooleanField(
        default=True,
        help_text="Check this box if the person is a current leader. Uncheck it for past leaders."
    )
    
    # --- New Fields (no changes here from the last step) ---
    bio = models.TextField(blank=True, help_text="A brief statement or fun fact about the leader.")
    linkedin_url = models.URLField(max_length=200, blank=True)
    twitter_url = models.URLField(max_length=200, blank=True)
    github_url = models.URLField(max_length=200, blank=True)
    

    def __str__(self):
        return f"{self.name} ({self.position})"

    class Meta:
        ordering = ['-is_current', 'position']
    

# -------- About Page (New Model) --------
class AboutContent(models.Model):
    """
    Model to store dynamic content for the About Us page.
    We'll assume there's only one instance of this model.
    """
    main_heading = models.CharField(max_length=200, default="About IndabaX Kabale AI Club")
    main_paragraph = models.TextField()
    purpose_heading = models.CharField(max_length=200, default="Our Purpose and Objectives")
    purpose_paragraph = models.TextField()

    # Dynamic Objectives
    # IMPORTANT FIX: Use 'AboutContent' as a string here
    class Objective(models.Model):
        about_content = models.ForeignKey('AboutContent', related_name='objectives', on_delete=models.CASCADE)
        title = models.CharField(max_length=200)
        description = models.TextField()

        def __str__(self):
            return self.title
        
        class Meta:
            verbose_name = "Objective"
            verbose_name_plural = "Objectives"

    # Dynamic Affiliations and Contact (optional)
    affiliations_heading = models.CharField(max_length=200, blank=True, null=True, default="Affiliations and Contact")
    affiliations_paragraph = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    # IMPORTANT FIX: Use 'AboutContent' as a string here
    class AffiliationLink(models.Model):
        about_content = models.ForeignKey('AboutContent', related_name='affiliation_links', on_delete=models.CASCADE)
        text = models.CharField(max_length=100)
        url = models.URLField()

        def __str__(self):
            return self.text
        
        class Meta:
            verbose_name = "Affiliation Link"
            verbose_name_plural = "Affiliation Links"


    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"
    
class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery_hero_images/', help_text="Image for the main hero slider.")
    title = models.CharField(max_length=100, blank=True, help_text="Short title for the hero image (optional).")
    description = models.TextField(blank=True, help_text="Brief description for the hero image (optional).")
    order = models.IntegerField(default=0, help_text="Order in which images appear in the slider.")

    class Meta:
        ordering = ['order']
        verbose_name = "Hero Gallery Image"
        verbose_name_plural = "Hero Gallery Images"

    def __str__(self):
        return self.title or f"Gallery Image {self.id}"
    
class HeroBackgroundImage(models.Model):
    image = models.ImageField(upload_to='hero_backgrounds/', help_text="Upload an image for the rotating hero background.")
    # You might want a title or description for admin identification, but it won't be displayed
    title = models.CharField(max_length=200, blank=True, null=True, help_text="Internal title for admin reference.")
    order = models.IntegerField(default=0, help_text="Order in which images should appear in the rotation.")
    is_active = models.BooleanField(default=True, help_text="Only active images will be used in the rotation.")

    def __str__(self):
        return self.title if self.title else f"Hero Background Image {self.id}"

    class Meta:
        ordering = ['order']
        verbose_name = "Hero Background Image"
        verbose_name_plural = "Hero Background Images"



class Album(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(max_length=400, help_text="Paste the shareable link from Google Photos here.")
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
# --- Modified Session Model ---
class Session(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Provide a general overview and detailed description of the session content."
    )
    session_date = models.DateField(default=timezone.now)
    google_photos_link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        help_text="Optional: Link to the full Google Photos album for this session."
    )
    is_published = models.BooleanField(default=True)

    tagline = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="A short, catchy phrase for the session (e.g., 'Discover Hidden Patterns')."
    )
    venue = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="e.g., 'New Computer Lab', 'Online via Zoom'"
    )
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    # NEW: Many-to-Many field for existing Leaders
    # This creates a selectable list in the admin.
    speakers = models.ManyToManyField(
        Leader,
        related_name='sessions_spoken_at',
        blank=True,
        help_text="Select existing leaders who spoke at this session."
    )

    # NEW: TextField for manually entered guest speakers or additional speaker info
    guest_speakers_info = models.TextField(
        blank=True,
        null=True,
        help_text="Enter names of guest speakers not listed above, or additional speaker details. Use new lines for each speaker."
    )

    class Meta:
        ordering = ['-session_date']

    def __str__(self):
        return f"{self.title} ({self.session_date.year}-{self.session_date.month}-{self.session_date.day})"

# NEW MODEL: For individual photos within a session
class SessionImage(models.Model):
    session = models.ForeignKey(Session, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='session_photos/') # Images will be stored in media/session_photos/
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image for {self.session.title} - {self.caption or self.image.name}"