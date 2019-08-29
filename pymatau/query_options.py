from __future__ import unicode_literals
import operator
from collections import defaultdict
import re
from urllib.parse import unquote

from rest_framework import serializers, pagination, filters
from rest_framework.response import Response
from django.db.models import Q, Lookup, Func, CharField, TextField, F, Value
from django.db.models.fields import Field
from rest_framework.exceptions import ParseError
from django.db.models.functions import Length, Lower, Upper
from expander import ExpanderSerializerMixin
from .errors import NotImplemented501, Conflicts, BadRequest, Unprocessable
import boolean
from django.db.models.fields import FloatField, IntegerField
from django.utils import timezone
from datetime import datetime


class Select(serializers.ModelSerializer):
    """
    The $select query option requests specific properties of an entity from
    the SensorThings service.
    """
    def __init__(self, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)
        select = self.context['request'].query_params.get('$select')
        if select:
            select = select.split(',')
            allowed = set(select)
            existing = set(self.fields.keys())
            for selected in existing - allowed:
                self.fields.pop(selected)


class Orderby(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        """
        Extends the OrderingFilter of the django rest framework to define the
        $orderby query option. Use $orderby query option to sort the response
        based on properties of requested entity in accending (asc) or
        decending (desc) order.
        """
        params = request.query_params.get(self.ordering_param)
        if params:
            field_queries = [param.strip() for param in params.split(',')]
            fields = []
            for field_query in field_queries:
                field_query = field_query.split()
                if len(field_query) <= 2:
                    while "asc" in field_query:
                        field_query.remove("asc")
                    for i, field in enumerate(field_query):
                        if field == "desc":
                            field_query[i-1] = "-" + field_query[i-1]
                    while "desc" in field_query:
                        field_query.remove("desc")
                    fields.append(field_query[0])
                else:
                    fields.append(
                        [param.strip() for param in params.split(',')]
                        )
            ordering = self.remove_invalid_fields(queryset,
                                                  fields,
                                                  view,
                                                  request)
            if ordering:
                return ordering
        return self.get_default_ordering(view)

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            new_ordering = []
            for item in ordering:
                if item[0] == '-':
                    new_ordering.append(F(item[1:]).desc(nulls_last=True))
                else:
                    new_ordering.append(F(item).asc(nulls_first=True))
            return queryset.order_by(*new_ordering)
        return queryset


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


class CustomParser:
    def limited_parse_qsl(qs, keep_blank_values=False, encoding='utf-8',
                          errors='replace', fields_limit=None):
        """
        Return a list of key/value tuples parsed from query string.
        Copied from urlparse with modifications to reserved characters.
        Copyright (C) 2013 Python Software Foundation (see LICENSE.python).
        """
        date = {'phenomenonTime', 'resultTime', 'validTime'}
        FIELDS_MATCH = re.compile('[&]')
        pairs = FIELDS_MATCH.split(qs)
        r = []
        for name_value in pairs:
            if not name_value:
                continue
            nv = name_value.split('=', 1)
            if len(nv) != 2:
                # Handle case of a control-name with no equal sign
                if keep_blank_values:
                    nv.append('')
                else:
                    continue
            if nv[1] or keep_blank_values:
                name = nv[0].replace('+', ' ')
                name = nv[0]
                name = unquote(name, encoding=encoding, errors=errors)
                if not any(a in nv[1] for a in date):
                    value = nv[1].replace('+', ' ')
                value = nv[1]
                value = unquote(value, encoding=encoding, errors=errors)
                r.append((name, value))
        query_dict = {}
        for key, value in r:
            query_dict[key] = value
        return query_dict


class Millisecond(Func):
    output_field = FloatField()
    template = "EXTRACT('milliseconds' FROM %(expressions)s) / 1000.00"
    # I should extract the milliseconds and then divide it by 1000, since it must be < 1.


class ExtractMinutes(Func):
    output_field = IntegerField()
    template = "EXTRACT('timezone_minute' FROM %(expressions)s)"


class Round(Func):
    function = 'ROUND'
    template = "%(function)s(NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', 'g'), '')::numeric)"


class Floor(Func):
    function = 'FLOOR'
    template = "%(function)s(NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', 'g'), '')::numeric)"


class Ceiling(Func):
    function = 'CEILING'
    template = "%(function)s(NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', 'g'), '')::numeric)"


class ST_Distance(Func):
    function = 'ST_Distance'
    output_field = FloatField()
    template = '%(function)s(%(expressions)s)'


class ST_Length(Func):
    function = 'ST_Length'
    output_field = FloatField()
    template = '%(function)s(%(expressions)s)'


class NullIf(Func):
    template = "NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', 'g'), '')::numeric"


class Filter(object):
    """
    Use $filter query option to perform conditional operations on the
    property values and filter request result.
    """
    class FilterOperators:
        """
        Built-in filter operatations of the Sensor Things API.
        """

        class NotEqual(Lookup):
            """
            Defines a "Not Equals" comparison operator.
            """
            lookup_name = 'ne'

            def as_postgresql(self, compiler, connection):
                lhs, lhs_params = self.process_lhs(compiler, connection)
                rhs, rhs_params = self.process_rhs(compiler, connection)
                params = lhs_params + rhs_params
                return '%s <> %s' % (lhs, rhs), params
        Field.register_lookup(NotEqual)

        comparison_operators = {
            "eq": '__exact',
            "ne": '__ne',
            "gt": '__gt',
            "ge": '__gte',
            "lt": '__lt',
            "le": '__lte'
        }

        def odata_add(parameterstring, **kwargs):
            if kwargs['numbers']:
                arguments = parameterstring.split(',')
                value = operator.add(float(arguments[0]), float(arguments[1]))
                return value
            else:
                d = dict()
                arguments = parameterstring.split(',')
                try:
                    num = float(arguments[0])
                    field = arguments[1]
                except ValueError:
                    num = float(arguments[1])
                    field = arguments[0]
                if field == 'result':
                    field = 'result__result'
                    value = operator.add(NullIf(field), num)
                else:
                    value = operator.add(F(field), num)
                temporary_field = "temp" + str(kwargs['index'])
                d['query_field'] = temporary_field
                d['annotation'] = {temporary_field: value}
                return d

        def odata_sub(parameterstring, **kwargs):
            if kwargs['numbers']:
                arguments = parameterstring.split(',')
                value = operator.sub(float(arguments[0]), float(arguments[1]))
                return value
            else:
                d = dict()
                arguments = parameterstring.split(',')
                try:
                    num = float(arguments[0])
                    field = arguments[1]
                except ValueError:
                    num = float(arguments[1])
                    field = arguments[0]
                if field == 'result':
                    field = 'result__result'
                    value = operator.sub(NullIf(field), num)
                else:
                    value = operator.sub(F(field), num)
                temporary_field = "temp" + str(kwargs['index'])
                d['query_field'] = temporary_field
                d['annotation'] = {temporary_field: value}
                return d

        def odata_mul(parameterstring, **kwargs):
            if kwargs['numbers']:
                arguments = parameterstring.split(',')
                value = operator.mul(float(arguments[0]), float(arguments[1]))
                return value
            else:
                d = dict()
                arguments = parameterstring.split(',')
                try:
                    num = float(arguments[0])
                    field = arguments[1]
                except ValueError:
                    num = float(arguments[1])
                    field = arguments[0]
                if field == 'result':
                    field = 'result__result'
                    value = operator.mul(NullIf(field), num)
                else:
                    value = operator.mul(F(field), num)
                temporary_field = "temp" + str(kwargs['index'])
                d['query_field'] = temporary_field
                d['annotation'] = {temporary_field: value}
                return d

        def odata_div(parameterstring, **kwargs):
            if kwargs['numbers']:
                arguments = parameterstring.split(',')
                value = operator.truediv(float(arguments[0]), float(arguments[1]))
                return value
            else:
                d = dict()
                arguments = parameterstring.split(',')
                try:
                    num = float(arguments[0])
                    field = arguments[1]
                except ValueError:
                    num = float(arguments[1])
                    field = arguments[0]
                if field == 'result':
                    field = 'result__result'
                    value = operator.truediv(NullIf(field), num)
                else:
                    value = operator.truediv(F(field), num)
                temporary_field = "temp" + str(kwargs['index'])
                d['query_field'] = temporary_field
                d['annotation'] = {temporary_field: value}
                return d

        def odata_mod(parameterstring, **kwargs):
            if kwargs['numbers']:
                arguments = parameterstring.split(',')
                value = operator.mul(float(arguments[0]), float(arguments[1]))
                return value
            else:
                d = dict()
                arguments = parameterstring.split(',')
                try:
                    num = float(arguments[0])
                    field = arguments[1]
                except ValueError:
                    num = float(arguments[1])
                    field = arguments[0]
                if field == 'result':
                    field = 'result__result'
                    value = operator.mod(NullIf(field), num)
                else:
                    value = operator.mul(F(field), num)
                temporary_field = "temp" + str(kwargs['index'])
                d['query_field'] = temporary_field
                d['annotation'] = {temporary_field: value}
                return d

        arithmetic_operators = {
            "add": odata_add,
            "sub": odata_sub,
            "mul": odata_mul,
            "div": odata_div,
            "mod": odata_mod
        }

    class QueryFunctions:
        """
        Built-in query functions of the Sensor Things API. Most function
        definitions act as a wrapper for django's ORM.
        """
        CharField.register_lookup(Length)
        CharField.register_lookup(Lower)
        CharField.register_lookup(Upper)
        TextField.register_lookup(Length)
        TextField.register_lookup(Lower)
        TextField.register_lookup(Upper)


        def substringof(parameterstring, **kwargs):
            """
            Returns the queryset based on a case-sensitive containment test.
            """
            django_function = '__contains'
            parsedlist = parameterstring.split(',')
            # need to do some validation: only accept two arguments!
            string_index = [i for i, s in enumerate(parsedlist) if s[0] == "'" and s[-1] == "'"]
            field_index = [i for i, s in enumerate(parsedlist) if s[0] != "'" or s[-1] != "'"]

            string = parsedlist[string_index[0]]
            field = parsedlist[field_index[0]]

            if field == 'result':
                field = 'result__result'

            if string[0] == "'" and string[-1] == "'":
                string = string[1:-1]
            elif string[0] == '"' and string[-1] == '"':
                string = string[1:-1]
                # REALLY I SHOULD RAISE AN ERROR HERE
            d = dict()
            d["query"] = Q(**{field + django_function: string})
            return d


        def endswith(parameterstring, **kwargs):
            """
            Returns the queryset for entries that are True for case-sensitive
            ends-with.
            """
            django_function = '__endswith'
            parsedlist = parameterstring.split(',')
            field = parsedlist[0]
            if field == 'result':
                field = 'result__result'
            string = parsedlist[1]
            if string[0] == "'" and string[-1] == "'":
                string = string[1:-1]
            elif string[0] == '"' and string[-1] == '"':
                string = string[1:-1]
            d = dict()
            d["query"] = Q(**{field + django_function: string})
            return d

        def startswith(parameterstring, **kwargs):
            """
            Returns the queryset for entries that are True for case-sensitive
            starts-with.
            """
            django_function = '__startswith'
            parsedlist = parameterstring.split(',')
            field = parsedlist[0]
            if field == 'result':
                field = 'result__result'
            string = parsedlist[1]
            if string[0] == "'" and string[-1] == "'":
                string = string[1:-1]
            elif string[0] == '"' and string[-1] == '"':
                string = string[1:-1]
            d = dict()
            d["query"] = Q(**{field + django_function: string})
            return d

        def length(parameterstring, **kwargs):
            """
            Wraps the query with the PostgreSQL Length function and
            registers as a transform.
            """
            django_function = '__length'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def tolower(parameterstring, **kwargs):
            """
            Wraps the query with the PostgreSQL Lower function and
            registers as a transform.
            """
            django_function = '__lower'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def toupper(parameterstring, **kwargs):
            """
            Wraps the query with the PostgreSQL Upper function and
            registers as a transform.
            """
            django_function = '__upper'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def year(parameterstring, **kwargs):
            django_function = '__year'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = {}
            d['query_field'] = field + django_function
            return d

        def month(parameterstring, **kwargs):
            django_function = '__month'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def day(parameterstring, **kwargs):
            django_function = '__day'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def hour(parameterstring, **kwargs):
            django_function = '__hour'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def minute(parameterstring, **kwargs):
            django_function = '__minute'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def second(parameterstring, **kwargs):
            django_function = '__second'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def millisecond(parameterstring, **kwargs):
            d = dict()
            django_function = Millisecond
            field = parameterstring
            temporary_field = "temp" + str(kwargs['index'])
            d['query_field'] = temporary_field
            d['annotation'] = {temporary_field: django_function(field)}
            return d

        def offsetminutes(parameterstring, **kwargs):
            d = dict()
            django_function = ExtractMinutes
            field = parameterstring
            temporary_field = "temp" + str(kwargs['index'])
            d['query_field'] = temporary_field
            d['annotation'] = {temporary_field: django_function(field)}
            return d

        def date(parameterstring, **kwargs):
            django_function = '__date'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def time(parameterstring, **kwargs):
            django_function = '__time'
            field = parameterstring
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query_field'] = field + django_function
            return d

        def round(parameterstring, **kwargs):
            d = dict()
            django_function = Round
            field = parameterstring
            temporary_field = "temp" + str(kwargs['index'])
            d['query_field'] = temporary_field
            d['annotation'] = {temporary_field: django_function(field)}
            return d

        def floor(parameterstring, **kwargs):
            d = dict()
            django_function = Floor
            field = parameterstring
            temporary_field = "temp" + str(kwargs['index'])
            d['query_field'] = temporary_field
            d['annotation'] = {temporary_field: django_function(field)}
            return d

        def ceiling(parameterstring, **kwargs):
            d = dict()
            django_function = Ceiling
            field = parameterstring
            temporary_field = "temp" + str(kwargs['index'])
            d['query_field'] = temporary_field
            d['annotation'] = {temporary_field: django_function(field)}
            return d

        def geo_distance(parameterstring, **kwargs):
            d = dict()
            django_function = ST_Distance
            parsedlist = parameterstring.split(',')
            # this is not very good ... easy to break
            point_index = [i for i, s in enumerate(parsedlist) if "POINT" in s]
            field_index = [i for i, s in enumerate(parsedlist) if s[0] != "'" or s[-1] != "'"]

            string = parsedlist[point_index[0]]
            try:
                string = string.split("'")[1]
            except:
                pass

            field = parsedlist[field_index[0]]

            temporary_field = "temp" + str(kwargs['index'])
            d['query_field'] = temporary_field
            d['annotation'] = {temporary_field: django_function(field, Value(string))}
            return d

        def geo_length(parameterstring, **kwargs):
            d = dict()
            django_function = ST_Length
            field = parameterstring
            temporary_field = "temp" + str(kwargs['index'])
            d['query_field'] = temporary_field
            d['annotation'] = {temporary_field: django_function(field)}
            return d

        def st_equals(parameterstring, **kwargs):
            django_function = '__equals'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_within(parameterstring, **kwargs):
            django_function = '__within'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_disjoint(parameterstring, **kwargs):
            django_function = '__disjoint'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_touches(parameterstring, **kwargs):
            django_function = '__touches'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_overlaps(parameterstring, **kwargs):
            django_function = '__overlaps'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_intersects(parameterstring, **kwargs):
            django_function = '__intersects'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_contains(parameterstring, **kwargs):
            django_function = '__contains'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_crosses(parameterstring, **kwargs):
            django_function = '__crosses'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: geometry})
            return d

        def st_relate(parameterstring, **kwargs):
            django_function = '__relate'
            field = parameterstring.split(',')[0]
            geometry = parameterstring.split("'")[1]
            intersection = parameterstring.split(",")[-1]
            intersection = intersection.split("'")[1]
            if field == 'result':
                field = 'result__result'
            d = dict()
            d['query'] = Q(**{field + django_function: (geometry, intersection)})
            return d

        implemented = {
            # string functions
            "substringof": substringof,
            "endswith": endswith,
            "startswith": startswith,
            "length": length,
            "tolower": tolower,
            "toupper": toupper,
            # date functions
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "fractionalseconds": millisecond,
            "totaloffsetminutes": offsetminutes,
            # "now": now,
            "date": date,
            "time": time,
            # math functions
            "round": round,
            "floor": floor,
            "ceiling": ceiling,
            ## geospatial functions
            "geo.distance": geo_distance,
            "geo.length": geo_length,
            "geo.intersects": st_intersects,
            # spatial relationship functions
            "st_equals": st_equals,
            "st_disjoint": st_disjoint,
            "st_touches": st_touches,
            "st_within": st_within,
            "st_crosses": st_crosses,
            "st_intersects": st_intersects,
            "st_contains": st_contains,
            "st_relate": st_relate,
            "st_overlaps": st_overlaps
        }

    class QueryCompiler:
        """
        Compiles and runs filter queries on the database.
        """
        d = {}
        b = []
        ind = 0
        temp_field = None

        def lexer(string):
            """
            Takes the url decoded querystring and returns a
            """
            parsedlist = []
            parsedstring = ''
            leftbcounter = 0
            rightbcounter = 0
            qcounter = 0
            for index, a in enumerate(string):
                if qcounter == 2:
                    if a.isalpha():
                        qcounter = 1
                    else:
                        qcounter = 0
                if a == '(':
                    leftbcounter += 1
                if a == ')':
                    rightbcounter += 1
                if a == "'" and leftbcounter == rightbcounter:
                    qcounter += 1
                if a != ' ' and leftbcounter == rightbcounter \
                        and qcounter == 0:
                    parsedstring += a
                    if index+1 == len(string):
                        parsedlist.append(parsedstring)
                        parsedstring = ''
                elif leftbcounter != rightbcounter:
                    parsedstring += a
                elif qcounter > 0:
                    parsedstring += a
                    if index+1 == len(string):
                        parsedlist.append(parsedstring)
                        parsedstring = ''
                else:
                    parsedlist.append(parsedstring)
                    parsedstring = ''
            if leftbcounter != rightbcounter:
                raise BadRequest()
            bl = []
            sl = []
            counter = 0
            for index, query in enumerate(parsedlist, 1):
                if query == "and" or query == "or" or query == "not":
                    if sl:
                        bl.append(sl)
                    bl.append([query])
                    counter = 0
                    sl = []
                    continue
                sl.append(query)
                counter += 1
                if index == len(parsedlist) and sl:
                    bl.append(sl)
            # i later added a third nested list to seperate AND and OR
            query_list = []
            al = []
            counter = 0
            for index, grouped_query in enumerate(bl, 1):
                if grouped_query[0] == "or":
                    query_list.append(al)
                    query_list.append([grouped_query])
                    counter = 0
                    al = []
                    continue
                al.append(grouped_query)
                counter += 1
                if index == len(bl):
                    query_list.append(al)

            for x in query_list:
                for y in x:
                    if y[0] == 'and' or y[0] == 'or' or y[0] == 'not':
                        Filter.QueryCompiler.b.append(y[0])
                        continue
                    if y[0][0] == '(' and y[0][-1] == ')':
                        Filter.QueryCompiler.b.append(y[0][0])
                        Filter.QueryCompiler.lexer(y[0][1:-1])
                        Filter.QueryCompiler.b.append(y[0][-1])
                    else:
                        Filter.QueryCompiler.ind += 1
                        n = 'arg' + str(Filter.QueryCompiler.ind)
                        Filter.QueryCompiler.d[n] = Filter.QueryCompiler.\
                            query_mapping(y, Filter.QueryCompiler.ind)["query"]
                        Filter.QueryCompiler.b.append(n)
            return Filter.QueryCompiler.b

        def function_lexer(string):
            """A brute force lexer for funcions of the SensorThings API.
            Returns a list of the function and parameters"""
            parsedlist = []
            parsedstring = ''
            leftbcounter = 0
            rightbcounter = 0
            for i, a in enumerate(string):
                if a == '(':
                    leftbcounter += 1
                if a == ')':
                    rightbcounter += 1
                if a == '(' and leftbcounter != 1:
                    parsedstring += a
                elif a == '(' and leftbcounter == 1:
                    parsedlist.append(parsedstring)
                    parsedstring = ''
                elif a == ')' and i+1 == len(string):
                    parsedlist.append(parsedstring)
                else:
                    parsedstring += a
            return parsedlist


        def solve_arithmetic(expression):
            indices = [i for i, x in enumerate(expression) if x in Filter.FilterOperators.arithmetic_operators]

            if len(indices) > 1:
                raise NotImplemented501()

            new_expression = expression
            for ind in indices:
                lhs = new_expression[ind - 1]
                rhs = new_expression[ind + 1]
                value = new_expression[ind] + "(" + lhs + "," + rhs + ")"
                new_expression[ind-1:ind+2] = str(value),

            return new_expression


        def query_mapping(y, index):
            """
            Maps Sensor Things filter expressions with their django or raw
            PostgreSQL counterparts.
            """
            d = {}
            if any([i in Filter.FilterOperators.arithmetic_operators
                    for i in y]):

                y = Filter.QueryCompiler.solve_arithmetic(y)

            if len(y) == 1:
                parse_function = Filter.QueryCompiler.function_lexer(y[0])

                if parse_function[0] in Filter.FilterOperators.arithmetic_operators:
                    raise NotImplemented501()
                    # I shld raise a 400 as this query, although given as example in docs,
                    # should not be allowed in my opinion
                else:
                    func = Filter.QueryFunctions.implemented[parse_function[0]]

                return func(parse_function[1], index=index)

            elif len(y) == 3:  # valid must be comparison
                operandA = y[0].replace('/', '__')
                operator = Filter.FilterOperators.comparison_operators[y[1]]
                operandB = y[2]

                if Filter.QueryCompiler.function_lexer(operandA):
                    parse_function = Filter.QueryCompiler.function_lexer(operandA)

                    if parse_function[0] in Filter.FilterOperators.arithmetic_operators:
                        func = Filter.FilterOperators.arithmetic_operators[parse_function[0]]

                    else:
                        func = Filter.QueryFunctions.implemented[parse_function[0]]


                    strng = re.search('^(?![0-9.]*$).+$', operandB)

                    if (func == Filter.QueryFunctions.round or
                            func == Filter.QueryFunctions.floor or
                            func == Filter.QueryFunctions.ceiling) and strng:
                        raise BadRequest

                    funcres = func(parse_function[1], index=index, numbers=False)

                    try:
                        operandA = funcres['query_field']
                        Filter.QueryCompiler.temp_field = funcres['annotation']
                    except KeyError:
                        pass
                if operandB[0] == "'" or operandB[0] == '"':
                    operandB = operandB[1:-1]

                if operandB == "now()":
                    now = timezone.now()
                    operandB = now
                    operandB = now.strftime("%Y-%m-%d %H:%M:%S.%f")

                if operandB == "maxdatetime()":
                    maxdatetime = datetime(
                        year=9999,
                        month=12,
                        day=30,
                        hour=11,
                        minute=59,
                        second=59,
                        tzinfo=timezone.utc
                    )  # postgres error: date out of range if day = 31
                    operandB = maxdatetime.strftime("%Y-%m-%d %H:%M:%S.%f")

                if operandB == "mindatetime()":
                    mindatetime = datetime(
                        year=1,
                        month=1,
                        day=2,
                        hour=0,
                        minute=0,
                        second=0,
                        tzinfo=timezone.utc
                    )  # postgres error: "date out of range" if day = 1
                    operandB = mindatetime.strftime("%Y-%m-%d %H:%M:%S.%f")

                if Filter.QueryCompiler.function_lexer(operandB):
                    parse_function = Filter.QueryCompiler.function_lexer(operandB)
                    if parse_function[0] in Filter.FilterOperators.arithmetic_operators:
                        func = Filter.FilterOperators.arithmetic_operators[parse_function[0]]
                        operandB = func(parse_function[1], numbers=True)


                    else:
                        func = Filter.QueryFunctions.implemented[parse_function[0]]
                    # return func(parse_function[1], index=index)

                        raise NotImplemented501()


                try:
                    operandB = float(operandB)
                except ValueError:
                    pass
                if operandA == 'result':
                    operandA = 'result__result'
                if operandB == 'result':
                    operandB = 'result__result'
                d['query'] = Q(**{operandA + operator: operandB})
                return d
            else:
                raise ParseError()

        def parser(string, queryset):
            """
            Parses the lexicated list and applies the appropriate django
            filters. Returns a queryset.
            """
            Filter.QueryCompiler.d = {}
            Filter.QueryCompiler.b = []
            Filter.QueryCompiler.ind = 0
            Filter.QueryCompiler.temp_field = None

            algebra = boolean.BooleanAlgebra()
            query_list = Filter.QueryCompiler.lexer(string)
            query_string = ' '.join(query_list)
            qs = algebra.parse(query_string)

            if Filter.QueryCompiler.temp_field:
                queryset = queryset.annotate(**Filter.QueryCompiler.temp_field)
                Filter.QueryCompiler.temp_field = None

            locals().update(Filter.QueryCompiler.d.items())
            query = str(qs)
            query = eval(query)
            queryset = queryset.filter(query)
            return queryset

    def get_queryset(self):
        qs = super(Filter, self).get_queryset()
        raw_querystring = self.request.META['QUERY_STRING']
        querydict = CustomParser.limited_parse_qsl(raw_querystring)
        queryfilter = querydict.get('$filter', None)
        queryexpand = querydict.get('$expand', None)
        if queryfilter:
            try:
                qs = Filter.QueryCompiler.parser(queryfilter, qs)
            except NotImplemented501:
                raise NotImplemented501()
            except Unprocessable:
                raise Unprocessable()
            except Exception as e:
                raise BadRequest("Malformed request: " + str(e))
        elif queryexpand:
            expanded_list = re.split(r',\s*(?![^()]*\))', queryexpand)
            queried_fields = {}
            expanded_fields = []
            for field in expanded_list:
                children = field.split('/')
                fields_only = ''
                for i, child in enumerate(children, 1):
                    if child[-1] == ')':
                        d = "("
                        split_fields = [e+d for e in child.split(d) if e]
                        f = split_fields[0][:-1]
                        q = ''.join(split_fields[1:])[:-1]
                        queried_fields[f] = q[:-1]
                        if i == len(children):
                            fields_only += f
                        else:
                            fields_only += f + '/'
                    else:
                        queried_fields[child] = None
                        if i == len(children):
                            fields_only += child
                        else:
                            fields_only += child + '/'
                expanded_fields.append(fields_only)
            expanded_fields = ','.join(expanded_fields)

            for key, value in queried_fields.items():
                if value:
                    raise NotImplemented501()
        return qs


class DataArray(object):
    def __init__(self, *args, **kwargs):
        super(DataArray, self).__init__(*args, **kwargs)
        resultFormat = self.context['request'].query_params.get('$resultFormat')
        if resultFormat:
            raise NotImplemented501()


class Expand(ExpanderSerializerMixin):
    """
    Extends and modifies the ExpanderSerializerMixin class to define the
    $expand query option. Use $expand query option to request inline
    information for related entities of the requested entity collection.
    """
    def __init__(self, *args, **kwargs):
        expanded_fields = kwargs.pop('expanded_fields', None)
        get_expandable_fields = getattr(self.Meta,
                                        'get_expandable_fields',
                                        None
                                        )
        expand_arg = '$expand'
        super(Expand, self).__init__(*args, **kwargs)
        if not get_expandable_fields:
            return
        if not expanded_fields:
            context = self.context
            if not context:
                return
            request = context.get('request', None)
            if not request:
                return
            entity = request.META['PATH_INFO'].split('/')[-1]
            entity = entity.split('(')[0]
            querystring = request.META['QUERY_STRING']
            querydict = CustomParser.limited_parse_qsl(querystring)
            try:
                expanded_fields = querydict[expand_arg]
            except KeyError:
                pass
            if not expanded_fields:
                return
        expanded_list = re.split(r',\s*(?![^()]*\))', expanded_fields)
        new_list = []
        for exp in expanded_list:
            test = exp.split('/')[0]
            if test in [x.split('/')[0] for x in new_list]:
                continue
            else:
                new_list.append(exp)
        expanded_list = new_list
        queried_fields = {}
        expanded_fields = []
        for field in expanded_list:
            children = field.split('/')
            fields_only = ''
            for i, child in enumerate(children, 1):
                if child[-1] == ')':
                    d = "("
                    split_fields = [e+d for e in child.split(d) if e]
                    f = split_fields[0][:-1]
                    q = ''.join(split_fields[1:])[:-1]
                    queried_fields[f] = q[:-1]
                    if i == len(children):
                        fields_only += f
                    else:
                        fields_only += f + '/'
                else:
                    queried_fields[child] = None
                    if i == len(children):
                        fields_only += child
                    else:
                        fields_only += child + '/'
            expanded_fields.append(fields_only)
        expanded_fields = ','.join(expanded_fields)
        expansions = dict_from_qs(expanded_fields)
        base_field = set()
        for expanded_field, nested_expand in expansions.items():
            base_field.add(expanded_field)
            seen_base = list(base_field)
            expandable_fields = get_expandable_fields(*seen_base)
            if expanded_field in expandable_fields:
                serializer_class_info = expandable_fields[expanded_field]
                if isinstance(serializer_class_info, tuple):
                    serializer_class, args, kwargs = serializer_class_info
                else:
                    args = ()
                    kwargs = {}
                    serializer_class = serializer_class_info

                kwargs = kwargs.copy()
                kwargs.setdefault('context', self.context)

                if issubclass(serializer_class, Expand):
                    serializer = serializer_class(
                                   expanded_fields=qs_from_dict(nested_expand),
                                   *args,
                                   **kwargs)
                else:
                    serializer = serializer_class(*args, **kwargs)

                self.fields[expanded_field] = serializer
                Conflicts.conflicts = []


def dict_from_qs(qs):
    """
    Slightly introverted parser for lists of comma seperated nested fields
    i.e. "period.di,period/fhr" => {"period": {"di": {}, "fhr": {}}}
    """
    entries = qs.split(',') if qs.strip() else []
    entries = [entry.strip() for entry in entries]

    def _dict_from_qs(line, d):
        if '/' in line:
            key, value = line.split('/', 1)
            d.setdefault(key, {})
            return _dict_from_qs(value, d[key])
        else:
            d[line] = {}

    def _default():
        return defaultdict(_default)

    d = defaultdict(_default)
    for line in entries:
        _dict_from_qs(line, d)
    return d


def qs_from_dict(qsdict, prefix=""):
    """
    Same as dict_from_qs, but in reverse
    i.e. {"period": {"di": {}, "fhr": {}}} => "period/di,period/fhr"
    """
    prefix = prefix + '/' if prefix else ""

    def descend(qsd):
        for key, val in sorted(qsd.items()):
            if val:
                yield qs_from_dict(val, prefix + key)
            else:
                yield prefix + key
    return ",".join(descend(qsdict))
