"""
URL configuration for web_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# web_app/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import home, select_medications, report_side_effects, show_side_effects, analysis_report_symptoms

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='custom_login'),
    path('select-medications/', select_medications, name='select_medications'),
    path('show-side-effects/', show_side_effects, name='show_side_effects'),
    path('report-side-effects/', report_side_effects, name='report_side_effects'),
    path('admin/', admin.site.urls),
    path('analysis_report_symptoms/', analysis_report_symptoms, name='analysis_report_symptoms'),
    # ...
]