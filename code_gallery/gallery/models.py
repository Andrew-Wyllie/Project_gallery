from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    """
    Model to represent individual coding projects
    """
    CATEGORY_CHOICES = [
        ('python', 'Python'),
        ('java', 'Java'),
        ('web', 'Web Development'),
        ('c', 'C'),
        ('other', 'Other')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    github_link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title

# class Project(models.Model):
#     CATEGORY_CHOICES = [
#         ('web', 'Web Development'),
#         ('data', 'Data Science'),
#         ('mobile', 'Mobile Development'),
#         ('backend', 'Backend Engineering'),
#         ('frontend', 'Frontend Development'),
#         ('other', 'Other')
#     ]

#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
#     github_link = models.URLField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.title