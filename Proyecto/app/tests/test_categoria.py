"""
Para el testing de este endpoint se tomó la "IS H3" correspondiente al registro de una nueva categoría.
"""

import unittest
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.test.utils import setup_test_environment, teardown_test_environment
from app.models import Categoria  

class CrearCategoriaEndpointTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.admin = User.objects.create_superuser(username='admin', password='1234')
        cls.client.login(username='admin', password='1234')

    @classmethod
    def tearDownClass(cls):
        User.objects.filter(username='admin').delete()
        Categoria.objects.filter(nombre="Categoría Test").delete() 
        super().tearDownClass()

    def test_creacion_exitosa_categoria(self):
        """
        ******** TABLA PARA EL CASO DE CREACIÓN EXITOSA DE CATEGORÍA ********

        Input:
            POST /crear_categoria/ con {
                'nombre': 'Categoría Test'
            }
        Salida esperada:
            HTTP 302 (redirect a 'index') y la categoría existe en la BD
        Contexto:
            Usuario autenticado como administrador, formulario válido
        """

        url = reverse("crear_categoria")  
        data = {"nombre": "Categoría Test"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Categoria.objects.filter(nombre="Categoría Test").exists())

    def test_creacion_fallida_categoria_por_formulario_invalido(self):
        """
        ******** TABLA PARA EL CASO DE FORMULARIO INVÁLIDO ********

        Input:
            POST /crear_categoria/ con {
                'nombre': '' }
        Salida esperada:
            HTTP 200 (sin redirección) y mensaje de error en campo 'nombre'
        Contexto:
            Administrador autenticado, campo obligatorio vacío
        """

        url = reverse("crear_categoria")
        data = {"nombre": ""}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This field is required.", response.content)
