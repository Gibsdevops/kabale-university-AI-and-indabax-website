from django.views.generic import TemplateView, ListView, DetailView
from .models import (
    SiteConfig, AboutPageContent, NewsPost, ClubEvent,
    ExecutiveLeader, ResearchArea, ClubProject, Community,
    ResourceLink, Partner
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
class NewsListView(ListView):
    model = NewsPost
    template_name = "kuai_club/news_list.html" # Placeholder template
    context_object_name = "news_posts"
    queryset = NewsPost.objects.filter(is_published=True).order_by('-published_date')
    paginate_by = 10

# News Detail View
class NewsDetailView(DetailView):
    model = NewsPost
    template_name = "kuai_club/news_detail.html" # Placeholder template
    context_object_name = "post"

# Event List View
class EventListView(ListView):
    model = ClubEvent
    template_name = "kuai_club/event_list.html" # Placeholder template
    context_object_name = "events"
    queryset = ClubEvent.objects.all().order_by('-date')
    paginate_by = 10

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
class ResourceLinkListView(ListView):
    model = ResourceLink
    template_name = "kuai_club/resource_list.html" # Placeholder template
    context_object_name = "resources"
    queryset = ResourceLink.objects.all().order_by('category__order', 'title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_categories'] = ResourceLink.objects.values('category__name', 'category__order').distinct().order_by('category__order')
        return context

# Partner List View
class PartnerListView(ListView):
    model = Partner
    template_name = "kuai_club/partner_list.html" # Placeholder template
    context_object_name = "partners"
    queryset = Partner.objects.all().order_by('order', 'name')