from __future__ import unicode_literals

import re
import boolean

from urllib.parse import unquote
from rest_framework import filters
from django.db.models import Q, F
from rest_framework.exceptions import ParseError
from .errors import NotImplemented501, BadRequest, Unprocessable
from django.utils import timezone
from datetime import datetime
from .functions import QueryFunctions, QueryOperations
from .viewsets import MODEL_KEYS
from .models import Datastream


def lexer(string):  # TODO: refactor
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
                QueryObjects.B.append(y[0])
                continue
            if y[0][0] == '(' and y[0][-1] == ')':
                QueryObjects.B.append(y[0][0])
                lexer(y[0][1:-1])
                QueryObjects.B.append(y[0][-1])
            else:
                QueryObjects.IND += 1
                n = 'arg' + str(QueryObjects.IND)
                QueryObjects.D[n] = query_mapping(y, QueryObjects.IND)["query"]
                QueryObjects.B.append(n)
    return QueryObjects.B


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
    # TODO: allow multiple arithmetic operations
    indices = [i for i, x in enumerate(expression) if x in QueryOperations.arithmetic_operators]

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
    if any([i in QueryOperations.arithmetic_operators
            for i in y]):

        y = solve_arithmetic(y)

    if len(y) == 1:
        parse_function = function_lexer(y[0])

        if parse_function[0] in QueryOperations.arithmetic_operators:
            raise NotImplemented501()
            # I shld raise a 400 as this query, although given as example in docs,
            # should not be allowed in my opinion
        else:
            func = QueryFunctions.implemented[parse_function[0]]

        return func(parse_function[1], index=index)

    elif len(y) == 3:  # valid must be comparison
        operandA = y[0].split("/")
        operandA = [MODEL_KEYS[x] if x in MODEL_KEYS else x for x in operandA]
        operandA = '__'.join(operandA)
        operator = QueryOperations.comparison_operators[y[1]]
        operandB = y[2]

        if function_lexer(operandA):
            parse_function = function_lexer(operandA)
            if parse_function[0] in QueryOperations.arithmetic_operators:
                func = QueryOperations.arithmetic_operators[parse_function[0]]
            else:
                func = QueryFunctions.implemented[parse_function[0]]
            strng = re.search('^(?![0-9.]*$).+$', operandB)

            if (func == QueryFunctions.round or
                    func == QueryFunctions.floor or
                    func == QueryFunctions.ceiling) and strng:
                raise BadRequest

            funcres = func(parse_function[1], index=index, numbers=False)

            try:
                operandA = funcres['query_field']
                QueryObjects.TEMP_FIELD = funcres['annotation']
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

        if function_lexer(operandB):
            parse_function = function_lexer(operandB)
            if parse_function[0] in QueryOperations.arithmetic_operators:
                func = QueryOperations.arithmetic_operators[parse_function[0]]
                operandB = func(parse_function[1], numbers=True)

            else:
                func = QueryFunctions.implemented[parse_function[0]]
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
    QueryObjects.D = {}
    QueryObjects.B = []
    QueryObjects.IND = 0
    QueryObjects.TEMP_FIELD = None

    algebra = boolean.BooleanAlgebra()
    query_list = lexer(string)
    query_string = ' '.join(query_list)
    qs = algebra.parse(query_string)

    if QueryObjects.TEMP_FIELD:
        queryset = queryset.annotate(**QueryObjects.TEMP_FIELD)
        QueryObjects.TEMP_FIELD = None

    locals().update(QueryObjects.D.items())
    query = str(qs)
    query = eval(query)
    queryset = queryset.filter(query)
    return queryset


class QueryObjects:
    D = {}
    B = []
    IND = 0
    TEMP_FIELD = None


class Orderby(filters.OrderingFilter):
    """$orderby
    Extends the OrderingFilter of the django rest framework to define the
    $orderby query option. Use $orderby query option to sort the response
    based on properties of requested entity in accending (asc) or
    decending (desc) order.
    """
    def get_ordering(self, request, queryset, view):
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


class Filter:
    """$filter
    Use $filter query option to perform conditional operations on the
    property values and filter request result.
    """

    def get_queryset(self):
        qs = super(Filter, self).get_queryset()
        raw_querystring = self.request.META['QUERY_STRING']

        querydict = CustomParser.limited_parse_qsl(raw_querystring)

        queryfilter = querydict.get('$filter', None)
        queryexpand = querydict.get('$expand', None)

        if queryfilter:
            try:
                qs = parser(queryfilter, qs)
            except NotImplemented501:
                raise NotImplemented501()
            except Unprocessable:
                raise Unprocessable()
            except Exception as e:
                raise BadRequest("Malformed request: " + str(e))

        elif queryexpand:
            # Datastream.objects.filter(id=1)
            print(qs)
        return qs


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

