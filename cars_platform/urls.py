from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from vehicles.views import home, ExportCSVView, ExportPDFView
from api.views import generate_pdf
from accounts.views import register_view, home_view

urlpatterns = [
    path('', home, name='root'),  # 🚀 Root health check
    path('admin/', admin.site.urls),

    # 🧭 Frontend Views
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),

    # 📦 Modular API routing
    path('api/', include('api.urls')),
    path('api/', include('vehicles.urls')),
    path('api/', include('accounts.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('audit.urls')),

    # 📤 Secure Export Endpoints
    path('api/export/csv/', ExportCSVView.as_view(), name='export_csv'),
    path('api/export/pdf/', ExportPDFView.as_view(), name='export_pdf'),

    # 📤 Optional Legacy PDF Export
    path('export/pdf/', generate_pdf, name='generate_pdf'),
]

# 🖼️ Media file serving (for development only)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
