from django import forms
from .models import Project

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

class ProjectWithFolderForm(forms.Form):
    # Project fields
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    category = forms.ChoiceField(choices=Project.CATEGORY_CHOICES)
    github_link = forms.URLField(required=False)
    image = forms.ImageField(required=False)
    
    # Folder fields
    create_folder = forms.BooleanField(required=False, initial=False, 
                                      label="Create a root folder for this project")
    folder_name = forms.CharField(max_length=100, required=False, 
                                 label="Folder name (if creating a folder)")
    
    # Folder upload option
    upload_folder = forms.BooleanField(required=False, initial=False,
                                      label="Upload an existing folder")
    
    def clean(self):
        cleaned_data = super().clean()
        create_folder = cleaned_data.get('create_folder')
        folder_name = cleaned_data.get('folder_name')
        upload_folder = cleaned_data.get('upload_folder')
        
        if create_folder and upload_folder:
            raise forms.ValidationError(
                "You can either create a new folder or upload an existing one, not both."
            )
        
        if create_folder and not folder_name:
            raise forms.ValidationError(
                "Folder name is required when creating a folder."
            )
        
        return cleaned_data