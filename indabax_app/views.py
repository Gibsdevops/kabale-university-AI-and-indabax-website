from django.views.generic import TemplateView
from .models import EventImage, TutorialCategory, Leader
from datetime import date

class HomePageView(TemplateView):
    template_name = "indabax_app/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider_images'] = EventImage.objects.all()
        return context

class AboutPageView(TemplateView):
    template_name = "indabax_app/about.html"

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
