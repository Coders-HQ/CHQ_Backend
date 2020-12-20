from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from users import exceptions, news
from users.models import Profile
from rest_framework.test import APIRequestFactory


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        user = User()
        user.username = "testUsername"
        user.set_password("mynewPASS33")
        user.email = "test@email.com"
        user.full_clean()
        user.save()

    # Test profile model

    def test_create_new_user(self):
        user = User()
        user.username = "newUser"
        user.set_password("new_pass")
        user.email = "emailME@email.com"
        user.full_clean()
        user.save()

    def test_automatic_profile_creation(self):
        user = User.objects.get(username="testUsername")
        profile2 = Profile.objects.get(user=user)
        self.assertEqual(profile2.user.email, "test@email.com")

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_user_change_password(self):
        user = User.objects.get(id=1)
        user.set_password("userNEWpass")
        user.full_clean()
        self.assertEqual(user.check_password("userNEWpass"), True)

    def test_user_profile_default_score(self):
        profile = Profile.objects.get(id=1)

        self.assertEqual(profile.back_end_score, 20)
        self.assertEqual(profile.front_end_score, 20)
        self.assertEqual(profile.devops_score, 20)
        self.assertEqual(profile.mobile_score, 20)
        self.assertEqual(profile.database_score, 20)

    def test_user_profile_max_score(self):
        profile = Profile.objects.get(id=1)

        profile.back_end_score = 21
        profile.front_end_score = 20
        profile.devops_score = 20
        profile.mobile_score = 20
        profile.database_score = 20

        self.assertRaises(ValidationError, profile.save)

    def test_wrong_github_url(self):
        user = User.objects.get(id=1)
        profile = Profile.objects.get(user=user)
        wrong_urls = [
            "https://www.github.com",
            "https://www.github.com/profile/code",
            "https://www.github.com/profile/code/something",
            "https://www.code.com/profile",
            "https://www.github/profile",
        ]
        for url in wrong_urls:
            profile.github_url = url
            self.assertRaises(ValidationError, profile.full_clean)

    def test_right_github_url(self):
        """fails "github.com/profile" because django checks for
        "https" """
        profile = Profile.objects.get(id=1)
        right_urls = [
            "https://www.github.com/profile",
            "https://www.github.com/profile/",
            "http://www.github.com/profile/",
            "http://www.github.com/profile",
        ]
        for url in right_urls:
            profile.github_url = url
            profile.full_clean()

    def test_biography_size_limit(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').max_length
        self.assertEqual(field_label, 200)

    def test_biography_verbose_name(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'biography')

    def test_projects_verbose_name(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('projects').verbose_name
        self.assertEqual(field_label, 'personal projects')

    def test_default_news(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.news_pref, news.DEFAULT_NEWS)

    def test_wrong_news_source(self):
        profile = Profile.objects.get(id=1)
        profile.news_pref = "wrong news source"
        self.assertRaises(ValidationError, profile.full_clean)

    def test_right_news_source(self):
        profile = Profile.objects.get(id=1)
        for k, v in news.NEWS_SITES.items():
            profile.news_pref = k
            profile.full_clean()

    def test_languages_wrong_schema(self):
        profile = Profile.objects.get(id=1)
        wrong_categories = [{"name": "django", "category": "python", "score": 10}, {
            "name": "react", "category": "fire", "score": 1}]
        wrong_struct = [{"name": "django", "category": "backend"}, {
            "name": "react", "category": "frontend"}]
        wrong_values = [{"namse": "django", "category": "backend"}, {
            "namew": "react", "category": "frontend"}]
        profile.languages = wrong_categories
        self.assertRaises(ValidationError, profile.full_clean)
        profile.languages = wrong_struct
        self.assertRaises(ValidationError, profile.full_clean)
        profile.languages = wrong_values
        self.assertRaises(ValidationError, profile.full_clean)

    def test_languages_wrong_score(self):
        profile = Profile.objects.get(id=1)
        wrong_score = [{"name": "django", "category": "back_end", "score": 11}, {
            "name": "react", "category": "front_end", "score": 1}]
        profile.languages = wrong_score
        self.assertRaises(ValidationError, profile.full_clean)

    def test_right_language_schema(self):
        profile = Profile.objects.get(id=1)
        right_schema = [{"name": "django", "category": "back_end", "score": 10}, {
            "name": "react", "category": "front_end", "score": 1}]
        profile.languages = right_schema
        profile.full_clean()

    def test_total_self_score(self):
        profile = Profile.objects.get(id=1)
        self.assertEqual(profile.total_self_score(), 100)
