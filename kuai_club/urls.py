from django.urls import path
from . import views

app_name = 'kuai_club' # Namespacing for this app

urlpatterns = [
    # Main website pages
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'), # Using PK for simplicity for now
    path('research-areas/', views.ResearchAreaListView.as_view(), name='research_area_list'),
    path('research-areas/<slug:slug>/', views.ResearchAreaDetailView.as_view(), name='research_area_detail'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'), # Using PK for simplicity for now
    path('leaders/', views.ExecutiveLeaderListView.as_view(), name='executive_leaders'),
    path('communities/', views.CommunityListView.as_view(), name='community_list'),
    path('resources/', views.ResourceLinkListView.as_view(), name='resource_list'),
    path('partners/', views.PartnerListView.as_view(), name='partner_list'),
]