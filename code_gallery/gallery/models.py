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
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class ProjectFolder(models.Model):
    """
    Model to represent folders within a project
    """
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='folders')
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'project', 'parent_folder')
        ordering = ['name']

class ProjectFile(models.Model):
    """
    Model of each file within a project or folder
    """
    file = models.FileField(upload_to='project_files/')
    description = models.TextField(blank=True)
    filename = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    folder = models.ForeignKey(ProjectFolder, on_delete=models.CASCADE, null=True, blank=True, related_name='files')
    upload_date = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField(default=0)  # Size in bytes
    
    def __str__(self):
        return self.filename
    
    def save(self, *args, **kwargs):
        # Auto-set filename from the uploaded file if not provided
        if not self.filename and self.file:
            self.filename = self.file.name.split('/')[-1]
        
        # Set file size if file is present
        if self.file and hasattr(self.file, 'size'):
            self.file_size = self.file.size
            
        super().save(*args, **kwargs)