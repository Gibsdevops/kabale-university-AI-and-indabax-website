from django.views.generic import TemplateView
from .models import EventImage, TutorialCategory, Leader, AboutContent
from datetime import date

class HomePageView(TemplateView):
    template_name = "indabax_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_images'] = EventImage.objects.all()
        return context

class AboutPageView(TemplateView):
    template_name = "indabax_app/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch the AboutContent. We'll assume there's only one.
        # Use .first() to avoid DoesNotExist error if no content exists yet.
        # Or .get() if you want to enforce one instance, but then handle the exception.
        about_content = AboutContent.objects.prefetch_related('objectives', 'affiliation_links').first()
        context['about_content'] = about_content
        return context

class TutorialsPageView(TemplateView):
    template_name = "indabax_app/tutorials.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = TutorialCategory.objects.prefetch_related('tutorial_set').all()
        context['categories'] = categories
        return context

class LeadersPageView(TemplateView):
    template_name = "indabax_app/leaders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        context['current_leaders'] = Leader.objects.filter(term_end__isnull=True) | Leader.objects.filter(term_end__gte=today)
        context['past_leaders'] = Leader.objects.filter(term_end__lt=today)
        return context
