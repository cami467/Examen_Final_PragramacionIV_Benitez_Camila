from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class EmpresaAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('tester', 't@example.com', 'pass1234')
        self.user.is_staff = True
        self.user.save()
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_and_retrieve_empresa(self):
        url = '/api/v1/empresas/'
        data = {
            'ruc': '80099999-1',
            'nombre': 'Prueba S.A.',
            'sector': 'Test',
            'email': 'p@t.com'
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, 201)
        obj = resp.json()
        pk = obj['id']

        resp2 = self.client.get(f'{url}{pk}/')
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp2.json()['ruc'], data['ruc'])
