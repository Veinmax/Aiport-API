from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from airport.models import AirplaneType
from airport.serializers import AirplaneTypeSerializer
from django.contrib.auth import get_user_model

AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")


def sample_airplane_type(**params):
    defaults = {
        "name": "test_name",
    }
    defaults.update(params)

    return AirplaneType.objects.create(**defaults)


class UnauthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_airplane_types(self):
        sample_airplane_type()

        response = self.client.get(AIRPLANE_TYPE_URL)

        airplane_types = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(airplane_types, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_airplane_types(self):
        payload = {
            "name": "test_name",
        }

        response = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirplaneTypeApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_airplane_types(self):
        payload = {
            "name": "test_name",
        }

        response = self.client.post(AIRPLANE_TYPE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_airplane_type(self):
        sample_airplane_type()

        response = self.client.get(f"{AIRPLANE_TYPE_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_airplane_type(self):
        sample_airplane_type()

        response = self.client.put(f"{AIRPLANE_TYPE_URL}1/", {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_airplane_type(self):
        sample_airplane_type()

        response = self.client.delete(f"{AIRPLANE_TYPE_URL}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
