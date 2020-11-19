from rest_framework import pagination
from rest_framework.response import Response
from .errors import BadRequest


class SensorThingsPagination(pagination.LimitOffsetPagination):
    """
    Extends the LimitOffsetPagination class of the Django Rest Framework to
    provide the $top, $skip, and $count query options.

    Use $top query option to limit the number of requested entities.

    Use $skip to specify the number of entities that should be skipped before
    returning the requested entities.

    Use $count query option to get the total number of result entities for
    the request.
    """
    limit_query_param = '$top'
    offset_query_param = '$skip'
    max_limit = 100

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return pagination._positive_int(
                    request.query_params[self.limit_query_param],
                    strict=True,
                    cutoff=self.max_limit
                )
            except KeyError:
                pass
            except ValueError:
                raise BadRequest()

        return self.default_limit

    def get_offset(self, request):
        try:
            return pagination._positive_int(
                request.query_params[self.offset_query_param],
            )
        except KeyError:
            return 0
        except ValueError:
            raise BadRequest()

    def get_paginated_response(self, data):
        count = self.request.query_params.get('$count')
        if count == 'false':
            if self.get_next_link():
                return Response({
                    'value': data,
                    '@iot.nextLink': self.get_next_link()
                    })
            else:
                return Response({
                    'value': data
                    })
        elif count == 'true' or not count:
            if self.get_next_link():
                return Response({
                    '@iot.count': self.count,
                    'value': data,
                    '@iot.nextLink': self.get_next_link()
                    })
            else:
                return Response({
                    '@iot.count': self.count,
                    'value': data
                    })
        else:
            raise BadRequest()

