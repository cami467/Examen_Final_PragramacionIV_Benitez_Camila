import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_empresas.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json


u, created = User.objects.get_or_create(username='testadmin', defaults={'email':'admin@example.com'})
if created:
    u.set_password('TestPass123')
    u.is_staff = True
    u.is_superuser = True
    u.save()

token, _ = Token.objects.get_or_create(user=u)
print('Using token:', token.key)

client = Client(HTTP_AUTHORIZATION=f'Token {token.key}')

def show(resp):
    print('Status:', resp.status_code)
    try:
        print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
    except Exception:
        print(resp.content)


print('\nGET /api/empresas/')
show(client.get('/api/empresas/'))

print('\nPOST /api/empresas/')
new = {
    'ruc': '80012345-6',
    'nombre': 'ACME S.A.',
    'sector': 'Tecnología',
    'email': 'contacto@acme.com',
    'telefono': '+595 21 123456',
    'direccion': 'Av. Principal 123, Asunción'
}
resp = client.post('/api/empresas/', data=json.dumps(new), content_type='application/json')
show(resp)

if resp.status_code in (200,201):
    obj = resp.json()
    pk = obj.get('id')
    print(f'\nGET /api/empresas/{pk}/')
    show(client.get(f'/api/empresas/{pk}/'))

    print(f'\nPATCH /api/empresas/{pk}/')
    patch = {'email':'nuevo@acme.com','telefono':'+595 21 999888'}
    show(client.patch(f'/api/empresas/{pk}/', data=json.dumps(patch), content_type='application/json'))

    print(f'\nDELETE /api/empresas/{pk}/')
    show(client.delete(f'/api/empresas/{pk}/'))
