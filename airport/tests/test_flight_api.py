import datetime

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Flight, Route, Airplane, Crew
from airport.tests.test_airport_api import sample_airport
from airport.tests.test_crew_api import sample_crew
from airport.tests.test_route_api import sample_route
from airport.tests.test_airplane_api import sample_airplane
from airport.serializers import FlightDetailSerializer
from django.contrib.auth import get_user_model

FLIGHT_URL = reverse("airport:flight-list")


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()

    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": datetime.datetime(
            year=2022,
            month=9,
            day=2,
        ),
        "arrival_time": datetime.datetime(
            year=2022,
            month=12,
            day=5,
        ),
    }
    defaults.update(params)

    return Flight.objects.create(**defaults)



def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_flights(self):
        sample_flight()

        response = self.client.get(FLIGHT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_flight(self):
        flight = sample_flight()

        url = detail_url(flight.id)
        response = self.client.get(url)

        serializer = FlightDetailSerializer(flight, many=False)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_flight(self):
        response = self.client.post(FLIGHT_URL, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_flight(self):
        flight = sample_flight()

        url = detail_url(flight.id)
        response = self.client.put(url, {})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_movie_session(self):
        flight = sample_flight()

        url = detail_url(flight.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_movie_session(self):
        route = sample_route()
        airplane = sample_airplane()
        crew = sample_crew()

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": datetime.datetime(
                year=2022,
                month=9,
                day=2,
            ),
            "arrival_time": datetime.datetime(
                year=2022,
                month=12,
                day=5,
            ),
            "crews": crew.id
        }

        response = self.client.post(FLIGHT_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_flight(self):
        flight = sample_flight()

        url = detail_url(flight.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
