
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('warehouse.urls')),
    path('analytics/', include('analysis.urls')),
    path('delivery/', include('measures.urls')),
    path('units/',include('logistics.urls')),

]
