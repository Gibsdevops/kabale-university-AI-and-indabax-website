from django.urls import path
from .views import (HomePageView, AboutPageView, TutorialsPageView, 
                   LeadersPageView, AllLeadersPageView, PhotosView, 
                   SessionsListView)  # Add SessionsListView import
from . import views

app_name = 'indabax_app'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('tutorials/', TutorialsPageView.as_view(), name='tutorials'),
    path('leaders/', LeadersPageView.as_view(), name='leaders'),
    path('leaders/all/', AllLeadersPageView.as_view(), name='all_leaders'),
    path('photos/', PhotosView.as_view(), name='photos'),
    path('sessions/', SessionsListView.as_view(), name='sessions'),  # ADD THIS LINE
    path('search/', views.search, name='search'),
    path('sessions/<int:pk>/', views.session_detail, name='session_detail'),
]