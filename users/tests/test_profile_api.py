from users.views import ProfileDetail
from users.models import Profile
from users import exceptions, news
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AnonymousUser, User
import json


class ProfileApiTest(APITestCase):

    def setUp(self):
        # Set up non-modified objects used by all test methods

        self.client = APIClient()

        data_user_1 = {
            'username': 'user1',
            'password1': 'myNEWPASS123',
            'password2': 'myNEWPASS123',
            'email': 'user1@email.com'
        }
        response = self.client.post('/auth/register/', data_user_1)

        data_user_2 = {
            'username': 'user2',
            'password1': 'myNEWPASS123',
            'password2': 'myNEWPASS123',
            'email': 'user2@email.com'
        }
        response = self.client.post('/auth/register/', data_user_2)

        self.user1 = User.objects.get(username='user1')
        self.user2 = User.objects.get(username='user2')

    def test_create_new_user(self):
        data = {
            'username': 'newUser',
            'password1': 'myNEWPASS123',
            'password2': 'myNEWPASS123',
            'email': 'newuser@email.com'
        }
        response = self.client.post('/auth/register/', data)
        newUser = User.objects.get(username='newUser')
        newUserToken = Token.objects.get(user=newUser)
        self.assertEqual(response.data['key'], newUserToken.key)

    def test_new_user_has_token(self):
        is_tokened = Token.objects.filter(user=self.user1).exists()
        self.assertEqual(is_tokened, True)

    def test_user_login(self):
        data = {'username': 'user1', "password": "myNEWPASS123"}
        response = self.client.post('/auth/login/', data)
        token = Token.objects.get(user=self.user1)
        self.assertEqual(response.data['key'], token.key)

    def test_change_user_detail_no_auth(self):
        data = {'first_name': 'mahalo', "last_name": "aloha"}
        response = self.client.put('/auth/user/', data)
        self.assertEqual(
            response.data['detail'], 'Authentication credentials were not provided.')

    def test_change_user_detail(self):
        data = {'username': 'user1',
                'first_name': 'mahalo', "last_name": "aloha"}
        token = Token.objects.get(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put('/auth/user/', data)
        self.assertEqual(response.data['first_name'], 'mahalo')
        self.client.credentials()

    def test_get_default_profile(self):
        # Create an instance of a GET request.
        response = self.client.get('/profiles/user1/')

        self.assertEqual(response.data, {
            'github_url': '',
            'bio': '',
            'username': 'user1',
            'first_name': '',
            'last_name': '',
            'email': 'user1@email.com',
            'mobile_score': 20,
            'devops_score': 20,
            'front_end_score': 20,
            'back_end_score': 20,
            'database_score': 20,
            'languages': None,
            'cv': None,
            'academic_qualification': '',
            'academic_qualification_file': None,
            'projects': '',
            'hackathons': [],
            'news_pref': news.DEFAULT_NEWS
        })

    def test_profile_add_bio(self):
        data = {'bio': 'This is a test bio'}
        token = Token.objects.get(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put('/profiles/user1/', data)
        self.assertEqual(response.data['bio'], 'This is a test bio')
        self.client.credentials()

    def test_profile_correct_github(self):
        key = 'github_url'
        value = 'https://github.com/profile/'
        data = {key: value}
        token = Token.objects.get(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put('/profiles/user1/', data)
        self.assertEqual(response.data[key], value)
        self.client.credentials()

    def test_profile_wrong_github(self):
        key = 'github_url'
        value = 'https://github.com/profile/wrong'
        data = {key: value}
        token = Token.objects.get(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put('/profiles/user1/', data)
        self.assertEqual(
            str(response.data[key][0]), value+' is not a valid github profile.')
        self.client.credentials()

    def test_valid_language_schema(self):
        key = 'languages'
        value = [{"name": "django", "category": "back_end", "score": 10}, {
            "name": "react", "category": "front_end", "score": 1}]
        data = {key: value}
        token = Token.objects.get(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # post list as json
        response = self.client.put(
            '/profiles/user1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.data['languages'], [{'name': 'django', 'category': 'back_end', 'score': 10}, {
                         'name': 'react', 'category': 'front_end', 'score': 1}])
        self.client.credentials()

    def test_wrong_language_schema(self):
        key = 'languages'
        # wrong category name
        value = [{"name": "django", "category": "bback_end", "score": 10}, {
            "name": "react", "category": "front_end", "score": 1}]
        data = {key: value}
        token = Token.objects.get(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # post list as json
        response = self.client.put(
            '/profiles/user1/', json.dumps(data), content_type='application/json')
        self.assertEqual(response.data[key][0], str(value)+' failed JSON schema check')
        self.client.credentials()

    def test_write_to_other_profile(self):
        key = 'github_url'
        value = 'https://github.com/profile/'
        data = {key: value}
        token = Token.objects.get(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put('/profiles/user1/', data)
        self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
        self.client.credentials()