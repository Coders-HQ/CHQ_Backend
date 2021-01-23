"""
Custom model validators
"""

import re

import django
import jsonschema
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.translation import gettext_lazy as _
from users.CHQ_Scoring.github_score import CHQScore
from django.conf import settings
from users.utils import get_github_username

from users import news


class JSONSchemaValidator(BaseValidator):
    """validate json schemas against templates"""
    def compare(self, input, schema):
        try:
            jsonschema.validate(input, schema)
        except jsonschema.exceptions.ValidationError:
            raise django.core.exceptions.ValidationError(
                '%(value)s failed JSON schema check', params={'value': input})


def validate_no_news_source(value):
    """news needs to be part of news source"""

    if value not in news.NEWS_SITES:
        raise ValidationError(
            _('%(value)s is not an available news source'),
            params={'value': value},
        )

def validate_github_url(value):
    """validate github profile"""

    pattern = r'github.com\/[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*\/?$'
    if re.search(pattern, value) is None:
        raise ValidationError(
            _('%(value)s is not a valid github profile.'),
            params={'value': value},
        )

def validate_github_user(value):
    user_name = get_github_username(value)
    chq_score = CHQScore(settings.GITHUB_TOKEN)
    if chq_score.check_user_exists(user_name) == False:
        raise ValidationError(_('github username %(value)s doesnt exist'),
                                params={'value': user_name},)