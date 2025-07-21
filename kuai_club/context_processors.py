from django.core.cache import cache
from django.utils.timezone import now # Ensure now is imported for time-based filtering

from .models import (
    SiteSettings,
    Aboutus,
    Leader,
    News,
    Event,
    Research,
    Resource,
    CommunityOutreach,
    Project,
    HeroSlide,
    GalleryImage # Make sure all models are imported once at the top
)

# You can combine all these into one main context processor function
# to avoid multiple entries in settings.py, or keep them separate
# if you prefer granular control over which context processors are active.

# Let's assume for now you want to keep them separate for modularity,
# but clean up imports and refine the 'resource_processor'.

def site_settings(request):
    """Global site settings."""
    settings = cache.get('site_settings')
    if not settings:
        settings = SiteSettings.objects.first()
        # Handle case where no SiteSettings exists yet
        if settings is None:
            # You might want to create a default one, or handle this gracefully in templates
            # For now, return an empty dict or None if no settings exist
            return {'site_settings': None}
        cache.set('site_settings', settings, 300)
    return {'site_settings': settings}


def about_pages_processor(request):
    """Context processor to provide about_pages (list) and about_page (first item)."""
    # It's better to fetch these together if they are always used together
    about_pages = cache.get('about_pages')
    if not about_pages:
        about_pages = Aboutus.objects.all()
        cache.set('about_pages', about_pages, 300)

    # Note: about_page will be the first item from about_pages, so no need for a separate query
    about_page = about_pages.first() if about_pages else None # Safely get the first item

    return {
        'about_pages': about_pages,
        'about_page': about_page,
    }


def leader_processor(request):
    """Pass categorized leaders globally to templates."""
    # Consider caching the individual leader categories if they don't change often
    leaders_student = cache.get('leaders_student')
    if not leaders_student:
        leaders_student = Leader.objects.filter(category='student').order_by('position')
        cache.set('leaders_student', leaders_student, 300)

    leaders_executive = cache.get('leaders_executive')
    if not leaders_executive:
        leaders_executive = Leader.objects.filter(category='executive').order_by('position')
        cache.set('leaders_executive', leaders_executive, 300)

    leaders_faculty = cache.get('leaders_faculty')
    if not leaders_faculty:
        leaders_faculty = Leader.objects.filter(category='faculty').order_by('position')
        cache.set('leaders_faculty', leaders_faculty, 300)

    return {
        'leaders_student': leaders_student,
        'leaders_executive': leaders_executive,
        'leaders_faculty': leaders_faculty
    }


def news_processor(request):
    """News items with caching for 5 minutes."""
    news = cache.get('news_items')
    if not news:
        news = News.objects.filter(is_published=True).order_by('-publish_date')[:5] # Limit for dropdown
        cache.set('news_items', news, 300)
    return {'news': news}


def events_processor(request):
    """Events - cached for 5 minutes."""
    # Filter for upcoming events for the dropdown
    events = cache.get('events_list_upcoming') # Use a distinct cache key
    if not events:
        events = Event.objects.filter(is_published=True, event_start__gte=now()).order_by('event_start')[:5] # Limit for dropdown
        cache.set('events_list_upcoming', events, 300)
    return {'upcoming_events': events} # Rename context variable for clarity


def research_processor(request):
    """Research links."""
    research = cache.get('research_links')
    if not research:
        # Assuming you want top 5 for the dropdown
        research = Research.objects.filter(is_published=True).order_by('-publish_date')[:5]
        cache.set('research_links', research, 300)
    return {'research': research}


def resource_processor(request):
    """Categorized resources for navbar dropdown."""
    learning_resources = cache.get('navbar_learning_resources')
    tool_resources = cache.get('navbar_tool_resources')

    if not learning_resources:
        learning_resources = Resource.objects.filter(is_active=True, resource_type='learning').order_by('-created_at')[:3] # Limit to 3 for dropdown
        cache.set('navbar_learning_resources', learning_resources, 300)

    if not tool_resources:
        tool_resources = Resource.objects.filter(is_active=True, resource_type='tool').order_by('-created_at')[:3] # Limit to 3 for dropdown
        cache.set('navbar_tool_resources', tool_resources, 300)

    return {
        'learning_resources': learning_resources,
        'tool_resources': tool_resources,
    }


def community_processor(request):
    """Community outreach links."""
    community = cache.get('community_links')
    if not community:
        community = CommunityOutreach.objects.all().order_by('title')[:5] # Limit for dropdown to prevent overload
        cache.set('community_links', community, 300)
    return {'communities': community}


def project_processor(request):
    """Project links processor for navbar."""
    projects = cache.get('project_links')
    if not projects:
        projects = Project.objects.filter(is_published=True).order_by('title')
        cache.set('project_links', projects, 300)
    return {'projects': projects}

def hero_processor(request):
    """Hero slides context processor with caching."""
    hero_slides = cache.get('hero_slides')
    if not hero_slides:
        hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')[:5]
        cache.set('hero_slides', hero_slides, 300)
    return {'hero_slides': hero_slides}

def gallery_processor(request):
    """Latest gallery images with caching for 5 minutes."""
    gallery_images = cache.get('latest_gallery_images')
    if not gallery_images:
        gallery_images = GalleryImage.objects.order_by('-upload_date', '-id')[:10]
        cache.set('latest_gallery_images', gallery_images, 300)
    return {'gallery_images': gallery_images}