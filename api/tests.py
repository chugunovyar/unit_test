from django.test import TestCase
from django.test import Client
from rest_framework.test import APIRequestFactory
import json
from rest_framework.test import APIClient, RequestsClient


# class TestAuth(TestCase):
#
#     def setUp(self):
#         self.root = {"username": "root", "password":"Qwerty123"}
#         self.partner_user = {"username": "partner", "password":"Qwerty123"}
#         self.credit_user = {"username": "partner", "password":"Qwerty123"}
#         self.headers = {"content-type":"application/json"}
#
#     def test_partner(self):
#         c = Client()
#         response = c.post('/api-token-auth/',
#                               data={
#                                   "username": "root",
#                                   "password":"Qwerty123"
#                               },
#                           )
#         if response.status_code == 200:
#             print(response)
#         else:
#             print(response)
#
# class TestAuth(TestCase):
#     """
#
#     """
#     def test_supuseruser_auth(self):
#
#         client = RequestsClient()
#         response = client.post(
#             '/api-token-auth/',
#             json={'username': 'root', 'password':'Qwerty123'},
#             headers={"content-type":"application/json"}
#         )
#         print(response)