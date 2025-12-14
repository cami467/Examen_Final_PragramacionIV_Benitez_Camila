from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmpresaViewSet

# Crear router
router = DefaultRouter()
router.register(r'empresas', EmpresaViewSet, basename='empresa')

urlpatterns = [
    path('', include(router.urls)),
]
