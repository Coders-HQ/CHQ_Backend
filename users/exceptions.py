from rest_framework.exceptions import APIException
from users import news

class ScoreNot100(APIException):
    status_code = 400
    default_detail = 'Total score must be 100'
    default_code = 'score_not_100'
