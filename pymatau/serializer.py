from .models import Datastream, Thing, Sensor, Location, \
    ObservedProperty, Observation, HistoricalLocation, FeatureOfInterest
from rest_framework import serializers
from .mixins import Expand, Select, ResultFormat
from .viewsets import NavigationLinks
from .representation import Representation
from .errors import Conflicts


class FeatureOfInterestSerializer(
        Select, Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer
        ):
    """
    Serializer for the nested Features of Interest
    of the Datastreams entity.
    """
    observationsLink = serializers.SerializerMethodField()

    class Meta:
        model = FeatureOfInterest
        fields = (
            'id',
            'selfLink',
            'observationsLink',
            'name',
            'description',
            'encodingType',
            'feature',
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Observations': (
                    ObservationSerializer,
                    (),
                    {'many': True}
                ),
            }
            Conflicts.conflicts.append('FeaturesOfInterest')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class HistoricalLocationSerializer(
        Select, Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer
        ):
    """
    Serializer for the nested Historical Locations of the
    Datastreams entity.
    """
    thingsLink = serializers.SerializerMethodField()
    locationsLink = serializers.SerializerMethodField()

    class Meta:
        model = HistoricalLocation
        fields = (
            'id',
            'selfLink',
            'thingsLink',
            'locationsLink',
            'time'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Thing': (ThingSerializer),
                'Locations': (
                    LocationSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('HistoricalLocations')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class LocationSerializer(
        Select,  Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer):
    """
    Serializer for the nested Locations of the Datastreams entity.
    """
    thingsLink = serializers.SerializerMethodField()
    historicallocationsLink = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            'id',
            'selfLink',
            'thingsLink',
            'historicallocationsLink',
            'name',
            'description',
            'encodingType',
            'location'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Things': (
                    ThingSerializer,
                    (),
                    {'many': True}
                    ),
                'HistoricalLocations': (
                    HistoricalLocationSerializer,
                    (),
                    {'many': True}
                    )
            }
            Conflicts.conflicts.append('Locations')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class ThingSerializer(
        Select, Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer):
    """
    Serializer for the nested Things of the Datastreams entity.
    """
    datastreamsLink = serializers.SerializerMethodField()
    locationsLink = serializers.SerializerMethodField()
    historicallocationsLink = serializers.SerializerMethodField()

    class Meta:
        model = Thing
        fields = (
            'id',
            'selfLink',
            'datastreamsLink',
            'locationsLink',
            'historicallocationsLink',
            'name',
            'description',
            'properties'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Datastreams': (
                    DatastreamSerializer,
                    (),
                    {'many': True}
                ),
                'Locations': (
                    LocationSerializer,
                    (),
                    {'many': True}
                ),
                'HistoricalLocations': (
                    HistoricalLocationSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('Things')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class SensorSerializer(
        Select, Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer):
    """
    Serializer for the nested Sensors of the Datastreams entity.
    """
    datastreamsLink = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = (
            'id',
            'selfLink',
            'datastreamsLink',
            'name',
            'description',
            'encodingType',
            'metadata'
            )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Datastream': (
                    DatastreamSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('Sensors')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class ObservedPropertySerializer(
        Select, Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer):
    """
    Serializer for the nested Observed Properties of the
    Datastreams entity.
    """
    datastreamsLink = serializers.SerializerMethodField()

    class Meta:
        model = ObservedProperty
        fields = (
            'id',
            'selfLink',
            'datastreamsLink',
            'name',
            'definition',
            'description'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Datastream': (
                    DatastreamSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('ObservedProperties')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class ObservationSerializer(
        Select, Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer):
    """
    Serializer for the nested Observations of the Datastreams entity.
    """
    datastreamsLink = serializers.SerializerMethodField()
    featuresOfInterestLink = serializers.SerializerMethodField()

    class Meta:
        model = Observation
        fields = (
            'id',
            'selfLink',
            'datastreamsLink',
            'featuresOfInterestLink',
            'phenomenonTime',
            'result',
            'resultTime'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Datastream': (DatastreamSerializer),
                'FeatureOfInterest': (FeatureOfInterestSerializer),
            }
            Conflicts.conflicts.append('Observations')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class DatastreamSerializer(
        Select, Expand, ResultFormat, Representation,
        NavigationLinks, serializers.ModelSerializer):
    """
    Base serializer for the Datastreams entity.
    """
    thingsLink = serializers.SerializerMethodField()
    observationsLink = serializers.SerializerMethodField()
    observedpropertiesLink = serializers.SerializerMethodField()
    sensorsLink = serializers.SerializerMethodField()

    class Meta:
        model = Datastream
        fields = (
            'id',
            'selfLink',
            'thingsLink',
            'observationsLink',
            'observedpropertiesLink',
            'sensorsLink',
            'name',
            'description',
            'unitOfMeasurement',
            'observationType',
            'observedArea',
            'phenomenonTime',
            'resultTime',
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Thing': (ThingSerializer),
                'Sensor': (SensorSerializer),
                'ObservedProperty': (ObservedPropertySerializer),
                'Observations': (
                    ObservationSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('Datastreams')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields
