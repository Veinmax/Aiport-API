from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Route
from airport.tests.test_airport_api import sample_airport
from airport.serializers import RouteDetailSerializer
from django.contrib.auth import get_user_model

ROUTE_URL = reverse("airport:route-list")


def sample_route(**params):
    source = sample_airport()
    destination = sample_airport(name="test2", closest_big_city="test3")
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 90,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def detail_url(route_id):
    return reverse("airport:route-detail", args=[route_id])


class UnauthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ROUTE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_routes(self):
        sample_route()

        response = self.client.get(ROUTE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_route(self):
        route = sample_route()

        url = detail_url(route.id)
        response = self.client.get(url)

        serializer = RouteDetailSerializer(route, many=False)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_route(self):
        source = sample_airport()
        destination = sample_airport(name="test2", closest_big_city="test3")
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 90,
        }

        response = self.client.post(ROUTE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminRouteApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_post_route(self):
        source = sample_airport(name="test1", closest_big_city="test1")
        destination = sample_airport(name="test2", closest_big_city="test3")
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 90,
        }

        response = self.client.post(ROUTE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_route(self):
        route = sample_route()

        url = detail_url(route.id)

        source = sample_airport(name="test1", closest_big_city="test1")
        destination = sample_airport(name="test3", closest_big_city="test4")
        payload = {
            "source": source.id,
            "destination": destination.id,
            "distance": 90,
        }

        response = self.client.put(url, payload)
        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def test_delete_route(self):
        route = sample_route()

        url = detail_url(route.id)
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
