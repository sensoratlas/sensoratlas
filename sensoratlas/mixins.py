from expander import ExpanderSerializerMixin
from rest_framework import serializers
from .utils import dict_from_qs, qs_from_dict
from .errors import Conflicts, NotImplemented501
from .parsers import CustomParser
from rest_framework.reverse import reverse
import json
from .models import Datastream


class ControlInformation:
    keys = {
        "Thing": [
            "thing",
            "Things_pk",
            [
                {'datastream': 'Datastreams'},
                {'location': 'Locations'},
                {'historicallocation': 'HistoricalLocations'}
            ]
        ],
        "Location": [
            "location",
            "Locations_pk",
            [
                {'thing': 'Things'},
                {'historicallocation': 'HistoricalLocations'}
            ]
        ],
        "HistoricalLocation": [
            "historicallocation",
            "HistoricalLocations_pk",
            [
                {"thing": "Things"},
                {'location': 'Locations'}
            ]
        ],
        "Datastream": [
            "datastream",
            "Datastreams_pk",
            [
                {'sensor': "Sensors"},
                {'observedproperty': "ObservedProperties"},
                {'thing': "Things"},
                {"observation": "Observations"}
            ]
        ],
        "Sensor": [
            "sensor",
            "Sensors_pk",
            [
                {"datastream": 'Datastreams'}
            ]
        ],
        "ObservedProperty": [
            "observedproperty",
            "ObservedProperties_pk",
            [
                {"datastream": 'Datastreams'}
            ]
        ],
        "Observation": [
            "observation",
            "Observations_pk",
            [
                {"datastream": 'Datastreams'},
                {"featureofinterest": 'FeaturesOfInterest'}
            ]
        ],
        "FeatureOfInterest": [
            "featureofinterest",
            "FeaturesOfInterest_pk",
            [
                {"observation": "Observations"}
            ]
        ]
    }

    def get_selfLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        return request.build_absolute_uri(
                    reverse(ControlInformation.keys[model][0] + '-detail',
                            kwargs={'pk': obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_navigationLinks(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        nav_links = {}
        model_kwarg = ControlInformation.keys[model][1]
        for related_entity in ControlInformation.keys[model][2]:
            nav_links[list(related_entity.values())[0] + '@iot.navigationLink'] = request.build_absolute_uri(
                    reverse(list(related_entity.keys())[0] + '-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )
        return nav_links

    def to_representation(self, obj):
        """
        doc string here
        :param obj:
        :return:
        """
        data = super(ControlInformation, self).to_representation(obj)
        # have to rename plural fields ...

        model = self.Meta.model.__name__
        if model == "Thing":
            try:
                data['Datastreams'] = data["Datastream"]
                data.pop('Datastream')
            except KeyError:
                pass
            try:
                data['Locations'] = data["Location"]
                data.pop("Location")
            except KeyError:
                pass
            try:
                data['HistoricalLocations'] = data["HistoricalLocation"]
                data.pop('HistoricalLocation')
            except KeyError:
                pass

        if model == "Datastream":
            try:
                data['Observations'] = data["Observation"]
                data.pop('Observation')
            except KeyError:
                pass

        if model == "FeatureOfInterest":
            try:
                data['Observations'] = data["Observation"]
                data.pop('Observation')
            except KeyError:
                pass

        if model == "Location":
            try:
                data['Things'] = data["Thing"]
                data.pop('Thing')
            except KeyError:
                pass
            try:
                data['HistoricalLocations'] = data["HistoricalLocation"]
                data.pop('HistoricalLocation')
            except KeyError:
                pass

        if model == "HistoricalLocation":
            try:
                data['Things'] = data["Thing"]
                data.pop('Thing')
            except KeyError:
                pass
            try:
                data['Locations'] = data["Location"]
                data.pop('Location')
            except KeyError:
                pass

        try:
            data['@iot.selfLink'] = data['selfLink']
            data.pop('selfLink')
            data.move_to_end('@iot.selfLink', last=False)
        except KeyError:
            pass
        try:
            data['@iot.id'] = data['id']
            data.pop('id')
            data.move_to_end('@iot.id', last=False)
        except KeyError:
            pass

        try:
            for navigation_key, navigation_value in data['navigationLinks'].items():
                data[navigation_key] = navigation_value
            data.pop('navigationLinks')
        except KeyError:
            pass

        if 'observedArea' in data:
            if obj.observedArea:
                data['observedArea'] = json.loads(obj.observedArea.geojson)
        if 'feature' in data:
            if obj.feature:
                data['feature'] = json.loads(obj.feature.geojson)
        if 'location' in data:
            if obj.location:
                data['location'] = json.loads(obj.location.geojson)
        if 'result' in data:
            data['result'] = obj.result['result']
        return data


class Expand(ExpanderSerializerMixin):
    """
    Extends and modifies the ExpanderSerializerMixin class to define the
    $expand query option. Use $expand query option to request inline
    information for related entities of the requested entity collection.
    """
    def __init__(self, *args, **kwargs):
        expanded_fields = kwargs.pop('expanded_fields', None)
        get_expandable_fields = getattr(self.Meta, 'get_expandable_fields', None)

        super().__init__(*args, **kwargs)

        if not get_expandable_fields:
            return

        if not expanded_fields:
            context = self.context
            if not context:
                return

            request = context.get('request', None)
            if not request:
                return

            raw_querystring = request.META['QUERY_STRING']

            querydict = CustomParser.limited_parse_qsl(raw_querystring)
            expanded_fields = querydict.get('$expand', None)

            if not expanded_fields:
                return

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

                print("context", context)

                if issubclass(serializer_class, Expand):
                    serializer = serializer_class(
                        expanded_fields=qs_from_dict(nested_expand),
                        *args,
                        **kwargs
                    )
                else:
                    serializer = serializer_class(
                        *args,
                        **kwargs
                    )

                print(serializer)
                print(serializer.__dict__)

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
            print("existing", existing)
            for selected in existing - allowed:
                # not self.fields --> this does all fields. It shuold be the fields in the unnested serializer
                self.fields.pop(selected)


class ResultFormat(object):
    def __init__(self, *args, **kwargs):
        super(ResultFormat, self).__init__(*args, **kwargs)
        resultFormat = self.context['request'].query_params.get('$resultFormat')
        if resultFormat:
            raise NotImplemented501()
