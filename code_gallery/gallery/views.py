from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
#from .forms import ProjectForm, ProjectFileForm

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

# @login_required
# def add_project(request):
#     """
#     View to add a new project
#     """
#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         if form.is_valid():
#             project = form.save()
#             return redirect('project_detail', pk=project.pk)
#     else:
#         form = ProjectForm()
    
#     return render(request, 'gallery/add_project.html', {'form': form})

# def project_detail(request, pk):
#     """
#     Detailed view of a specific project
#     """
#     project = get_object_or_404(Project, pk=pk)
#     files = project.files.all()
    
#     context = {
#         'project': project,
#         'files': files
#     }
#     return render(request, 'gallery/project_detail.html', context)

# @login_required
# def upload_project_file(request, project_pk):
#     """
#     View to upload files to a specific project
#     """
#     project = get_object_or_404(Project, pk=project_pk)
    
#     if request.method == 'POST':
#         form = ProjectFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file_instance = form.save(commit=False)
#             file_instance.project = project
#             file_instance.save()
#             return redirect('project_detail', pk=project_pk)
#     else:
#         form = ProjectFileForm()
    
#     return render(request, 'gallery/upload_file.html', {
#         'form': form, 
#         'project': project
#     })