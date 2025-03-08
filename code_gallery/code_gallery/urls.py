"""
URL configuration for code_gallery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from gallery import views  # Import views directly from the gallery app

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', views.home_view, name='home'),
    
    # Project-related URLs
    #path('project/add/', views.add_project, name='add_project'),
    #path('project/<int:pk>/', views.project_detail, name='project_detail'),
    
    # File upload URLs
    #path('project/<int:project_pk>/upload/', 
     #    views.upload_project_file, 
      #   name='upload_project_file'),
]

# Add media file serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)