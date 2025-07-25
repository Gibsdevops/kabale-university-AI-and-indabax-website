

from django.views.generic import TemplateView
from .models import EventImage, TutorialCategory, Leader, AboutContent, HomePageContent, Pillar, Event, Partner, GalleryImage, HeroBackgroundImage# Ensure GalleryImage is imported
from datetime import date
from django.db.models import Q
import json


class HomePageView(TemplateView):
    template_name = 'indabax_app/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- Data for the NEW Hero/Gallery Slider (top of the page) ---
        context['hero_slider_images'] = GalleryImage.objects.all().order_by('order') 

        # For the general home page content (main heading, about initiative, CTA)
        context['home_content'] = HomePageContent.objects.first() # Assuming only one instance
        

        hero_background_images = HeroBackgroundImage.objects.filter(is_active=True).order_by('order')
        context['hero_background_images'] = hero_background_images

        # Prepare a JSON list of URLs for JavaScript
        background_urls = [img.image.url for img in hero_background_images]
        context['hero_background_urls_json'] = json.dumps(background_urls)

        # For the Core Pillars section
        context['pillars'] = Pillar.objects.all()

        # --- Data for the Events Carousel (within Upcoming Events section) ---
        # These are your actual event listings, which will now be displayed in a carousel.
        today = date.today()
        context['upcoming_events'] = Event.objects.filter(date__gte=today).order_by('date')
        context['past_events'] = Event.objects.filter(date__lt=today).order_by('-date')

        # For Partners
        context['partners'] = Partner.objects.all()

        return context
    

class AboutPageView(TemplateView):
    template_name = "indabax_app/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        context['current_leaders'] = Leader.objects.filter(Q(term_end__isnull=True) | Q(term_end__gte=today))
        context['past_leaders'] = Leader.objects.filter(term_end__lt=today)
        return context