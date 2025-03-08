from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from gallery import views  # Import views directly from the gallery app

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', views.home_view, name='home'),
    
    # Project-related URLs
    path('project/add_project/', views.add_project, name='add_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    
    # Folder management URLs
    path('project/<int:project_pk>/create-folder/', views.create_folder, name='create_folder'),
    path('folder/<int:folder_pk>/', views.folder_detail, name='folder_detail'),
    
    # File upload URLs
    path('project/<int:project_pk>/upload/', views.upload_project_file, name='upload_project_file'),

    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='gallery/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

# Add media file serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)