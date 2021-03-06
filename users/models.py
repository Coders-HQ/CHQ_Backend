
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.exceptions import ScoreNot100
from users import news, schema, validators
from users.tasks import update_github_score
from users.utils import get_github_username


class Profile(models.Model):
    """
    Main user profile
    """

    # main profile items
    bio = models.TextField(verbose_name="biography",
                           blank=True, max_length=200)
    cv = models.FileField(null=True, blank=True, upload_to="cv")
    academic_qualification = models.CharField(blank=True, max_length=30)
    projects = models.CharField(
        _("personal projects"), blank=True, max_length=200)
    academic_qualification_file = models.FileField(
        null=True, blank=True, upload_to="academic")

    # github
    # must add http/s to url
    github_url = models.URLField(blank=True, validators=[
                                 validators.validate_github_url,
                                 validators.validate_github_user])
    github_score = models.IntegerField(null=False, default=0)
    # time when score is updated
    github_updated = models.DateTimeField(null=True, blank=True)

    # scoring and language
    # must add up to 100
    front_end_score = models.IntegerField(null=False, default=20)
    back_end_score = models.IntegerField(null=False, default=20)
    database_score = models.IntegerField(null=False, default=20)
    devops_score = models.IntegerField(null=False, default=20)
    mobile_score = models.IntegerField(null=False, default=20)
    # validated using schema
    languages = models.JSONField(null=True, blank=True, validators=[
        validators.JSONSchemaValidator(limit_value=schema.LANGUAGE_SCHEMA)])

    # connect to user
    user = models.OneToOneField(
        'auth.User', related_name='profile', on_delete=models.CASCADE)

    # news
    # default news if none selected
    news_pref = models.CharField(max_length=100, default=news.DEFAULT_NEWS, validators=[
                                 validators.validate_no_news_source])

    def __str__(self):
        return "%s's profile" % (self.user)

    @property
    def user__username(self):
        """
        This property allows to search for the profile's user's username
        in the lookup_field
        """
        return self.user.username

    @property
    def github_username(self):
        """
        github username as a profile's property
        """
        return get_github_username(self.github_url)

    def total_self_score(self):
        """
        add total score together
        """
        return self.mobile_score+self.devops_score+self.database_score+self.front_end_score+self.back_end_score

    def save(self, *args, **kwargs):
        """
        Fails if score does not have a total of 100 and if news source is not available.
        """

        # raise error if score doesnt add to 100
        if self.total_self_score() != 100:
            raise ScoreNot100()

        # if profile has a github_url
        if self.github_url != '':
            # if profile score was updated
            if self.github_updated != None:
                # only get score when enough time has passed
                if timezone.now()-timezone.timedelta(seconds=24) >= self.github_updated <= timezone.now():
                    # save current score and use it if api call fails
                    old_score = self.github_score
                    # set github score to -1 until value is set by celery
                    self.github_score = -1
                    # call celery task
                    update_github_score.delay(
                        self.github_username, self.pk, old_score)
            else:
                # first time get score
                self.github_score = -1
                update_github_score.delay(self.github_username, self.pk)

        super(Profile, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    automatically create a profile after a save signal
    and use the signal's instance to associate with the
    user
    """

    if created:
        Profile.objects.create(user=instance)


class Hackathon(models.Model):
    # TODO: add more fields to hackathon
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
