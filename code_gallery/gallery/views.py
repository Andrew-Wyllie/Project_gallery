from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, ProjectFile, ProjectFolder
from .forms import ProjectForm, ProjectFileForm, ProjectFolderForm

def home_view(request):
    # Reorganize the context to make template rendering easier
    context = {
        'categories': [
            {
                'key': category_key,
                'name': category_name,
                'projects': Project.objects.filter(category=category_key)
            }
            for category_key, category_name in Project.CATEGORY_CHOICES
        ]
    }
    return render(request, 'gallery/home.html', context)

#@login_required
def add_project(request):
    """
    View to add a new project
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'gallery/add_project.html', {'form': form})

def project_detail(request, pk):
    """
    Detailed view of a specific project
    """
    project = get_object_or_404(Project, pk=pk)
    
    # Get root-level files (not in any folder)
    root_files = project.files.filter(folder__isnull=True)
    
    # Get root-level folders (no parent folder)
    root_folders = project.folders.filter(parent_folder__isnull=True)
    
    context = {
        'project': project,
        'root_files': root_files,
        'root_folders': root_folders
    }
    return render(request, 'gallery/project_detail.html', context)

@login_required
def create_folder(request, project_pk):
    """
    View to create a new folder in a project
    """
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = ProjectFolderForm(request.POST, project=project)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.project = project
            folder.save()
            messages.success(request, f'Folder "{folder.name}" created successfully!')
            return redirect('project_detail', pk=project_pk)
    else:
        form = ProjectFolderForm(project=project)
    
    return render(request, 'gallery/create_folder.html', {
        'form': form,
        'project': project
    })

@login_required
def folder_detail(request, folder_pk):
    """
    View to display contents of a folder
    """
    folder = get_object_or_404(ProjectFolder, pk=folder_pk)
    project = folder.project
    
    # Get files in this folder
    files = folder.files.all()
    
    # Get subfolders
    subfolders = folder.subfolders.all()
    
    context = {
        'folder': folder,
        'project': project,
        'files': files,
        'subfolders': subfolders
    }
    return render(request, 'gallery/folder_detail.html', context)

@login_required
def upload_project_file(request, project_pk):
    """
    View to upload files to a specific project
    """
    project = get_object_or_404(Project, pk=project_pk)
    
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES, project=project)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.project = project
            file_instance.save()
            
            # Determine redirect based on whether file was added to a folder
            if file_instance.folder:
                messages.success(request, 'File uploaded successfully to folder!')
                return redirect('folder_detail', folder_pk=file_instance.folder.pk)
            else:
                messages.success(request, 'File uploaded successfully!')
                return redirect('project_detail', pk=project_pk)
    else:
        form = ProjectFileForm(project=project)
    
    return render(request, 'gallery/upload_file.html', {
        'form': form, 
        'project': project
    })