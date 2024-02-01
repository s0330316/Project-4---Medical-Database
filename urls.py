# project_name/urls.py

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('web_app/', include('web_app.urls')),  # 'web_app' ist der Name deiner App
    # Füge andere URLs hinzu, falls erforderlich
]
