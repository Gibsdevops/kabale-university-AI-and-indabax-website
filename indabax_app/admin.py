from django.contrib import admin
from .models import EventImage, TutorialCategory, Tutorial, Leader

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_uploaded')
    search_fields = ('title',)

@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_posted')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Leader)
class LeaderAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'term_start', 'term_end')
    list_filter = ('position',)
    search_fields = ('name',)
