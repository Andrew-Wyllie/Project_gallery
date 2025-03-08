from django import forms
from .models import Project, ProjectFile

# class ProjectForm(forms.ModelForm):
#     """
#     Form for creating and editing projects
#     """
#     class Meta:
#         model = Project
#         fields = ['title', 'description', 'category', 'github_link']
#         widgets = {
#             'description': forms.Textarea(attrs={'rows': 4}),
#         }

# class ProjectFileForm(forms.ModelForm):
#     """
#     Form for uploading project files
#     """
#     class Meta:
#         model = ProjectFile
#         fields = ['file', 'description']