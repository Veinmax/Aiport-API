from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Crew
from airport.serializers import CrewSerializer
from django.contrib.auth import get_user_model

CREW_URL = reverse("airport:crew-list")


def sample_crew(**params):
    defaults = {
        "first_name": "test_name",
        "last_name": "test_last",
    }
    defaults.update(params)

    return Crew.objects.create(**defaults)


class UnauthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CREW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_crews(self):
        sample_crew()

        response = self.client.get(CREW_URL)

        crews = Crew.objects.all()
        serializer = CrewSerializer(crews, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_crews(self):
        payload = {
            "first_name": "test_name",
            "last_name": "test_last",
        }

        response = self.client.post(CREW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCrewApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_crews(self):
        payload = {
            "first_name": "test_name",
            "last_name": "test_last",
        }

        response = self.client.post(CREW_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_crew(self):
        sample_crew()

        response = self.client.get(f"{CREW_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_crew(self):
        sample_crew()

        response = self.client.put(f"{CREW_URL}1/", {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_crew(self):
        sample_crew()

        response = self.client.delete(f"{CREW_URL}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
