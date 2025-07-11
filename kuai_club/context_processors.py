from django.core.cache import cache
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
    HeroSlide
)

def site_settings(request):
    """Global site settings."""
    settings = cache.get('site_settings')
    if not settings:
        settings = SiteSettings.objects.first()
        cache.set('site_settings', settings, 300)
    return {'site_settings': settings}


def about_pages_processor(request):
    """About pages list."""
    pages = cache.get('about_pages')
    if not pages:
        pages = Aboutus.objects.all().order_by('title')
        cache.set('about_pages', pages, 300)
    return {'about_pages': pages}


def leader_processor(request):
    """Pass categorized leaders globally to templates."""
    leaders_student = Leader.objects.filter(category='student').order_by('position')
    leaders_executive = Leader.objects.filter(category='executive').order_by('position')
    leaders_faculty = Leader.objects.filter(category='faculty').order_by('position')

    return {
        'leaders_student': leaders_student,
        'leaders_executive': leaders_executive,
        'leaders_faculty': leaders_faculty
    }


def news_processor(request):
    """News items with caching for 5 minutes."""
    news = cache.get('news_items')
    if not news:
        news = News.objects.filter(is_published=True).order_by('-publish_date')
        cache.set('news_items', news, 300)  # Cache for 300 seconds = 5 minutes
    return {'news': news}


def events_processor(request):
    """Events - cached for 5 minutes."""
    events = cache.get('events_list')
    if not events:
        events = Event.objects.filter(is_published=True).order_by('event_start')
        cache.set('events_list', events, 300)
    return {'events': events}


def research_processor(request):
    """Research links."""
    research = cache.get('research_links')
    if not research:
        research = Research.objects.all().order_by('title')
        cache.set('research_links', research, 300)
    return {'research': research}


def resource_processor(request):
    """Categorized resources for navbar dropdown."""
    resources = cache.get('navbar_resources')
    if not resources:
        resources = Resource.objects.filter(is_active=True).order_by('title')
        cache.set('navbar_resources', resources, 300)
    return {'resources': resources}  # still using 'services' in template



def community_processor(request):
    """Community outreach links."""
    community = cache.get('community_links')
    if not community:
        community = CommunityOutreach.objects.all().order_by('title')
        cache.set('community_links', community, 300)
    return {'community': community}


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
        hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')[:5]  # Only active slides, ordered, limited to 5
        cache.set('hero_slides', hero_slides, 300)  # Cache for 5 minutes
    return {'hero_slides': hero_slides}

