from django.db import models

#----home page: slider images ------
class EventImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='slider/')
    description = models.TextField(blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
# -------- Tutorials Page --------
class TutorialCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE)
    video_url = models.URLField()
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# -------- Leaders Page --------
class Leader(models.Model):
    POSITION_CHOICES = [
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Technical Lead', 'Technical Lead'),
        ('Treasurer', 'Treasurer'),
        ('Secretary', 'Secretary'),
        ('Graphics Designer Lead', 'Graphics Designer Lead'),
        ('Social Media Manager', 'Social Media Manager'),
        ('Event Manger', 'Event Manager'),
        ('Mobilizer', 'Mobilizer'),
        ('Year One Representative', 'Year One Representative'),
        ('Year Two Representative', 'Year Two Representative'),
        ('Presidential Advisor', 'Presidential Advisor'),
        
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    photo = models.ImageField(upload_to='leaders/')
    term_start = models.DateField()
    term_end = models.DateField(null=True, blank=True)

    def is_current(self):
        return self.term_end is None or self.term_end >= date.today()

    def __str__(self):
        return f"{self.name} ({self.position})"