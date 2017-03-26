from random import choice

from django.contrib.auth.models import User
from django.urls import reverse

from hypothesis.extra.django.models import models
from hypothesis.strategies import just
from hypothesis.extra.django.models import default_value

from bargainflow.models import Commission
from bargainflow.tests import Client, TestCase, status


class CommissionApiTest(TestCase):

    USERS_NUMBER = 10
    COMMISSIONS_NUMBER = 100
    AUTH_USER = "testing"

    def setUp(self):
        users = [models(User).example()
                 for _ in range(CommissionApiTest.USERS_NUMBER)]


        test_commissions = [models(Commission, date_added=default_value,
                                   orderer=just(choice(users)),
                                   status=default_value).example()
                            for _ in range(CommissionApiTest.COMMISSIONS_NUMBER)]

        User.objects.create_user(CommissionApiTest.AUTH_USER,
                                 'testing@test.com',
                                 CommissionApiTest.AUTH_USER)

    def test_listing_commissions(self):
        url = reverse('bargainflow:commission-list')
        raw_response = self.client.get(url)
        api_response = raw_response.data
        self.assertEqual(raw_response.status_code, status.HTTP_200_OK)
        self.assertEqual(Commission.objects.count(), len(api_response))

    def test_create_commission_no_auth(self):
        user_ids = [user.id for user in User.objects.all()]
        data_dict = {'description': 'very important task',
                     'status': 'O', 'tags': [],
                     'orderer': choice(user_ids)}

        url = reverse('bargainflow:commission-list')
        raw_response = self.client.post(url, data_dict, format='json')

        self.assertEqual(raw_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_commission_ok(self):
        user_ids = [user.id for user in User.objects.all()]
        data_dict = {'description': 'very important task',
                     'status': 'F', 'tags': ['dark-net']}

        url = reverse('bargainflow:commission-list')

        self.client.login(username=CommissionApiTest.AUTH_USER,
                          password=CommissionApiTest.AUTH_USER)
        raw_response = self.client.post(url, data_dict, format='json')

        self.assertEqual(raw_response.status_code, status.HTTP_201_CREATED)

        self.client.logout()

    def test_update_commission_status_ok(self):
        pass

    def test_update_commission_status_error(self):
        pass
