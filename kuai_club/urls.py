from django.urls import path
from . import views

app_name = 'kuai_club' # Namespacing for this app

urlpatterns = [
    
    # Home
    path('', views.home, name='home'),

    # About
    path('about/', views.about_pages_processor, name='about_pages_processor'),
    path('about/<int:page_id>/', views.about_detail, name='about_detail'),

    # Leaders
    path('leaders/category/<str:category>/', views.leaders_by_category, name='leaders_by_category'),
    path('leader/<int:leader_id>/', views.leader_detail, name='leader_detail'),

    # News detail page
    path('news/<int:page_id>/', views.news_page, name='news_page'),


    # Event 
    path('event/<int:page_id>/', views.event_page, name='event_page'),

    # Research
    path('research/<int:page_id>/', views.research_page, name='research_page'),

    # Resources
    path('resources/<int:page_id>/', views.resource_page, name='resource_page'),


    # Community
    path('community/<int:page_id>/', views.community_page, name='community_page'),

    # Projects
    path('projects/<int:page_id>/', views.project_page, name='project_page'),

    
]