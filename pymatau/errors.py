from rest_framework import status
from rest_framework.exceptions import APIException
from django.core.exceptions import ValidationError
import dateutil.parser


class NotImplemented501(APIException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = 'Sorry, this query type is not yet implemented.'
    default_code = 'not_implemented'


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Malformed request.'
    default_code = 'bad_request'


class Unprocessable(APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = """Unprocessable request"""
    default_code = 'unprocessable_entity'


class Conflicts:
    conflicts = []


class Validators:
    def validate_interval(value):
        times = value.split("/")
        for time in times:
            try:
                dateutil.parser.parse(time)
            except ValueError:
                raise ValidationError(
                    """%(value)s is not in an ISO 8601 recognized time interval
                    format or contains a duration.""",
                    params={'value': value},
                )
