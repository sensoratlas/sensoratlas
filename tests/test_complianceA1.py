from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from sensorAtlas.models import Thing, Location, HistoricalLocation, \
    Datastream, Sensor, ObservedProperty, Observation, FeatureOfInterest
from django.contrib.gis.geos import Point, Polygon
from django.utils import timezone


# A.1.1 Conformance class: SensorThings API Entity Control Information
class A_1_1(APITestCase):
    """
    Check if each entity has the common control information as defined in
    the requirement http://www.opengis.net/spec/iot_sensing/1.0/req/entity-
    control-information/common-control-information.
    """
    def setUp(self):
        """
        Create test resources
        """
        url = reverse('observation-list', kwargs={'version': 'v1.0'})
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "Datastream": {
                "name": "Air Temperature DS",
                "description": "Datastream for recording temperature",
                "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "unitOfMeasurement": {
                    "name": "Degree Celsius",
                    "symbol": "degC",
                    "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius"
                },
                "ObservedProperty": {
                    "name": "Area Temperature",
                    "description": "The degree or intensity of heat present in the area",
                    "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AreaTemperature"
                },
                "Sensor": {
                    "name": "DHT22",
                    "description": "DHT22 temperature sensor",
                    "encodingType": "application/pdf",
                    "metadata": "https://cdn-shop.adafruit.com/datasheets/DHT22.pdf"
                },
                "Thing": {
                    "name": "Temperature Monitoring System",
                    "description": "Sensor system monitoring area temperature",
                    "properties": {
                        "Deployment Condition": "Deployed in a third floor balcony",
                        "Case Used": "Radiation shield"
                    },
                    "Locations": [
                        {
                            "name": "UofC CCIT",
                            "description": "University of Calgary, CCIT building",
                            "encodingType": "application/vnd.geo+json",
                            "location": {
                                "type": "Point",
                                "coordinates": [-114.133, 51.08]
                            }
                        }
                    ]
                }
            },
            "FeatureOfInterest": {
                "name": "UofC CCIT",
                "description": "University of Calgary, CCIT building",
                "encodingType": "application/vnd.geo+json",
                "feature": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
                        ]
                    ]
                }
            }
        }
        self.client.post(url, data, format='json')

    def test_requirement1(self):
        urls = [
            "/api/v1.0/Things",
            "/api/v1.0/Locations",
            "/api/v1.0/HistoricalLocations",
            "/api/v1.0/Datastreams",
            "/api/v1.0/Sensors",
            "/api/v1.0/ObservedProperties",
            "/api/v1.0/Observations",
            "/api/v1.0/FeaturesOfInterest",
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data['value'][0]['@iot.id'])
            self.assertTrue(response.data['value'][0]['@iot.selfLink'])
            count = 0
            for key in response.data['value'][0]:
                if '@iot.navigationLink' in key:
                    self.assertIn('@iot.navigationLink', key)
                    count += 1
            self.assertGreaterEqual(count, 1)


class A_1_2(APITestCase):
    """
    Check if each Thing entity has the mandatory properties and
    mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create test resources.
        """
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )

    def test_thing_properties(self):
        """
        Tests requirement 2.
        """
        thing = Thing.objects.get(name='Thing 1')
        properties = [
            'name',
            'description',
            'properties'
        ]
        for property in properties:
            self.assertTrue(hasattr(thing, property))

    def test_thing_relations(self):
        """
        Tests requirement 3.
        """
        thing = Thing.objects.get(name='Thing 1')
        entities = [
            'Location',
            'HistoricalLocation',
            'Datastream'
        ]
        for entity in entities:
            self.assertTrue(hasattr(thing, entity))


class A_1_3(APITestCase):
    """
    Check if each Location entity has the mandatory properties
    and mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create test resources.
        """
        Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )

    def test_location_properties(self):
        """
        Tests requirement 4.
        """
        location = Location.objects.get(name='Location 1')
        properties = [
            'name',
            'description',
            'encodingType',
            'location'
        ]
        for property in properties:
            self.assertTrue(hasattr(location, property))

    def test_location_relations(self):
        """
        Tests requirement 5.
        """
        location = Location.objects.get(name='Location 1')
        entities = [
            'Thing',
            'HistoricalLocation'
        ]
        for entity in entities:
            self.assertTrue(hasattr(location, entity))


class A_1_4(APITestCase):
    """
    Check if each Historicalocation entity has the mandatory properties and
    mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create each resource
        """
        location = Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        thing = Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        historicallocation = HistoricalLocation.objects.create(
            time=timezone.now(),
            Thing=thing
        )
        historicallocation.Location.add(location)

    def test_historicallocation_properties(self):
        """
        Tests requirement 6.
        """
        hlocat = HistoricalLocation.objects.get(Thing__name="Thing 1")
        properties = [
            'time'
        ]
        for property in properties:
            self.assertTrue(hasattr(hlocat, property))

    def test_historicallocation_relations(self):
        """
        Tests requirement 7.
        """
        hlocat = HistoricalLocation.objects.get(Thing__name="Thing 1")
        entities = [
            'Thing',
            'Location'
        ]
        for entity in entities:
            self.assertTrue(hasattr(hlocat, entity))


class A_1_5(APITestCase):
    """
    Check if each Datastream entity has the mandatory properties and
    mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create test resources.
        """
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )

    def test_datastream_properties(self):
        """
        Tests requirement 9.
        """
        datastream = Datastream.objects.get(name='Chunt')
        properties = [
            'name',
            'description',
            'unitOfMeasurement',
            'observationType',
            'observedArea',
            'phenomenonTime',
            'resultTime'
        ]
        for property in properties:
            self.assertTrue(hasattr(datastream, property))

    def test_datastream_relations(self):
        """
        Tests requirement 10.
        """
        datastream = Datastream.objects.get(name='Chunt')
        entities = [
            'Thing',
            'Sensor',
            'ObservedProperty',
            'Observation'
        ]
        for entity in entities:
            self.assertTrue(hasattr(datastream, entity))


class A_1_6(APITestCase):
    """
    Check if each Sensor entity has the mandatory properties and
    mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create each resource
        """
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )

    def test_sensor_properties(self):
        """
        Tests requirement 11.
        """
        sensor = Sensor.objects.get(name='Temperature Sensor')
        properties = [
            'name',
            'description',
            'encodingType',
            'metadata'
        ]
        for property in properties:
            self.assertTrue(hasattr(sensor, property))

    def test_sensor_relations(self):
        """
        Tests requirement 12.
        """
        sensor = Sensor.objects.get(name='Temperature Sensor')
        entities = [
            'Datastream'
        ]
        for entity in entities:
            self.assertTrue(hasattr(sensor, entity))


class A_1_7(APITestCase):
    """
    Check if each ObservedProperty entity has the mandatory properties and
    mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create each resource
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )

    def test_observedproperty_properties(self):
        """
        Tests requirement 13.
        """
        observedproperty = ObservedProperty.objects.get(name='Temperature')
        properties = [
            'name',
            'definition',
            'description'
        ]
        for property in properties:
            self.assertTrue(hasattr(observedproperty, property))

    def test_observedproperty_relations(self):
        """
        Tests requirement 14.
        """
        observedproperty = ObservedProperty.objects.get(name='Temperature')
        entities = [
            'Datastream'
        ]
        for entity in entities:
            self.assertTrue(hasattr(observedproperty, entity))


class A_1_8(APITestCase):
    """
    Check if each Observation entity has the mandatory properties and
    mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create each resource
        """
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        FeatureOfInterest.objects.create(
            name='Usidore',
            description='this is a place',
            encodingType='application/vnd.geo+json',
            feature=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ))
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:00:00.000Z",
            result=42,
            resultTime="2019-02-07T18:00:00.000Z",
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore')
            )

    def test_observation_properties(self):
        """
        Tests requirement 15.
        """
        observation = Observation.objects.last()
        properties = [
            'phenomenonTime',
            'result',
            'resultTime',
            'resultQuality',
            'validTime',
            'parameters'
        ]
        for property in properties:
            self.assertTrue(hasattr(observation, property))

    def test_observation_relations(self):
        """
        Tests requirement 16.
        """
        observation = Observation.objects.last()
        entities = [
            'Datastream',
            'FeatureOfInterest'
        ]
        for entity in entities:
            self.assertTrue(hasattr(observation, entity))


class A_1_9(APITestCase):
    """
    Check if each FeatureOfInterest entity has the mandatory properties and
    mandatory relations as defined in this specification.
    """
    def setUp(self):
        """
        Create each resource
        """
        FeatureOfInterest.objects.create(
            name='Usidore',
            description='this is a place',
            encodingType='application/vnd.geo+json',
            feature=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ))

    def test_featureofinterest_properties(self):
        """
        Tests requirement 17.
        """
        featureofinterest = FeatureOfInterest.objects.get(name='Usidore')
        properties = [
            'name',
            'description',
            'encodingType',
            'feature'
        ]
        for property in properties:
            self.assertTrue(hasattr(featureofinterest, property))

    def test_featureofinterest_relations(self):
        """
        Tests requirement 18.
        """
        featureofinterest = FeatureOfInterest.objects.get(name='Usidore')
        entities = [
            'Observation'
        ]
        for entity in entities:
            self.assertTrue(hasattr(featureofinterest, entity))


class A_1_10(APITestCase):
    """
    Check if the service supports all the resource path usages as defined
    in the requirement
    http://www.opengis.net/spec/iot_sensing/1.0/req/resource-path/resource-path-to-entities.
    """

    def setUp(self):
        """
        Create each resource
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        location = Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        thing = Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing.Location.add(location)
        FeatureOfInterest.objects.create(
            name='Usidore',
            description='this is a place',
            encodingType='application/vnd.geo+json',
            feature=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ))
        Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature'),
            observedArea=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            )
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:01:00.000Z",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:01:00.000Z",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:02:00.000Z",
            result=3,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:02:00.000Z",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:03:00.000Z",
            result=15.7,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:04:00.000Z",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:04:00.000Z",
            result=23,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:04:00.000Z",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:05:00.000Z",
            result=1,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:05:00.000Z",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:06:00.000Z",
            result=35,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:06:00.000Z",
            )

    def test_no_resource_path(self):
        """
        Ensure that we can access the base resource path and the appropriate
        response is returned. Response: A JSON object with a property named
        value. The value of the property SHALL be a JSON Array containing one
        element for each entity set of the SensorThings Service
        """
        url = reverse('api-root', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 8)
        for entity in response.data['value']:
            self.assertTrue(entity['name'])
            self.assertTrue(entity['url'])

    def test_things_paths(self):
        """
        Ensure that all nested paths for the things entity are available and
        the appropriate response is returned.
        """
        thing = Thing.objects.get(name='Thing 1')
        location = thing.Location.get(name='Location 1')
        hlocat = HistoricalLocation.objects.get(Thing__name=thing.name)
        datastream = Datastream.objects.get(Thing__name=thing.name)
        sensor = Sensor.objects.get(Datastream__name=datastream.name)
        oprop = ObservedProperty.objects.get(Datastream__name=datastream.name)
        obs = Observation.objects.filter(Datastream__name=datastream.name)
        foi = FeatureOfInterest.objects.get(Observation__id=obs[0].id)

        url = reverse('thing-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Locations_pk': location.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id,
                              'pk': sensor.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id,
                              'pk': oprop.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id,
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_location_paths(self):
        """
        Ensure that all nested paths for the Locations entity are available and
        the appropriate response is returned.
        """
        location = Location.objects.get(name='Location 1')
        thing = Thing.objects.filter(Location__name=location.name)
        hlocat = HistoricalLocation.objects.filter(Location__name=location.name)
        datastream = Datastream.objects.filter(Thing__name=thing[0].name)
        sensor = Sensor.objects.filter(Datastream__name=datastream[0].name)
        oprop = ObservedProperty.objects.filter(Datastream__name=datastream[0].name)
        obs = Observation.objects.filter(Datastream__name=datastream[0].name)
        foi = FeatureOfInterest.objects.get(Observation__id=obs[0].id)

        url = reverse('location-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'pk': hlocat[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'pk': thing[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': sensor[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': oprop[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'pk': thing[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': sensor[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': oprop[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'Things_pk': thing[0].id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_historicallocation_paths(self):
        """
        Ensure that all nested paths for the Historical Locations entity are
        available and the appropriate response is returned.
        """
        hlocat = HistoricalLocation.objects.get(Location__name='Location 1')
        thing = Thing.objects.get(HistoricalLocation__id=hlocat.id)
        location = Location.objects.get(HistoricalLocation__id=hlocat.id)
        datastream = Datastream.objects.filter(Thing__name=thing.name)
        sensor = Sensor.objects.filter(Datastream__name=datastream[0].name)
        oprop = ObservedProperty.objects.filter(Datastream__name=datastream[0].name)
        obs = Observation.objects.filter(Datastream__name=datastream[0].name)
        foi = FeatureOfInterest.objects.get(Observation__id=obs[0].id)

        url = reverse('historicallocation-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': sensor[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': oprop[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': sensor[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': oprop[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'HistoricalLocations_pk': hlocat.id,
                              'Locations_pk': location.id,
                              'Thing_pk': thing.id,
                              'Datastreams_pk': datastream[0].id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_datastreams_paths(self):
        """
        Ensure that all nested paths for the datastreams entity are available
        and the appropriate response is returned.
        """
        datastream = Datastream.objects.get(name='Chunt')
        thing = datastream.Thing
        location = datastream.Thing.Location.get(name='Location 1')
        hlocat = HistoricalLocation.objects.get(Thing__name=thing.name)
        sensor = Sensor.objects.get(Datastream__name=datastream.name)
        oprop = ObservedProperty.objects.get(Datastream__name=datastream.name)
        obs = Observation.objects.filter(Datastream__name=datastream.name)
        foi = FeatureOfInterest.objects.get(Observation__id=obs[0].id)

        url = reverse('datastream-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'pk': sensor.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'pk': oprop.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sensor_paths(self):
        """
        Ensure that all nested paths for the sensors entity are available and
        the appropriate response is returned.
        """
        sensor = Sensor.objects.get(name='Temperature Sensor')
        datastream = Datastream.objects.get(Sensor__name=sensor.name)
        thing = datastream.Thing
        location = thing.Location.get(name='Location 1')
        hlocat = HistoricalLocation.objects.get(Thing__name=thing.name)
        oprop = ObservedProperty.objects.get(Datastream__name=datastream.name)
        obs = Observation.objects.filter(Datastream__name=datastream.name)
        foi = FeatureOfInterest.objects.get(Observation__id=obs[0].id)

        url = reverse('sensor-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'pk': sensor.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'pk': oprop.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id,
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_observedproperty_paths(self):
        """
        Ensure that all nested paths for the Observed Properties entity are
        available and the appropriate response is returned.
        """
        oprop = ObservedProperty.objects.get(name='Temperature')
        datastream = Datastream.objects.get(ObservedProperty__name=oprop.name)
        thing = datastream.Thing
        location = thing.Location.get(name='Location 1')
        hlocat = HistoricalLocation.objects.get(Thing__name=thing.name)
        sensor = Sensor.objects.get(Datastream__name=datastream.name)
        obs = Observation.objects.filter(Datastream__name=datastream.name)
        foi = FeatureOfInterest.objects.get(Observation__id=obs[0].id)

        url = reverse('observedproperty-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'pk': oprop.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'pk': sensor.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': oprop.id,
                              'Datastreams_pk': datastream.id,
                              'Observations_pk': obs[0].id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_observation_paths(self):
        """
        Ensure that all nested paths for the Observation entity are
        available and the appropriate response is returned.
        """
        obs = Observation.objects.last()
        datastream = Datastream.objects.get(Observation__id=obs.id)
        thing = datastream.Thing
        location = thing.Location.get(name='Location 1')
        hlocat = HistoricalLocation.objects.get(Thing__name=thing.name)
        sensor = Sensor.objects.get(Datastream__name=datastream.name)
        oprop = ObservedProperty.objects.get(Datastream__name=datastream.name)
        foi = FeatureOfInterest.objects.get(Observation__id=obs.id)

        url = reverse('observation-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'pk': obs.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'Locations_pk': location.id,
                              'pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'Thing_pk': thing.id,
                              'HistoricalLocations_pk': hlocat.id,
                              'pk': location.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'pk': thing.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'pk': sensor.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'Datastream_pk': datastream.id,
                              'pk': oprop.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'Observations_pk': obs.id,
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_featuresofinterest_paths(self):
        """
        Ensure that all nested paths for the Features Of Interest entity are
        available and the appropriate response is returned.
        """
        foi = FeatureOfInterest.objects.get(name="Usidore")
        obs = Observation.objects.filter(FeatureOfInterest__name=foi.name)
        datastream = Datastream.objects.filter(Observation__id=obs[0].id)
        sensor = Sensor.objects.filter(Datastream__name=datastream[0].name)
        oprop = ObservedProperty.objects.filter(Datastream__name=datastream[0].name)
        thing = Thing.objects.filter(Datastream__name=datastream[0].name)
        location = Location.objects.filter(Thing__name=thing[0].name)
        hlocat = HistoricalLocation.objects.filter(Location__name=location[0].name)

        url = reverse('featureofinterest-list', kwargs={'version': 'v1.0'})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('featureofinterest-detail',
                      kwargs={'version': 'v1.0',
                              'pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observation-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('datastream-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('observedproperty-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'pk': oprop[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sensor-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'pk': sensor[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('thing-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'pk': thing[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id,
                              'pk': hlocat[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id,
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id,
                              'pk': location[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id,
                              'Locations_pk': location[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('historicallocation-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id,
                              'Locations_pk': location[0].id,
                              'pk': hlocat[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id,
                              'HistoricalLocations_pk': hlocat[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('location-detail',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id,
                              'Observations_pk': obs[0].id,
                              'Datastream_pk': datastream[0].id,
                              'Thing_pk': thing[0].id,
                              'HistoricalLocations_pk': hlocat[0].id,
                              'pk': location[0].id
                              })
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_things_property_value(self):
        """
        Ensure that all nested paths for the things entity are available and
        the appropriate response is returned.
        """
        thing = Thing.objects.get(name='Thing 1')
        properties = [
            'name',
            'description',
            'properties'
        ]
        baseurl = reverse('thing-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': thing.id
                                  })
        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_location_property_value(self):
        """
        Ensure that all nested paths for the things entity are available and
        the appropriate response is returned.
        """
        location = Location.objects.get(name='Location 1')
        properties = [
            'name',
            'description',
            'encodingType',
            'location'
        ]
        baseurl = reverse('location-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': location.id
                                  })
        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_historicallocation_property_value(self):
        """
        Ensure that all nested paths for the things entity are available and
        the appropriate response is returned.
        """
        hlocat = HistoricalLocation.objects.get(Location__name='Location 1')
        properties = [
            'time'
        ]
        baseurl = reverse('historicallocation-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': hlocat.id
                                  })
        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_datastreams_property_value(self):
        """
        Ensure that all nested paths for the things entity are available and
        the appropriate response is returned.
        """
        datastream = Datastream.objects.get(name='Chunt')
        properties = [
            'name',
            'description',
            'unitOfMeasurement',
            'observationType',
            'observedArea',
            'phenomenonTime',
            'resultTime'
        ]
        baseurl = reverse('datastream-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': datastream.id
                                  })
        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_sensors_property_value(self):
        """
        Ensure that all nested paths for the things entity are available and
        the appropriate response is returned.
        """
        sensor = Sensor.objects.get(name='Temperature Sensor')
        properties = [
            'name',
            'description',
            'encodingType',
            'metadata'
        ]
        baseurl = reverse('sensor-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': sensor.id
                                  })
        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_observedproperty_property_value(self):
        """
        Ensure that all nested paths for the observedproperty entity are
        available and the appropriate response is returned.
        """
        observedproperty = ObservedProperty.objects.get(name='Temperature')
        properties = [
            'name',
            'definition',
            'description'
        ]
        baseurl = reverse('observedproperty-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': observedproperty.id
                                  })
        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_observation_property_value(self):
        """
        Ensure that all nested paths for the observation entity are
        available and the appropriate response is returned.
        """
        observation = Observation.objects.last()
        properties = [
            'phenomenonTime',
            'result',
            'resultTime',
            'resultQuality',
            'validTime',
            'parameters'
        ]
        baseurl = reverse('observation-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': observation.id
                                  })

        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_featureofinterest_property_value(self):
        """
        Ensure that all nested paths for the featureofinterest entity are
        available and the appropriate response is returned.
        """
        featureofinterest = FeatureOfInterest.objects.get(name='Usidore')
        properties = [
            'name',
            'description',
            'encodingType',
            'feature'
        ]
        baseurl = reverse('featureofinterest-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': featureofinterest.id
                                  })
        for property in properties:
            url = baseurl + '/' + property
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn(property, response.data)
            if response.data[property]:
                url = baseurl + '/' + property + '/$value'
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data)

    def test_obervation_associationlink(self):
        """
        Ensure that all nested paths for the things entity are available and
        the appropriate response is returned.
        """
        baseurl = reverse('observation-list',
                          kwargs={'version': 'v1.0'})
        baseurl = baseurl + '/$ref'
        response = self.client.get(baseurl, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 6)
        for ref in response.data['value']:
            self.assertIn('@iot.selfLink', ref)

        Datastream.objects.create(
            name='Arnie',
            description='Kneecamp',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Human",
                               "Class": "Jester"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:08:00.000Z",
            result=21,
            Datastream=Datastream.objects.get(name="Arnie"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:08:00.000Z",
            )

        datastream = Datastream.objects.get(name='Arnie')
        baseurl = reverse('datastream-detail',
                          kwargs={'version': 'v1.0',
                                  'pk': datastream.id
                                  })
        baseurl = baseurl + '/Observations/$ref'
        response = self.client.get(baseurl, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        for ref in response.data['value']:
            self.assertIn('@iot.selfLink', ref)
