from django.contrib import admin
from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    """Configuración del admin para Empresa"""

    list_display = [
        'ruc',
        'nombre',
        'sector',
        'email',
        'activo',
        'created_at'
    ]

    list_filter = ['activo', 'sector', 'created_at']

    search_fields = ['ruc', 'nombre', 'email']

    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Información Básica', {
            'fields': ('ruc', 'nombre', 'sector')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono', 'direccion')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activar_empresas', 'desactivar_empresas']

    def activar_empresas(self, request, queryset):
        updated = queryset.update(activo=True)
        self.message_user(
            request,
            f'{updated} empresas activadas correctamente'
        )
    activar_empresas.short_description = "Activar empresas seleccionadas"

    def desactivar_empresas(self, request, queryset):
        updated = queryset.update(activo=False)
        self.message_user(
            request,
            f'{updated} empresas desactivadas correctamente'
        )
    desactivar_empresas.short_description = "Desactivar empresas"
