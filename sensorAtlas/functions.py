import operator

from django.db.models import Q, Lookup, Func, CharField, TextField, F, Value
from django.db.models.fields import FloatField, IntegerField, Field
from django.db.models.functions import Length, Lower, Upper


class CustomFunctions:
    """
    blah
    """
    class FractionalSecond(Func):
        output_field = FloatField()
        template = "EXTRACT(SECOND FROM %(expressions)s)::decimal % 1"


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
        django_function = CustomFunctions.FractionalSecond
        field = parameterstring
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def offsetminutes(parameterstring, **kwargs):
        d = dict()
        django_function = CustomFunctions.ExtractMinutes
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
        # TODO: this only looks up aware times in a query if the django settings timezone matches the query one.
        django_function = '__time'
        field = parameterstring
        if field == 'result':
            field = 'result__result'
        d = dict()
        d['query_field'] = field + django_function
        return d

    def round(parameterstring, **kwargs):
        d = dict()
        django_function = CustomFunctions.Round
        field = parameterstring
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def floor(parameterstring, **kwargs):
        d = dict()
        django_function = CustomFunctions.Floor
        field = parameterstring
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def ceiling(parameterstring, **kwargs):
        d = dict()
        django_function = CustomFunctions.Ceiling
        field = parameterstring
        temporary_field = "temp" + str(kwargs['index'])
        d['query_field'] = temporary_field
        d['annotation'] = {temporary_field: django_function(field)}
        return d

    def geo_distance(parameterstring, **kwargs):
        d = dict()
        django_function = CustomFunctions.ST_Distance
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
        django_function = CustomFunctions.ST_Length
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
                value = operator.add(CustomFunctions.NullIf(field), num)
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
                value = operator.sub(CustomFunctions.NullIf(field), num)
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
                value = operator.mul(CustomFunctions.NullIf(field), num)
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
                value = operator.truediv(CustomFunctions.NullIf(field), num)
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
                value = operator.mod(CustomFunctions.NullIf(field), num)
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


