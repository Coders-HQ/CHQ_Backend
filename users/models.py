from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

import users.exceptions as CustomExceptions
from users import news, schema, validators
from users.utils import external_api


class Profile(models.Model):
    bio = models.TextField(verbose_name="biography",
                           blank=True, max_length=200)
    cv = models.FileField(null=True, blank=True, upload_to="cv")
    academic_qualification = models.CharField(blank=True, max_length=30)
    projects = models.CharField(
        _("personal projects"), blank=True, max_length=200)
    academic_qualification_file = models.FileField(
        null=True, blank=True, upload_to="academic")

    # must add http/s to url
    github_url = models.URLField(blank=True, validators=[
                                 validators.validate_github_url])

    # must add up to 100
    front_end_score = models.IntegerField(null=False, default=20)
    back_end_score = models.IntegerField(null=False, default=20)
    database_score = models.IntegerField(null=False, default=20)
    devops_score = models.IntegerField(null=False, default=20)
    mobile_score = models.IntegerField(null=False, default=20)

    # connect to user
    user = models.OneToOneField(
        'auth.User', related_name='profile', on_delete=models.CASCADE)

    # default news if none selected
    news_pref = models.CharField(max_length=100, default=news.DEFAULT_NEWS, validators=[
                                 validators.validate_no_news_source])

    # validated using schema
    languages = models.JSONField(null=True, blank=True, validators=[
        validators.JSONSchemaValidator(limit_value=schema.LANGUAGE_SCHEMA)])

    def __str__(self):
        return "%s's profile" % (self.user)

    # this property allows to search for the profile's user's username
    # in the lookup_field
    @property
    def user__username(self):
        return self.user.username

    def total_self_score(self):
        return self.mobile_score+self.devops_score+self.database_score+self.front_end_score+self.back_end_score

    def save(self, *args, **kwargs):
        """
        Fails if score does not have a total of 100 and if news source is not available.
        """
        if self.total_self_score() != 100:
            raise ValidationError(
                _('Total score must be 100 and not %(value)s'),
                params={'value': self.total_self_score()},
            )

        super(Profile, self).save(*args, **kwargs)

# automatically create a profile after a save signal
# and use the signal's instance to associate with the
# user


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Hackathon(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=30)
    members = models.ManyToManyField(
        Profile, related_name="hackathons", blank=True)
    website = models.URLField(null=True)
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title
