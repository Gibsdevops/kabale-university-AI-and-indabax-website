from django.urls import path
from .views import HomePageView, AboutPageView, TutorialsPageView, LeadersPageView

app_name = 'indabax_app'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('tutorials/', TutorialsPageView.as_view(), name='tutorials'),
    path('leaders/', LeadersPageView.as_view(), name='leaders'),
]
