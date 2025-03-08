from django import forms
from .models import Project, ProjectFile, ProjectFolder

class ProjectForm(forms.ModelForm):
    """
    Form for creating and editing projects
    """
    class Meta:
        model = Project
        fields = ['title', 'description', 'category', 'github_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProjectFolderForm(forms.ModelForm):
    """
    Form for creating folders within a project
    """
    class Meta:
        model = ProjectFolder
        fields = ['name', 'parent_folder']
        
    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            # Only show folders from the current project
            self.fields['parent_folder'].queryset = ProjectFolder.objects.filter(project=project)
            # Add an empty label for the parent folder dropdown
            self.fields['parent_folder'].empty_label = "No parent folder (root level)"

class ProjectFileForm(forms.ModelForm):
    """
    Form for uploading project files
    """
    class Meta:
        model = ProjectFile
        fields = ['file', 'description', 'folder']
        
    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            # Only show folders from the current project
            self.fields['folder'].queryset = ProjectFolder.objects.filter(project=project)
            # Add an empty label for the folder dropdown
            self.fields['folder'].empty_label = "No folder (project root)"