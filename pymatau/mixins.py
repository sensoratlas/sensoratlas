import re
from expander import ExpanderSerializerMixin
from rest_framework import serializers
from .utils import dict_from_qs, qs_from_dict
from .errors import Conflicts, NotImplemented501
from .parsers import CustomParser


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


class ResultFormat(object):
    def __init__(self, *args, **kwargs):
        super(ResultFormat, self).__init__(*args, **kwargs)
        resultFormat = self.context['request'].query_params.get('$resultFormat')
        if resultFormat:
            raise NotImplemented501()
