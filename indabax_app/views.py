

from django.views.generic import TemplateView
from .models import (EventImage, 
                     TutorialCategory, 
                     Leader, 
                     AboutContent, 
                     HomePageContent, 
                     Pillar, 
                     Event, 
                     Partner, 
                     GalleryImage, 
                     Album,
                     HeroBackgroundImage)# Ensure GalleryImage is imported
from datetime import date
from django.db.models import Q
import json
from django.views.generic import ListView


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
        #fetch only three pst_events
        past_events = Event.objects.filter(date__lt=date.today()).order_by('-date')[:4]
        context['past_events'] = past_events

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
        
        # Get only the top 4 current leaders for the main leaders page
        context['current_leaders'] = Leader.objects.filter(is_current=True).order_by('position')
        
        # Get only the top 4 past leaders for the main leaders page
        context['past_leaders'] = Leader.objects.filter(is_current=False).order_by('-term_start')[:6]
        
        return context

class AllLeadersPageView(TemplateView):
    template_name = "indabax_app/all_leaders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all leaders for the dedicated page, sorted by current and then position
        context['all_leaders'] = Leader.objects.all().order_by('-is_current', 'position')
        
        return context
    

class PhotosView(ListView):
    # This specifies the model to retrieve a list of objects from.
    model = Album

    # This tells the view which template to render.
    template_name = 'indabax_app/photos.html'

    # This sets the name of the context variable in the template.
    # The template will receive a list of albums under the name 'albums'.
    context_object_name = 'albums'
    
    # This method is used to specify the queryset (the list of objects)
    # that should be passed to the template. We use it to filter and order the albums.
    def get_queryset(self):
        """
        Returns all published albums, ordered from newest to oldest.
        """
        return Album.objects.filter(is_published=True).order_by('-id')
