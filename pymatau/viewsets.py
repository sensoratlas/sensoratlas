from .models import Location, Thing, Datastream, Sensor, \
    ObservedProperty, Observation, FeatureOfInterest, HistoricalLocation
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.reverse import reverse
import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import status
from .errors import Unprocessable, BadRequest
import dateutil.parser
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.apps import apps


MODEL_KEYS = {
    "Thing": "Thing",
    "Things": "Thing",
    "Location": "Location",
    "Locations": "Location",
    "HistoricalLocation": "HistoricalLocation",
    "HistoricalLocations": "HistoricalLocation",
    "Datastream": "Datastream",
    "Datastreams": "Datastream",
    "Sensor": "Sensor",
    "Sensors": "Sensor",
    "ObservedProperty": "ObservedProperty",
    "ObservedProperties": "ObservedProperty",
    "Observation": "Observation",
    "Observations": "Observation",
    "FeatureOfInterest": "FeatureOfInterest",
    "FeaturesOfInterest": "FeatureOfInterest"
}
DEFAULT_ENCODING = "application/vnd.geo+json"
NAME_LOOKUP = {
    'thing': 'Things',
    'historicallocation': 'HistoricalLocations',
    'location': 'Locations',
    'datastream': 'Datastreams',
    'sensor': 'Sensors',
    'observedproperty': 'ObservedProperties',
    'observation': 'Observations',
    'featureofinterest': 'FeaturesOfInterest'
}
INDICES = {
    'HistoricalLocations': 'historicallocation_index',
    'Locations': 'location_index',
    'Things': 'thing_index',
    'Thing': 'thing_index',
    'Datastreams': 'datastream_index',
    'Datastream': 'datastream_index',
    'ObservedProperties': 'observedproperty_index',
    'ObservedProperty': 'observedproperty_index',
    'Sensors': 'sensor_index',
    'Sensor': 'sensor_index',
    'Observations': 'observation_index',
    'FeaturesOfInterest': 'featureofinterest_index',
    'FeatureOfInterest': 'featureofinterest_index'
}
REQUIRED_FIELDS = {
    'historicallocation': [
        'time',
        'Thing',
        'Locations'
    ],
    'location': [
        'name',
        'description',
        'encodingType',
        'location'
    ],
    'thing': [
        'name',
        'description'
    ],
    'datastream': [
        'name',
        'description',
        'unitOfMeasurement',
        'observationType',
        'Thing',
        'ObservedProperty',
        'Sensor'
    ],
    'sensor': [
        'name',
        'description',
        'encodingType',
        'metadata'
    ],
    'observedproperty': [
        'name',
        'definition',
        'description'
    ],
    'observation': [
        'result',
        'Datastream',
        'FeatureOfInterest'
    ],
    'featureofinterest': [
        'name',
        'description',
        'encodingType',
        'feature'
    ]
}


def geojson_to_geos(data):
    """
    Checks to see if either location, feature, or observedArea are in json
    object and if they are, and are a dictionary, convert geojson geometery
    to geos geometry.
    """

    def convert2geos(obj, fields):
        if isinstance(obj, dict):
            new = obj.__class__()
            for k, v in obj.items():
                if k in fields:
                    new[k] = GEOSGeometry(str(v))
                else:
                    new[k] = convert2geos(v, fields)
        elif isinstance(obj, (list, set, tuple)):
            new = obj.__class__(convert2geos(v, fields) for v in obj)
        else:
            return obj
        return new

    geometry_fields = ['location', 'feature', 'observedArea']

    geometry_fixed = convert2geos(data, geometry_fields)

    return geometry_fixed


def parse_interval_time(data):
    interval_times = ['phenomenonTime', 'resultTime', 'validTime']
    for time_obj in interval_times:
        try:
            for time in data[time_obj].split("/"):
                try:
                    dateutil.parser.parse(time)
                except ValueError:
                    raise Unprocessable()
        except KeyError:
            pass
    return data


def relate_parent(data, basename, url_kwargs):
    """
    Add parent as related entity if created entity is nested.
    """
    if list(url_kwargs.keys())[-1] != "version":
        parent = list(url_kwargs.keys())[-1]
        if parent == "Locations_pk":
            data['Locations'] = [{"@iot.id": url_kwargs[parent]}]

        if parent == "Sensors_pk":
            data['Sensor'] = {"@iot.id": url_kwargs[parent]}

        if parent == "ObservedProperties_pk":
            data['ObservedProperty'] = {"@iot.id": url_kwargs[parent]}

        if parent == "Things_pk":
            if basename == "location":
                data['Things'] = [{"@iot.id": url_kwargs[parent]}]
            else:
                data['Thing'] = {"@iot.id": url_kwargs[parent]}

        if parent == "Observations_pk":
            data['Observations'] = [{"@iot.id": url_kwargs[parent]}]

        if parent == "Datastreams_pk":
            if basename == "observation":
                data['Datastream'] = {"@iot.id": url_kwargs[parent]}
            else:
                data['Datastreams'] = [{"@iot.id": url_kwargs[parent]}]

        if parent == "FeaturesOfInterest_pk":
            data['FeatureOfInterest'] = {"@iot.id": url_kwargs[parent]}
    return data


def process_data(data, basename, url_kwargs):
    data = relate_parent(data, basename, url_kwargs)
    data = geojson_to_geos(data)
    data = parse_interval_time(data)
    if basename == 'observation':
        try:
            result = data['result']
            data['result'] = {'result': result}
            return data
        except KeyError:
            raise BadRequest()
    return data


class NestedViewSet:
    def __init__(self, **kwargs):
        if kwargs:
            self.data = process_data(kwargs["data"], kwargs["basename"], kwargs["url_kwargs"])

    def get_or_create_children(self, data, given_entity, **kwargs):
        entity = MODEL_KEYS[given_entity]
        model = apps.get_model('pymatau', entity)

        many_children = False
        if isinstance(data, dict):
            if "@iot.id" in data:
                given_id = data["@iot.id"]
                try:
                    existing_entity = model.objects.get(id=given_id)
                    return existing_entity
                except model.DoesNotExist:
                    return
            else:
                for key in MODEL_KEYS:
                    if key in data:
                        if isinstance(data[key], dict):
                            child = self.get_or_create_children(data[key], key)
                            data.pop(key)
                            data[key] = child
                        if isinstance(data[key], list):
                            children = []
                            for d in data[key]:
                                child = self.get_or_create_children(d, key)
                                children.append(child)
                            data.pop(key)
                            many_children = children
                            child_entity = key

                # TODO: check for other exceptions
                try:
                    # need to check for related fields: and create them seperately
                    new_entity, created = model.objects.get_or_create(**data)
                    if created:
                        if many_children:
                            getattr(new_entity, child_entity).add(*many_children)
                        return new_entity
                except FieldError:
                    return
        elif isinstance(data, list):
            parent_basename = kwargs["parent_basename"]
            parent_entity = kwargs["parent_entity"]

            entity_list = []
            for entity in data:
                if "@iot.id" in entity:
                    given_id = entity["@iot.id"]
                    try:
                        existing_entity = model.objects.get(id=given_id)
                        entity_list.append(existing_entity)
                    except model.DoesNotExist:
                        return
                else:
                    # TODO: run parse_interval_time(ds)
                    # first remove all related fields:
                    nested_entity_list = []
                    for key in MODEL_KEYS.keys():
                        if key in entity:
                            nested_entity_list.append({key: entity[key]})
                            entity.pop(key)

                    # now try to create:
                    for t in nested_entity_list:
                        entity[list(t.keys())[0]] = self.get_or_create(list(t.values())[0])

                    new_entity, created = model.objects.get_or_create(**entity)

                    if not created:
                        if parent_basename == given_entity:
                            entity[given_entity] = parent_entity
                            new_entity, created = model.objects.get_or_create(**entity)
                        else:
                            return
                    entity_list.append(new_entity)
            return entity_list

    def get_or_update_children(self, data, given_entity):
        entity = MODEL_KEYS[given_entity]
        model = apps.get_model('pymatau', entity)

        if isinstance(data, dict):
            if "@iot.id" in data:
                given_id = data["@iot.id"]
                try:
                    existing_entity = model.objects.get(id=given_id)
                    return existing_entity
                except model.DoesNotExist:
                    return
            else:
                raise BadRequest()
        elif isinstance(data, list):
            entity_list = []
            for entity in data:
                if "@iot.id" in entity:
                    given_id = entity["@iot.id"]
                    try:
                        existing_entity = model.objects.get(id=given_id)
                        entity_list.append(existing_entity)
                    except model.DoesNotExist:
                        # TODO: check if it should break and return nothing or append null to list
                        return
                else:
                    raise BadRequest()
            return entity_list

    def queryset_methods(self, path_list, method, kwargs):
        """
        Adds nested entites to the queryset of the current viewset, thereby
        allowing nested expansions to be properly queried.
        """
        d = {}
        if method == "list":
            cv = INDICES[path_list[-1]]
            path_list = [item.split('(')[0] for item
                         in path_list if item[-1] == ')']
        elif method == "retrieve":
            cv = INDICES[path_list[-1].split('(')[0]]
            path_list = [item.split('(')[0] for item in path_list[:-1]]
        elif method == "associationLink":
            cv = INDICES[path_list[-1]]
            path_list = [item.split('(')[0] for item
                         in path_list if item[-1] == ')']
            try:
                del kwargs['version']
            except KeyError:
                pass
        # the following works because dictionaries are ordered in Python > 3.6
        for i, (k, v) in enumerate(kwargs.items()):
            if i == len(kwargs)-1 and method == "retrieve":
                break
            path = list(reversed(path_list[i:]))
            if method == "retrieve":
                path = [x[:-1] if x[-1] == '(' else x for x in path]
            IND = {}
            try:
                IND['featureofinterest_index'] = path.index('FeaturesOfInterest') + 1
            except ValueError:
                pass
            try:
                IND['featureofinterest_index'] = path.index('FeatureOfInterest') + 1
            except ValueError:
                pass
            try:
                IND['observedproperty_index'] = path.index('ObservedProperties') + 1
            except ValueError:
                pass
            try:
                IND['observedproperty_index'] = path.index('ObservedProperty') + 1
            except ValueError:
                pass
            try:
                IND['sensor_index'] = path.index('Sensors') + 1
            except ValueError:
                pass
            try:
                IND['sensor_index'] = path.index('Sensor') + 1
            except ValueError:
                pass
            try:
                IND['thing_index'] = path.index('Things') + 1
            except ValueError:
                pass
            try:
                IND['thing_index'] = path.index('Thing') + 1
            except ValueError:
                pass
            try:
                IND['datastream_index'] = path.index('Datastreams') + 1
            except ValueError:
                pass
            try:
                IND['datastream_index'] = path.index('Datastream') + 1
            except ValueError:
                pass
            try:
                IND['historicallocation_index'] = path.index('HistoricalLocations') + 1
            except ValueError:
                pass
            try:
                IND['observation_index'] = path.index('Observations') + 1
            except ValueError:
                pass
            try:
                IND['location_index'] = path.index('Locations') + 1
            except ValueError:
                pass
            IND[cv] = 0
            # Datastreams
            try:
                if IND['sensor_index'] > IND['datastream_index']:
                    path[IND['sensor_index'] - 1] = 'Sensor'
            except KeyError:
                pass
            try:
                if IND['thing_index'] > IND['datastream_index']:
                    path[IND['thing_index'] - 1] = 'Thing'
            except KeyError:
                pass
            try:
                if IND['observedproperty_index'] > IND['datastream_index']:
                    path[IND['observedproperty_index'] - 1] = 'ObservedProperty'
            except KeyError:
                pass
            # Locations
            try:
                if IND['thing_index'] > IND['location_index']:
                    path[IND['thing_index'] - 1] = 'Things'
            except KeyError:
                pass
            # Historical Locations
            try:
                if IND['location_index'] > IND['historicallocation_index']:
                    path[IND['location_index'] - 1] = 'Locations'
            except KeyError:
                pass
            try:
                if IND['thing_index'] > IND['historicallocation_index']:
                    path[IND['thing_index'] - 1] = 'Thing'
            except KeyError:
                pass
            try:
                if IND['datastream_index'] > IND['observation_index']:
                    path[IND['datastream_index'] - 1] = 'Datastream'
            except KeyError:
                pass

            try:
                if IND['datastream_index'] > IND['sensor_index']:
                    path[IND['datastream_index'] - 1] = 'Datastreams'
            except KeyError:
                pass

            try:
                if IND['datastream_index'] > IND['observedproperty_index']:
                    path[IND['datastream_index'] - 1] = 'Datastreams'
            except KeyError:
                pass

            try:
                if IND['datastream_index'] > IND['thing_index']:
                    path[IND['datastream_index'] - 1] = 'Datastreams'
            except KeyError:
                pass

            try:
                if IND['featureofinterest_index'] > IND['observation_index']:
                    path[IND['featureofinterest_index'] - 1] = 'FeatureOfInterest'
            except KeyError:
                pass
            try:
                if IND['location_index'] < IND['thing_index'] and IND['location_index'] != 0:
                    path[IND['location_index'] - 1] = 'Locations'
                    if IND['thing_index'] > IND['historicallocation_index']:
                        path[IND['thing_index'] - 1] = 'Things'
            except KeyError:
                pass

            field = '__'.join(path)
            d[field] = v
        return d

    def get_or_update_related(self):
        d = {}
        for key in MODEL_KEYS:
            if key in self.data:
                child = self.get_or_update_children(self.data[key], key)
                if child:
                    d[key] = child
        return d

    def get_or_create_related(self, basename, serializer):
        d = {}
        for key in MODEL_KEYS:
            if key in self.data:
                if isinstance(self.data[key], dict):
                    child = self.get_or_create_children(self.data[key], key)
                    if child:
                        d[key] = child
                if isinstance(self.data[key], list):
                    xData = self.data[key]
                    xBasename = NAME_LOOKUP[basename]
                    # TODO: add special case for locations/historicallocations? (not necessay if HistoricalLocation.Thing can be null)
                    entity = serializer.save()
                    child = self.get_or_create_children(
                        xData,
                        key,
                        parent_basename=xBasename,
                        parent_entity=entity
                    )
                    if child:
                        d[key] = child
        return d

    def create_missing_featureofinterest(self):
        if 'Datastreams' in self.data:
            ds = self.data['Datastreams']
            if len(ds) == 1:
                datastream = self.get_or_create_children(ds[0], "Datastreams")
        elif 'Datastream' in self.data:
            ds = self.data['Datastream']
            datastream = self.get_or_create_children(ds, "Datastream")
        if datastream:
            try:
                location = datastream.Thing.Locations.get(
                            encodingType=DEFAULT_ENCODING
                            )
                featureofinterest = FeatureOfInterest.objects.create(
                            name=location.name,
                            description=location.description,
                            encodingType=location.encodingType,
                            feature=location.location
                )
                return featureofinterest
            except ObjectDoesNotExist:
                raise BadRequest()


class ViewSet(viewsets.ModelViewSet):
    """
    Overrides the DRF ModelViewSet methods of list, retrieve, and create, update.
    """
    def list(self, request, version, **kwargs):
        path = request._request.path
        path_list = path.split('/')[3:]
        method = 'list'
        vs = NestedViewSet()
        d = vs.queryset_methods(path_list, method, kwargs)
        queryset = self.get_queryset().filter(**d)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        single_link = ['Thing', 'Sensor', 'ObservedProperty', 'Datastream',
                       'FeatureOfInterest']
        if page is not None:
            if len(path_list) > 1 and path_list[-1] in single_link:
                id = queryset[0].id
                location = get_object_or_404(queryset, pk=id)
                serializer = self.get_serializer(location)
                return Response(serializer.data)
            else:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        if len(path_list) > 1 and path_list[-1] in single_link:
            id = queryset[0].id
            location = get_object_or_404(queryset, pk=id)
            serializer = self.get_serializer(location)
            return Response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, version, **kwargs):
        path = request._request.path
        path_list = path.split('/')[3:]
        method = 'retrieve'
        vs = NestedViewSet()
        d = vs.queryset_methods(path_list, method, kwargs)
        d['pk'] = kwargs['pk']
        queryset = self.get_queryset().filter(**d)
        queryset = self.filter_queryset(queryset)
        location = get_object_or_404(queryset, pk=d['pk'])
        serializer = self.get_serializer(location)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # TODO: in POST of anything with a time, I think timezones are ignored. Need to test.
        """
        Override the create method to allow related entity creation.
        """
        data = request.data
        if isinstance(data, list):
            raise Unprocessable()
        basename = self.basename
        vs = NestedViewSet(data=data, basename=basename, url_kwargs=kwargs)
        if basename == 'observation' and 'FeatureOfInterest' not in vs.data:
            foi = vs.create_missing_featureofinterest()
            vs.data["FeatureOfInterest"] = {"@iot.id": foi.id}

        for entity, fields in REQUIRED_FIELDS.items():
            if entity == basename:
                for field in fields:
                    if field not in vs.data:
                        raise BadRequest()

        serializer = self.get_serializer(data=vs.data)

        if serializer.is_valid(raise_exception=True):
            d = vs.get_or_create_related(
                basename,
                serializer
            )
            if d:
                serializer.save(**d)
            else:
                self.perform_create(serializer)
        response = Response(
            {"Location": serializer.data['@iot.selfLink']},
            status=status.HTTP_201_CREATED
        )
        return response

    def update(self, request, *args, **kwargs):
        """
        Override the patch method to allow related entity updates when
        appropriate.
        """
        super(ViewSet, self).update(request, *args, **kwargs)
        if request._request.method == 'PATCH':
            data = request.data
            basename = self.basename
            vs = NestedViewSet(data=data, basename=basename, url_kwargs=kwargs)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=vs.data, partial=True)
            serializer.is_valid(raise_exception=True)
            d = vs.get_or_update_related()
            if d:
                serializer.save(**d)
            else:
                serializer.save()
            return Response(
                    {"Location": serializer.data['@iot.selfLink']},
                    status=status.HTTP_200_OK
                    )
        if request._request.method == 'PUT':
            raise BadRequest("Method PUT is not allowed. Please use PATCH.")


class PropertyPath(object):
    """
    Address to a property of an entity.
    """
    class Thing:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, version, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('thing-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='name')
        def get_name(self, request, version, **kwargs):
            """
            Returns the name JSON of the current entity
            """
            entity = self.get_object()
            namae = {'name': entity.name}
            return Response(namae)

        @action(detail=True, url_path=r'name/\$value')
        def get_name_value(self, request, version, **kwargs):
            """
            Returns the name value of the current entity
            """
            entity = self.get_object()
            namae = entity.name
            return Response(namae)

        @action(detail=True, url_path='description')
        def get_description(self, request, version, **kwargs):
            """
            Returns the description JSON of the current entity
            """
            entity = self.get_object()
            descript = {'description': entity.description}
            return Response(descript)

        @action(detail=True, url_path=r'description/\$value')
        def get_description_value(self, request, version, **kwargs):
            """
            Returns the description value of the current entity
            """
            entity = self.get_object()
            descript = entity.description
            return Response(descript)

        @action(detail=True, url_path='properties')
        def get_properties(self, request, version, **kwargs):
            """
            Returns the properties JSON of the current entity
            """
            entity = self.get_object()
            properti = {'properties': entity.properties}
            return Response(properti)

        @action(detail=True, url_path=r'properties/\$value')
        def get_properties_value(self, request, version, **kwargs):
            """
            Returns the properties value of the current entity
            """
            entity = self.get_object()
            properti = entity.properties
            return Response(properti)

    class Location:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, version, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('location-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='name')
        def get_name(self, request, version, **kwargs):
            """
            Returns the name JSON of the current entity
            """
            entity = self.get_object()
            namae = {'name': entity.name}
            return Response(namae)

        @action(detail=True, url_path=r'name/\$value')
        def get_name_value(self, request, version, **kwargs):
            """
            Returns the name value of the current entity
            """
            entity = self.get_object()
            namae = entity.name
            return Response(namae)

        # get_description
        @action(detail=True, url_path='description')
        def get_description(self, request, version, **kwargs):
            """
            Returns the description JSON of the current entity
            """
            entity = self.get_object()
            descript = {'description': entity.description}
            return Response(descript)

        @action(detail=True, url_path=r'description/\$value')
        def get_description_value(self, request, version, **kwargs):
            """
            Returns the description value of the current entity
            """
            entity = self.get_object()
            descript = entity.description
            return Response(descript)

        # get_encodingType
        @action(detail=True, url_path='encodingType')
        def get_encodingType(self, request, version, **kwargs):
            """
            Returns the encoding type JSON of the current entity
            """
            entity = self.get_object()
            encoding = {'encodingType': entity.encodingType}
            return Response(encoding)

        @action(detail=True, url_path=r'encodingType/\$value')
        def get_encodingType_value(self, request, version, **kwargs):
            """
            Returns the encoding type value of the current entity
            """
            entity = self.get_object()
            encoding = entity.encodingType
            return Response(encoding)

        # get_location
        @action(detail=True, url_path='location')
        def get_location(self, request, version, **kwargs):
            """
            Returns the location JSON of the current entity
            """
            entity = self.get_object()
            locat = {'location': json.loads(entity.location.geojson)}
            return Response(locat)

        @action(detail=True, url_path=r'location/\$value')
        def get_location_value(self, request, version, **kwargs):
            """
            Returns the location value of the current entity
            """
            entity = self.get_object()
            locat = json.loads(entity.location.geojson)
            return Response(locat)

    class HistoricalLocation:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, version, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('historicallocation-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='time')
        def get_historicallocationtime(self, request, version, **kwargs):
            """
            Returns the historical location time JSON of the current entity
            """
            entity = self.get_object()
            tim = {'time': entity.time}
            return Response(tim)

        @action(detail=True, url_path=r'time/\$value')
        def get_historicallocationtime_value(self, request, version, **kwargs):
            """
            Returns the historical location time value of the current entity
            """
            entity = self.get_object()
            tim = entity.time
            return Response(tim)

    class Datastream:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, version, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('datastream-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='name')
        def get_name(self, request, version, **kwargs):
            """
            Returns the name JSON of the current entity
            """
            entity = self.get_object()
            namae = {'name': entity.name}
            return Response(namae)

        @action(detail=True, url_path=r'name/\$value')
        def get_name_value(self, request, **kwargs):
            """
            Returns the name value of the current entity
            """
            entity = self.get_object()
            namae = entity.name
            return Response(namae)

        @action(detail=True, url_path='description')
        def get_description(self, request, **kwargs):
            """
            Returns the description JSON of the current entity
            """
            entity = self.get_object()
            descript = {'description': entity.description}
            return Response(descript)

        @action(detail=True, url_path=r'description/\$value')
        def get_description_value(self, request, **kwargs):
            """
            Returns the description value of the current entity
            """
            entity = self.get_object()
            descript = entity.description
            return Response(descript)

        @action(detail=True, url_path='unitOfMeasurement')
        def get_unitOfMeasurement(self, request, **kwargs):
            """
            Returns the unitOfMeasurement JSON of the current entity
            """
            entity = self.get_object()
            unitmeasure = {'unitOfMeasurement': entity.unitOfMeasurement}
            return Response(unitmeasure)

        @action(detail=True, url_path=r'unitOfMeasurement/\$value')
        def get_unitOfMeasurement_value(self, request, **kwargs):
            """
            Returns the unitOfMeasurement value of the current entity
            """
            entity = self.get_object()
            unitmeasure = entity.unitOfMeasurement
            return Response(unitmeasure)

        @action(detail=True, url_path='observationType')
        def get_observationType(self, request, **kwargs):
            """
            Returns the observationType JSON of the current entity
            """
            entity = self.get_object()
            observedtype = {'observationType': entity.observationType}
            return Response(observedtype)

        @action(detail=True, url_path=r'observationType/\$value')
        def observationType_value(self, request, **kwargs):
            """
            Returns the observationType value of the current entity
            """
            entity = self.get_object()
            observedtype = entity.observationType
            return Response(observedtype)

        @action(detail=True, url_path='observedArea')
        def get_observedArea(self, request, **kwargs):
            """
            Returns the observedArea JSON of the current entity
            """
            entity = self.get_object()
            if entity.observedArea:
                observedarea = {'observedArea': json.loads(entity.observedArea.geojson)}
            else:
                observedarea = {'observedArea': None}
            return Response(observedarea)

        @action(detail=True, url_path=r'observedArea/\$value')
        def observedArea_value(self, request, **kwargs):
            """
            Returns the observedArea value of the current entity
            """
            entity = self.get_object()
            if entity.observedArea:
                observedarea = json.loads(entity.observedArea.geojson)
            else:
                observedarea = None
            return Response(observedarea)

        @action(detail=True, url_path='phenomenonTime')
        def get_phenomenonTime(self, request, **kwargs):
            """
            Returns the phenomenonTime JSON of the current entity
            """
            entity = self.get_object()
            phenomenontime = {'phenomenonTime': entity.phenomenonTime}
            return Response(phenomenontime)

        @action(detail=True, url_path=r'phenomenonTime/\$value')
        def phenomenonTime_value(self, request, **kwargs):
            """
            Returns the phenomenonTime value of the current entity
            """
            entity = self.get_object()
            phenomenontime = entity.phenomenonTime
            return Response(phenomenontime)

        @action(detail=True, url_path='resultTime')
        def get_resultTime(self, request, **kwargs):
            """
            Returns the resultTime JSON of the current entity
            """
            entity = self.get_object()
            resulttime = {'resultTime': entity.resultTime}
            return Response(resulttime)

        @action(detail=True, url_path=r'resultTime/\$value')
        def resultTime_value(self, request, **kwargs):
            """
            Returns the resultTime value of the current entity
            """
            entity = self.get_object()
            resulttime = entity.resultTime
            return Response(resulttime)

    class Sensor:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('sensor-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='name')
        def get_name(self, request, version, **kwargs):
            """
            Returns the name JSON of the current entity
            """
            entity = self.get_object()
            namae = {'name': entity.name}
            return Response(namae)

        @action(detail=True, url_path=r'name/\$value')
        def get_name_value(self, request, version, **kwargs):
            """
            Returns the name value of the current entity
            """
            entity = self.get_object()
            namae = entity.name
            return Response(namae)

        @action(detail=True, url_path='description')
        def get_description(self, request, version, **kwargs):
            """
            Returns the description JSON of the current entity
            """
            entity = self.get_object()
            descript = {'description': entity.description}
            return Response(descript)

        @action(detail=True, url_path=r'description/\$value')
        def get_description_value(self, request, version, **kwargs):
            """
            Returns the description value of the current entity
            """
            entity = self.get_object()
            descript = entity.description
            return Response(descript)

        @action(detail=True, url_path='encodingType')
        def get_encodingType(self, request, **kwargs):
            """
            Returns the encoding type JSON of the current entity
            """
            entity = self.get_object()
            encoding = {'encodingType': entity.encodingType}
            return Response(encoding)

        @action(detail=True, url_path=r'encodingType/\$value')
        def get_encodingType_value(self, request, **kwargs):
            """
            Returns the encoding type value of the current entity
            """
            entity = self.get_object()
            encoding = entity.encodingType
            return Response(encoding)

        @action(detail=True, url_path='metadata')
        def get_metadata(self, request, **kwargs):
            """
            Returns the metadata JSON of the current entity
            """
            entity = self.get_object()
            metadat = {'metadata': entity.metadata}
            return Response(metadat)

        @action(detail=True, url_path=r'metadata/\$value')
        def get_metadata_value(self, request, **kwargs):
            """
            Returns the metadata value of the current entity
            """
            entity = self.get_object()
            metadat = entity.metadata
            return Response(metadat)

    class ObservedProperty:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('observedproperty-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='name')
        def get_name(self, request, version, **kwargs):
            """
            Returns the name JSON of the current entity
            """
            entity = self.get_object()
            namae = {'name': entity.name}
            return Response(namae)

        @action(detail=True, url_path=r'name/\$value')
        def get_name_value(self, request, version, **kwargs):
            """
            Returns the name value of the current entity
            """
            entity = self.get_object()
            namae = entity.name
            return Response(namae)

        @action(detail=True, url_path='definition')
        def get_definition(self, request, **kwargs):
            """
            Returns the definition JSON of the current entity
            """
            entity = self.get_object()
            definitn = {'definition': entity.definition}
            return Response(definitn)

        @action(detail=True, url_path=r'definition/\$value')
        def get_definition_value(self, request, **kwargs):
            """
            Returns the definition value of the current entity
            """
            entity = self.get_object()
            definitn = entity.definition
            return Response(definitn)

        @action(detail=True, url_path='description')
        def get_description(self, request, version, **kwargs):
            """
            Returns the description JSON of the current entity
            """
            entity = self.get_object()
            descript = {'description': entity.description}
            return Response(descript)

        @action(detail=True, url_path=r'description/\$value')
        def get_description_value(self, request, version, **kwargs):
            """
            Returns the description value of the current entity
            """
            entity = self.get_object()
            descript = entity.description
            return Response(descript)

    class Observation:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('observation-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='phenomenonTime')
        def get_phenomenonTime(self, request, **kwargs):
            """
            Returns the phenomenonTime JSON of the current entity
            """
            entity = self.get_object()
            phenomenontime = {'phenomenonTime': entity.phenomenonTime}
            return Response(phenomenontime)

        @action(detail=True, url_path=r'phenomenonTime/\$value')
        def get_phenomenonTime_value(self, request, **kwargs):
            """
            Returns the phenomenonTime value of the current entity
            """
            entity = self.get_object()
            phenomenontime = entity.phenomenonTime
            return Response(phenomenontime)

        @action(detail=True, url_path='result')
        def get_result(self, request, **kwargs):
            """
            Returns the result JSON of the current entity
            """
            entity = self.get_object()
            rezult = {'result': entity.result}
            return Response(rezult)

        @action(detail=True, url_path=r'result/\$value')
        def get_result_value(self, request, **kwargs):
            """
            Returns the result value of the current entity
            """
            entity = self.get_object()
            rezult = entity.result
            return Response(rezult)

        @action(detail=True, url_path='resultTime')
        def get_resultTime(self, request, **kwargs):
            """
            Returns the resultTime JSON of the current entity
            """
            entity = self.get_object()
            resulttime = {'resultTime': entity.resultTime}
            return Response(resulttime)

        @action(detail=True, url_path=r'resultTime/\$value')
        def get_resultTime_value(self, request, **kwargs):
            """
            Returns the resultTime value of the current entity
            """
            entity = self.get_object()
            resulttime = entity.resultTime
            return Response(resulttime)

        @action(detail=True, url_path='resultQuality')
        def get_resultQuality(self, request, **kwargs):
            """
            Returns the resultQuality JSON of the current entity
            """
            entity = self.get_object()
            resultquality = {'resultQuality': entity.resultQuality}
            return Response(resultquality)

        @action(detail=True, url_path=r'resultQuality/\$value')
        def get_resultQuality_value(self, request, **kwargs):
            """
            Returns the resultQuality value of the current entity
            """
            entity = self.get_object()
            resultquality = entity.resultQuality
            return Response(resultquality)

        @action(detail=True, url_path='validTime')
        def get_validTime(self, request, **kwargs):
            """
            Returns the validTime JSON of the current entity
            """
            entity = self.get_object()
            validtime = {'validTime': entity.validTime}
            return Response(validtime)

        @action(detail=True, url_path=r'validTime/\$value')
        def get_validTime_value(self, request, **kwargs):
            """
            Returns the validTime value of the current entity
            """
            entity = self.get_object()
            validtime = entity.validTime
            return Response(validtime)

        @action(detail=True, url_path='parameters')
        def get_parameters(self, request, **kwargs):
            """
            Returns the parameters JSON of the current entity
            """
            entity = self.get_object()
            parameters = {'parameters': entity.parameters}
            return Response(parameters)

        @action(detail=True, url_path=r'parameters/\$value')
        def get_parameters_value(self, request, **kwargs):
            """
            Returns the parameters value of the current entity
            """
            entity = self.get_object()
            parameters = entity.parameters
            return Response(parameters)

    class FeatureOfInterest:
        @action(detail=False, url_path=r'\$ref')
        def get_association_link(self, request, **kwargs):
            """
            Returns the address to an association link.
            """
            path = request._request.path
            path_list = path.split('/')[3:-1]
            method = "associationLink"
            vs = NestedViewSet()
            d = vs.queryset_methods(path_list, method, kwargs)
            queryset = self.get_queryset().filter(**d)
            queryset = self.filter_queryset(queryset)
            d = []
            for o in queryset:
                d.append({'@iot.selfLink': reverse('featureofinterest-detail',
                                                   kwargs={'pk': o.pk},
                                                   request=request)})
            return Response({"value": d})

        @action(detail=True, url_path='name')
        def get_name(self, request, version, **kwargs):
            """
            Returns the name JSON of the current entity
            """
            entity = self.get_object()
            namae = {'name': entity.name}
            return Response(namae)

        @action(detail=True, url_path=r'name/\$value')
        def get_name_value(self, request, version, **kwargs):
            """
            Returns the name value of the current entity
            """
            entity = self.get_object()
            namae = entity.name
            return Response(namae)

        @action(detail=True, url_path='description')
        def get_description(self, request, version, **kwargs):
            """
            Returns the description JSON of the current entity
            """
            entity = self.get_object()
            descript = {'description': entity.description}
            return Response(descript)

        @action(detail=True, url_path=r'description/\$value')
        def get_description_value(self, request, version, **kwargs):
            """
            Returns the description value of the current entity
            """
            entity = self.get_object()
            descript = entity.description
            return Response(descript)

        @action(detail=True, url_path='encodingType')
        def get_encodingType(self, request, **kwargs):
            """
            Returns the encoding type JSON of the current entity
            """
            entity = self.get_object()
            encoding = {'encodingType': entity.encodingType}
            return Response(encoding)

        @action(detail=True, url_path=r'encodingType/\$value')
        def get_encodingType_value(self, request, **kwargs):
            """
            Returns the encoding type value of the current entity
            """
            entity = self.get_object()
            encoding = entity.encodingType
            return Response(encoding)

        @action(detail=True, url_path='feature')
        def get_feature(self, request, **kwargs):
            """
            Returns the feature JSON of the current entity
            """
            entity = self.get_object()
            feat = {'feature': json.loads(entity.feature.geojson)}
            return Response(feat)

        @action(detail=True, url_path=r'feature/\$value')
        def get_feature_value(self, request, **kwargs):
            """
            Returns the feature value of the current entity
            """
            entity = self.get_object()
            feat = json.loads(entity.feature.geojson)
            return Response(feat)
