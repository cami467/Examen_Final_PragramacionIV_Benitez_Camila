from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Empresa
from .serializers import EmpresaSerializer, EmpresaListSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class EmpresaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de Empresas
    """

    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]

    # Filtros, búsqueda y ordenación
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Campos por los que se puede filtrar
    filterset_fields = ['sector', 'activo']

    # Campos en los que se puede buscar
    search_fields = ['nombre', 'ruc', 'email']

    # Campos por los que se puede ordenar
    ordering_fields = ['nombre', 'created_at', 'ruc']
    ordering = ['-created_at']  # Orden por defecto

    def get_serializer_class(self):
        """Usar serializer ligero para listados"""
        if self.action == 'list':
            return EmpresaListSerializer
        return EmpresaSerializer

    @method_decorator(cache_page(60*10), name='list')
    def list(self, *args, **kwargs):
        """List view cached for 10 minutes in production when cache is configured."""
        return super().list(*args, **kwargs)

    def get_permissions(self):
        """
        Define permisos por acción:
        - list, retrieve: Usuarios autenticados
        - create, update, destroy: Solo admin
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        """Soft delete en lugar de eliminar"""
        instance.activo = False
        instance.save()

    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Endpoint personalizado: retorna solo empresas activas"""
        empresas = self.queryset.filter(activo=True)
        serializer = self.get_serializer(empresas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activa una empresa"""
        empresa = self.get_object()
        empresa.activo = True
        empresa.save()
        serializer = self.get_serializer(empresa)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Retorna estadísticas generales"""
        from django.db.models import Count

        stats = {
            'total': self.queryset.count(),
            'activas': self.queryset.filter(activo=True).count(),
            'inactivas': self.queryset.filter(activo=False).count(),
            'por_sector': list(
                self.queryset.values('sector')
                .annotate(cantidad=Count('id'))
                .order_by('-cantidad')
            )
        }

        return Response(stats)
