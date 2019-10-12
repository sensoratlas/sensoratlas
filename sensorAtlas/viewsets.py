from .models import Location, Thing, DataStream, Sensor, \
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
from django.core.exceptions import ObjectDoesNotExist


class PostRelations(object):
    """
    Gets or creates nested entities given either entity details or entity id.
    """
    def get_or_update_sensor(data):
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                sensor = Sensor.objects.get(id=id)
                return sensor
            except Sensor.DoesNotExist:
                return
        except KeyError:
            raise BadRequest()

    def get_or_update_observedproperty(data):
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                observedproperty = ObservedProperty.objects.get(id=id)
                return observedproperty
            except ObservedProperty.DoesNotExist:
                return
        except KeyError:
            raise BadRequest()

    def get_or_update_datastream(data):
        """
        Creates (or gets if exists) a single Datastream object. Can only be
        called by an Observation entity create request.
        """
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                datastream = DataStream.objects.get(id=id)
                return datastream
            except DataStream.DoesNotExist:
                return
        except KeyError:
            raise BadRequest()

    def get_or_update_featureofinterest(data):
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                featureofinterest = FeatureOfInterest.objects.get(id=id)
                return featureofinterest
            except FeatureOfInterest.DoesNotExist:
                return
        except KeyError:
            raise BadRequest()

    def get_or_update_thing(data):
        try:
            id = data["@iot.id"]
            try:
                thing = Thing.objects.get(id=id)
                return thing
            except Thing.DoesNotExist:
                return
        except KeyError:
            raise BadRequest()

    def get_or_update_things(data):
        things = []
        for thing in data:
            try:
                id = thing["@iot.id"]
                try:
                    t = Thing.objects.get(id=id)
                    things.append(t)
                except DataStream.DoesNotExist:
                    return
            except KeyError:
                raise BadRequest()
        return things

    def get_or_update_locations(data):
        locationlist = []
        for loc in data:
            try:
                id = loc["@iot.id"]
                try:
                    location = Location.objects.get(id=id)
                    locationlist.append(location)
                except Location.DoesNotExist:
                    return
            except KeyError:
                raise BadRequest()
        return locationlist

    def get_or_update_datastreams(data):
        datastream = []
        for ds in data:
            try:
                id = ds["@iot.id"]
                try:
                    datastr = DataStream.objects.get(id=id)
                    datastream.append(datastr)
                except DataStream.DoesNotExist:
                    return
            except KeyError:
                raise BadRequest()
        return datastream

    def get_or_update_observations(data):
        observation = []
        for obs in data:
            try:
                id = obs["@iot.id"]
                try:
                    observ = Observation.objects.get(id=id)
                    observation.append(observ)
                except DataStream.DoesNotExist:
                    return
            except KeyError:
                raise BadRequest()
        return observation

    def get_or_update_historicallocations(data):
        historicallocation = []
        for his in data:
            try:
                id = his["@iot.id"]
                try:
                    hilocat = HistoricalLocation.objects.get(id=id)
                    historicallocation.append(hilocat)
                except HistoricalLocation.DoesNotExist:
                    return
            except KeyError:
                raise BadRequest()
        return historicallocation

    def get_or_create_sensor(data):
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                sensor = Sensor.objects.get(id=id)
                return sensor
            except Sensor.DoesNotExist:
                return
        except KeyError:
            try:
                name = data["name"]
                description = data["description"]
                encodingType = data["encodingType"]
                metadata = data["metadata"]
                sens, created = Sensor.objects.get_or_create(
                    name=name,
                    description=description,
                    encodingType=encodingType,
                    metadata=metadata
                    )
                return sens
            except KeyError:
                return

    def get_or_create_observedproperty(data):
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                observedproperty = ObservedProperty.objects.get(id=id)
                return observedproperty
            except ObservedProperty.DoesNotExist:
                return
        except KeyError:
            try:
                name = data["name"]
                definition = data["definition"]
                description = data["description"]
                oprop, created = ObservedProperty.objects.get_or_create(
                    name=name,
                    definition=definition,
                    description=description
                    )
                return oprop
            except KeyError:
                return

    def get_or_create_datastream(data):
        """
        Creates (or gets if exists) a single Datastream object. Can only be
        called by an Observation entity create request.
        """
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                datastream = DataStream.objects.get(id=id)
                return datastream
            except DataStream.DoesNotExist:
                return
        except KeyError:
            d = {}
            try:
                data = ViewSet.parse_interval_time(data)
                sensor = data["Sensor"]
                observedproperty = data["ObservedProperty"]
                thing = data['Thing']

                d['name'] = data["name"]
                d['description'] = data["description"]
                d['unitOfMeasurement'] = data["unitOfMeasurement"]
                d['observationType'] = data["observationType"]
                # create necessary related fields
                d['Sensor'] = PostRelations.get_or_create_sensor(
                    sensor
                )
                d['ObservedProperty'] = PostRelations.get_or_create_observedproperty(
                    observedproperty
                )
                d['Thing'] = PostRelations.get_or_create_thing(
                    thing
                )
                # optional fields
                try:
                    d['observedArea'] = GEOSGeometry(str(data["observedArea"]))
                except KeyError:
                    pass
                try:
                    d['phenomenonTime'] = data["phenomenonTime"]
                except KeyError:
                    pass
                try:
                    d['resultTime'] = data["resultTime"]
                except KeyError:
                    pass
                datastr, created = DataStream.objects.get_or_create(**d)
                return datastr
            except KeyError:
                return

    def get_or_create_featureofinterest(data):
        # should test if data is json dictionary
        try:
            id = data["@iot.id"]
            try:
                featureofinterest = FeatureOfInterest.objects.get(id=id)
                return featureofinterest
            except FeatureOfInterest.DoesNotExist:
                return
        except KeyError:
            try:
                name = data["name"]
                description = data["description"]
                encodingType = data["encodingType"]
                feature = GEOSGeometry(str(data["feature"]))
                foi, created = FeatureOfInterest.objects.get_or_create(
                    name=name,
                    description=description,
                    encodingType=encodingType,
                    feature=feature
                    )
                return foi
            except KeyError:
                return

    def get_or_create_thing(data):
        try:
            id = data["@iot.id"]
            try:
                thing = Thing.objects.get(id=id)
                return thing
            except Thing.DoesNotExist:
                return
        except KeyError:
            d = {}
            try:
                d['name'] = data["name"]
                d['description'] = data["description"]
                try:
                    d['properties'] = data["properties"]
                except KeyError:
                    pass
                thin, created = Thing.objects.get_or_create(**d)
                try:
                    locationData = data['Locations']
                    basename = "Things"
                    entity = thin
                    location = PostRelations.get_or_create_locations(
                        locationData,
                        basename,
                        entity
                        )
                    if location:
                        thin.Locations.set(location)
                except KeyError:
                    pass
                return thin
            except KeyError:
                return

    def get_or_create_things(data):
        things = []
        for thing in data:
            try:
                id = thing["@iot.id"]
                try:
                    t = Thing.objects.get(id=id)
                    things.append(t)
                except DataStream.DoesNotExist:
                    return
            except KeyError:
                d = {}
                try:
                    d['name'] = thing["name"]
                    d['description'] = thing["description"]
                    try:
                        d['properties'] = thing["properties"]
                    except KeyError:
                        pass
                    t, created = Thing.objects.get_or_create(**d)
                    # not required relations
                    try:
                        HistoricalLocationData = data['HistoricalLocations']
                        basename = 'HistoricalLocations'
                        entity = t
                        historicallocation = PostRelations.get_or_create_historicallocations(
                                    HistoricalLocationData,
                                    basename,
                                    entity
                                    )
                        t.HistoricalLocations.add(*historicallocation)
                    except KeyError:
                        pass
                except KeyError:
                    return
                things.append(t)
        return things

    def get_or_create_locations(data, basename, entity):
        locationlist = []
        for loc in data:
            try:
                id = loc["@iot.id"]
                try:
                    location = Location.objects.get(id=id)
                    locationlist.append(location)
                except Location.DoesNotExist:
                    return
            except KeyError:
                try:
                    name = loc["name"]
                    description = loc["description"]
                    encodingType = loc["encodingType"]
                    location = GEOSGeometry(str(loc["location"]))
                    locat, created = Location.objects.get_or_create(
                        name=name,
                        description=description,
                        encodingType=encodingType,
                        location=location
                        )
                    if basename == 'Things' and entity:
                        locat.Things.add(entity)
                    try:
                        HistoricalLocationData = loc['HistoricalLocations']
                        bn = 'HistoricalLocations'
                        entity = locat
                        historicallocation = PostRelations.get_or_create_historicallocations(
                                    HistoricalLocationData,
                                    bn,
                                    entity
                                    )
                        locat.HistoricalLocations.add(*historicallocation)
                    except KeyError:
                        pass
                    # historical locations is tricky
                    try:
                        thingData = loc['Things']
                        if basename == 'HistoricalLocations':
                            thing = PostRelations.get_or_create_things(
                                        thingData
                                        )
                            locat.Things.add(*thing)
                    except KeyError:
                        pass
                except KeyError:
                    return
                locationlist.append(locat)
        return locationlist

    def get_or_create_datastreams(data, basename, entity):
        datastream = []
        for ds in data:
            try:
                id = ds["@iot.id"]
                try:
                    datastr = DataStream.objects.get(id=id)
                    datastream.append(datastr)
                except DataStream.DoesNotExist:
                    return
            except KeyError:
                try:
                    ds = ViewSet.parse_interval_time(ds)
                    d = {}
                    d['name'] = ds["name"]
                    d['description'] = ds["description"]
                    d['unitOfMeasurement'] = ds["unitOfMeasurement"]
                    d['observationType'] = ds["observationType"]
                    # create necessary related fields
                    try:
                        sensor = ds["Sensor"]
                        d['Sensor'] = PostRelations.get_or_create_sensor(
                                    sensor
                                    )
                    except KeyError:
                        if basename == 'Sensors':
                            d['Sensor'] = entity
                        else:
                            return
                    try:
                        observedproperty = ds["ObservedProperty"]
                        d['ObservedProperty'] = PostRelations.get_or_create_observedproperty(
                                    observedproperty
                                    )
                    except KeyError:
                        if basename == 'ObservedProperties':
                            d['ObservedProperty'] = entity
                        else:
                            return
                    try:
                        thing = ds['Thing']
                        d['Thing'] = PostRelations.get_or_create_thing(
                                    thing
                                    )
                    except KeyError:
                        if basename == 'Things':
                            d['Thing'] = entity
                        else:
                            return
                    # optional fields
                    try:
                        d['observedArea'] = GEOSGeometry(str(ds["observedArea"]))
                    except KeyError:
                        pass
                    try:
                        d['phenomenonTime'] = ds["phenomenonTime"]
                    except KeyError:
                        pass
                    try:
                        d['resultTime'] = ds["resultTime"]
                    except KeyError:
                        pass
                    datastr, created = DataStream.objects.get_or_create(**d)
                    # not required relations
                    try:
                        observationData = ds['Observations']
                        basename = 'Datastreams'
                        entity = datastr
                        observation = PostRelations.get_or_create_observations(
                                    observationData,
                                    basename,
                                    entity
                        )
                        datastr.Observations.add(*observation, bulk=False)
                    except KeyError:
                        pass
                except KeyError:
                    return
                datastream.append(datastr)
        return datastream

    def get_or_create_observations(data, basename, entity):
        observation = []
        for obs in data:
            try:
                id = obs["@iot.id"]
                try:
                    observ = Observation.objects.get(id=id)
                    observation.append(observ)
                except DataStream.DoesNotExist:
                    return
            except KeyError:
                try:
                    obs = ViewSet.parse_interval_time(obs)
                    d = {}
                    d['phenomenonTime'] = obs["phenomenonTime"]
                    d['result'] = obs["result"]
                    d['resultTime'] = obs["resultTime"]
                    # create necessary related fields
                    try:
                        datastream = obs["Datastream"]
                        datastream = PostRelations.get_or_create_datastream(datastream)
                        d['Datastream'] = datastream
                    except KeyError:
                        if basename == 'Datastreams':
                            datastream = entity
                            d['Datastream'] = datastream
                        else:
                            return
                    try:
                        featureofinterest = obs["FeatureOfInterest"]
                        d['FeatureOfInterest'] = PostRelations.get_or_create_featureofinterest(
                                           featureofinterest
                                           )
                    except KeyError:
                        if basename == 'FeaturesOfInterest':
                            d['FeatureOfInterest'] = entity
                        else:
                            foi = ViewSet.create_missing_featureofinterest(obs)
                            if foi:
                                d["FeatureOfInterest"] = foi
                            else:
                                return
                    # optional fields
                    try:
                        d['resultQuality'] = obs["resultQuality"]
                    except KeyError:
                        pass
                    try:
                        d['validTime'] = obs["validTime"]
                    except KeyError:
                        pass
                    try:
                        d['parameters'] = obs["parameters"]
                    except KeyError:
                        pass
                    observ, created = Observation.objects.get_or_create(**d)
                    observation.append(observ)
                except KeyError:
                    return
        return observation

    def get_or_create_historicallocations(data, basename, entity):
        historicallocation = []
        for his in data:
            try:
                id = his["@iot.id"]
                try:
                    hilocat = HistoricalLocation.objects.get(id=id)
                    historicallocation.append(hilocat)
                except HistoricalLocation.DoesNotExist:
                    return
            except KeyError:
                try:
                    d = {}
                    d['time'] = his["time"]
                    # create necessary related fields
                    try:
                        thing = his["Thing"]
                        d['Thing'] = PostRelations.get_or_create_thing(thing)
                    except KeyError:
                        if basename == 'Things':
                            d['Thing'] = entity
                        else:
                            return
                    try:
                        location = his["Locations"]
                        bn = "HistoricalLocations"
                        d['Locations'] = PostRelations.get_or_create_locations(
                                           location,
                                           bn,
                                           None
                                           )
                    except KeyError:
                        if basename == 'Locations':
                            d['Locations'] = entity
                        else:
                            return
                    hlocat, created = HistoricalLocation.objects.get_or_create(**d)
                    historicallocation.append(hlocat)
                except KeyError:
                    return
        return historicallocation


class ViewSet(viewsets.ModelViewSet):
    """
    Overrides the DRF ModelViewSet methods of list, retrieve, and create.
    """
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

    def queryset_methods(path_list, method, kwargs):
        """
        Adds nested entites to the queryset of the current viewset, thereby
        allowing nested expansions to be properly queried.
        """
        d = {}
        if method == "list":
            cv = ViewSet.INDICES[path_list[-1]]
            path_list = [item.split('(')[0] for item
                         in path_list if item[-1] == ')']
        elif method == "retrieve":
            cv = ViewSet.INDICES[path_list[-1].split('(')[0]]
            path_list = [item.split('(')[0] for item in path_list[:-1]]
        elif method == "associationLink":
            cv = ViewSet.INDICES[path_list[-1]]
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

    def relate_parent(data, basename, kwargs):
        """
        Add parent as related entity if created entity is nested.
        """
        if list(kwargs.keys())[-1] != "version":
            parent = list(kwargs.keys())[-1]
            if parent == "Locations_pk":
                data['Locations'] = [{"@iot.id": kwargs[parent]}]
            if parent == "Sensors_pk":
                data['Sensor'] = {"@iot.id": kwargs[parent]}
            if parent == "ObservedProperties_pk":
                data['ObservedProperty'] = {"@iot.id": kwargs[parent]}
            if parent == "Things_pk":
                if basename == "location":
                    data['Things'] = [{"@iot.id": kwargs[parent]}]
                else:
                    data['Thing'] = {"@iot.id": kwargs[parent]}
            if parent == "Observations_pk":
                data['Observations'] = [{"@iot.id": kwargs[parent]}]
            if parent == "Datastreams_pk":
                if basename == "observation":
                    data['Datastream'] = {"@iot.id": kwargs[parent]}
                else:
                    data['Datastreams'] = [{"@iot.id": kwargs[parent]}]
            if parent == "FeaturesOfInterest_pk":
                data['FeatureOfInterest'] = {"@iot.id": kwargs[parent]}
        return data

    def geojson_to_geos(data):
        """
        Checks to see if either location, feature, or observedArea are in json
        object and if they are, and are a dictionary, convert geojson geometery
        to geos geometry.
        """
        geometries = ['location', 'feature', 'observedArea']
        for geometry in geometries:
            try:
                if isinstance(data[geometry], dict):
                    data[geometry] = GEOSGeometry(str(data[geometry]))
            except KeyError:
                pass
        return data

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

    def process_data(data, basename, kwargs):
        data = ViewSet.relate_parent(data, basename, kwargs)
        data = ViewSet.geojson_to_geos(data)
        data = ViewSet.parse_interval_time(data)
        if basename == 'observation':
            try:
                result = data['result']
                data['result'] = {'result': result}
                return data
            except KeyError:
                raise BadRequest()
        return data

    def get_or_update_related(data):
        d = {}
        if 'FeatureOfInterest' in data:
            featureofinterestData = data['FeatureOfInterest']
            featureofinterest = PostRelations.get_or_update_featureofinterest(
                featureofinterestData
                )
            if featureofinterest:
                d['FeatureOfInterest'] = featureofinterest
        if 'Thing' in data:
            thingData = data['Thing']
            thing = PostRelations.get_or_update_thing(
                thingData
                )
            if thing:
                d['Thing'] = thing

        if 'Sensor' in data:
            sensorData = data['Sensor']
            sensor = PostRelations.get_or_update_sensor(
                sensorData
                )
            if sensor:
                d['Sensor'] = sensor

        if 'ObservedProperty' in data:
            observedpropertyData = data['ObservedProperty']
            observedproperty = PostRelations.get_or_update_observedproperty(
                observedpropertyData
                )
            if observedproperty:
                d['ObservedProperty'] = observedproperty

        if 'Datastream' in data:
            datastreamData = data['Datastream']
            datastream = PostRelations.get_or_update_datastream(
                datastreamData
                )
            if datastream:
                d['Datastream'] = datastream

        if 'Locations' in data:
            locationData = data['Locations']
            location = PostRelations.get_or_update_locations(
                locationData
                )
            if location:
                d['Locations'] = location

        if 'Things' in data:
            thingData = data['Things']
            things = PostRelations.get_or_update_things(
                thingData
                )
            if things:
                d['Things'] = things

        if 'Datastreams' in data:
            datastreamData = data['Datastreams']
            datastreams = PostRelations.get_or_update_datastreams(
                            datastreamData
                            )
            if datastreams:
                d['Datastreams'] = datastreams

        if 'HistoricalLocations' in data:
            historicallocationData = data['HistoricalLocations']
            historicallocation = PostRelations.get_or_update_historicallocations(
                historicallocationData
            )
            if historicallocation:
                d['HistoricalLocations'] = historicallocation

        if 'Observations' in data:
            observationData = data['Observations']
            observations = PostRelations.get_or_update_observations(
                            observationData
                            )
            if observations:
                d['Observations'] = observations

        return d

    def get_or_create_related(data, basename, serializer):
        d = {}
        if 'FeatureOfInterest' in data:
            featureofinterestData = data['FeatureOfInterest']
            featureofinterest = PostRelations.get_or_create_featureofinterest(
                featureofinterestData
                )
            if featureofinterest:
                d['FeatureOfInterest'] = featureofinterest
        if 'Thing' in data:
            thingData = data['Thing']
            thing = PostRelations.get_or_create_thing(
                thingData
                )
            if thing:
                d['Thing'] = thing

        if 'Sensor' in data:
            sensorData = data['Sensor']
            sensor = PostRelations.get_or_create_sensor(
                sensorData
                )
            if sensor:
                d['Sensor'] = sensor

        if 'ObservedProperty' in data:
            observedpropertyData = data['ObservedProperty']
            observedproperty = PostRelations.get_or_create_observedproperty(
                observedpropertyData
                )
            if observedproperty:
                d['ObservedProperty'] = observedproperty

        if 'Datastream' in data:
            datastreamData = data['Datastream']
            datastream = PostRelations.get_or_create_datastream(
                datastreamData
                )
            if datastream:
                d['Datastream'] = datastream

        if 'Locations' in data:
            locationData = data['Locations']
            location_basename = ViewSet.NAME_LOOKUP[basename]
            if location_basename == 'HistoricalLocations':
                entity = None
            else:
                entity = serializer.save()
            location = PostRelations.get_or_create_locations(
                locationData,
                location_basename,
                entity
                )
            if location:
                d['Locations'] = location

        if 'Things' in data:
            thingData = data['Things']
            things = PostRelations.get_or_create_things(
                thingData
                )
            if things:
                d['Things'] = things

        if 'Datastreams' in data:
            datastreamData = data['Datastreams']
            datastream_basename = ViewSet.NAME_LOOKUP[basename]
            entity = serializer.save()
            datastreams = PostRelations.get_or_create_datastreams(
                            datastreamData,
                            datastream_basename,
                            entity
                            )
            if datastreams:
                d['Datastreams'] = datastreams

        if 'HistoricalLocations' in data:
            historical_basename = ViewSet.NAME_LOOKUP[basename]
            entity = serializer.save()
            historicallocationData = data['HistoricalLocations']
            historicallocation = PostRelations.get_or_create_historicallocations(
                historicallocationData,
                historical_basename,
                entity
            )
            d['HistoricalLocations'] = historicallocation

        if 'Observations' in data:
            observationData = data['Observations']
            observation_basename = ViewSet.NAME_LOOKUP[basename]
            entity = serializer.save()
            observations = PostRelations.get_or_create_observations(
                            observationData,
                            observation_basename,
                            entity
                            )
            if observations:
                d['Observations'] = observations
        return d

    def create_missing_featureofinterest(data):
        if 'Datastreams' in data:
            ds = data['Datastreams']
            if len(ds) == 1:
                datastream = PostRelations.get_or_create_datastream(ds[0])
        elif 'Datastream' in data:
            ds = data['Datastream']
            datastream = PostRelations.get_or_create_datastream(ds)
        if datastream:
            try:
                location = datastream.Thing.Locations.get(
                            encodingType=ViewSet.DEFAULT_ENCODING
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

    def list(self, request, version, **kwargs):
        path = request._request.path
        path_list = path.split('/')[3:]
        method = 'list'
        d = ViewSet.queryset_methods(path_list, method, kwargs)
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
        d = ViewSet.queryset_methods(path_list, method, kwargs)
        d['pk'] = kwargs['pk']
        queryset = self.get_queryset().filter(**d)
        queryset = self.filter_queryset(queryset)
        location = get_object_or_404(queryset, pk=d['pk'])
        serializer = self.get_serializer(location)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Override the create method to allow related entity creation.
        """
        data = request.data
        if isinstance(data, list):
            raise Unprocessable()
        basename = self.basename
        processed_data = ViewSet.process_data(data, basename, kwargs)
        if basename == 'observation' and 'FeatureOfInterest' not in processed_data:
            foi = ViewSet.create_missing_featureofinterest(processed_data)
            processed_data["FeatureOfInterest"] = {"@iot.id": foi.id}
        for entity, fields in ViewSet.REQUIRED_FIELDS.items():
            if entity == basename:
                for field in fields:
                    if field not in processed_data:
                        raise BadRequest()
        serializer = self.get_serializer(data=processed_data)
        if serializer.is_valid(raise_exception=True):
            d = ViewSet.get_or_create_related(
                    processed_data,
                    basename,
                    serializer
                    )
            if d:
                serializer.save(**d)
            else:
                self.perform_create(serializer)
        # It is tricky when the response is for observations
        # when it is observations, the serializer doesnt make the id pr create
        # a self link. Instead, the id is managed by pipelinedb. So, guess it:
        basename = self.basename
        if basename == 'observation':
            test = Observation.objects.last()
            if test:
                url = request.build_absolute_uri(reverse(
                        'observation-detail',
                        kwargs={
                            'version': 'v1.0',
                            'pk': test.id + 1
                        }
                    )
                )
            else:
                url = request.build_absolute_uri(reverse(
                        'observation-detail',
                        kwargs={
                            'version': 'v1.0',
                            'pk': 1
                        }
                    )
                )
            response = Response(
                                {"Location": url},
                                status=status.HTTP_201_CREATED
                                )
        else:
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
            processed_data = ViewSet.process_data(data, basename, kwargs)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            d = ViewSet.get_or_update_related(
                    processed_data
                )
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


class NavigationLinks:
    keys = {
        "Thing": "Things_pk",
        "Location": "Locations_pk",
        "HistoricalLocation": "HistoricalLocations_pk",
        "DataStream": "Datastreams_pk",
        "Sensor": "Sensors_pk",
        "ObservedProperty": "ObservedProperties_pk",
        "Observation": "Observations_pk",
        "FeatureOfInterest": "FeaturesOfInterest_pk"
    }

    def get_observationsLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('observation-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_thingsLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('thing-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_observedpropertiesLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('observedproperty-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_sensorsLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('sensor-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_locationsLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('location-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_historicallocationsLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('historicallocation-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_datastreamsLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('datastream-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )

    def get_featuresOfInterestLink(self, obj):
        request = self.context.get('request')
        model = self.Meta.model.__name__
        model_kwarg = NavigationLinks.keys[model]
        return request.build_absolute_uri(
                    reverse('featureofinterest-list',
                            kwargs={model_kwarg: obj.id,
                                    "version": "v1.0"
                                    }
                            )
                    )


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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
            d = ViewSet.queryset_methods(path_list, method, kwargs)
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
