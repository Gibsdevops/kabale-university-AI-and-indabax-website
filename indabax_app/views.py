

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
                     HeroBackgroundImage,
                     Session,
                     SessionImage)


from datetime import date
from django.db.models import Q
import json
from django.shortcuts import render, get_object_or_404
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

        # --- NEW: Data for Latest Session Highlights --- #
        # Fetch a few recent local session images for the homepage
        # We order by uploaded_at to get the very latest individual images
        context['recent_session_images'] = SessionImage.objects.filter(
            session__is_published=True
        ).order_by('-uploaded_at')[:6] # Get the last 6 images

        # You might also want to display recent sessions if you prefer to link to sessions directly
        context['recent_sessions'] = Session.objects.filter(is_published=True).order_by('-session_date')[:3] # Get last 3 sessions

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
    model = Album # This view primarily handles Google Photo Albums
    template_name = 'indabax_app/photos.html'
    context_object_name = 'albums' # For Google Photo Albums

    def get_queryset(self):
        """
        Returns all published Google Photo Albums.
        """
        return Album.objects.filter(is_published=True).order_by('-id')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Add local sessions to the context
        context['sessions'] = Session.objects.filter(is_published=True).order_by('-session_date')
        return context
    
class SessionsListView(ListView):
    model = Session
    template_name = 'indabax_app/sessions.html'
    context_object_name = 'sessions'
    paginate_by = 10  # Optional: Add pagination

    def get_queryset(self):
        """
        Returns all published sessions, ordered by date (most recent first).
        """
        return Session.objects.filter(is_published=True).order_by('-session_date')
    
def session_detail(request, pk):
    session = get_object_or_404(Session, pk=pk)
    images = session.images.all() # Fetch related images

    # --- NEW LOGIC TO COMBINE SPEAKERS ---
    combined_speakers = []

    # 1. Add selected Leaders from the ManyToMany field
    for leader in session.speakers.all().order_by('name'): # Order them by name for consistent display
        combined_speakers.append({
            'type': 'leader',
            'obj': leader
        })

    # 2. Add guest speakers from the TextField
    if session.guest_speakers_info:
        # Split by newlines, strip whitespace, and filter out empty lines
        guest_lines = [line.strip() for line in session.guest_speakers_info.splitlines() if line.strip()]
        for guest_name in guest_lines:
            combined_speakers.append({
                'type': 'guest',
                'name': guest_name
            })
    # --- END NEW LOGIC ---

    context = {
        'session': session,
        'images': images,
        'combined_speakers': combined_speakers, # Pass the combined list to the template
    }
    return render(request, 'indabax_app/session_detail.html', context)


def search(request):
    query = request.GET.get('q')
    all_results = []

    if query:
        # Search the Leader model for matching names and positions
        leader_results = Leader.objects.filter(
            Q(name__icontains=query) | Q(position__icontains=query)
        )
        
        # Search the Album model for matching titles and descriptions
        album_results = Album.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        # Add this to your search function
        session_results = Session.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

            # Then add to your all_results
        all_results = list(leader_results) + list(album_results) + list(session_results)
    context = {
        'query': query,
        'results': all_results
    }
    return render(request, 'indabax_app/search_results.html', context)