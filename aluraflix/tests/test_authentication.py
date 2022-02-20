from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.contrib.auth import authenticate
from django.urls import reverse
from rest_framework import status

class AuthUserTestCase(APITestCase):

    def setUp(self):
      self.list_url = reverse('programas-list')
      self.user = User.objects.create_user('c3po', password='123456')


    def test_auntetica_usuario(self):
      """garante que um usuário foi autenticado corretamente"""
      user = authenticate(username='c3po', password='123456')
      self.assertTrue((user is not None) and user.is_authenticated)

    
    def test_requisicao_sem_autenticacao(self):
      """Garante que um usuário não autenticado não consegue consultar programas"""
      response = self.client.get(self.list_url)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_requisicao_com_username_invalido(self):
      """Garante que um usuário com username inválido não seja autenticado"""
      user = authenticate(username='c3pa', password='123456')
      self.assertFalse((user is not None) and user.is_authenticated)


    def test_requisicao_com_password_invalido(self):
      """Garante que um usuário com password inválido não seja autenticado"""
      user = authenticate(username='c3po', password='123441')
      self.assertFalse((user is not None) and user.is_authenticated)


    def test_requisicao_com_usuario_autenticado(self):
      """Garante que o usuário autenticado consegue realizar um GET"""
      self.client.force_authenticate(self.user)
      response = self.client.get(self.list_url)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
