# from rest_framework import status
# from rest_framework.test import APITestCase
# from sensorthings.models import Thing, Location, Datastream, Sensor, \
#     ObservedProperty, Observation, FeatureOfInterest
# from django.contrib.gis.geos import Point, Polygon
# from django.utils import timezone
# from operator import getitem
#
#
# class SensorThingsAPISensingDataArray(APITestCase):
#     """
#     test id
#     requirements
#     test purpose
#     test method
#     """
#     # here are the tests
#     def test_data_array(self):
#         query = '$resultFormat=dataArray'
#         response = self.client.get('/api/v1.0/FeaturesOfInterest?' + query)
#         self.assertEqual(response.status_code, status.HTTP_501_NOT_IMPLEMENTED)
