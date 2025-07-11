from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render, get_object_or_404
from datetime import date 

from django.shortcuts import render
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
   
   

)

def home(request):
    site_settings = SiteSettings.objects.first()
    about_pages = Aboutus.objects.all().order_by('title')

    # All link models
    leader = Leader.objects.all().order_by('position')
    news = News.objects.all().order_by('title')
    events = Event.objects.all().order_by('title')
    research = Research.objects.all().order_by('title')
    resources = Resource.objects.all().order_by('title')
    community = CommunityOutreach.objects.all().order_by('title')
    projects = Project.objects.all().order_by('title')
 



    # Add your new context here
    hero_slides = HeroSlide.objects.filter(is_active=True).order_by('order')  
    return render(request, 'kuai_club/home.html', {
        'site_settings': site_settings,
        'about_pages': about_pages, 

        # Add your new context here
        'leader': leader,
        'news': news,
        'events': events,
        'research': research,
        'resources': resources,
        'community': community,
        'projects': projects,

        'hero_slides': hero_slides,

    })

def about_pages_processor(request):
    pages = Aboutus.objects.all().order_by('title')
    return {'about_pages': pages}


def about_detail(request, page_id):
    try:
        page = Aboutus.objects.get(id=page_id)
    except Aboutus.DoesNotExist:
        return render(request, '404.html', status=404)

    return render(request, 'kuai_club/about.html', {'page': page})

def leaders_processor(request):
    leaders = Leader.objects.all().order_by('full_name')
    return {'leaders': leaders}

def leaders_detail(request):
    leaders_student = Leader.objects.filter(category='student').order_by('full_name')
    leaders_executive = Leader.objects.filter(category='executive').order_by('full_name')
    leaders_faculty = Leader.objects.filter(category='faculty').order_by('full_name')

    context = {
        'leaders_student': leaders_student,
        'leaders_executive': leaders_executive,
        'leaders_faculty': leaders_faculty,
    }

    return render(request, 'leaders_list.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Leader

def leaders_by_category(request, category):
    # Validate category to avoid bad URLs
    valid_categories = ['student', 'executive', 'faculty']
    if category not in valid_categories:
        return render(request, '404.html', status=404)
    
    leaders = Leader.objects.filter(category=category).order_by('full_name')
    category_verbose = dict(Leader.CATEGORY_CHOICES).get(category, category.title())
    return render(request, 'leaders_by_category.html', {
        'leaders': leaders,
        'category': category_verbose,
    })

def leader_detail(request, leader_id):
    leader = get_object_or_404(Leader, id=leader_id)
    return render(request, 'leader_detail.html', {'leader': leader})


def news_processor(request):
    news = News.objects.filter(is_published=True).order_by('-publish_date')
    return {'news': news}

def news_page(request, page_id):
    page = get_object_or_404(News, id=page_id, is_published=True)
    return render(request, 'news_detail.html', {'page': page})

#Event Details

def events_processor(request):
    events = Event.objects.filter(is_published=True).order_by('event_start')
    return {'events': events}

def event_page(request, page_id):
    try:
        page = Event.objects.get(id=page_id, is_published=True)
    except Event.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'EventDetails.html', {'page': page})

#research details

def research_processor(request):
    research = Research.objects.all().order_by('title')
    return {'research': research}

def research_page(request,page_id):
    try:
        page = Research.objects.get(id=page_id)
    except Research.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'research.html', {'page': page})

#Resource details
def resource_processor(request):
    resources = Resource.objects.all().order_by('title')
    return {'resources': resources}

def resource_page(request,page_id):
    try:
        page = Resource.objects.get(id=page_id)
    except Resource.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'resource_list.html', {'page': page})


#contact details
def contact_processor(request):
    projects = Project.objects.all().order_by('title')
    return {'projects': projects}

def project_page(request, page_id):
    try:
        page = Project.objects.get(id=page_id, is_published=True)
    except Project.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'projects/project_detail.html', {'page': page})



#community details

def community_processor(request):
    community = CommunityOutreach.objects.all().order_by('title')
    return {'community': community}

def community_page(request,page_id):
    try:
        page = CommunityOutreach.objects.get(id=page_id)
    except CommunityOutreach.DoesNotExist:
        return render(request, '404.html', status=404)
    return render(request, 'community.html', {'page': page})

#Hero Slide details
def hero_processor(request):
    hero_slides = HeroSlide.objects.all().order_by('title')
    return {'hero_slides': hero_slides}

