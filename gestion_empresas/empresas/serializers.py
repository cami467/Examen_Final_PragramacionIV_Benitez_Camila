from rest_framework import serializers
from .models import Empresa


class EmpresaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Empresa"""

    # Campo calculado (no existe en el modelo)
    antiguedad_dias = serializers.SerializerMethodField()

    class Meta:
        model = Empresa
        fields = [
            'id',
            'ruc',
            'nombre',
            'sector',
            'email',
            'telefono',
            'direccion',
            'activo',
            'created_at',
            'updated_at',
            'antiguedad_dias'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'email': {'required': True},
            'nombre': {'required': True},
            'ruc': {'required': True}
        }

    def get_antiguedad_dias(self, obj):
        """Calcula días desde la creación"""
        from django.utils import timezone
        delta = timezone.now() - obj.created_at
        return delta.days

    def validate_ruc(self, value):
        """Validación personalizada para RUC"""
        # Verificar formato básico
        if not value or len(value) < 10:
            raise serializers.ValidationError(
                "El RUC debe tener al menos 10 caracteres"
            )

        # Verificar que no exista (solo en creación)
        if not self.instance:  # Creación
            if Empresa.objects.filter(ruc=value, activo=True).exists():
                raise serializers.ValidationError(
                    "Ya existe una empresa activa con este RUC"
                )

        return value.upper()  # Normalizar a mayúsculas

    def validate_email(self, value):
        """Validación personalizada para email"""
        if not value:
            raise serializers.ValidationError(
                "El email es obligatorio"
            )
        return value.lower()  # Normalizar a minúsculas

    def validate(self, attrs):
        """Validaciones que involucran múltiples campos"""
        # Si la empresa está inactiva, verificar que tenga motivo
        if not attrs.get('activo', True):
            # Aquí podrías agregar lógica adicional
            pass

        return attrs


class EmpresaListSerializer(serializers.ModelSerializer):
    """Serializer ligero para listados"""

    class Meta:
        model = Empresa
        fields = ['id', 'ruc', 'nombre', 'sector', 'activo']
