from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
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
    Partner,
    ClubJoinRequest,
    ContactInfo

)
import logging

logger = logging.getLogger(__name__)

def home(request):
    site_settings = SiteSettings.objects.first()

    # One main About Us entry
    about_page = Aboutus.objects.first()

    # All entries for menus/navigation
    about_pages = Aboutus.objects.all()

    leader = Leader.objects.all().order_by('position')
    news = News.objects.all().order_by('title')
    events = Event.objects.all().order_by('title')
    research = Research.objects.all().order_by('title')
    resources = Resource.objects.all().order_by('title')
    community = CommunityOutreach.objects.all().order_by('title')
    projects = Project.objects.all().order_by('title')
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')

    upcoming_events = Event.objects.filter(is_published=True, event_start__gte=now()).order_by('event_start')[:6]
    past_events = Event.objects.filter(is_published=True, event_end__lt=now()).order_by('-event_start')[:6]

    today = now().date()
    current_leaders = Leader.objects.filter(start_date__lte=today, end_date__gte=today)

    gallery_images = GalleryImage.objects.order_by('-upload_date', '-id')[:20] 
    partners = Partner.objects.filter(is_active=True).order_by('name')

    # contact and join request information
    contact_info = ContactInfo.objects.first()
    join_requests = ClubJoinRequest.objects.all().order_by('-date_joined')  # or 'date_joined' depending on your field name
    

    categories = [
        ('student', 'Student Leaders', current_leaders.filter(category='student')),
        ('faculty', 'Faculty Mentors', current_leaders.filter(category='faculty')),
]

     
    

  
    
    if upcoming_events and upcoming_events[0].background_image:
        background_image_url = upcoming_events[0].background_image.url
    else:
        # Fallback to SiteSettings or a default static image
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.background_image:
            background_image_url = site_settings.background_image.url
        else:
            background_image_url = '/static/images/default-background.jpg'

    return render(request, 'kuai_club/home.html', {
        'site_settings': site_settings,
        'about_page': about_page,
        'about_pages': about_pages,
        'leader': leader,
        'news': news,
        'events': events,
        'research': research,
        'resources': resources,
        'community': community,
        'projects': projects,
        'hero_slides': hero_slides,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'background_image_url': background_image_url,

        'categories': categories,
        'gallery_images': gallery_images, 
        'partners': partners,
        'contact_info': contact_info,
        'join_requests': join_requests,
    })

def about_pages_processor(request):
    return {
        'about_pages': Aboutus.objects.all(),
        'about_page': Aboutus.objects.first(),
    }

class AboutView(TemplateView):
    template_name = 'kuai_club/about.html'  # Adjust if your template path differs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['about'] = Aboutus.get_instance()
        except Aboutus.DoesNotExist:
            # Render a custom 404 page if no Aboutus instance exists
            # Note: you can customize the template path for your 404 page
            return render(self.request, '404.html', status=404)
        return context

def leaders_processor(request):
    leaders = Leader.objects.all().order_by('full_name')
    return {'leaders': leaders}

from django.shortcuts import render
from django.utils import timezone
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

def previous_leaders_by_category(request, category):
    """Display previous leaders filtered by category"""
    valid_categories = ['student', 'faculty']
    
    if category not in valid_categories:
        return render(request, '404.html', status=404)
    
    today = timezone.now().date()
    
    # Get leaders whose term has ended (past leaders)
    previous_leaders = Leader.objects.filter(
        category=category,
        end_date__isnull=False,  # Must have an end date
        end_date__lt=today       # End date must be in the past
    ).order_by('-year_served', '-end_date', 'full_name')
    
    logger.info(f"Found {previous_leaders.count()} previous leaders for category: {category}")
    
    # Debug: Log some details about the leaders found
    for leader in previous_leaders[:5]:  # Log first 5 for debugging
        logger.debug(f"Leader: {leader.full_name}, Year: {leader.year_served}, End Date: {leader.end_date}")
    
    # Group leaders by year_served
    leaders_by_year = defaultdict(list)
    for leader in previous_leaders:
        leaders_by_year[leader.year_served].append(leader)
    
    # Sort years in descending order (most recent first)
    sorted_years = sorted(leaders_by_year.keys(), reverse=True)
    
    # Create list of tuples for template iteration
    leaders_by_year_list = [(year, leaders_by_year[year]) for year in sorted_years]
    
    logger.info(f"Years with previous leaders: {sorted_years}")
    logger.info(f"Total years: {len(sorted_years)}")
    
    # If no leaders found, log additional debug info
    if not previous_leaders.exists():
        all_leaders = Leader.objects.filter(category=category)
        logger.info(f"Total leaders in {category} category: {all_leaders.count()}")
        for leader in all_leaders:
            logger.info(f"  - {leader.full_name}: start={leader.start_date}, end={leader.end_date}, is_past={leader.is_past_leader}")
    
    context = {
        'leaders_by_year_list': leaders_by_year_list,
        'category': category.title(),
        'total_previous_leaders': previous_leaders.count(),
    }
    
    return render(request, 'kuai_club/previous_leaders_by_category.html', context)


def current_leaders_by_category(request, category):
    """Display current leaders filtered by category"""
    valid_categories = ['student', 'faculty']
    
    if category not in valid_categories:
        return render(request, '404.html', status=404)
    
    today = timezone.now().date()
    
    # Get current leaders (those whose term hasn't ended yet)
    current_leaders = Leader.objects.filter(
        category=category,
        start_date__lte=today,  # Started on or before today
    ).filter(
        models.Q(end_date__isnull=True) |  # No end date (ongoing)
        models.Q(end_date__gte=today)      # Or end date is today or future
    ).order_by('-year_served', 'position', 'full_name')
    
    logger.info(f"Found {current_leaders.count()} current leaders for category: {category}")
    
    context = {
        'leaders': current_leaders,
        'category': category.title(),
        'total_current_leaders': current_leaders.count(),
    }
    
    return render(request, 'kuai_club/current_leaders_by_category.html', context)


def leaders_by_category(request, category):
    valid_categories = ['student', 'faculty']
    if category not in valid_categories:
        return render(request, '404.html', status=404)
    
    # Redirect to homepage section for the category
    return redirect(f'/#category-{category}')


def news_processor(request):
    news = News.objects.filter(is_published=True).order_by('-publish_date')
    return {'news': news}

def events_processor(request):
    events = Event.objects.filter(is_published=True).order_by('event_start')
    return {'events': events}

def event_page(request, page_id):
    try:
        page = Event.objects.get(id=page_id, is_published=True)
    except Event.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'EventDetails.html', {'page': page})

def research_processor(request):
    research = Research.objects.all().order_by('title')
    return {'research': research}

def research_page(request, page_id):
    page = get_object_or_404(Research, id=page_id)

    # Prepare category list by splitting and stripping commas
    if page.category:
        category_list = [tag.strip() for tag in page.category.split(',')]
    else:
        category_list = []

    # Prepare researchers list by splitting and stripping commas
    if page.researchers:
        researchers_list = [r.strip() for r in page.researchers.split(',')]
    else:
        researchers_list = []

    context = {
        'page': page,
        'category_list': category_list,
        'researchers_list': researchers_list,
    }

    return render(request, 'kuai_club/research.html', context)


def resource_processor(request):
    resources = Resource.objects.all().order_by('title')
    return {'resources': resources}

def resource_page(request, page_id):
    try:
        page = Resource.objects.get(id=page_id)
    except Resource.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'resource_list.html', {'page': page})

def project_processor(request):
    projects = Project.objects.all().order_by('title')
    return {'projects': projects}

# Add this new function to your views.py

def project_detail(request, slug):
    """
    Display a single project detail page using slug
    """
    try:
        # Get the project by slug, only if it's published
        project = get_object_or_404(Project, slug=slug, is_published=True)
        
        # Debug logging
        logger.info(f"Found project: {project.title} with slug: {slug}")
        
        context = {
            'project': project,  # ✅ Correct context variable name
        }
        
        return render(request, 'kuai_club/project_detail.html', context)
        
    except Project.DoesNotExist:
        logger.error(f"Project not found with slug: {slug}")
        return render(request, '404.html', status=404)

# Keep your existing project_page function for backward compatibility if needed
def project_page(request, page_id):
    """
    Legacy function - redirects to slug-based URL
    """
    try:
        project = Project.objects.get(id=page_id, is_published=True)
        # Redirect to the slug-based URL
        return redirect('kuai_club:project_detail', slug=project.slug)
    except Project.DoesNotExist:
        return render(request, '404.html', status=404)

def community_processor(request):
    community = CommunityOutreach.objects.all().order_by('title')
    return {'community': community}

def community_page(request, page_id):
    try:
        page = CommunityOutreach.objects.get(id=page_id)
    except CommunityOutreach.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'indabax_app/home.html', {'page': page})

def hero_processor(request):
    hero_slides = HeroSlide.objects.all().order_by('title')
    return {'hero_slides': hero_slides}

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
    """
    Events API endpoint - NOTE: This should match the URL pattern /api/events/
    """
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
        # Calculate time until start for upcoming events
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

# Keep the old function name for backward compatibility
def event_api_view(request):
    return api_events(request)

from django.shortcuts import redirect
from django.contrib import messages
from .models import ClubJoinRequest

def join_club_submit(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        profession = request.POST.get('profession', '').strip()
        message_text = request.POST.get('message', '').strip()

        # Basic validation
        if not full_name or not email or not phone or not profession or not message_text:
            messages.error(request, '🚫 All fields are required. Please fill out the form completely.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Save the request
        ClubJoinRequest.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            profession=profession,
            message=message_text
        )

        messages.success(request, '🎉 Thank you for joining! We’ll get back to you soon.')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        messages.error(request, '⚠️ Invalid request method.')
        return redirect('/')
