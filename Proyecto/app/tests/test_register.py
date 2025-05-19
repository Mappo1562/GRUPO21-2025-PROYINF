
"""

Para el testing de este endpoint se tomó la HU 3 realizada en análisis y diseño de software.

"""

import unittest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment, teardown_test_environment
from app.models import Profile

class RegisterEndpointTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            setup_test_environment()
        except RuntimeError:
            pass

        cls.client = Client()

        User.objects.filter(username='admin').delete()  # evita UNIQUE

        cls.admin = User.objects.create_superuser(
            username='admin',
            password='1234'
        )

        cls.client.login(username="admin", password="1234")

    @classmethod
    def tearDownClass(cls):

        User.objects.filter(username__in=["admin", "testing_user_1", "x"]).delete()

        try:
            teardown_test_environment()
        except RuntimeError:
            pass

        super().tearDownClass()

    def test_registro_exitoso_con_rol_bibliotecologa(self):

        """
        ******** TABLA PARA EL CASO DE ASIGNACIÓN CORRECTA DE ROL ********

        Input:
            POST /Register/ con {
                'username': 'testing_user_1',
                'password1': 'Abcdef12',
                'password2': 'Abcdef12',
                'role': 'B' }
        Salida esperada:
            HTTP 302 (redirect) y Profile.role == 'B'
        Contexto:
            Administrador autenticado, rol válido ('B' = Bibliotecóloga)
        """

        url = reverse("Register")
        data = {
            "username": "testing_user_1",
            "password1": "Abcdef12",
            "password2": "Abcdef12",
            "role": "B",
        }
        response = self.client.post(url, data)
        self.assertIn(response.status_code, (200, 302))
        user = User.objects.get(username="testing_user_1")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.role, "B")

    def test_registro_fallido_por_rol_invalido(self):

        """
        ******** TABLA PARA EL CASO DE REGISTRO FALLIDO (ROL NO VÁLIDO) ********

        Input:
            POST /Register/ con {
                'username': 'x',
                'password1': 'Abcdef12',
                'password2': 'Abcdef12',
                'role': 'X' }
        Salida esperada:
            HTTP 200 (sin redirect) y mensaje de error
        Contexto:
            Administrador autenticado, rol inválido ('X' no está en ROLE_CHOICES)
        """

        url = reverse("Register")
        data = {
            "username": "x",
            "password1": "Abcdef12",
            "password2": "Abcdef12",
            "rol": "X",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

        self.assertFalse(User.objects.filter(username="x").exists())

        if response.context and "form" in response.context:
            self.assertTrue(response.context["form"].errors)