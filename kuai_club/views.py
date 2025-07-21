# kuai_club/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from datetime import datetime, timedelta
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
    GalleryImage,
    Partner # Ensure Partner is imported if you're using it in partner_list
)
import logging

logger = logging.getLogger(__name__)

# --- EXISTING VIEWS (Ensure these are present as you had them) ---

def home(request):
    site_settings = SiteSettings.objects.first()
    about_page = Aboutus.objects.first()
    about_pages = Aboutus.objects.all() 
    
    latest_news_for_dropdown = News.objects.filter(is_published=True).order_by('-publish_date')[:3] 
    
    # --- IMPORTANT: FOR EVENTS DROPDOWN ---
    # Fetch only upcoming events for the dropdown, limited to a few (e.g., 3 or 5)
    # Filter by is_published=True and event_start >= now()
    # Order by event_start to get the soonest upcoming events first
    events_for_dropdown = Event.objects.filter(is_published=True, event_start__gte=now()).order_by('event_start')[:3] 
    # ^^^ Change [:3] to whatever number you want in the dropdown.

    leader = Leader.objects.all().order_by('position')
    research = Research.objects.all().order_by('title')
    resources = Resource.objects.all().order_by('title')
    all_communities_outreach = CommunityOutreach.objects.all().order_by('order') 
    featured_communities_outreach = CommunityOutreach.objects.filter(is_featured=True).order_by('order') 
    projects = Project.objects.all().order_by('title')
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')

    # Your existing upcoming_events and past_events are good for dedicated sections if used on homepage.
    upcoming_events = Event.objects.filter(is_published=True, event_start__gte=now()).order_by('event_start')[:6]
    past_events = Event.objects.filter(is_published=True, event_end__lt=now()).order_by('-event_start')[:6]

    today = now().date()
    current_leaders = Leader.objects.filter(start_date__lte=today, end_date__gte=today)

    gallery_images = GalleryImage.objects.order_by('-upload_date', '-id')[:20] 

    categories = [
        ('student', 'Student Leaders', current_leaders.filter(category='student')),
        ('executive', 'Executive Board', current_leaders.filter(category='executive')),
        ('faculty', 'Faculty Mentors', current_leaders.filter(category='faculty')),
    ]
   
    if upcoming_events and upcoming_events[0].background_image:
        background_image_url = upcoming_events[0].background_image.url
    else:
        site_settings_for_bg = SiteSettings.objects.first() 
        if site_settings_for_bg and site_settings_for_bg.background_image:
            background_image_url = site_settings_for_bg.background_image.url
        else:
            background_image_url = '/static/images/default-background.jpg'

    return render(request, 'kuai_club/home.html', {
        'site_settings': site_settings,
        'about_page': about_page,
        'about_pages': about_pages,
        'leader': leader,
        'news': latest_news_for_dropdown, # This is for the news dropdown
        'events': events_for_dropdown, # Use this for the events dropdown
        'research': research,
        'resources': resources,
        'all_communities_outreach': all_communities_outreach,
        'featured_communities_outreach': featured_communities_outreach,
        'projects': projects,
        'hero_slides': hero_slides,
        'upcoming_events': upcoming_events, # Keep if used elsewhere on home (e.g., a dedicated events section)
        'past_events': past_events,       # Keep if used elsewhere on home
        'background_image_url': background_image_url,
        'categories': categories,
        'gallery_images': gallery_images, 
    })


# --- CONTEXT PROCESSORS (These should NOT be in urls.py, but in settings.py TEMPLATES 'OPTIONS') ---
# These functions should not be directly called by URLs.
# If you have them defined in settings.py like:
# 'kuai_club.views.about_pages_processor',
# Then they are fine here. Just make sure they are not mapped in urls.py.
def about_pages_processor(request):
    return {
        'about_pages': Aboutus.objects.all(),
        'about_page': Aboutus.objects.first(), # for general 'About Us' link
    }

def leaders_processor(request): # This is fine if used as a context processor
    leaders = Leader.objects.all().order_by('full_name')
    return {'leaders': leaders}

def news_processor(request): # This is fine if used as a context processor
    news = News.objects.filter(is_published=True).order_by('-publish_date')
    return {'news': news}

def events_processor(request): # This is fine if used as a context processor
    events = Event.objects.filter(is_published=True).order_by('event_start')
    return {'events': events}

def research_processor(request): # This is fine if used as a context processor
    research = Research.objects.all().order_by('title')
    return {'research': research}

def resource_processor(request): # This is fine if used as a context processor
    resources = Resource.objects.all().order_by('title')
    return {'resources': resources}

def project_processor(request): # This is fine if used as a context processor
    projects = Project.objects.filter(is_published=True).order_by('-publish_date')[:5] 
    return {'projects': projects}


def community_processor(request): # This is fine if used as a context processor
    community = CommunityOutreach.objects.all().order_by('title')
    return {'community': community}

def hero_processor(request): # This is fine if used as a context processor
    hero_slides = HeroSlide.objects.all().order_by('title')
    return {'hero_slides': hero_slides}


# --- END CONTEXT PROCESSORS ---


# --- DETAIL VIEWS (Existing ones, ensure correct template paths) ---

def about_detail(request, page_id):
    try:
        page = Aboutus.objects.get(id=page_id)
    except Aboutus.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'kuai_club/about.html', {'page': page}) # Corrected template path

def leaders_list_view(request): # Renamed from leaders_list_all
    site_settings = SiteSettings.objects.first() # Get site settings for base.html title
    today = now().date()

    # Fetch and filter current leaders by category
    student_leaders = Leader.objects.filter(
        category='student',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('full_name') # Added ordering for consistency

    executive_board = Leader.objects.filter(
        category='executive',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('full_name')

    faculty_mentors = Leader.objects.filter(
        category='faculty',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('full_name')

    context = {
        'site_settings': site_settings, # Pass site settings
        'student_leaders': student_leaders,
        'executive_board': executive_board,
        'faculty_mentors': faculty_mentors,
        'page_title': 'Our Leaders', # For template use
    }
    return render(request, 'kuai_club/leaders_list.html', context)


def leader_detail(request, leader_id):
    leader = get_object_or_404(Leader, id=leader_id) # Renamed variable from 'leaders' to 'leader' for clarity
    return render(request, 'kuai_club/leader_detail.html', {'leader': leader}) # Corrected template path

def event_page(request, page_id):
    try:
        page = Event.objects.get(id=page_id, is_published=True)
    except Event.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'kuai_club/event_detail.html', {'page': page}) # Corrected template name and path

def research_page(request, page_id):
    try:
        page = Research.objects.get(id=page_id)
    except Research.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'kuai_club/research_detail.html', {'page': page}) # Assuming research_detail.html is your actual detail page

def resource_page(request, page_id): # This view's name 'resource_page' suggests it's for details
    try:
        page = Resource.objects.get(id=page_id)
    except Resource.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'kuai_club/resource_detail.html', {'page': page}) # Changed to resource_detail.html

def project_page(request, page_id):
    try:
        page = Project.objects.get(id=page_id, is_published=True)
    except Project.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'kuai_club/project_detail.html', {'page': page}) # Corrected path and name

def community_page(request, page_id):
    try:
        page = CommunityOutreach.objects.get(id=page_id)
    except CommunityOutreach.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'kuai_club/community_detail.html', {'page': page}) # Changed to community_detail.html

# --- API VIEWS (Keep as they are) ---
def api_projects(request):
    logger.info(f"API called with method: {request.method}")
    logger.info(f"GET parameters: {request.GET}")
    
    page = int(request.GET.get('page', 1))
    logger.info(f"Requested page: {page}")
    
    projects_qs = Project.objects.filter(is_published=True).order_by('-publish_date', 'id')
    total_count = projects_qs.count()
    logger.info(f"Total published projects: {total_count}")
    
    paginator = Paginator(projects_qs, 3)
    logger.info(f"Total pages: {paginator.num_pages}")

    try:
        projects_page = paginator.page(page)
        logger.info(f"Page {page} loaded successfully with {len(projects_page)} projects")
    except Exception as e:
        logger.error(f"Error loading page {page}: {e}")
        return JsonResponse({
            "projects": [], 
            "has_next": False, 
            "error": str(e),
            "page": page,
            "total_pages": 0
        })

    projects_list = []
    for project in projects_page:
        project_data = {
            "id": project.id,
            "title": project.title,
            "summary": project.summary,
            "image_url": project.image.url if project.image else "",
            "publish_date": project.publish_date.isoformat() if project.publish_date else "",
            "url": project.url or "",
        }
        projects_list.append(project_data)
        logger.info(f"Added project ID {project.id}: {project.title}")

    response_data = {
        "projects": projects_list,
        "has_next": projects_page.has_next(),
        "page": page,
        "total_pages": paginator.num_pages,
        "total_count": total_count
    }
    
    logger.info(f"Returning response: {len(projects_list)} projects, has_next: {projects_page.has_next()}")
    return JsonResponse(response_data)


@require_GET
def api_events(request):
    event_type = request.GET.get('type', 'upcoming')
    page_number = int(request.GET.get('page', 1))
    per_page = request.GET.get('per_page')

    logger.info(f"Events API called - type: {event_type}, page: {page_number}, per_page: {per_page}")

    if event_type == 'past':
        queryset = Event.objects.filter(
            is_published=True,
            event_end__lt=now()
        ).order_by('-event_end')
        default_per_page = 1
    else:  # upcoming
        queryset = Event.objects.filter(
            is_published=True,
            event_start__gte=now()
        ).order_by('event_start')
        default_per_page = 2

    if per_page and per_page.isdigit():
        per_page = int(per_page)
        per_page = max(1, min(per_page, 10))
    else:
        per_page = default_per_page

    paginator = Paginator(queryset, per_page)
    
    try:
        page = paginator.page(page_number)
    except Exception as e:
        logger.error(f"Error loading events page {page_number}: {e}")
        return JsonResponse({
            "events": [],
            "has_next": False,
            "has_previous": False,
            "page": page_number,
            "total_pages": 0,
            "per_page": per_page,
            "error": str(e)
        })

    event_data = []
    for event in page:
        time_until_start = None
        if event_type == 'upcoming' and event.event_start:
            time_diff = event.event_start - now()
            if time_diff.total_seconds() > 0:
                days = time_diff.days
                hours = time_diff.seconds // 3600
                minutes = (time_diff.seconds % 3600) // 60
                
                time_parts = []
                if days > 0:
                    time_parts.append(f"{days}d")
                if hours > 0:
                    time_parts.append(f"{hours}h")
                if minutes > 0:
                    time_parts.append(f"{minutes}m")
                
                time_until_start = " ".join(time_parts) if time_parts else "Less than 1 minute"
            else:
                time_until_start = "Event has started!"

        event_dict = {
            "id": event.id,
            "title": event.title,
            "summary": event.summary,
            "event_url": event.event_url,
            "image_url": event.image.url if event.image else "",
            "organizer": getattr(event, 'organizer', ''),
            "event_start": event.event_start.isoformat() if event.event_start else "",
            "event_end": event.event_end.isoformat() if event.event_end else "",
        }
        
        if time_until_start:
            event_dict["time_until_start"] = time_until_start
        
        event_data.append(event_dict)

    logger.info(f"Returning {len(event_data)} events for page {page_number}")
    
    return JsonResponse({
        "events": event_data,
        "has_next": page.has_next(),
        "has_previous": page.has_previous(),
        "page": page.number,
        "total_pages": paginator.num_pages,
        "per_page": per_page,
        "total_count": queryset.count()
    })

def event_api_view(request): # This can likely be removed if not used anywhere
    return api_events(request)


# --- NEW LIST VIEWS (Add these new functions) ---

def news_list(request):
    all_news = News.objects.filter(is_published=True).order_by('-publish_date')
    return render(request, 'kuai_club/news_list.html', {'all_news': all_news})


def news_detail(request, pk): # pk needs to be here
    news_item = get_object_or_404(News, pk=pk) # This line correctly uses pk
    context = {
        'news_item': news_item,
        'site_settings': SiteSettings.objects.first(),
    }
    return render(request, 'kuai_club/news_detail.html', context)


def event_list(request):
    # Fetch all upcoming events (or filter by time if you want separate sections)
    upcoming = Event.objects.filter(is_published=True, event_start__gte=now()).order_by('event_start')
    # Fetch all past events
    past = Event.objects.filter(is_published=True, event_end__lt=now()).order_by('-event_start') # Order by most recent past event first

    context = {
        'upcoming_events_list': upcoming, # Use distinct names to avoid confusion with homepage context
        'past_events_list': past,
        'site_settings': SiteSettings.objects.first(),
    }
    return render(request, 'kuai_club/event_list.html', context)


def event_detail(request, pk):
    event_item = get_object_or_404(Event, pk=pk)
    context = {
        'event_item': event_item,
        'site_settings': SiteSettings.objects.first(),
    }
    return render(request, 'kuai_club/event_detail.html', context)

# def project_list(request):
#     projects = Project.objects.filter(is_published=True).order_by('-publish_date') # Assumed publish_date
#     return render(request, 'kuai_club/project_list.html', {'projects': projects})

def project_list(request):
    # This view is for the main 'All Projects' page
    all_projects = Project.objects.filter(is_published=True).order_by('-publish_date') 
    context = {
        'projects': all_projects, # This 'projects' is for the list page
        'page_title': 'Our Projects'
    }
    return render(request, 'kuai_club/project_list.html', context)

def project_detail(request, slug): # Changed from page_id to slug for cleaner URLs
    # This view is for individual project detail pages
    project_item = get_object_or_404(Project, slug=slug, is_published=True) # Use slug for lookup
    context = {
        'project_item': project_item,
        'page_title': project_item.title
    }
    return render(request, 'kuai_club/project_detail.html', context)

def research_list(request):
    all_research = Research.objects.all().order_by('-publish_date') # Order as desired
    context = {
        'research_areas': all_research,
        'page_title': 'All Research' # For base.html title block
    }
    return render(request, 'kuai_club/research_area_list.html', context)

def research_detail(request, pk):
    research_item = get_object_or_404(Research, pk=pk)
    context = {
        'research_item': research_item,
        'page_title': research_item.title # For base.html title block
    }
    return render(request, 'kuai_club/research_area_detail.html', context)

def resource_list(request):
    all_resources = Resource.objects.filter(is_active=True).order_by('title') # Order alphabetically
    context = {
        'resources': all_resources,
        'page_title': 'All Resources'
    }
    return render(request, 'kuai_club/resource_list.html', context)

def resource_detail(request, slug):
    resource_item = get_object_or_404(Resource, slug=slug, is_active=True)
    context = {
        'resource_item': resource_item,
        'page_title': resource_item.title
    }
    return render(request, 'kuai_club/resource_detail.html', context) 


def community_list(request):
    all_communities_outreach = CommunityOutreach.objects.all().order_by('order')
    site_settings = SiteSettings.objects.first()
    context = {
        'site_settings': site_settings,
        'all_communities_outreach': all_communities_outreach,
    }
    return render(request, 'kuai_club/community_list.html', context)
def partner_list(request):
    # Fetch partners, ordering by 'display_order' and then 'name' as per your model's Meta
    partners = Partner.objects.filter(is_active=True).order_by('display_order', 'name')
    context = {
        'partners': partners,
        'page_title': 'Our Partners' # For base.html title block
    }
    return render(request, 'kuai_club/partner_list.html', context)