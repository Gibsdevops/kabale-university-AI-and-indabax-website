from django.views.generic import TemplateView, ListView, DetailView
from .models import (
    SiteConfig, AboutPageContent, NewsPost, ClubEvent,
    ExecutiveLeader, ResearchArea, ClubProject, Community,
    ResourceCategory, Partner
) # Import all necessary models
from datetime import date # For current/past leaders/events logic


# Main Homepage View
class HomePageView(TemplateView):
    template_name = "kuai_club/home.html" # Placeholder template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch site config (assuming there's only one instance)
        context['site_config'] = SiteConfig.objects.first()
        # You can add more context here later, e.g., latest news, featured projects
        context['latest_news'] = NewsPost.objects.filter(is_published=True).order_by('-published_date')[:3]
        context['upcoming_events'] = ClubEvent.objects.filter(is_upcoming=True).order_by('date')[:3]
        return context

# About Us Page View
class AboutPageView(TemplateView):
    template_name = "kuai_club/about.html" # Placeholder template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about_content'] = AboutPageContent.objects.first()
        context['partners'] = Partner.objects.all().order_by('order', 'name')
        return context

# News List View
class NewsPostListView(ListView):
    model = NewsPost
    template_name = "kuai_club/news_list.html"
    context_object_name = 'news_posts' # Variable name in template
    queryset = NewsPost.objects.filter(is_published=True).order_by('-published_date') # Show only published posts
    paginate_by = 10

# News Detail View
class NewsPostDetailView(DetailView):
    model = NewsPost
    template_name = "kuai_club/news_detail.html"
    context_object_name = 'news_post' # Variable name in template
    slug_field = 'slug' # Tell DetailView to use the 'slug' field
    slug_url_kwarg = 'slug' # The URL keyword argument will also be 'slug'
    # Optional: ensure only published posts can be viewed
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

# Event List View
class ClubEventListView(ListView):
    model = ClubEvent
    template_name = "kuai_club/event_list.html" # We'll create this template next
    context_object_name = 'events' # Variable name in template
    
    def get_queryset(self):
        # By default, show upcoming events ordered by date (soonest first)
        queryset = ClubEvent.objects.filter(is_upcoming=True).order_by('date', 'time')

        # Allow filtering for past events via a URL parameter (e.g., /events/?status=past)
        status = self.request.GET.get('status')
        if status == 'past':
            queryset = ClubEvent.objects.filter(is_upcoming=False).order_by('-date', '-time') # Show most recent past events first
        elif status == 'all':
            queryset = ClubEvent.objects.all().order_by('-date', '-time') # Show all, most recent first
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'upcoming') # Pass current filter to template
        return context

# Event Detail View
class EventDetailView(DetailView):
    model = ClubEvent
    template_name = "kuai_club/event_detail.html" # Placeholder template
    context_object_name = "event"

# Executive Leaders List View
class ExecutiveLeaderListView(ListView):
    model = ExecutiveLeader
    template_name = "kuai_club/executive_leaders.html" # Placeholder template
    context_object_name = "leaders"

    def get_queryset(self):
        # Separate current and past leaders
        today = date.today()
        current_leaders = ExecutiveLeader.objects.filter(term_end__isnull=True) | ExecutiveLeader.objects.filter(term_end__gte=today)
        past_leaders = ExecutiveLeader.objects.filter(term_end__lt=today)
        return {
            'current_leaders': current_leaders.order_by('position__order', 'name'),
            'past_leaders': past_leaders.order_by('-term_end', 'name')
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The queryset is a dictionary, so we need to add its contents to context
        qs = self.get_queryset()
        context['current_leaders'] = qs['current_leaders']
        context['past_leaders'] = qs['past_leaders']
        return context

# Research Area List View
class ResearchAreaListView(ListView):
    model = ResearchArea
    template_name = "kuai_club/research_area_list.html" # Placeholder template
    context_object_name = "research_areas"
    queryset = ResearchArea.objects.all().order_by('order', 'name')

# Research Area Detail View
class ResearchAreaDetailView(DetailView):
    model = ResearchArea
    template_name = "kuai_club/research_area_detail.html" # Placeholder template
    context_object_name = "area"

# Project List View
class ProjectListView(ListView):
    model = ClubProject
    template_name = "kuai_club/project_list.html" # Placeholder template
    context_object_name = "projects"
    queryset = ClubProject.objects.all().order_by('-start_date')

# Project Detail View
class ProjectDetailView(DetailView):
    model = ClubProject
    template_name = "kuai_club/project_detail.html" # Placeholder template
    context_object_name = "project"

# Community List View
class CommunityListView(ListView):
    model = Community
    template_name = "kuai_club/community_list.html" # Placeholder template
    context_object_name = "communities"
    queryset = Community.objects.filter(is_active=True).order_by('order', 'name')

# Resource Link List View
class ResourcePageView(TemplateView):
    template_name = "kuai_club/resource_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all active categories and their active links, ordered by display_order
        categories = ResourceCategory.objects.all().order_by('display_order', 'name')
        
        # Create a list of dictionaries, each containing a category and its active links
        # This pre-fetches links to optimize database queries
        resource_data = []
        for category in categories:
            active_links = category.links.filter(is_active=True).order_by('display_order', 'title')
            if active_links.exists(): # Only include categories that have active links
                resource_data.append({
                    'category': category,
                    'links': active_links
                })
        
        context['resource_data'] = resource_data
        return context


# Partner List View
class PartnerListView(ListView):
    model = Partner
    template_name = "kuai_club/partner_list.html" # Placeholder template
    context_object_name = "partners"
    queryset = Partner.objects.all().order_by('order', 'name')