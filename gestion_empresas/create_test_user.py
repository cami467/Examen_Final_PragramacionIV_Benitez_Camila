import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_empresas.settings')
import django
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

username = 'testadmin'
password = 'TestPass123'
email = 'admin@example.com'

u, created = User.objects.get_or_create(username=username, defaults={'email': email})
if created:
    u.set_password(password)
    u.is_staff = True
    u.is_superuser = True
    u.save()

token, _ = Token.objects.get_or_create(user=u)
print('USER:', username)
print('PASSWORD:', password)
print('TOKEN:', token.key)
