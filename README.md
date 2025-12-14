# Gestión de Empresas — API Django + DRF

## Descripción
Proyecto API REST para gestionar el catálogo de empresas: creación, lectura, actualización y baja lógica (soft-delete).
Es un ejercicio/plantilla para proyectos Django + DRF con buenas prácticas: autenticación por token, paginación, filtros, documentación OpenAPI y despliegue en contenedores.

## Características principales
- CRUD completo para `Empresa` con validaciones (RUC, email, unicidad).
- Baja lógica: los borrados marcan la empresa como inactiva (`activo=False`).
- Filtros por `sector`, búsqueda por `nombre`/`ruc`, ordenamiento y paginación.
- Autenticación por token (DRF TokenAuth) y permisos por rol (administradores para operaciones peligrosas).
- Cache en listados con Redis (fallback a memoria local si no hay Redis), throttling básico y logging de consola.
- Documentación OpenAPI con Swagger UI.

## Tecnologías y dependencias
- Python 3.10+ / 3.11+
- Django
- Django REST Framework (DRF)
- `rest_framework.authtoken` (Token Auth)
- `django-filter`
- `drf-spectacular` (OpenAPI / Swagger)
- `django-cors-headers`
- `django-redis` + `redis` (caching)
- Docker / docker-compose
- Gunicorn (producción)

## Requisitos
- `python` y `pip`

## Instalación rápida (Windows - PowerShell)
1) Crear y activar virtualenv
```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

2) Instalar dependencias
```powershell
pip install -r requirements.txt
```

3) Migraciones y (opcional) superuser
```powershell
python gestion_empresas/manage.py makemigrations
python gestion_empresas/manage.py migrate
python gestion_empresas/manage.py createsuperuser
```

4) (Opcional) crear usuario de prueba y token
```powershell
python gestion_empresas/create_test_user.py
# Muestra credenciales de prueba (dev).
```

## Ejecutar servidor (desarrollo)
```powershell
python gestion_empresas/manage.py runserver
```

## Credenciales de ejemplo (entorno de desarrollo)
- Usuario: `testadmin`
- Contraseña: `TestPass123`
- Para obtener/regenear el token ejecuta `python gestion_empresas/create_test_user.py`.

## Rutas importantes
- Admin: http://127.0.0.1:8000/admin/
- API (versionada): http://127.0.0.1:8000/api/v1/empresas/
- OpenAPI JSON: http://127.0.0.1:8000/api/schema/
- Swagger UI: http://127.0.0.1:8000/api/schema/swagger-ui/

## Ejemplos rápidos (usar Token en `Authorization: Token <TU_TOKEN>`)
```bash
# Listar
curl -H "Authorization: Token <TU_TOKEN>" http://127.0.0.1:8000/api/v1/empresas/

# Crear
curl -X POST -H "Authorization: Token <TU_TOKEN>" -H "Content-Type: application/json" \
  -d '{"ruc":"80012345-6","nombre":"ACME S.A.","sector":"Tecnología","email":"contacto@acme.com"}' \
  http://127.0.0.1:8000/api/v1/empresas/

# Detalle
curl -H "Authorization: Token <TU_TOKEN>" http://127.0.0.1:8000/api/v1/empresas/1/

# Patch
curl -X PATCH -H "Authorization: Token <TU_TOKEN>" -H "Content-Type: application/json" \
  -d '{"email":"nuevo@acme.com"}' http://127.0.0.1:8000/api/v1/empresas/1/

# Delete (soft-delete)
curl -X DELETE -H "Authorization: Token <TU_TOKEN>" http://127.0.0.1:8000/api/v1/empresas/1/
```

## Archivos clave
- `gestion_empresas/empresas/models.py`
- `gestion_empresas/empresas/serializers.py`
- `gestion_empresas/empresas/views.py`
- `gestion_empresas/empresas/urls.py`

## Tests
- Tests de integración básicos en `empresas_tests/test_api.py`.
- Ejecutar tests:
```bash
python gestion_empresas/manage.py test
```

## Docker (local)
- Levantar con Redis y la app:
```bash
docker compose up --build
```

## Mejoras implementadas
- Caching con Redis (fallback a memoria local si no hay `REDIS_URL`).
- Versionado de la API en `/api/v1/`.
- Documentación OpenAPI/Swagger disponible en `/api/schema/` y `/api/schema/swagger-ui/`.
- Throttling básico (Anon y User rate limits).
- Logging básico a consola.
- `Dockerfile` y `docker-compose.yml` con servicio `redis`.
- `requirements.txt` con dependencias recomendadas.
- Tests de integración básicos.

La app quedará en http://127.0.0.1:8000/ y Redis disponible en el contenedor.
