from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('apps.authentication.urls')),
    # All authentication URLs start with /api/auth/
    # include() pulls in all urls from our authentication app
]
