from django.contrib import admin
from .models import (
    SiteConfig, AboutPageContent, Partner, ExecutivePosition,
    ExecutiveLeader, NewsPost, ClubEventType, ClubEvent,
    ResearchArea, ClubProject, Community, ResourceCategory,
    ResourceLink
)

# Register your models here.
admin.site.register(SiteConfig)
admin.site.register(AboutPageContent)
admin.site.register(Partner)
admin.site.register(ExecutivePosition)
admin.site.register(ExecutiveLeader)
admin.site.register(NewsPost)
admin.site.register(ClubEventType)
admin.site.register(ClubEvent)
admin.site.register(ResearchArea)
admin.site.register(ClubProject)
admin.site.register(Community)
admin.site.register(ResourceCategory)
admin.site.register(ResourceLink)