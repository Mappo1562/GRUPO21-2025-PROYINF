
"""

Para el testing de este endpoint se tomó la HU 3 realizada en análisis y diseño de software.

"""

import unittest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment, teardown_test_environment

class LoginEndpointTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            setup_test_environment()
        except RuntimeError:
            pass

        cls.client = Client()

        User.objects.filter(username='admin').delete()

        cls.user = User.objects.create_user(
            username='admin',
            password='1234'
        )

    @classmethod
    def tearDownClass(cls):

        User.objects.filter(username='admin').delete()

        try:
            teardown_test_environment()
        except RuntimeError:
            pass

        super().tearDownClass()

    def test_login_exitoso_redireccionando(self):

        """

        ******** TABLA PARA EL CASO DE QUE EL LOGIN SEA EXITOSO Y REDIRECCIONE DE FORMA CORRECTA ********

        Input:
            POST /login/ con {'username': 'admin', 'password': '1234'}
        Salida esperada:
            HTTP 302 (redirect) y '_auth_user_id' en session
        Contexto:
            Usuario existe y credenciales válidas


        """

        url = reverse('login')
        response = self.client.post(url, {"username": "admin", "password": "1234"})
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertIn("_auth_user_id", session)
        self.assertEqual(session["_auth_user_id"], str(self.user.pk))

    def test_login_credenciales_invalidas(self):

        """

        ******** TABLA PARA EL CASO DE QUE EL LOGIN SEA FALLIDO POR CREDENCIALES INVALIDAS ********

        Input:
            POST /login/ con {'username': 'admin', 'password': 'esta_no_es'}
        Salida esperada:
            HTTP 200 (no redirect) y mensaje de error en el formulario
        Contexto:
            Usuario existe pero contraseña incorrecta


        """

        url = reverse('login')
        response = self.client.post(
            url, {"username": "admin", "password": "esta_no_es"}
        )
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        self.assertIn(
            'Please enter a correct username and password. Note that both fields may be case-sensitive.',
            html
        )