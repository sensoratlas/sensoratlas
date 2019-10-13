from rest_framework import status
from rest_framework.test import APITestCase
from sensorAtlas.models import Thing, Location, Datastream, Sensor, \
    ObservedProperty, Observation, FeatureOfInterest, HistoricalLocation
from django.contrib.gis.geos import Point, Polygon
from django.urls import reverse


class A_3_1_1(APITestCase):
    """
    Check if the service supports the creation of entities as defined in
    this specification.
    """
    # For each SensorThings entity type creates an entity instance by
    # following the integrity constraints of Table 24 and creating the
    # related entities with a single request (i.e., deep insert), check
    # if the entity instance is successfully created and the server responds
    # as defined in this specification.
    # def test_create_thing(self):
    #     """
    #     Create a Thing without a Location.
    #     """
    #     url = reverse('thing-list',
    #                   kwargs={'version': 'v1.0'})
    #     data = {
    #             "name": "Temperature Monitoring System",
    #             "description": "Sensor system monitoring area temperature",
    #             "properties": {
    #                 "Deployment Condition": "Deployed in a third floor balcony",
    #                 "Case Used": "Radiation shield"
    #             }
    #            }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # def test_create_location(self):
    #     """
    #     Create a Location without a Thing.
    #     """
    #     url = reverse('location-list',
    #                   kwargs={'version': 'v1.0'})
    #     data = {
    #             "name": "UofC CCIT",
    #             "description": "University of Calgary, CCIT building",
    #             "encodingType": "application/vnd.geo+json",
    #             "location": {
    #                 "type": "Point",
    #                 "coordinates": [-114.133, 51.08]
    #             }
    #         }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_historicallocation(self):
        """
        Create a HistoricalLocation mandatory relations.
        """
        thing = Thing.objects.create(
            name="Thing",
            description="This is a thing",
            properties=None
        )
        location = Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
        )
        url = reverse(
            'historicallocation-list',
            kwargs={'version': 'v1.0'}
        )
        data = {
            "time": "2019-03-26T03:42:02Z",
            "Thing": {"@iot.id": thing.id},
            "Locations": [{"@iot.id": location.id}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_datastream(self):
        """
        Create a Datastream with required related fields
        """
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0'})
        data = {
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
              }
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sensor(self):
        """
        Create a Sensor.
        """
        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0'})
        data = {
            "name": "DHT22",
            "description": "DHT22 temperature sensor",
            "encodingType": "application/pdf",
            "metadata": "https://cdn-shop.adafruit.com/datasheets/DHT22.pdf"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_observedproperty(self):
        """
        Create a Observed Property.
        """
        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0'})
        data = {
            "name": "Area Temperature",
            "description": "The degree or intensity of heat present in the area",
            "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AreaTemperature"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_observation(self):
        """
        Create a Observation and link with existing datastream and feature of
        interest.
        """
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0'})
        data = {
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
              }
             }
        }
        response = self.client.post(url, data, format='json')
        datastream = Datastream.objects.get(name="Air Temperature DS")

        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0'})
        data = {
          "name": "UofC CCIT",
          "description": "University of Calgary, CCIT building",
          "encodingType": "application/vnd.geo+json",
          "feature": {
            "type": "Polygon",
            "coordinates": [((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ]
          }
        }
        response = self.client.post(url, data, format='json')
        featureofinterest = FeatureOfInterest.objects.get(name="UofC CCIT")

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0'})
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "Datastream": {"@iot.id": datastream.id},
            "FeatureOfInterest": {"@iot.id": featureofinterest.id}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_featureofinterest(self):
        """
        Create a Feature of Interest
        """
        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0'})
        data = {
          "name": "UofC CCIT",
          "description": "University of Calgary, CCIT building",
          "encodingType": "application/vnd.geo+json",
          "feature": {
            "type": "Polygon",
            "coordinates": [((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ]
          }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Create an entity instance and its related entities with a deep insert
    # request that does not conform to the specification (e.g., missing a
    # mandatory property), check if the service fails the request without
    # creating any entity within the deep insert request and responds the
    # appropriate HTTP status code.
    # and
    # For each SensorThings entity type issue an entity creation request
    # that does not follow the integrity constraints of Table 24 with deep
    # insert, check if the service fails the request without creating any
    # entity within the deep insert request and responds the appropriate
    # HTTP status code.
    def test_fail_create_thing(self):
        """
        Thing without a required field does not create.
        """
        url = reverse('thing-list',
                      kwargs={'version': 'v1.0'})
        required_fields = ['name', 'description']
        data = {
                "name": "Fail",
                "description": "Fail!"
               }
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Thing.DoesNotExist,
                              Thing.objects.get,
                              name="Fail"
                              )

    def test_fail_create_location(self):
        """
        Location without a required field does not create.
        """
        url = reverse('location-list',
                      kwargs={'version': 'v1.0'})
        required_fields = ['name', 'description', 'encodingType', 'location']
        data = {
                "name": "UofC CCIT",
                "description": "University of Calgary, CCIT building",
                "encodingType": "application/vnd.geo+json",
                "location": {
                    "type": "Point",
                    "coordinates": [-114.133, 51.08]
                }
              }
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Location.DoesNotExist,
                              Location.objects.get,
                              name="UofC CCIT"
                              )

    def test_fail_create_historicallocation(self):
        """
        HistoricalLocation without a required field does not create. Nested
        entities also do not create.
        """
        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0'})
        required_fields = ['time', 'Thing', 'Locations']
        data = {
                "time": "2019-03-26T03:42:02+0900",
                "Thing": {
                    "name": "Temperature Monitoring System",
                    "description": "Sensor system monitoring area temperature",
                    "properties": {
                        "Deployment Condition": "Deployed in a third floor balcony",
                        "Case Used": "Radiation shield"
                        }
                    },
                "Locations": [{
                    "name": "Location 2",
                    "description": "University of Calgary, CCIT building",
                    "encodingType": "application/vnd.geo+json",
                    "location": {
                        "type": "Point",
                        "coordinates": [-115.133, 51.08]
                    }
                }]
              }
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              HistoricalLocation.DoesNotExist,
                              HistoricalLocation.objects.get,
                              time="2019-03-26T03:42:02+0900"
                              )
            if field == 'Locations':
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )
            if field == 'Thing':
                self.assertRaises(
                                  Location.DoesNotExist,
                                  Location.objects.get,
                                  name="Location 2"
                                  )

    def test_fail_create_datastream(self):
        """
        Datastreams without a required field does not create. Nested
        entities also do not create.
        """
        url = reverse(
                'datastream-list',
                kwargs={'version': 'v1.0'}
                )
        required_fields = [
                'name',
                'description',
                'unitOfMeasurement',
                'observationType',
                'Thing',
                'Sensor',
                'ObservedProperty'
                ]
        data = {
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
                    }
                }
            }
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Datastream.DoesNotExist,
                              Datastream.objects.get,
                              name="Air Temperature DS"
                              )
            if field == 'Thing':
                self.assertRaises(
                                  Sensor.DoesNotExist,
                                  Sensor.objects.get,
                                  name="DHT22"
                                  )
                self.assertRaises(
                                  ObservedProperty.DoesNotExist,
                                  ObservedProperty.objects.get,
                                  name="Area Temperature"
                                  )
            if field == 'Sensor':
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )
                self.assertRaises(
                                  ObservedProperty.DoesNotExist,
                                  ObservedProperty.objects.get,
                                  name="Area Temperature"
                                  )
            if field == 'ObservedProperty':
                self.assertRaises(
                                  Sensor.DoesNotExist,
                                  Sensor.objects.get,
                                  name="DHT22"
                                  )
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )

    def test_fail_create_sensor(self):
        """
        Sensors without a required field does not create.
        """
        url = reverse('sensor-list',
                      kwargs={'version': 'v1.0'})
        required_fields = [
                'name',
                'description',
                'encodingType',
                'metadata'
                ]
        data = {
                "name": "DHT22",
                "description": "DHT22 temperature sensor",
                "encodingType": "application/pdf",
                "metadata": "https://cdn-shop.adafruit.com/datasheets/DHT22.pdf"
               }
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Sensor.DoesNotExist,
                              Sensor.objects.get,
                              name="DHT22"
                              )

    def test_fail_create_observedproperty(self):
        """
        Observed Properties without a required field does not create.
        """
        url = reverse('observedproperty-list',
                      kwargs={'version': 'v1.0'})
        required_fields = [
                'name',
                'description',
                'definition'
                ]
        data = {
                "name": "Area Temperature",
                "description": "The degree or intensity of heat present in the area",
                "definition": "http://www.qudt.org/qudt/owl/1.0.0/quantity/Instances.html#AreaTemperature"
               }
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              ObservedProperty.DoesNotExist,
                              ObservedProperty.objects.get,
                              name="Area Temperature"
                              )

    def test_fail_create_observation(self):
        """
        Observation without a required field does not create. Nested
        entities also do not create.
        """
        url = reverse('observation-list',
                      kwargs={'version': 'v1.0'})
        required_fields = ['result', 'Datastream', 'FeatureOfInterest']
        data = {
                "result": 2,
                "Datastream": {
                    "name": "oven temperature",
                    "description": "This is a datastream for an oven’s internal temperature.",
                    "unitOfMeasurement": {
                        "name": "degree Celsius",
                        "symbol": "°C",
                        "definition": "http://unitsofmeasure.org/ucum.html#para-30"
                        },
                    "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                    "ObservedProperty": {
                        "name": "DewPoint Temperature",
                        "definition": "http://sweet.jpl.nasa.gov/ontology/property.owl#DewPointTemperature",
                        "description": """The dewpoint temperature is the temperature to which the air must be
                                        cooled, at constant pressure, for dew to form. As the grass and other objects
                                        near the ground cool to the dewpoint, some of the water vapor in the
                                        atmosphere condenses into liquid water on the objects."""
                    },
                    "Sensor": {
                        "name": "DS18B20",
                        "description": "DS18B20 is an air temperature sensor…",
                        "encodingType": "application/pdf",
                        "metadata": "http://datasheets.maxim-ic.com/en/ds/DS18B20.pdf"
                    },
                    "Thing": {
                        "name": "Thing 1",
                        "description": "Just a thing"
                    }
                },
                "FeatureOfInterest": {
                    "name": "Location 2",
                    "description": "University of Calgary, CCIT building",
                    "encodingType": "application/vnd.geo+json",
                    "feature": {
                        "type": "Point",
                        "coordinates": [-115.133, 51.08]
                    }
                }
              }
        for field in required_fields:
            if field == "FeatureOfInterest":
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Observation.DoesNotExist,
                              Observation.objects.get,
                              result=2
                              )
            if field == 'Datastream':
                self.assertRaises(
                                  FeatureOfInterest.DoesNotExist,
                                  FeatureOfInterest.objects.get,
                                  name="Location 2"
                                  )

    def test_fail_create_featureofinterest(self):
        """
        FeatureOfInterest without a required field does not create.
        """
        url = reverse('featureofinterest-list',
                      kwargs={'version': 'v1.0'})
        required_fields = ['name', 'description', 'encodingType', 'feature']
        data = {
                "name": "UofC CCIT",
                "description": "University of Calgary, CCIT building",
                "encodingType": "application/vnd.geo+json",
                "feature": {
                    "type": "Point",
                    "coordinates": [-114.133, 51.08]
                }
              }
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              FeatureOfInterest.DoesNotExist,
                              FeatureOfInterest.objects.get,
                              name="UofC CCIT"
                              )

    # For each SensorThings entity type creates an entity instance by linking
    # to existing entities with a single request, check if the server responds
    # as defined in this specification.
    # and
    # For each SensorThings entity type creates an entity instance that does
    # not follow the integrity constraints of Table 24 by linking to existing
    # entities with a single request, check if the server responds as defined
    # in this specification.
    def test_create_location_thing_linking(self):
        """
        Create a Location by linking to an existing Thing
        """
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing = Thing.objects.get(name='Thing 1')
        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        data = {
                "name": "UofC CCIT",
                "description": "University of Calgary, CCIT building",
                "encodingType": "application/vnd.geo+json",
                "location": {
                    "type": "Point",
                    "coordinates": [-114.133, 51.08]
                  }
              }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_historicallocation_location_linking(self):
        """
        Create a HistoricalLocation by linking to an existing Location
        """
        Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        location = Location.objects.get(name='Location 1')
        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id
                              })
        data = {
                "time": "2019-03-26T03:42:02+0900",
                "Thing": {
                    "name": "Temperature Monitoring System",
                    "description": "Sensor system monitoring area temperature",
                    "properties": {
                        "Deployment Condition": "Deployed in a third floor balcony",
                        "Case Used": "Radiation shield"
                    }
                }
              }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_historicallocation_thing_linking(self):
        """
        Create a HistoricalLocation by linking to an existing Thing
        """
        thing = Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing = Thing.objects.get(name='Thing 1')
        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        data = {
                "time": "2019-03-26T03:42:02+0900",
                "Locations": [{
                    "name": "Location 3",
                    "description": "University of Calgary, CCIT building",
                    "encodingType": "application/vnd.geo+json",
                    "location": {
                        "type": "Point",
                        "coordinates": [-105.133, 55.08]
                    }
                }]
              }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_thing_location_linking(self):
        """
        Create a Thing by linking to an existing Location
        """
        Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        location = Location.objects.get(name='Location 1')
        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id
                              })
        data = {
                "name": "Temperature Monitoring System",
                "description": "Sensor system monitoring area temperature",
                "properties": {
                    "Deployment Condition": "Deployed in a third floor balcony",
                    "Case Used": "Radiation shield"
                }
              }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_datastream_thing_linking(self):
        """
        Create a Datastream by linking to an existing Thing
        """
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing = Thing.objects.get(name='Thing 1')
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        data = {
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
                }
              }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_datastream_sensor_linking(self):
        """
        Create a Datastream by linking to an existing Sensor
        """
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        sensor = Sensor.objects.get(name='Temperature Sensor')
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id
                              })
        data = {
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
                "Thing": {
                  "name": "Temperature Monitoring System",
                  "description": "Sensor system monitoring area temperature",
                  "properties": {
                      "Deployment Condition": "Deployed in a third floor balcony",
                      "Case Used": "Radiation shield"
                  }
                }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_datastream_observedproperty_linking(self):
        """
        Create a Datastream by linking to an existing Observed Property
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        observedproperty = ObservedProperty.objects.get(name='Temperature')
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': observedproperty.id
                              })
        data = {
                "name": "Air Temperature DS",
                "description": "Datastream for recording temperature",
                "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "unitOfMeasurement": {
                  "name": "Degree Celsius",
                  "symbol": "degC",
                  "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius"
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
                  }
                }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_observation_datastream_linking(self):
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
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        foi = FeatureOfInterest.objects.create(
            name='Usidore',
            description='this is a place',
            encodingType='application/vnd.geo+json',
            feature=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ))
        datastream = Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id
                              })
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "FeatureOfInterest": {"@iot.id": foi.id}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_observation_featureofinterest_linking(self):
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
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        foi = FeatureOfInterest.objects.create(
            name='Usidore',
            description='this is a place',
            encodingType='application/vnd.geo+json',
            feature=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ))
        datastream = Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )

        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id
                              })
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "Datastream": {"@iot.id": datastream.id}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_create_location_thing_linking(self):
        """
        Create a Location by linking to an existing Thing
        """
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing = Thing.objects.get(name='Thing 1')
        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        data = {
                "name": "UofC CCIT",
                "description": "University of Calgary, CCIT building",
                "encodingType": "application/vnd.geo+json",
                "location": {
                    "type": "Point",
                    "coordinates": [-114.133, 51.08]
                  }
              }
        required_fields = ['name', 'description', 'encodingType', 'location']
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Location.DoesNotExist,
                              Location.objects.get,
                              name="UofC CCIT"
                              )

    def test_fail_create_historicallocation_location_linking(self):
        """
        Create a HistoricalLocation by linking to an existing Location
        """
        Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        location = Location.objects.get(name='Location 1')
        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id
                              })
        data = {
                "time": "2019-03-26T03:42:02+0900",
                "Thing": {
                    "name": "Temperature Monitoring System",
                    "description": "Sensor system monitoring area temperature",
                    "properties": {
                        "Deployment Condition": "Deployed in a third floor balcony",
                        "Case Used": "Radiation shield"
                    }
                }
              }
        required_fields = ['time', 'Thing', 'Locations']
        for field in required_fields:
            if field == 'Locations':
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              HistoricalLocation.DoesNotExist,
                              HistoricalLocation.objects.get,
                              time="2019-03-26T03:42:02+0900"
                              )
            if field == 'Thing':
                self.assertRaises(
                                  Location.DoesNotExist,
                                  Location.objects.get,
                                  name="Location 2"
                                  )

    def test_fail_create_historicallocation_thing_linking(self):
        """
        Create a HistoricalLocation by linking to an existing Thing
        """
        thing = Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing = Thing.objects.get(name='Thing 1')
        url = reverse('historicallocation-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        data = {
                "time": "2019-03-26T03:42:02+0900",
                "Locations": [{
                    "name": "Location 3",
                    "description": "University of Calgary, CCIT building",
                    "encodingType": "application/vnd.geo+json",
                    "location": {
                        "type": "Point",
                        "coordinates": [-105.133, 55.08]
                    }
                }]
              }
        required_fields = ['time', 'Thing', 'Locations']
        for field in required_fields:
            if field == 'Thing':
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              HistoricalLocation.DoesNotExist,
                              HistoricalLocation.objects.get,
                              time="2019-03-26T03:42:02+0900"
                              )
            if field == 'Locations':
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )

    def test_fail_create_thing_location_linking(self):
        """
        Create a Thing by linking to an existing Location
        """
        Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        location = Location.objects.get(name='Location 1')
        url = reverse('thing-list',
                      kwargs={'version': 'v1.0',
                              'Locations_pk': location.id
                              })
        data = {
                "name": "Temperature Monitoring System",
                "description": "Sensor system monitoring area temperature",
                "properties": {
                    "Deployment Condition": "Deployed in a third floor balcony",
                    "Case Used": "Radiation shield"
                }
              }
        required_fields = ['name', 'description']
        for field in required_fields:
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Thing.DoesNotExist,
                              Thing.objects.get,
                              name="Fail"
                              )

    def test_fail_create_datastream_thing_linking(self):
        """
        Create a Datastream by linking to an existing Thing
        """
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing = Thing.objects.get(name='Thing 1')
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        data = {
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
                }
              }
        required_fields = [
                'name',
                'description',
                'unitOfMeasurement',
                'observationType',
                'Thing',
                'Sensor',
                'ObservedProperty'
                ]
        for field in required_fields:
            if field == "Thing":
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Datastream.DoesNotExist,
                              Datastream.objects.get,
                              name="Air Temperature DS"
                              )
            if field == 'Sensor':
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )
                self.assertRaises(
                                  ObservedProperty.DoesNotExist,
                                  ObservedProperty.objects.get,
                                  name="Area Temperature"
                                  )
            if field == 'ObservedProperty':
                self.assertRaises(
                                  Sensor.DoesNotExist,
                                  Sensor.objects.get,
                                  name="DHT22"
                                  )
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )

    def test_fail_create_datastream_sensor_linking(self):
        """
        Create a Datastream by linking to an existing Sensor
        """
        Sensor.objects.create(
            name='Temperature Sensor',
            description='This is a sensor test',
            encodingType='PDF',
            metadata='This is some very descriptive metadata.'
            )
        sensor = Sensor.objects.get(name='Temperature Sensor')
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'Sensors_pk': sensor.id
                              })
        data = {
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
                "Thing": {
                  "name": "Temperature Monitoring System",
                  "description": "Sensor system monitoring area temperature",
                  "properties": {
                      "Deployment Condition": "Deployed in a third floor balcony",
                      "Case Used": "Radiation shield"
                  }
                }
        }
        required_fields = [
                'name',
                'description',
                'unitOfMeasurement',
                'observationType',
                'Thing',
                'Sensor',
                'ObservedProperty'
                ]
        for field in required_fields:
            if field == "Sensor":
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Datastream.DoesNotExist,
                              Datastream.objects.get,
                              name="Air Temperature DS"
                              )
            if field == 'Thing':
                self.assertRaises(
                                  Sensor.DoesNotExist,
                                  Sensor.objects.get,
                                  name="DHT22"
                                  )
                self.assertRaises(
                                  ObservedProperty.DoesNotExist,
                                  ObservedProperty.objects.get,
                                  name="Area Temperature"
                                  )
            if field == 'ObservedProperty':
                self.assertRaises(
                                  Sensor.DoesNotExist,
                                  Sensor.objects.get,
                                  name="DHT22"
                                  )
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )

    def test_fail_create_datastream_observedproperty_linking(self):
        """
        Create a Datastream by linking to an existing Observed Property
        """
        ObservedProperty.objects.create(
            name='Temperature',
            definition='https://wikipedia.org',
            description='This is a test'
            )
        observedproperty = ObservedProperty.objects.get(name='Temperature')
        url = reverse('datastream-list',
                      kwargs={'version': 'v1.0',
                              'ObservedProperties_pk': observedproperty.id
                              })
        data = {
                "name": "Air Temperature DS",
                "description": "Datastream for recording temperature",
                "observationType": "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
                "unitOfMeasurement": {
                  "name": "Degree Celsius",
                  "symbol": "degC",
                  "definition": "http://www.qudt.org/qudt/owl/1.0.0/unit/Instances.html#DegreeCelsius"
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
                  }
                }
        }
        required_fields = [
                'name',
                'description',
                'unitOfMeasurement',
                'observationType',
                'Thing',
                'Sensor',
                'ObservedProperty'
                ]
        for field in required_fields:
            if field == "ObservedProperty":
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Datastream.DoesNotExist,
                              Datastream.objects.get,
                              name="Air Temperature DS"
                              )
            if field == 'Thing':
                self.assertRaises(
                                  Sensor.DoesNotExist,
                                  Sensor.objects.get,
                                  name="DHT22"
                                  )
                self.assertRaises(
                                  ObservedProperty.DoesNotExist,
                                  ObservedProperty.objects.get,
                                  name="Area Temperature"
                                  )
            if field == 'Sensor':
                self.assertRaises(
                                  Thing.DoesNotExist,
                                  Thing.objects.get,
                                  name="Temperature Monitoring System"
                                  )
                self.assertRaises(
                                  ObservedProperty.DoesNotExist,
                                  ObservedProperty.objects.get,
                                  name="Area Temperature"
                                  )

    def test_fail_create_observation_datastream_linking(self):
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
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        foi = FeatureOfInterest.objects.create(
            name='Usidore',
            description='this is a place',
            encodingType='application/vnd.geo+json',
            feature=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ))
        datastream = Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'Datastreams_pk': datastream.id
                              })
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "FeatureOfInterest": {"@iot.id": foi.id}
        }
        required_fields = ['result', 'Datastream', 'FeatureOfInterest']
        for field in required_fields:
            if field == "FeatureOfInterest" or field == "Datastream":
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Observation.DoesNotExist,
                              Observation.objects.get,
                              result=2
                              )

    def test_fail_create_observation_featureofinterest_linking(self):
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
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        foi = FeatureOfInterest.objects.create(
            name='Usidore',
            description='this is a place',
            encodingType='application/vnd.geo+json',
            feature=Polygon(((0.0, 0.0),
                             (0.0, 50.0),
                             (50.0, 50.0),
                             (50.0, 0.0),
                             (0.0, 0.0))
                            ))
        datastream = Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        url = reverse('observation-list',
                      kwargs={'version': 'v1.0',
                              'FeaturesOfInterest_pk': foi.id
                              })
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "Datastream": {"@iot.id": datastream.id}
        }
        required_fields = ['result', 'Datastream', 'FeatureOfInterest']
        for field in required_fields:
            if field == "FeatureOfInterest" or field == "Datastream":
                continue
            data_missing = data.copy()
            data_missing.pop(field)
            response = self.client.post(url, data_missing, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertRaises(
                              Observation.DoesNotExist,
                              Observation.objects.get,
                              result=2
                              )

    # Create an Observation entity for a Datastream without any Observations
    # and the Observation creation request does not create a new or linking
    # to an existing FeatureOfInterest, check if the service creates a new
    # FeatureOfInterest for the created Observation with the location property
    # of the Thing’s Location entity.
    # and
    # Create an Observation entity for a Datastream that already has
    # Observations and the Observation creation request does not create a
    # new or linking to an existing FeatureOfInterest, check if the service
    # automatically links the newly created Observation with an existing
    # FeatureOfInterest whose location property is from the Thing’s Location
    # entity.
    # and
    # Create an Observation entity and the Observation creation request does
    # not include resultTime, check if the resultTime property is created with
    # a null value.
    def test_create_observation_special(self):
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
            description='This is a thing'
            )
        thing.Location.add(location)
        datastream = Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        url = reverse('observation-list',
                      kwargs={'version': 'v1.0'
                              })
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "Datastream": {"@iot.id": datastream.id}
        }
        self.assertFalse(FeatureOfInterest.objects.all())
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(FeatureOfInterest.objects.all())

        obs = Observation.objects.all().first()
        self.assertTrue(obs.FeatureOfInterest)
        foi = FeatureOfInterest.objects.first()
        loc = Location.objects.get(id=location.id)
        self.assertEqual(loc.location, foi.feature)

        data = {
            "phenomenonTime": "2017-02-07T18:05:00.000Z",
            "resultTime": "2017-02-07T18:02:08.000Z",
            "result": 32.2,
            "Datastream": {"@iot.id": datastream.id}
        }
        self.assertTrue(FeatureOfInterest.objects.all())
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        obs = Observation.objects.get(result__result=32.2)
        self.assertTrue(obs.FeatureOfInterest)

        foi = FeatureOfInterest.objects.first()
        loc = Location.objects.get(id=location.id)
        self.assertEqual(loc.location, foi.feature)

        data = {
            "phenomenonTime": "2017-02-07T18:07:00.000Z",
            "result": 25,
            "Datastream": {"@iot.id": datastream.id}
        }
        self.assertTrue(FeatureOfInterest.objects.all())
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        null_check = Observation.objects.get(result__result=25)
        self.assertEqual(null_check.resultTime, None)

    def test_create_observation_special_fail(self):
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
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing'
            )
        datastream = Datastream.objects.create(
            name='Chunt',
            description='Bing Bong',
            observationType="http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement",
            unitOfMeasurement={"Race": "Badger",
                               "Class": "Shapeshifter"},
            Thing=Thing.objects.get(name='Thing 1'),
            Sensor=Sensor.objects.get(name='Temperature Sensor'),
            ObservedProperty=ObservedProperty.objects.get(name='Temperature')
            )
        url = reverse('observation-list',
                      kwargs={'version': 'v1.0'
                              })
        data = {
            "phenomenonTime": "2017-02-07T18:02:00.000Z",
            "resultTime": "2017-02-07T18:02:05.000Z",
            "result": 21.6,
            "Datastream": {"@iot.id": datastream.id}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Create a Location for a Thing entity, check if the Thing has a
    # HistoricalLocation created by the service according to the Location
    # entity.
    def test_create_historicallocation_autocreate(self):
        Thing.objects.create(
            name='Thing 1',
            description='This is a thing',
            properties={}
            )
        thing = Thing.objects.get(name='Thing 1')
        url = reverse('location-list',
                      kwargs={'version': 'v1.0',
                              'Things_pk': thing.id
                              })
        data = {
                "name": "UofC CCIT",
                "description": "University of Calgary, CCIT building",
                "encodingType": "application/vnd.geo+json",
                "location": {
                    "type": "Point",
                    "coordinates": [-114.133, 51.08]
                  }
              }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(HistoricalLocation.objects.get(Thing__name='Thing 1'))


class A_3_1_2(APITestCase):
    """
    Check if the service supports the update of entities as defined
    in this specification.
    """
    # For each SensorThings entity type send an update request with PATCH,
    # check (1) if the properties provided in the payload corresponding to
    # updatable properties replace the value of the corresponding property
    # in the entity and (2) if the missing properties of the containing entity
    # or complex property are not directly altered.
    # 10.3.2    Response
    # On success, the response SHALL be a valid success response. In addition,
    # when the client sends an update request to a valid URL where an entity
    # does not exist, the service SHALL fail the request.
    # Upon successful completion, the service must respond with 200 OK or 204
    # No Content. Regarding all the HTTP status code, please refer to the HTTP
    # Status Code section.
    def test_update_thing(self):
        """
        Update an existing Thing.
        """
        thing = Thing.objects.create(
            name='Thing 1',
            description='(T.T)',
            properties={}
            )
        url = reverse(
            'thing-detail',
            kwargs={
                'version': 'v1.0',
                'pk': thing.id
                }
            )
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Thing 1')
        self.assertEqual(response.data['description'], '(T.T)')

        data = {
            "description": "(^_^)",
        }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Thing 1')
        self.assertEqual(response.data['description'], '(^_^)')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_location(self):
        """
        Update an existing Location.
        """
        location = Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        url = reverse(
            'location-detail',
            kwargs={
                'version': 'v1.0',
                'pk': location.id
                }
            )
        data = {
                "name": "UofC CCIT",
            }

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'UofC CCIT')
        self.assertEqual(response.data['description'], 'This is a sensor test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # For each SensorThings entity type send an update request with PATCH that
    # contains related entities as inline content, check if the service fails
    # the request and returns appropriate HTTP status code.
    def test_update_thing_inline(self):
        url = reverse('thing-list',
                      kwargs={'version': 'v1.0'})
        data = {
                "name": "Temperature Monitoring System",
                "description": "Sensor system monitoring area temperature",
                "properties": {
                    "Deployment Condition": "Deployed in a third floor balcony",
                    "Case Used": "Radiation shield"
                },
                'Locations': [{
                    "name": "UofC CCIT",
                    "description": "University of Calgary, CCIT building",
                    "encodingType": "application/vnd.geo+json",
                    "location": {
                        "type": "Point",
                        "coordinates": [-114.133, 51.08]
                    }
                }]
               }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        thing = Thing.objects.get(name='Temperature Monitoring System')
        url = reverse(
            'thing-detail',
            kwargs={
                'version': 'v1.0',
                'pk': thing.id
                }
            )

        response = self.client.get(url + '?$expand=Locations')
        self.assertEqual(response.data['name'], 'Temperature Monitoring System')
        self.assertEqual(response.data['Locations'][0]['name'], 'UofC CCIT')

        location = Location.objects.create(
            name='Location 42',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )

        data = {
            'Locations': [{"@iot.id": location.id}]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url + '?$expand=Locations')
        self.assertEqual(response.data['name'], 'Temperature Monitoring System')
        self.assertEqual(response.data['Locations'][0]['name'], 'Location 42')
        self.assertTrue(response.data['Locations'], 1)

    def test_update_thing_inline_fail(self):
        url = reverse('thing-list',
                      kwargs={'version': 'v1.0'})
        data = {
                "name": "Temperature Monitoring System",
                "description": "Sensor system monitoring area temperature",
                "properties": {
                    "Deployment Condition": "Deployed in a third floor balcony",
                    "Case Used": "Radiation shield"
                },
                'Locations': [{
                    "name": "UofC CCIT",
                    "description": "University of Calgary, CCIT building",
                    "encodingType": "application/vnd.geo+json",
                    "location": {
                        "type": "Point",
                        "coordinates": [-114.133, 51.08]
                    }
                }]
               }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        thing = Thing.objects.get(name='Temperature Monitoring System')
        url = reverse(
            'thing-detail',
            kwargs={
                'version': 'v1.0',
                'pk': thing.id
                }
            )

        response = self.client.get(url + '?$expand=Locations')
        self.assertEqual(response.data['name'], 'Temperature Monitoring System')
        self.assertEqual(response.data['Locations'][0]['name'], 'UofC CCIT')

        data = {
                'Locations': [{
                    "name": "Fail",
                    "description": "University of Calgary, CCIT building",
                    "encodingType": "application/vnd.geo+json",
                    "location": {
                        "type": "Point",
                        "coordinates": [-114.133, 51.08]
                    }
                }]
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(url + '?$expand=Locations')
        self.assertEqual(response.data['name'], 'Temperature Monitoring System')
        self.assertEqual(response.data['Locations'][0]['name'], 'UofC CCIT')

    # For each SensorThings entity type send an update request with PATCH that
    # contains binding information for navigation properties, check if the
    # service updates the navigationLink accordingly.
    def test_update_thing_linked(self):
        thing = Thing.objects.create(
            name='Thing 1',
            description='(T.T)',
            properties={}
            )
        location = Location.objects.create(
            name='Location 1',
            description='This is a sensor test',
            encodingType='application/vnd.geo+json',
            location=Point(954158.1, 4215137.1, srid=32140)
            )
        thing.Location.add(location)

        url = reverse(
            'location-detail',
            kwargs={
                'version': 'v1.0',
                'Things_pk': thing.id,
                'pk': location.id
                }
            )
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Location 1')
        self.assertEqual(response.data['description'], 'This is a sensor test')

        data = {
            "description": "(^_^)",
        }
        self.client.patch(url, data, format='json')
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Location 1')
        self.assertEqual(response.data['description'], '(^_^)')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # (Where applicable) For each SensorThings entity type send an update
    # request with PUT, check if the service responds as defined in Section
    # 10.3.
    def test_update_thing_put(self):
        thing = Thing.objects.create(
            name='Thing 1',
            description='(T.T)',
            properties={}
            )
        url = reverse(
            'thing-detail',
            kwargs={
                'version': 'v1.0',
                'pk': thing.id
                }
            )
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Thing 1')
        self.assertEqual(response.data['description'], '(T.T)')

        data = {
            "name": "Thing 1",
            "description": "(^_^)",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class A_3_1_3(APITestCase):
    """
    A successful DELETE request to an entity’s edit URL deletes the entity.
    The request body SHOULD be empty.
    Services SHALL implicitly remove relations to and from an entity when
    deleting it; clients need not delete the relations explicitly.
    Services MAY implicitly delete or modify related entities if required by
    integrity constraints. Table 25 listed SensorThings API’s integrity
    constraints when deleting an entity.
    """
    # Delete an entity instance, and check if the service responds as defined
    # in Section 10.4.
    def test_delete_thing(self):
        """
        Delete an existing Thing.
        """
        thing = Thing.objects.create(
            name='Thing 1',
            description='(T.T)',
            properties={}
            )
        url = reverse(
            'thing-detail',
            kwargs={
                'version': 'v1.0',
                'pk': thing.id
                }
            )
        response = self.client.get(url)
        self.assertEqual(response.data['name'], 'Thing 1')
        self.assertEqual(response.data['description'], '(T.T)')

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
