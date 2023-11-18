from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from airport.models import Ticket, Order
from airport.tests.test_flight_api import sample_flight

ORDER_URL = reverse("airport:order-list")


def sample_order(user):
    return Order.objects.create(user=user)


def sample_ticket(order, **params):
    flight = sample_flight()

    defaults = {
        "flight": flight,
        "row": 2,
        "seat": 2,
        "order": order,
    }

    defaults.update(params)

    return Ticket.objects.create(**defaults)


class UnauthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedOrderApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_order(self):
        order = sample_order(user=self.user)

        sample_ticket(order)

        response = self.client.get(ORDER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_order(self):
        response = self.client.post(ORDER_URL, {})

        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_order(self):
        order = sample_order(user=self.user)
        sample_ticket(order)

        response = self.client.get(f"{ORDER_URL}1/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_order(self):
        order = sample_order(user=self.user)

        sample_ticket(order)

        response = self.client.put(f"{ORDER_URL}1/", {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order(self):
        order = sample_order(user=self.user)

        sample_ticket(order)

        response = self.client.delete(f"{ORDER_URL}1/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AdminOrderApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="test@test.com",
            password="testpass",
            is_staff=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_order_when_admin_dont_have_order(self):
        user = get_user_model().objects.create_user(
            email="user@test.com",
            password="paspassjnf",
        )
        order = sample_order(user=user)

        sample_ticket(order)

        response = self.client.get(ORDER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

        self.client.force_authenticate(user=user)
        response = self.client.get(ORDER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
