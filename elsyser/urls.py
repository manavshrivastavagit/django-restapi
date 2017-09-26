from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^api/', include('elsyser.api')),
    url(r'^', include('django.contrib.auth.urls')),  # These urls are imported in order to make password reset work
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
