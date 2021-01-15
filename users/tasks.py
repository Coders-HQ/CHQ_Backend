from users.CHQ_Scoring.github_score import CHQScore
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.apps import apps

def _model(Profile):
    """Generically retrieve a model object.

    This is a hack around Django/Celery's inherent circular import
    issues with tasks.py/models.py. In order to keep clean abstractions, we use
    this to avoid importing from models, introducing a circular import.

    No solutions for this are good so far (unnecessary signals, inline imports,
    serializing the whole object, tasks forced to be in model, this), so we
    use this because at least the annoyance is constrained to tasks.
    """
    return apps.get_model('users', Profile)

logger = get_task_logger(__name__)

@task(name="update_github_score")
def update_github_score(github_url, id):
    profile = _model('Profile').objects.get(pk=id)
    profile.github_url = github_url

    # get username
    split_url = github_url.split('/')
    if split_url[-1] == '':
        user_name = split_url[-2]
    else:
        user_name = split_url[-1]

    try:
        logger.info("updating github score")
        chq_score = CHQScore(settings.GITHUB_TOKEN)
        profile.github_score = chq_score.get_score(user_name)
        profile.github_updated = timezone.now()
    except:
        raise ValidationError(_('couldnt get score')
                                )
    profile.full_clean()
    profile.save()