from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airport
from airport.serializers import AirportSerializer
from django.contrib.auth import get_user_model

AIRPORT_URL = reverse("airport:airport-list")


def sample_airport(**params):
    defaults = {
        "name": "test_name",
        "closest_big_city": "test_city",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPORT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_airports(self):
        sample_airport()

        response = self.client.get(AIRPORT_URL)

        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_airports(self):
        payload = {
            "name": "test_name",
            "closest_big_city": "test_city",
        }

        response = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_airports(self):
        payload = {
            "name": "test_name",
            "closest_big_city": "test_city",
        }

        response = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_airport(self):
        sample_airport()

        response = self.client.get(f"{AIRPORT_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_airport(self):
        sample_airport()

        response = self.client.put(f"{AIRPORT_URL}1/", {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_airport(self):
        sample_airport()

        response = self.client.delete(f"{AIRPORT_URL}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
