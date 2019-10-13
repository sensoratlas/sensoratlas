from rest_framework import status
from rest_framework.test import APITestCase
from sensorAtlas.models import Thing, Location, Datastream, Sensor, \
    ObservedProperty, Observation, FeatureOfInterest, HistoricalLocation
from django.contrib.gis.geos import Point, Polygon, LineString
from django.utils import timezone
from operator import getitem


class A_2_1_1(APITestCase):
    """
    Check if the results of the service requests are as if the system query
    options were evaluated in the order as defined in this specification.
    """
    def setUp(self):
        """
        Create test resources
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        ObservedProperty.objects.create(
            name='Truth',
            definition='https://hellofromthemagictavern.com/',
            description='This is a test'
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Sensor.objects.create(
            name='Lie Detector',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
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
        Datastream.objects.create(
            name='Spintax',
            description='The Green',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation",
            unitOfMeasurement={"Race": "Wizard",
                               "Class": "Master of Truth and Lies"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Lie Detector'),
            ObservedProperty=ObservedProperty.objects.get(name='Truth')
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:09:00+00:00",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:09:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:10:00+00:00",
            result=3,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:10:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:11:00+00:00",
            result=15.7,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:11:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:12:00+00:00",
            result=23,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:12:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:13:00+00:00",
            result=1,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:13:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:14:00+00:00",
            result=35,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:14:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:15:00+00:00",
            result='Lie',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:15:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:16:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:16:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T18:17:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T18:17:00+00:00",
            )
    # I will need to write a proper integration test later, but for now
    # this test checks that the desired output is generated.
    def test_query_order(self):
        query1 = "$filter=name eq 'Chunt' or name eq 'Spintax'"
        query2 = "$count=false"
        query3 = "$orderby=id desc"
        query4 = "$skip=1"
        query5 = "$top=1"
        query6 = "$expand=Observations"
        query7 = "$select=name"

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query1 + '&' +
                                   query2 + '&' +
                                   query3 + '&' +
                                   query4 + '&' +
                                   query5 + '&' +
                                   query6 + '&' +
                                   query7
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query7 + '&' +
                                   query6 + '&' +
                                   query3 + '&' +
                                   query4 + '&' +
                                   query2 + '&' +
                                   query1 + '&' +
                                   query5
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.count')
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_query_order1(self):
        query1 = "$filter=name eq 'Chunt' or name eq 'Spintax'"

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query1
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['@iot.count'], 2)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(len(response.data['value'][0]), 13)
        self.assertEqual(len(response.data['value'][1]), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')
        self.assertEqual(response.data['value'][1]['name'], 'Spintax')

    def test_query_order2(self):
        query1 = "$filter=name eq 'Chunt' or name eq 'Spintax'"
        query2 = "$count=false"

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query1 + '&' +
                                   query2
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.count')
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(len(response.data['value'][0]), 13)
        self.assertEqual(len(response.data['value'][1]), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')
        self.assertEqual(response.data['value'][1]['name'], 'Spintax')

    def test_query_order3(self):
        query1 = "$filter=name eq 'Chunt' or name eq 'Spintax'"
        query2 = "$count=false"
        query3 = "$orderby=id desc"

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query1 + '&' +
                                   query2 + '&' +
                                   query3
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.count')
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(len(response.data['value'][0]), 13)
        self.assertEqual(len(response.data['value'][1]), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')
        self.assertEqual(response.data['value'][1]['name'], 'Chunt')

    def test_query_order4(self):
        query1 = "$filter=name eq 'Chunt' or name eq 'Spintax'"
        query2 = "$count=false"
        query3 = "$orderby=id desc"
        query4 = "$skip=1"

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query1 + '&' +
                                   query2 + '&' +
                                   query3 + '&' +
                                   query4
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.count')
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_query_order5(self):
        query1 = "$filter=name eq 'Chunt' or name eq 'Spintax'"
        query2 = "$count=false"
        query3 = "$orderby=id desc"
        query4 = "$skip=1"
        query5 = "$top=1"

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query1 + '&' +
                                   query2 + '&' +
                                   query3 + '&' +
                                   query4 + '&' +
                                   query5
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.count')
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    # need to test if this is done after pagination
    def test_query_order6(self):
        query1 = "$filter=name eq 'Chunt' or name eq 'Spintax'"
        query2 = "$count=false"
        query3 = "$orderby=id desc"
        query4 = "$skip=1"
        query5 = "$top=1"
        query6 = "$expand=Observations"

        response = self.client.get('/api/v1.0/Datastreams?' +
                                   query1 + '&' +
                                   query2 + '&' +
                                   query3 + '&' +
                                   query4 + '&' +
                                   query5 + '&' +
                                   query6
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.count')
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]), 14)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')
        self.assertEqual(len(response.data['value'][0]['Observations']), 6)
        self.assertEqual(len(response.data['value'][0]['Observations'][0]), 7)
        self.assertEqual(response.data['value'][0]['Observations'][0]['result'], 42)


class A_2_1_2(APITestCase):
    """
    Check if the service supports $expand and $select as defined in this
    specification.
    """
    def setUp(self):
        """
        Create test resources
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        ObservedProperty.objects.create(
            name='Truth',
            definition='https://hellofromthemagictavern.com/',
            description='This is a test'
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Sensor.objects.create(
            name='Lie Detector',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        location = Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=4326)
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
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        Datastream.objects.create(
            name='Spintax',
            description='The Green',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation",
            unitOfMeasurement={"Race": "Wizard",
                               "Class": "Master of Truth and Lies"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Lie Detector'),
            ObservedProperty=ObservedProperty.objects.get(name='Truth')
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:00:00+00:00",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:00:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:01:00+00:00",
            result=3,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:01:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:02:00+00:00",
            result=15.7,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:02:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:03:00+00:00",
            result=23,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:03:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:04:00+00:00",
            result=1,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:04:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:05:00+00:00",
            result=35,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:05:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:06:00+00:00",
            result='Lie',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:06:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:07:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:07:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T19:08:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T19:08:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T15:00:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T15:00:00+00:00"
            )

    def test_expand_things1(self):
        query = '$expand=Datastreams'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]['Datastreams']), 2)
        self.assertEqual(len(response.data['value'][0]['Datastreams'][0]), 13)
        self.assertEqual(response.data['value'][0]['Datastreams'][0]['name'], 'Chunt')
        self.assertEqual(response.data['value'][0]['Datastreams'][1]['name'], 'Spintax')

    def test_expand_thing2(self):
        query = '$expand=Locations'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]['Locations'][0]), 8)
        self.assertEqual(response.data['value'][0]['Locations'][0]['name'], 'Location 1')

    def test_expand_things3(self):
        hlocat = HistoricalLocation.objects.get(Thing__name='Thing 1')
        query = '$expand=HistoricalLocations'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]['HistoricalLocations']), 1)
        self.assertEqual(len(response.data['value'][0]['HistoricalLocations'][0]), 5)
        self.assertEqual(response.data['value'][0]['HistoricalLocations'][0]['@iot.id'], hlocat.id)

    def test_expand_things_nested1(self):
        hlocat = HistoricalLocation.objects.get(Thing__name='Thing 1')
        query = '$expand=Locations/HistoricalLocations'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]['Locations'][0]), 9)
        self.assertEqual(response.data['value'][0]['Locations'][0]['name'], 'Location 1')
        self.assertEqual(len(response.data['value'][0]['Locations'][0]['HistoricalLocations']), 1)
        self.assertEqual(response.data['value'][0]['Locations'][0]['HistoricalLocations'][0]['@iot.id'], hlocat.id)

    def test_expand_things_nested2(self):
        hlocat = HistoricalLocation.objects.get(Thing__name='Thing 1')
        query = '$expand=HistoricalLocations/Locations'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]['HistoricalLocations']), 1)
        self.assertEqual(len(response.data['value'][0]['HistoricalLocations'][0]), 6)
        self.assertEqual(response.data['value'][0]['HistoricalLocations'][0]['@iot.id'], hlocat.id)
        self.assertEqual(len(response.data['value'][0]['HistoricalLocations'][0]['Locations'][0]), 8)
        self.assertEqual(response.data['value'][0]['HistoricalLocations'][0]['Locations'][0]['name'], 'Location 1')

    def test_expand_things_nested3(self):
        query = '$expand=Datastreams/Sensor'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]['Datastreams']), 2)
        self.assertEqual(len(response.data['value'][0]['Datastreams'][0]), 14)
        self.assertEqual(response.data['value'][0]['Datastreams'][0]['name'], 'Chunt')
        self.assertEqual(len(response.data['value'][0]['Datastreams'][0]['Sensor']), 7)
        self.assertEqual(response.data['value'][0]['Datastreams'][0]['Sensor']['name'], 'Temperature Sensor')

    def test_expand2(self):
        query = '$expand=Datastreams,Locations'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(len(response.data['value'][0]['Datastreams']), 2)
        self.assertEqual(len(response.data['value'][0]['Datastreams'][0]), 13)
        self.assertEqual(response.data['value'][0]['Datastreams'][0]['name'], 'Chunt')
        self.assertEqual(response.data['value'][0]['Datastreams'][1]['name'], 'Spintax')
        self.assertEqual(len(response.data['value'][0]['Locations'][0]), 8)
        self.assertEqual(response.data['value'][0]['Locations'][0]['name'], 'Location 1')

    def test_nested_expand(self):
        query = '$expand=Observations'
        thing = Thing.objects.get(name='Thing 1')
        response = self.client.get('/api/v1.0/Things('
                                   + str(thing.id) +
                                   ')/Datastreams?' +
                                   query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(len(response.data['value'][0]['Observations']), 6)
        self.assertEqual(len(response.data['value'][1]['Observations']), 4)
        self.assertEqual(response.data['value'][0]['Observations'][0]['result'], 42)

    def test_select1(self):
        query = '$select=name'
        response = self.client.get('/api/v1.0/Datastreams?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(len(response.data['value'][0]), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_select2(self):
        query = '$select=name,description'
        response = self.client.get('/api/v1.0/Datastreams?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(len(response.data['value'][0]), 2)
        self.assertEqual(response.data['value'][1]['name'], 'Spintax')

    def test_select3(self):
        thing = Thing.objects.get(name='Thing 1')
        datastream = Datastream.objects.get(name='Chunt')
        query = '$select=result,phenomenonTime'
        response = self.client.get(
            '/api/v1.0/Things(' + str(thing.id) + ')/Datastreams(' +
            str(datastream.id) + ')/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 6)
        self.assertEqual(len(response.data['value'][0]), 2)
        self.assertEqual(response.data['value'][0]['result'], 42)

    # # this feature hasnt been implemented yet
    # def test_expand_things_filter1(self):
    #     query = '$expand=Datastreams($top=1)'
    #     response = self.client.get('/api/v1.0/Things?' + query)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # so return 501 for now
    def test_expand_things_filter2(self):
        query = '$expand=Datastreams($top=1)'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)


class A_2_1_3(APITestCase):
    """
    Check when a client requests an entity that is not available in the
    service, if the service responds with 404 Not Found or 410 Gone as
    defined in the requirement
    http://www.opengis.net/spec/iot_sensing/1.0/req/request-data/status-code
    Check when a client use a query option that doesn't support by the
    service, if the service fails the request and responds with 501 NOT
    Implemented as defined in the requirement
    http://www.opengis.net/spec/iot_sensing/1.0/req/request-data/query-status-code.
    """
    def test__not_found(self):
        response = self.client.get("/api/v1.0/observe")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_requirement21(self):
        query1 = "$filter=year(resultTime) ne year(phenomenonTime)"
        query2 = "$select=result"
        response = self.client.get("/api/v1.0/Observations?"
                                   + query1 +
                                   '&' + query2)
        self.assertEqual(response.status_code,
                         status.HTTP_501_NOT_IMPLEMENTED)


class A_2_1_4(APITestCase):
    """
    Check if the service supports the $orderby query option as defined in this
    specification.
    """
    def setUp(self):
        """
        Create test resources
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        ObservedProperty.objects.create(
            name='Truth',
            definition='https://hellofromthemagictavern.com/',
            description='This is a test'
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Sensor.objects.create(
            name='Lie Detector',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
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
        Datastream.objects.create(
            name='Spintax',
            description='The Green',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation",
            unitOfMeasurement={"Race": "Wizard",
                               "Class": "Master of Truth and Lies"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Lie Detector'),
            ObservedProperty=ObservedProperty.objects.get(name='Truth')
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:01:00+00:00",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:01:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:02:00+00:00",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:02:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:03:00+00:00",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:03:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:04:00+00:00",
            result=23,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:04:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:05:00+00:00",
            result=1,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:05:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:06:00+00:00",
            result=35,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:06:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:07:00+00:00",
            result='Lie',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:07:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:08:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:08:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:09:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:09:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:00:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:00:00+00:00"
            )

    def test_orderby1(self):
        query = '$orderby=result'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 'Lie')
        self.assertEqual(response.data['value'][-1]['result'], 42)

    def test_orderby2(self):
        query = '$orderby=result asc'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 'Lie')
        self.assertEqual(response.data['value'][-1]['result'], 42)

    def test_orderby3(self):
        query = '$orderby=result desc'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)
        self.assertEqual(response.data['value'][-1]['result'], 'Lie')

    def test_orderby4(self):
        thing = Thing.objects.get(name='Thing 1')
        datastream = Datastream.objects.get(name='Chunt')
        query = '$orderby=id'
        response = self.client.get(
            '/api/v1.0/Things(' + str(thing.id) + ')/Datastreams(' +
            str(datastream.id) + ')/Observations?' + query)
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)
        self.assertEqual(response.data['value'][-1]['result'], 'Truth')

    def test_orderby5(self):
        query = '$orderby=result,id'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 'Lie')
        self.assertEqual(response.data['value'][-1]['result'], 42)

    def test_orderby6(self):
        query = '$orderby=result desc,id desc'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)
        self.assertEqual(response.data['value'][-1]['result'], 'Lie')

    def test_orderby7(self):
        Observation.objects.create(
            phenomenonTime="2019-02-07T20:11:00+00:00",
            result=None,
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T20:11:00+00:00"
            )
        query = '$orderby=result'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 11)
        self.assertEqual(response.data['value'][0]['result'], None)

        query = '$orderby=result desc'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 11)
        self.assertEqual(response.data['value'][-1]['result'], None)


class A_2_1_5(APITestCase):
    """
    Check if the service supports the $top, $skip and $count query option
    as defined in this specification.
    """
    def setUp(self):
        """
        Create test resources
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        ObservedProperty.objects.create(
            name='Truth',
            definition='https://hellofromthemagictavern.com/',
            description='This is a test'
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Sensor.objects.create(
            name='Lie Detector',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
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
        Datastream.objects.create(
            name='Spintax',
            description='The Green',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation",
            unitOfMeasurement={"Race": "Wizard",
                               "Class": "Master of Truth and Lies"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Lie Detector'),
            ObservedProperty=ObservedProperty.objects.get(name='Truth')
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:01:00+00:00",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:01:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:02:00+00:00",
            result=3,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:02:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:03:00+00:00",
            result=15.7,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:03:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:04:00+00:00",
            result=23,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:04:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:05:00+00:00",
            result=1,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:05:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:06:00+00:00",
            result=35,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:06:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:07:00+00:00",
            result='Lie',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:07:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:08:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:08:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:09:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:09:00+00:00",
            )
        Observation.objects.create(
            phenomenonTime="2019-02-07T21:00:00+00:00",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime="2019-02-07T21:00:00+00:00"
            )

    # requirement 26
    def test_top1(self):
        query = '$top=1'
        response = self.client.get('/api/v1.0/Datastreams?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_top2(self):
        query = '$top=3'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 3)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_top3(self):
        thing = Thing.objects.get(name='Thing 1')
        datastream = Datastream.objects.get(name='Chunt')
        query = '$top=2'
        response = self.client.get(
            '/api/v1.0/Things(' + str(thing.id) + ')/Datastreams(' +
            str(datastream.id) + ')/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_top4(self):
        query = '$top=-1'
        response = self.client.get('/api/v1.0/Datastreams?' + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top5(self):
        for i in range(2, 151):
            Thing.objects.create(
                name='Thing ' + str(i),
                description='This is a thing',
                properties={}
                )
        query = '$top=150'
        response = self.client.get('/api/v1.0/Things?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 100)

    # requirement 27
    def test_skip1(self):
        query = '$skip=5'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 5)
        self.assertEqual(response.data['value'][0]['result'], 35)

    def test_skip2(self):
        thing = Thing.objects.get(name='Thing 1')
        datastream = Datastream.objects.get(name='Chunt')
        query = '$skip=4'
        response = self.client.get(
            '/api/v1.0/Things(' + str(thing.id) + ')/Datastreams(' +
            str(datastream.id) + ')/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['result'], 1)

    def test_skip3(self):
        query = '$top=-1'
        response = self.client.get('/api/v1.0/Datastreams?' + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_skip4(self):
        query = '$skip=5'
        response = self.client.get('/api/v1.0/Datastreams?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    # requirement 28
    def test_count1(self):
        response = self.client.get('/api/v1.0/Observations?')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['@iot.count'], 10)

    def test_count2(self):
        query = '$count=true'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['@iot.count'], 10)

    def test_count3(self):
        query = '$count=false'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.count')

    def test_count4(self):
        query = '$count=certainly'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_count5(self):
        query = '$count=True'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_count6(self):
        query = '$top=1'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['@iot.count'], 10)

    def test_count7(self):
        query = '$skip=5'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['@iot.count'], 10)

    def test_count8(self):
        query = '$expand=FeaturesOfInterest'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['@iot.count'], 10)

    def test_count9(self):
        query = '$filter=result eq 42'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['@iot.count'], 1)


class A_2_1_6(APITestCase):
    """
    Check if the service supports the $filter query option and the built-in
    filter operators and built-in filter functions as defined in this
    specification.
    """
    def setUp(self):
        """
        Create test resources
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        ObservedProperty.objects.create(
            name='Truth',
            definition='https://hellofromthemagictavern.com/',
            description='This is a test'
            )
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Sensor.objects.create(
            name='Lie Detector',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        Location.objects.create(
            name='Location 3',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (135.288531, 34.789453),
                    (135.701559, 34.773257),
                    (135.608207, 34.587794),
                    (135.29794, 34.50302),
                    (135.288531, 34.789453)), srid=4326)
            )
        Location.objects.create(
            name='Location 4',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point((135.605054, 34.619524), srid=4326)
            )
        Location.objects.create(
            name='Location 5',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (135.517828, 34.542771),
                    (135.517828, 34.64922),
                    (135.703099, 34.64922),
                    (135.703099, 34.542771),
                    (135.517828, 34.542771)), srid=4326)
            )
        Location.objects.create(
            name='Location 6',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (135.639727, 34.590718),
                    (135.863411, 34.521241),
                    (135.80985, 34.425465),
                    (135.609516, 34.396287),
                    (135.639727, 34.590718)), srid=4326)
            )
        Location.objects.create(
            name='Location 7',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (134.863299, 34.47535),
                    (134.863299, 34.513064),
                    (134.915468, 34.513064),
                    (134.915468, 34.47535),
                    (134.863299, 34.47535)), srid=4326)
        )
        Location.objects.create(
            name='Location 8',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (135.758314, 34.520396),
                    (135.787657, 34.492533),
                    (135.991479, 34.582866),
                    (135.947796, 34.676051),
                    (135.877388, 34.681693),
                    (135.758314, 34.520396)), srid=4326)
        )
        # The following two should test for Contain or Within
        Location.objects.create(
            name='Location 9',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (134.833993, 35.584578),
                    (134.833993, 35.627626),
                    (134.922441, 35.627626),
                    (134.922441, 35.584578),
                    (134.833993, 35.584578)), srid=4326)
        )
        Location.objects.create(
            name='Location 10',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (134.686171, 35.450235),
                    (134.686171, 35.747313),
                    (135.064813, 35.747313),
                    (135.064813, 35.450235),
                    (134.686171, 35.450235)), srid=4326)
        )

        Location.objects.create(
            name='Location 11',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (135.952152, 34.529063),
                    (135.809416, 34.749979),
                    (136.170119, 34.821854),
                    (136.224428, 34.641664),
                    (136.259962, 34.504558),
                    (136.158049, 34.424753),
                    (135.952152, 34.529063)), srid=4326)
        )
        Location.objects.create(
            name='Location 12',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                    (135.288531, 34.789453),
                    (135.751882, 34.828926),
                    (135.64262, 34.831982),
                    (135.288531, 34.789453)), srid=4326)
            )
        Location.objects.create(
            name='Location 14',
            description='This is a test ofr location overlap',
            encodingType='application/vnd.geo+json',
            location=Polygon((
                            (135.228873, 34.358485),
                            (135.228873, 34.800581),
                            (135.856174, 34.800581),
                            (135.856174, 34.358485),
                            (135.228873, 34.358485)), srid=4326)
        )
        Location.objects.create(
            name='Location 15',
            description="This is to test st_crosses",
            encodingType='application/vnd.geo+json',
            location=LineString((135.466817, 34.709339),
                                (135.618555, 34.565613))
        )
        targ = Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        location = Location.objects.filter(name='Location 1')
        targ.Location.set(location)
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
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        Datastream.objects.create(
            name='Spintax',
            description='The Green',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation",
            unitOfMeasurement={"Race": "Wizard",
                               "Class": "Master of Truth and Lies"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Lie Detector'),
            ObservedProperty=ObservedProperty.objects.get(name='Truth')
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:00:00Z",
            result=42,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:01:00Z",
            result=3,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:02:00Z",
            result=15.7,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:03:00Z",
            result=23,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:04:00Z",
            result=1,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:05:00Z",
            result=35,
            Datastream=Datastream.objects.get(name="Chunt"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:00:00Z",
            result='Lie',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:01:00Z",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:02:00Z",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z"),
            )
        Observation.objects.create(
            phenomenonTime="2019-03-24T04:03:00Z",
            result='Truth',
            Datastream=Datastream.objects.get(name="Spintax"),
            FeatureOfInterest=FeatureOfInterest.objects.get(name='Usidore'),
            resultTime=timezone.now().strftime("%Y-%m-%d %H:%M:%S%z")
            )

    # test general complex queries: req 29
    def test_multiple1(self):
        query1 = '$filter=result gt 10 and result lt 100'
        query2 = '$select=result,phenomenonTime'
        response = self.client.get('/api/v1.0/Observations?'
                                   + query1 + '&' + query2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 4)
        self.assertEqual(len(response.data['value'][0]), 2)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_multiple2(self):
        query1 = '$filter=result lt 5'
        query2 = '$select=result,resultTime'
        query3 = '$orderby=id desc'
        datastream = Datastream.objects.get(name='Chunt')
        response = self.client.get(
            '/api/v1.0/Datastreams(' + str(datastream.id) +
            ')/Observations?' + query1 + '&' + query2 + '&' + query3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(len(response.data['value'][0]), 2)
        self.assertEqual(response.data['value'][0]['result'], 1)

    def test_multiple3(self):
        query1 = "$filter=Datastreams/Observations/FeatureOfInterest/name eq Usidore and substringof('thing',description)"
        query2 = '$top=1'
        response = self.client.get(
            '/api/v1.0/Things?' + query1 + '&' + query2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Thing 1')

    # req 30
    def test_filter_operations_eq(self):
        query = '$filter=result eq 35'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 35)

    def test_filter_operations_ne(self):
        query = "$filter=result ne 'Truth'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 7)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_gt(self):
        query = '$filter=result gt 35'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_ge(self):
        query = '$filter=result ge 35'
        response = self.client.get('/api/v1.0/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_lt(self):
        datastream = Datastream.objects.get(name="Chunt")
        query = '$filter=result lt 35'
        response = self.client.get('/api/v1.0/Datastreams(' +
                                   str(datastream.id) +
                                   ')/Observations?' +
                                   query
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 4)
        self.assertEqual(response.data['value'][0]['result'], 3)

    def test_filter_operations_le(self):
        datastream = Datastream.objects.get(name="Chunt")
        query = '$filter=result le 35'
        response = self.client.get('/api/v1.0/Datastreams(' +
                                   str(datastream.id) +
                                   ')/Observations?' +
                                   query
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 5)
        self.assertEqual(response.data['value'][0]['result'], 3)

    def test_filter_operations_and1(self):
        query = "$filter=phenomenonTime ge '2019-03-24 04:02:00Z' and result eq 'Truth'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['result'], 'Truth')

    def test_filter_operations_and2(self):
        query = "$filter=id lt 1 and result eq 'Lie'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    def test_filter_operations_and3(self):
        query = "$filter=id ge 1 and result eq 'Truth' and phenomenonTime eq '2019-03-24 04:03:00Z'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 'Truth')

    def test_filter_operations_or1(self):
        obs = Observation.objects.first()
        query = "$filter=id ge " + str(obs.id) + " or result eq 'Truth'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], obs.result['result'])

    def test_filter_operations_or2(self):
        query = "$filter=id lt 1 and result eq 'Lie' or result eq 35"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 35)

    def test_filter_operations_or3(self):
        query = "$filter=id ge 1 or result eq 'Truth' or result eq 'Lie'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_not1(self):
        query = "$filter=not result eq 'Lie' or result eq 'Truth'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 9)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_not2(self):
        query = "$filter=not (result eq Lie or result eq Truth)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 6)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_not3(self):
        query = "$filter=not (id gt 10 and result eq 'Truth')"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 7)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_not4(self):
        query = "$filter=not (result eq Truth or result ne 35)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 35)

    def test_filter_operations_not5(self):
        query = "$filter=not (result eq Truth or result ne 35) or result eq 3"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['result'], 3)

    def test_filter_operations_not6(self):
        query = "$filter=result eq 3 or not (result eq Truth or result ne 35)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['result'], 3)

    def test_filter_operations_not7(self):
        query = "$filter=not (result eq Truth or result ne 35) and id eq 1 or phenomenonTime eq '2019-03-24 04:00:00Z'"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_group1(self):
        query = "$filter=(result eq 15.7)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 15.7)

        query = "$filter=((result eq 15.7))"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 15.7)

        query = "$filter=(((result eq 15.7)))"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 15.7)

    def test_filter_operations_group2(self):
        query = "$filter=(result eq 42) and (result eq 35)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    def test_filter_operations_group3(self):
        query = "$filter=(result sub 5 gt 10) or (result eq 35)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 4)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_group4(self):
        query = "$filter=(result sub 5) gt 10"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    # FUNCTION TESTS: req 31
    def test_filter_functions_substringof1(self):
        query = "$filter=substringof('Bing Bong',description)"
        response = self.client.get("/api/v1.0/Datastreams?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_filter_functions_substringof2(self):
        query = "$filter=not substringof('Bing Bong',description)"
        response = self.client.get("/api/v1.0/Datastreams?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')

    def test_filter_functions_endswith1(self):
        query = "$filter=endswith(description,'Bong')"
        response = self.client.get("/api/v1.0/Datastreams?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_filter_functions_endswith2(self):
        query = "$filter=not endswith(description,'Bong')"
        response = self.client.get("/api/v1.0/Datastreams?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')

    def test_filter_functions_startswith1(self):
        query = "$filter=startswith(description,'Bing')"
        response = self.client.get("/api/v1.0/Datastreams?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_filter_functions_startswith2(self):
        query = "$filter=not startswith(description,'Bing')"
        response = self.client.get("/api/v1.0/Datastreams?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')

    def test_filter_functions_length1(self):
        query = "length(description) eq 9"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_filter_functions_length2(self):
        query = "not length(description) eq 9"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    def test_filter_functions_length3(self):
        query = "length(name) eq 12"
        response = self.client.get("/api/v1.0/Sensors?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Lie Detector')

    def test_filter_functions_tolower1(self):
        query = "tolower(description) eq 'the green'"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')

    def test_filter_functions_tolower2(self):
        query = "not tolower(description) eq 'the green'"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_filter_functions_tolower3(self):
        query = "tolower(name) eq 'spintax'"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')

    def test_filter_functions_toupper1(self):
        query = "toupper(description) eq 'THE GREEN'"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')

    def test_filter_functions_tupperr2(self):
        query = "not toupper(description) eq 'THE GREEN'"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Chunt')

    def test_filter_functions_toupper3(self):
        query = "toupper(name) eq 'SPINTAX'"
        response = self.client.get("/api/v1.0/Datastreams?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Spintax')

    def test_filter_functions_year1(self):
        query = "$filter=year(phenomenonTime) eq 2019"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_functions_year2(self):
        query = "$filter=not year(phenomenonTime) eq 2019"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    def test_filter_functions_year3(self):
        query = "$filter=year(phenomenonTime) eq year(phenomenonTime)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)

    def test_filter_functions_month1(self):
        query = "$filter=month(phenomenonTime) eq 03"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_functions_month2(self):
        query = "$filter=not month(phenomenonTime) eq 03"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    def test_filter_functions_day1(self):
        query = "$filter=day(phenomenonTime) eq 24"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_functions_day2(self):
        query = "$filter=not day(phenomenonTime) eq 24"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    def test_filter_functions_hour1(self):
        query = "$filter=hour(phenomenonTime) eq 04"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_functions_hour2(self):
        query = "$filter=not hour(phenomenonTime) eq 04"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['value'])

    def test_filter_functions_minute1(self):
        query = "$filter=minute(phenomenonTime) eq 01"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['value']), 2)

    def test_filter_functions_second1(self):
        query = "$filter=second(phenomenonTime) eq 00"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['value']), 10)

    def test_filter_functions_date1(self):
        query = "$filter=date(phenomenonTime) eq 2019-03-24"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['value']), 10)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_functions_time1(self):
        query = "time(phenomenonTime) eq 04:05:00Z"
        response = self.client.get("/api/v1.0/Observations?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 35)

    def test_filter_operations_round1(self):
        query = "$filter=round(result) eq 35"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 35)

    def test_filter_operations_round2(self):
        query = "$filter=not (round(result) eq 35)"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 5)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_round3(self):
        query = "$filter=round(result) eq 16"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 15.7)

    def test_filter_operations_round4(self):
        query = "$filter=round(result) eq Truth"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_operations_floor1(self):
        query = "$filter=floor(result) eq 15"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 15.7)

    def test_filter_operations_floor2(self):
        query = "$filter=not floor(result) eq 15"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 5)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_floor3(self):
        query = "$filter=floor(result) eq Truth"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_operations_ceiling1(self):
        query = "$filter=ceiling(result) eq 16"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 15.7)

    def test_filter_operations_ceiling2(self):
        query = "$filter=not ceiling(result) eq 16"
        response = self.client.get("/api/v1.0/Observations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 5)
        self.assertEqual(response.data['value'][0]['result'], 42)

    def test_filter_operations_ceiling3(self):
        query = "ceiling(result) eq Lie"
        response = self.client.get("/api/v1.0/Observations?$filter=" + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nested_filter_operations_eq(self):
        datastream = Datastream.objects.get(name='Spintax')
        query = '$filter=result eq Lie'
        response = self.client.get('/api/v1.0/Datastreams(' +
                                   str(datastream.id) +
                                   ')/Observations?' + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['result'], 'Lie')

    # Geospatial tests
    def test_filter_spatial_equal1(self):
        query = "$filter=st_equals(location, geography'SRID=32140;POINT(954158.1 4215137.1)')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Location 1')

    def test_filter_spatial_equal2(self):
        query = "$filter=st_equals(" + \
                    "location, " + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON((" + \
                            "135.288531 34.789453, "+ \
                            "135.701559 34.773257, " + \
                            "135.608207 34.587794, " + \
                            "135.29794 34.50302, " + \
                            "135.288531 34.789453" + \
                        "))'" + \
                    ")"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Location 3')

    def test_filter_spatial_equal3(self):
        query = "$filter=st_equals(location, geography'SRID=32140;Point(954158.1,4215137.1)')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_spatial_disjoint1(self):
        query = "$filter=st_disjoint(" + \
                    "location," + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON((" + \
                            "-180 -90, " + \
                            "-180 90, " + \
                            "180 90, " + \
                            "180 -90, " + \
                            "-180 -90" + \
                        "))'" + \
                    ")"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 0)

    def test_filter_spatial_disjoint2(self):
        query = "$filter=st_disjoint(" + \
                    "location," + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON((" + \
                            "-1 -1, " + \
                            "-1 1, " + \
                            "1 1, " + \
                            "1 -1, " + \
                            "-1 -1" + \
                        "))'" + \
                    ")"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Location 1')

    def test_filter_spatial_disjoint3(self):
        query = "$filter=st_disjoint(" + \
                    "location," + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON ((" + \
                            "-180," + \
                            "-90," + \
                            "-18090," + \
                            "180 90," + \
                            "180 -90," + \
                            "-180" + \
                        "))'" + \
                    ")"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_spatial_touches1(self):
        query = "$filter=st_touches(" + \
                    "location, " + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON ((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 0)

    def test_filter_spatial_touches2(self):
        query = "$filter=st_touches(" + \
                    "location, " + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON ((" + \
                            "135.288531 34.789453," + \
                            "135.701559 34.773257," + \
                            "135.608207 34.587794," + \
                            "135.29794 34.50302," + \
                            "135.288531 34.789453" + \
                        "))'" + \
                    ")"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Location 12')

    def test_filter_spatial_within1(self):
        query = "$filter=st_within(" + \
                    "location," + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON((" + \
                            "135.228873 34.358485," + \
                            "135.228873 34.800581," + \
                            "135.856174 34.800581," + \
                            "135.856174 34.358485," + \
                            "135.228873 34.358485" + \
                        "))'" + \
                    ")"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 5)
        self.assertEqual(response.data['value'][0]['name'], 'Location 4')

    def test_filter_spatial_within2(self):
        query = "$filter=st_within(location, geography'SRID=4326;POINT(95.222 42.22)')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 0)

    def test_filter_spatial_overlaps1(self):
        query = "$filter=st_overlaps(" + \
                    "location, " + \
                    "geography'" + \
                        "SRID=4326;" + \
                        "POLYGON((" + \
                            "135.952152 34.529063, " + \
                            "135.809416 34.749979, " + \
                            "136.170119 34.821854, " + \
                            "136.224428 34.641664, " + \
                            "136.259962 34.504558, " + \
                            "136.158049 34.424753, " + \
                            "135.952152 34.529063" + \
                        "))'" + \
                    ")"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['name'], 'Location 8')
        self.assertEqual(response.data['value'][1]['name'], 'Location 14')

    def test_filter_spatial_overlaps2(self):
        query2 = "$filter=st_overlaps(location, geography'SRID=4326;POINT(95.222 42.22)')"
        response2 = self.client.get("/api/v1.0/Locations?" + query2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['value']), 0)

    def test_filter_spatial_crosses1(self):
        query = "$filter=st_crosses(location, " + \
                    "geography'SRID=4326;LineString(135.466817 34.709339, 135.618555 34.565613)')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 2)
        self.assertEqual(response.data['value'][0]['name'], 'Location 3')
        self.assertEqual(response.data['value'][1]['name'], 'Location 5')

    def test_filter_spatial_crosses2(self):
        query2 = "$filter=st_crosses(location, geography'SRID=4326;POINT(954158.1 4215137.1)')"
        response2 = self.client.get("/api/v1.0/Locations?" + query2)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['value']), 0)

    def test_filter_spatial_intersects1(self):
        query = "$filter=st_intersects(location, " + \
                    "geography'SRID=4326;POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Location 1')

    def test_filter_spatial_intersects2(self):
        query = "$filter=st_intersects(location, geography'SRID=4326;POINT(95.222 42.22)')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 0)

    def test_filter_spatial_contains1(self):
        query = "$filter=st_contains(location, " \
                    "geography'SRID=4326;POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 0)

    def test_filter_spatial_contains2(self):
        query = "$filter=st_contains(location, geography'SRID=4326;POINT(135.452152 34.529063)')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 1)
        self.assertEqual(response.data['value'][0]['name'], 'Location 14')

    def test_filter_spatial_contains3(self):
        query = "$filter=st_contains(location, geography'SRID=4326;POINT(95.222 42.22)')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 0)

    def test_filter_spatial_relate1(self):
        query = "$filter=st_relate(location, " + \
                    "geography'SRID=4326;POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))', " + \
                    "'T********')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 13)
        self.assertEqual(response.data['value'][0]['name'], 'Location 1')

    def test_filter_spatial_relate2(self):
        query = "$filter=st_relate(location, geography'SRID=4326;POINT(95.222 42.22)', '****T****')"
        response = self.client.get("/api/v1.0/Locations?" + query)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['value']), 0)


class A_2_1_7(APITestCase):
    """
    Check if the service supports the server-driven pagination as defined in
    the requirement
    http://www.opengis.net/spec/iot_sensing/1.0/req/request-data/pagination.
    """
    def test_pagination(self):
        for i in range(1, 151):
            Thing.objects.create(
                name='Thing ' + str(i),
                description='This is a thing',
                properties={}
                )
        page1 = self.client.get('/api/v1.0/Things')
        self.assertEqual(page1.status_code, status.HTTP_200_OK)
        self.assertTrue(page1.data['@iot.nextLink'])
        self.assertEqual(len(page1.data['value']), 100)

        page2 = self.client.get(page1.data['@iot.nextLink'])
        self.assertEqual(page2.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, page2.data, '@iot.nextLink')
        self.assertEqual(len(page2.data['value']), 50)

        # i am not sure if the response should be a 400 or as is:
        response = self.client.get(page1.data['@iot.nextLink'] + "?$filter=name eq 'Thing 140'")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(KeyError, getitem, response.data, '@iot.nextLink')
        self.assertEqual(len(response.data['value']), 50)
