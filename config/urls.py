from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from leads.views import LoginView, login, logout_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('leads.urls')),
    path('login/', LoginView.as_view(), name="loginpage"),
    path('logout/', logout_view, name="logoutpage")
]

# This route is mandatory to access media folder from URL
if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
