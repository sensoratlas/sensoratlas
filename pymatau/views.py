from .models import Location, Thing, Datastream, Sensor, \
    ObservedProperty, Observation, FeatureOfInterest, HistoricalLocation
import pymatau.serializer as serializers
from .parsers import Filter, Orderby
from .viewsets import ViewSet, PropertyPath
from rest_framework import generics


class APIRoot(generics.GenericAPIView):
    """
    My API documentation
    """


class ThingView(Filter, PropertyPath.Thing, ViewSet):
    """Provides a view set of the Things entity."""
    queryset = Thing.objects.all()
    serializer_class = serializers.ThingSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class LocationView(Filter, PropertyPath.Location, ViewSet):
    """Provides a view set for the Locations entity."""
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class HistoricalLocationView(Filter, PropertyPath.HistoricalLocation, ViewSet):
    """Provides a view set for Historical Location entities."""
    queryset = HistoricalLocation.objects.all()
    serializer_class = serializers.HistoricalLocationSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class DataStreamView(Filter, PropertyPath.Datastream, ViewSet):
    """Provides a view set for the Datastreams entity"""
    queryset = DataStream.objects.all()
    serializer_class = serializers.DataStreamSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class SensorView(Filter, PropertyPath.Sensor, ViewSet):
    """Provides a view set for the Sensors entity"""
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class ObservedPropertyView(Filter, PropertyPath.ObservedProperty, ViewSet):
    """Provides a view set for the Observed Properties entity"""
    queryset = ObservedProperty.objects.all()
    serializer_class = serializers.ObservedPropertySerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class ObservationView(PropertyPath.Observation, Filter, ViewSet):
    """Provides a view set for the Observations entity"""
    queryset = Observation.objects.all()
    serializer_class = serializers.ObservationSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class FeatureOfInterestView(Filter, PropertyPath.FeatureOfInterest, ViewSet):
    """Provides a view set of the Features of Interest entity."""
    queryset = FeatureOfInterest.objects.all()
    serializer_class = serializers.FeatureOfInterestSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'
