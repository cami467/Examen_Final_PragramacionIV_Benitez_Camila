# Gestión de Empresas — API Django + DRF

Resumen rápido
- API REST para gestionar empresas con Django + Django REST Framework.
- Rutas principales expuestas en `/api/empresas/`.

Requisitos
- Python 3.11+ (o 3.10+)

Instalación (entorno Windows - PowerShell)

1) Crear y activar virtualenv
```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

2) Instalar dependencias
```powershell
pip install django djangorestframework djangorestframework-authtoken django-filter corsheaders
```

3) Migraciones y usuario
```powershell
python gestion_empresas/manage.py makemigrations
python gestion_empresas/manage.py migrate
# (opcional) crear superuser interactivo
python gestion_empresas/manage.py createsuperuser
```

4) (Opcional) crear el usuario de prueba y token automáticamente
```powershell
python gestion_empresas/create_test_user.py
# Esto mostrará USER, PASSWORD y TOKEN
```

Ejecutar servidor
```powershell
python gestion_empresas/manage.py runserver
```

Endpoints y pruebas
- Admin: http://127.0.0.1:8000/admin/
- API base: http://127.0.0.1:8000/api/empresas/

Ejemplos curl
```bash
# Listar (usar el token generado)
curl -H "Authorization: Token <TU_TOKEN>" http://127.0.0.1:8000/api/empresas/

# Crear
curl -X POST -H "Authorization: Token <TU_TOKEN>" -H "Content-Type: application/json" \
  -d '{"ruc":"80012345-6","nombre":"ACME S.A.","sector":"Tecnología","email":"contacto@acme.com"}' \
  http://127.0.0.1:8000/api/empresas/

# Detalle
curl -H "Authorization: Token <TU_TOKEN>" http://127.0.0.1:8000/api/empresas/1/

# Patch
curl -X PATCH -H "Authorization: Token <TU_TOKEN>" -H "Content-Type: application/json" \
  -d '{"email":"nuevo@acme.com"}' http://127.0.0.1:8000/api/empresas/1/

# Delete (soft-delete)
curl -X DELETE -H "Authorization: Token <TU_TOKEN>" http://127.0.0.1:8000/api/empresas/1/
```

Notas y recomendaciones
- En `gestion_empresas/gestion_empresas/settings.py` ya habilité `CORS_ALLOW_ALL_ORIGINS` para desarrollo y `ALLOWED_HOSTS=['*']`.
- Hay scripts útiles ya creados: `gestion_empresas/create_test_user.py` (genera `testadmin` y token) y `gestion_empresas/test_client_api.py` (prueba endpoints usando Django Test Client).
- Para producción: ajustar `ALLOWED_HOSTS`, desactivar `DEBUG`, usar base de datos y servidor WSGI/ASGI apropiado.

Archivos relevantes
- [gestion_empresas/empresas/models.py](gestion_empresas/empresas/models.py)
- [gestion_empresas/empresas/serializers.py](gestion_empresas/empresas/serializers.py)
- [gestion_empresas/empresas/views.py](gestion_empresas/empresas/views.py)
- [gestion_empresas/empresas/urls.py](gestion_empresas/empresas/urls.py)

Si quieres, agrego:
- Documentación automática (Swagger/OpenAPI)
- Tests unitarios para serializer y viewset

Mejoras añadidas en este commit:
- Caching con Redis (fallback a memoria local si no hay REDIS_URL).
- Versionado de la API en `/api/v1/`.
- Documentación OpenAPI/Swagger disponible en `/api/schema/` y `/api/schema/swagger-ui/`.
- Throttling básico (Anon y User rate limits).
- Logging básico a consola.
- `Dockerfile` y `docker-compose.yml` con servicio `redis`.
- `requirements.txt` con dependencias sugeridas.
- Tests de integración en `empresas_tests/test_api.py`.

Cómo usar Docker (rápido):
```bash
docker compose up --build
```
La app quedará en http://127.0.0.1:8000/ y Redis disponible en el contenedor.
