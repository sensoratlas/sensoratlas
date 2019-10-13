from .models import Datastream, Thing, Sensor, Location, \
    ObservedProperty, Observation, HistoricalLocation, FeatureOfInterest
from rest_framework import serializers
from .mixins import Expand, Select, ResultFormat, ControlInformation
from .errors import Conflicts


class FeatureOfInterestSerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Serializer for the nested Features of Interest
    of the Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = FeatureOfInterest
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
            'name',
            'description',
            'encodingType',
            'feature',
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Observation': (
                    ObservationSerializer,
                    (),
                    {'many': True}
                ),
            }
            Conflicts.conflicts.append('FeatureOfInterest')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class HistoricalLocationSerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Serializer for the nested Historical Locations of the
    Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = HistoricalLocation
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
            'time'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Thing': ThingSerializer,
                'Location': (
                    LocationSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('HistoricalLocation')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class LocationSerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Serializer for the nested Locations of the Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
            'name',
            'description',
            'encodingType',
            'location'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Thing': (
                    ThingSerializer,
                    (),
                    {'many': True}
                    ),
                'HistoricalLocation': (
                    HistoricalLocationSerializer,
                    (),
                    {'many': True}
                    )
            }
            Conflicts.conflicts.append('Location')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class ThingSerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Serializer for the nested Things of the Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = Thing
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
            'name',
            'description',
            'properties'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Datastream': (
                    DatastreamSerializer,
                    (),
                    {'many': True}
                ),
                'Location': (
                    LocationSerializer,
                    (),
                    {'many': True}
                ),
                'HistoricalLocation': (
                    HistoricalLocationSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('Thing')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class SensorSerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Serializer for the nested Sensors of the Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = Sensor
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
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
            Conflicts.conflicts.append('Sensor')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class ObservedPropertySerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Serializer for the nested Observed Properties of the
    Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = ObservedProperty
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
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
            Conflicts.conflicts.append('ObservedProperty')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class ObservationSerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Serializer for the nested Observations of the Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = Observation
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
            'phenomenonTime',
            'result',
            'resultTime'
        )

        def get_expandable_fields(*args):
            expandable_fields = {
                'Datastream': DatastreamSerializer,
                'FeatureOfInterest': FeatureOfInterestSerializer,
            }
            Conflicts.conflicts.append('Observation')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields


class DatastreamSerializer(ControlInformation, Select, Expand, ResultFormat, serializers.ModelSerializer):
    """
    Base serializer for the Datastreams entity.
    """
    selfLink = serializers.SerializerMethodField()
    navigationLinks = serializers.SerializerMethodField()

    class Meta:
        model = Datastream
        fields = (
            'id',
            'selfLink',
            'navigationLinks',
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
                'Thing': ThingSerializer,
                'Sensor': SensorSerializer,
                'ObservedProperty': ObservedPropertySerializer,
                'Observation': (
                    ObservationSerializer,
                    (),
                    {'many': True}
                )
            }
            Conflicts.conflicts.append('Datastream')
            for a in args:
                if a in Conflicts.conflicts:
                    expandable_fields.pop(a, expandable_fields)
                if a not in Conflicts.conflicts:
                    Conflicts.conflicts.append(a)
            return expandable_fields
