import operator
from abc import ABC

from django.db.models import Q, Lookup, Func, CharField, TextField, F, Value
from django.db.models.fields import FloatField, IntegerField, Field
from django.db.models.functions import Length, Lower, Upper


class FractionalSecond(Func, ABC):
    output_field = FloatField()
    template = "EXTRACT(SECOND FROM %(expressions)s)::decimal % 1"


class ExtractMinutes(Func, ABC):
    output_field = IntegerField()
    template = "EXTRACT('timezone_minute' FROM %(expressions)s)"


class Round(Func, ABC):
    function = 'ROUND'
    template = "%(function)s(NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', " \
               "'g'), '')::numeric) "


class Floor(Func, ABC):
    function = 'FLOOR'
    template = "%(function)s(NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', " \
               "'g'), '')::numeric) "


class Ceiling(Func, ABC):
    function = 'CEILING'
    template = "%(function)s(NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', " \
               "'g'), '')::numeric) "


class STDistance(Func, ABC):
    function = 'ST_Distance'
    output_field = FloatField()
    template = '%(function)s(%(expressions)s)'


class STLength(Func, ABC):
    function = 'ST_Length'
    output_field = FloatField()
    template = '%(function)s(%(expressions)s)'


class NullIf(Func, ABC):
    template = "NULLIF(REGEXP_REPLACE((%(expressions)s::json->'result')::text, '^(?![0-9.]*$).+$', '', 'g'), " \
               "'')::numeric "


def remove_quotes(string):
    if (string[0] == "'" or string[0] == '"') and (string[-1] == "'" or string[-1] == '"'):
        return string[1:-1]
    return string


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

    def substringof(self, **kwargs):
        """
        Returns the queryset based on a case-sensitive containment test.
        """
        django_function = '__contains'
        parsedlist = self.split(',')
        # need to do some validation: only accept two arguments!
        string_index = [i for i, s in enumerate(parsedlist) if s[0] == "'" and s[-1] == "'"]
        field_index = [i for i, s in enumerate(parsedlist) if s[0] != "'" or s[-1] != "'"]

        string = parsedlist[string_index[0]]
        field = parsedlist[field_index[0]]

        if field == 'result':
            field = 'result__result'

        # todo: raise error instead of below
        string = remove_quotes(string)

        d = dict()
        d["query"] = Q(**{field + django_function: string})
        return d

    def endswith(self, **kwargs):
        """
        Returns the queryset for entries that are True for case-sensitive
        ends-with.
        """
        django_function = '__endswith'
        parsedlist = self.split(',')
        field = parsedlist[0]
        if field == 'result':
            field = 'result__result'
        string = parsedlist[1]

        # todo: raise error instead of below
        string = remove_quotes(string)

        d = dict()
        d["query"] = Q(**{field + django_function: string})
        return d

    def startswith(self, **kwargs):
        """
        Returns the queryset for entries that are True for case-sensitive
        starts-with.
        """
        django_function = '__startswith'
        parsedlist = self.split(',')
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

    def length(self, **kwargs):
        """
        Wraps the query with the PostgreSQL Length function and
        registers as a transform.
        """
        django_function = '__length'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def tolower(self, **kwargs):
        """
        Wraps the query with the PostgreSQL Lower function and
        registers as a transform.
        """
        django_function = '__lower'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def toupper(self, **kwargs):
        """
        Wraps the query with the PostgreSQL Upper function and
        registers as a transform.
        """
        django_function = '__upper'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def year(self, **kwargs):
        django_function = '__year'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def month(self, **kwargs):
        django_function = '__month'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def day(self, **kwargs):
        django_function = '__day'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def hour(self, **kwargs):
        django_function = '__hour'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def minute(self, **kwargs):
        django_function = '__minute'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def second(self, **kwargs):
        django_function = '__second'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def millisecond(self, **kwargs):
        d = dict()
        django_function = FractionalSecond
        field = self
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def offsetminutes(self, **kwargs):
        d = dict()
        django_function = ExtractMinutes
        field = self
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def date(self, **kwargs):
        django_function = '__date'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def time(self, **kwargs):
        # TODO: this only looks up aware times in a query if the django settings timezone matches the query one.
        django_function = '__time'
        field = self
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def round(self, **kwargs):
        d = dict()
        django_function = Round
        field = self
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def floor(self, **kwargs):
        d = dict()
        django_function = Floor
        field = self
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def ceiling(self, **kwargs):
        d = dict()
        django_function = Ceiling
        field = self
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def geo_distance(self, **kwargs):
        d = dict()
        django_function = STDistance
        parsedlist = self.split(',')
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

    def geo_length(self, **kwargs):
        d = dict()
        django_function = STLength
        field = self
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def st_equals(self, **kwargs):
        django_function = '__equals'
        field = self.split(',')[0]
        geometry = self.split("'")[1]
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query'] = Q(**{field + django_function: geometry})
        return d

    def st_within(self, **kwargs):
        django_function = '__within'
        field = self.split(',')[0]
        geometry = self.split("'")[1]
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
        "substringof": substringof,
        "endswith": endswith,
        "startswith": startswith,
        "length": length,
        "tolower": tolower,
        "toupper": toupper,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "second": second,
        "fractionalseconds": millisecond,
        "totaloffsetminutes": offsetminutes,
        "date": date,
        "time": time,
        "round": round,
        "floor": floor,
        "ceiling": ceiling,
        "geo.distance": geo_distance,
        "geo.length": geo_length,
        "geo.intersects": st_intersects,
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


class QueryOperations:
    """
    Built-in filter operatations of the Sensor Things API.
    """

    class NotEqual(Lookup, ABC):
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
