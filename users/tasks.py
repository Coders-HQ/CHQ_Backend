from users.CHQ_Scoring.github_score import CHQScore
from celery import shared_task
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

@shared_task
def update_github_score(user_name, id, old_score=0):
    profile = _model('Profile').objects.get(pk=id)
    
    try:
        logger.info("updating github score")
        chq_score = CHQScore(settings.GITHUB_TOKEN)
        profile.github_score = chq_score.get_score(user_name)
        profile.github_updated = timezone.now()
    except:
        # use old score (or 0) if api call fails
        profile.github_score=old_score
    profile.full_clean()
    profile.save()