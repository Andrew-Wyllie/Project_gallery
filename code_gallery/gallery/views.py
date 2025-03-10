from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, ProjectFile, ProjectFolder
from .forms import ProjectWithFolderForm

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

@login_required
def add_project(request):
    """
    View to add a new project with options to create a folder or upload a folder
    """
    if request.method == 'POST':
        form = ProjectWithFolderForm(request.POST)
        
        # Check if we're uploading a folder - handle differently
        if 'upload_folder' in request.POST and request.POST.get('upload_folder') == 'on':
            # Create the project first
            project = Project(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                category=request.POST.get('category'),
                github_link=request.POST.get('github_link') or None
            )
            
            if 'image' in request.FILES:
                project.image = request.FILES['image']
            
            project.save()
            
            # Process folder upload similar to your upload_project_folder view
            folder_name = request.POST.get('root_folder_name')
            if not folder_name:
                messages.error(request, 'Folder name is required')
                return redirect('project_detail', pk=project.pk)
                
            # Create the top-level folder
            parent_folder = ProjectFolder.objects.create(
                name=folder_name,
                project=project,
                parent_folder=None  # This is a root-level folder
            )
            
            # Process all files
            file_count = 0
            for key in request.POST:
                if key.startswith('path_'):
                    index = key.split('_')[1]
                    file_path = request.POST.get(key)
                    file_obj = request.FILES.get(f'file_{index}')
                    
                    if file_obj and file_path:
                        # Split the path to get folder structure
                        path_parts = file_path.split('/')
                        
                        # Skip the top-level folder name as we've already created it
                        path_parts = path_parts[1:]
                        
                        # If there are subfolders in the path
                        current_folder = parent_folder
                        
                        # Process any folders in the path
                        if len(path_parts) > 1:  # More than just the filename
                            for i in range(len(path_parts) - 1):  # Exclude the filename
                                subfolder_name = path_parts[i]
                                
                                # Check if this subfolder already exists
                                subfolder, created = ProjectFolder.objects.get_or_create(
                                    name=subfolder_name,
                                    project=project,
                                    parent_folder=current_folder
                                )
                                current_folder = subfolder
                        
                        # Now we have the correct folder, create the file
                        filename = path_parts[-1]  # The last part is the filename
                        
                        # Create the file in the database
                        project_file = ProjectFile(
                            project=project,
                            folder=current_folder,
                            filename=filename,
                            file=file_obj
                        )
                        project_file.save()
                        file_count += 1
            
            messages.success(request, f'Project created with folder upload containing {file_count} files!')
            return redirect('project_detail', pk=project.pk)
            
        # Handle regular form submission
        elif form.is_valid():
            # Create the project
            project = Project(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                category=form.cleaned_data['category'],
                github_link=form.cleaned_data['github_link']
            )
            project.save()
            
            # Check if we need to create a folder
            if form.cleaned_data['create_folder']:
                folder = ProjectFolder(
                    name=form.cleaned_data['folder_name'],
                    project=project,
                    parent_folder=None  # Root-level folder
                )
                folder.save()
                messages.success(request, f'Project created with root folder "{folder.name}"')
            else:
                messages.success(request, 'Project created successfully')
                
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectWithFolderForm()
    
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

import os
import zipfile
from django.http import HttpResponse, FileResponse
from wsgiref.util import FileWrapper
from io import BytesIO
import tempfile
import shutil
from pathlib import Path

def download_folder(request, folder_pk):
    """
    Download a folder as a ZIP file
    """
    folder = get_object_or_404(ProjectFolder, pk=folder_pk)
    
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create a zip file in the buffer
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Function to add files recursively
        def add_folder_to_zip(current_folder, path=""):
            # Add files in this folder
            for file in current_folder.files.all():
                file_path = os.path.join(path, file.filename)
                zip_file.writestr(file_path, file.file.read())
            
            # Add subfolders recursively
            for subfolder in current_folder.subfolders.all():
                subfolder_path = os.path.join(path, subfolder.name)
                add_folder_to_zip(subfolder, subfolder_path)
        
        # Start adding files from the root folder
        add_folder_to_zip(folder, folder.name)
    
    # Reset the buffer position to the beginning
    buffer.seek(0)
    
    # Create the HTTP response with the ZIP file
    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{folder.name}.zip"'
    
    return response

def download_project(request, project_pk):
    """
    Download entire project as a ZIP file
    """
    project = get_object_or_404(Project, pk=project_pk)
    
    # Create a BytesIO buffer
    buffer = BytesIO()
    
    # Create a zip file in the buffer
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add root-level files
        for file in project.files.filter(folder__isnull=True):
            zip_file.writestr(file.filename, file.file.read())
        
        # Function to add folders recursively
        def add_folder_to_zip(folder, path=""):
            # Add files in this folder
            for file in folder.files.all():
                file_path = os.path.join(path, file.filename)
                zip_file.writestr(file_path, file.file.read())
            
            # Add subfolders recursively
            for subfolder in folder.subfolders.all():
                subfolder_path = os.path.join(path, subfolder.name)
                add_folder_to_zip(subfolder, subfolder_path)
        
        # Add all root-level folders
        for folder in project.folders.filter(parent_folder__isnull=True):
            add_folder_to_zip(folder, folder.name)
    
    # Reset the buffer position to the beginning
    buffer.seek(0)
    
    # Create the HTTP response with the ZIP file
    response = HttpResponse(buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{project.title.replace(" ", "_")}_project.zip"'
    
    return response


def folder_detail(request, folder_pk):
    """
    Detailed view of a specific folder
    """
    folder = get_object_or_404(ProjectFolder, pk=folder_pk)
    
    # Get files in this folder
    files = folder.files.all()
    
    # Get subfolders
    subfolders = folder.subfolders.all()
    
    context = {
        'folder': folder,
        'project': folder.project,
        'files': files,
        'subfolders': subfolders
    }
    return render(request, 'gallery/folder_detail.html', context)