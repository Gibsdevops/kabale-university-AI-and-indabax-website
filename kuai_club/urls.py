from django.urls import path
from . import views

app_name = 'kuai_club'  # Namespacing for this app

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # About    
    path('about/', views.AboutView.as_view(), name='about'),
    path('previous-leaders/<str:category>/', views.previous_leaders_by_category, name='previous_leaders'),
    path('leaders/previous/<str:category>/', views.previous_leaders_by_category, name='previous_leaders_by_category'),
    path('leaders/current/<str:category>/', views.current_leaders_by_category, name='current_leaders_by_category'),
    
    # Events
    path('event/<int:page_id>/', views.event_page, name='event_page'),
    path('api/events/', views.api_events, name='api_events'),
    
    # Projects - Multiple URL patterns for flexibility
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('project/<int:page_id>/', views.project_page, name='project_page'),  # This is what your template expects
    path('projects/id/<int:page_id>/', views.project_page, name='project_page_by_id'),  # Alternative pattern
    path('api/projects/', views.api_projects, name='api_projects'),
    
    # Research
    path('research/<int:page_id>/', views.research_page, name='research_page'),
    
    # Resources
    path('resources/<int:page_id>/', views.resource_page, name='resource_page'),
    
    # Community Outreach
    path('community/<int:page_id>/', views.community_page, name='community_page'),
    
    path('join/submit/', views.join_club_submit, name='join_club_submit'),
]