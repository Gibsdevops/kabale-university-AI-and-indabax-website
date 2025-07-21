# kuai_club/urls.py

from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = 'kuai_club'  # Namespacing for this app

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # About
    # Corrected: 'about/' now redirects to the about_detail for ID 1.
    path('about/', lambda request: redirect('kuai_club:about_detail', page_id=1), name='about'),
    path('about/<int:page_id>/', views.about_detail, name='about_detail'),

    # Leaders
    # main leaders.
    path('leaders/', views.leaders_list_view, name='leaders_list'),
    # Individual Leader Detail Page (keep this if you want separate profiles)
    path('leaders/<int:pk>/', views.leader_detail, name='leader_detail'), 


    # News
    path('news/', views.news_list, name='news_list'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),

    # Events
    path('events/', views.event_list, name='event_list'), # New list view for all events
    path('events/<int:pk>/', views.event_detail, name='event_detail'), # Detail for single event
    path('api/events/', views.api_events, name='api_events'), # Keep your API endpoint

    # Projects
    path('projects/', views.project_list, name='project_list'), # New list view for all projects
    path('project/<slug:slug>/', views.project_detail, name='project_detail'), # Detail for single project
    path('api/projects/', views.api_projects, name='api_projects'), # Keep your API endpoint

    # Research
    path('research/', views.research_list, name='research_list'), # New list view for all research
    path('research/<int:pk>/', views.research_detail, name='research_detail'), # Detail for single research

    # Resources
    path('resources/', views.resource_list, name='resource_list'), # For resource_list.html
    path('resources/<slug:slug>/', views.resource_detail, name='resource_detail'), # For individual resource detail


    # Communities URL
    path('communities/', views.community_list, name='community_list'),
    #path('community_outreach/<int:page_id>/', views.community_page, name='community_page'), # Detail for single community outreach

    # Partners (assuming you have a Partner model)
    path('partners/', views.partner_list, name='partner_list'),
]