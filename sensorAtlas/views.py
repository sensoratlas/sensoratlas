from .models import Location, Thing, Datastream, Sensor, \
    ObservedProperty, Observation, FeatureOfInterest, HistoricalLocation
import sensorAtlas.serializer as serializers
from .parsers import Filter, Orderby
from .viewsets import ViewSet
from rest_framework import generics


class APIRoot(generics.GenericAPIView):
    """
    My API documentation
    """


class ThingView(Filter, ViewSet):
    """Provides a view set of the Things entity."""
    queryset = Thing.objects.all()
    serializer_class = serializers.ThingSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class LocationView(Filter, ViewSet):
    """Provides a view set for the Locations entity."""
    queryset = Location.objects.all()
    serializer_class = serializers.LocationSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class HistoricalLocationView(Filter, ViewSet):
    """Provides a view set for Historical Location entities."""
    queryset = HistoricalLocation.objects.all()
    serializer_class = serializers.HistoricalLocationSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class DatastreamView(Filter, ViewSet):
    """Provides a view set for the Datastreams entity"""
    queryset = Datastream.objects.all()
    serializer_class = serializers.DatastreamSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class SensorView(Filter, ViewSet):
    """Provides a view set for the Sensors entity"""
    queryset = Sensor.objects.all()
    serializer_class = serializers.SensorSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class ObservedPropertyView(Filter, ViewSet):
    """Provides a view set for the Observed Properties entity"""
    queryset = ObservedProperty.objects.all()
    serializer_class = serializers.ObservedPropertySerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class ObservationView(Filter, ViewSet):
    """Provides a view set for the Observations entity"""
    queryset = Observation.objects.all()
    serializer_class = serializers.ObservationSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'


class FeatureOfInterestView(Filter, ViewSet):
    """Provides a view set of the Features of Interest entity."""
    queryset = FeatureOfInterest.objects.all()
    serializer_class = serializers.FeatureOfInterestSerializer
    filter_backends = (Orderby,)
    ordering_fields = '__all__'
