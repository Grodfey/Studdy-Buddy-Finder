from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user

from .forms import ChangeProfileForm

class UserAuthentication(TestCase):
    def test_login(self): # Danny
        self.client.login(username="danny", password="superSecure")
        self.assertTrue(get_user(self.client))

    def test_user(self): # Michael
        u = User.objects.create_user("testUser", "mst3k@virginia.edu", "password123", first_name="Mystery",
                                     last_name="Student")

        self.assertTrue(get_user(self.client))
        self.assertTrue(isinstance(u, User))

    # def test_url_http_verification(self): # Michael
    #     u = User.objects.create_user("testUser", "mst3k@virginia.edu", "password123", first_name="Mystery",
    #                                  last_name="Student")
    #     client = Client(u)
    #     # Attempt to access /profile then return HTTP response code as test
    #     url = "/profile/"
    #     response = client.get(url)
    #     self.assertEqual(response.status_code, 200)

    def test_user_edit(self): # Michael
        u = User.objects.create_user("testUser", "mst3k@virginia.edu", "password123", first_name="Mystery",
                                     last_name="Student")
        u.set_password("password123")
        client = Client(u)
        url = "/profile/edit"
        header = {"username": "test2", "email": "e2idb7sgabr@gmail.com",
                  "first_name": "Student", "last_name": "Mystery"}
        change = ChangeProfileForm(header)
        self.assertTrue(change.is_valid())


