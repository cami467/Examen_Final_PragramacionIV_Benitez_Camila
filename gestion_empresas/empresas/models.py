from django.db import models
from django.core.validators import EmailValidator, RegexValidator


class Empresa(models.Model):
    """Modelo para gestionar empresas"""

    # Validador personalizado para RUC paraguayo
    ruc_validator = RegexValidator(
        regex=r'^\d{8}-\d{1}$',
        message='El RUC debe tener formato: 12345678-9'
    )

    ruc = models.CharField(
        max_length=20,
        unique=True,
        validators=[ruc_validator],
        help_text='RUC de la empresa (formato: 12345678-9)'
    )
    nombre = models.CharField(
        max_length=200,
        help_text='Nombre o razón social de la empresa'
    )
    sector = models.CharField(
        max_length=100,
        help_text='Sector económico (ej: Tecnología, Retail)'
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        help_text='Email de contacto'
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Teléfono de contacto'
    )
    direccion = models.TextField(
        blank=True,
        null=True,
        help_text='Dirección física'
    )
    activo = models.BooleanField(
        default=True,
        help_text='Indica si la empresa está activa'
    )

    # Timestamps automáticos
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha de creación del registro'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Fecha de última actualización'
    )

    class Meta:
        ordering = ['-created_at']  # Ordenar por más reciente
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        indexes = [
            models.Index(fields=['ruc']),
            models.Index(fields=['nombre']),
            models.Index(fields=['activo']),
        ]

    def __str__(self):
        return f"{self.nombre} ({self.ruc})"

    def clean(self):
        """Validaciones adicionales a nivel de modelo"""
        from django.core.exceptions import ValidationError

        # Validar que empresas activas tengan RUC único
        if self.activo:
            exists = Empresa.objects.filter(
                ruc=self.ruc,
                activo=True
            ).exclude(pk=self.pk).exists()

            if exists:
                raise ValidationError(
                    'Ya existe una empresa activa con este RUC'
                )
