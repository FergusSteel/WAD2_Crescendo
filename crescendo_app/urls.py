"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from crescendo_app import views

app_name = 'crescendo'

urlpatterns = [
    # Add URL Paths, Uncomment as Views and Templates are implemented. (Make sure name parameter matches view's name)

    # Home Page
    path('', views.index, name='index'),
    #path('register/', views.register, name='register'),
    #path('login/', views.login, name='login'),
    #path('about/', views.about, name='about'),
    #path('contactUs/', views.contactUs, name='contactUs')

]
