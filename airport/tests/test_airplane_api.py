from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from airport.models import Airplane
from airport.tests.test_airplane_type_api import sample_airplane_type
from django.contrib.auth import get_user_model

AIRPLANE_URL = reverse("airport:airplane-list")


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    defaults = {
        "name": "Blue",
        "rows": 15,
        "seats_in_row": 20,
        "airplane_type": airplane_type
    }

    defaults.update(params)

    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_airplanes(self):
        sample_airplane()

        response = self.client.get(AIRPLANE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_airplane(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Blue",
            "rows": 15,
            "seats_in_row": 20,
            "airplane_type": airplane_type.id
        }

        response = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_airplane(self):
        airplane_type = sample_airplane_type()
        payload = {
            "name": "Blue",
            "rows": 15,
            "seats_in_row": 20,
            "airplane_type": airplane_type.id
        }

        response = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_airplane(self):
        sample_airplane()

        response = self.client.get(f"{AIRPLANE_URL}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_airplane(self):
        sample_airplane()

        response = self.client.put(f"{AIRPLANE_URL}1/", {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_airplane(self):
        sample_airplane()

        response = self.client.delete(f"{AIRPLANE_URL}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
