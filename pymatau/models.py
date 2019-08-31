"""SensorThings Model Definitions

doc string here...
"""

from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField, DateTimeRangeField
from django.db.models.signals import m2m_changed
from django.utils import timezone
from django.dispatch import receiver
from django.core.exceptions import ValidationError


ENCODING_TYPES_1 = (
        ("application/vnd.geo+json", "GeoJSON"),
    )

ENCODING_TYPES_2 = (
    ("application/pdf", "PDF"),
    ("http://www.opengis.net/doc/IS/SensorML/2.0", "SensorML")
)

OBSERVATION_TYPES = (
    (
    "http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CategoryObservation", "OM Category Observation (URI)"),
    ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation", "OM Count Observation (Integer)"),
    ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement", "OM Measurement (Double)"),
    ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation", "OM Observation (Any)"),
    ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_TruthObservation", "OM Truth Observation (Boolean)")
)


class Thing(models.Model):
    """
    Thing model definition. HistoricalLocation and Datastream relations in their data model
    definitions
    """
    name = models.TextField(
        "Name"
    )
    description = models.TextField(
        "Description"
    )
    properties = JSONField(
        blank=True,
        null=True
    )
    Locations = models.ManyToManyField(
        "Location",
        blank=True,
        null=True,
        related_name="Things",
        verbose_name="location"
    )

    class Meta:
        verbose_name = "Thing"
        verbose_name_plural = "Things"
        # TODO: add a "unique_together"-like constraint on Locations__encodingType.

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    Location model type definition. Related fields are defined it related models.
    """
    name = models.TextField(
        "Name"
    )
    description = models.TextField(
        "Description"
    )
    encodingType = models.TextField(
        choices=ENCODING_TYPES_1,
        verbose_name="Encoding Type"
    )
    location = models.GeometryField(
    )

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.name


class HistoricalLocation(models.Model):
    time = models.DateTimeField(
        "Time"
    )
    Locations = models.ManyToManyField(
        Location,
        verbose_name='Locations',
        related_name='HistoricalLocations'
    )
    Thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        verbose_name='Thing',
        related_name='HistoricalLocations'
    )


class Datastream(models.Model):
    """
    Datatsream model type definition. Related fields are defined it related models.
    """
    name = models.TextField(
        "Name"
    )
    description = models.TextField(
        "Description"
    )
    unitOfMeasurement = JSONField(
        verbose_name="Unit of Measurement"
        )
    observationType = models.TextField(
        verbose_name="Observation Type",
        choices=OBSERVATION_TYPES
        )
    observedArea = models.PolygonField(
        blank=True,
        null=True,
        verbose_name="Observed Area"
        )
    phenomenonTime = DateTimeRangeField(
        blank=True,
        null=True,
        # validators=[Validators.validate_interval],
        verbose_name="Phenomenon Time"
        )
    resultTime = DateTimeRangeField(
        blank=True,
        null=True,
        # validators=[Validators.validate_interval],
        verbose_name="Result Time"
        )
    Thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name="Datastreams",
        verbose_name='Thing'
        )
    Sensor = models.ForeignKey(
        "Sensor",
        on_delete=models.CASCADE,
        related_name="Datastreams",
        verbose_name="Sensor"
    )
    ObservedProperty = models.ForeignKey(
        "ObservedProperty",
        on_delete=models.CASCADE,
        related_name="Datastreams",
        verbose_name="Observed Property"
    )

    class Meta:
        verbose_name = "Datastream"
        verbose_name_plural = "Datastreams"

    def __str__(self):
        return self.name


class Sensor(models.Model):
    """
    Sensor model type definition. Related fields are defined it related models.
    """
    name = models.TextField(
        "Name"
    )
    description = models.TextField(
        "Description"
    )
    encodingType = models.TextField(
        choices=ENCODING_TYPES_2,
        verbose_name="Encoding Type"
    )
    metadata = models.TextField(
        "Metadata"
    )

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensor"

    def __str__(self):
        return self.name


class ObservedProperty(models.Model):
    name = models.TextField(
        "Name"
    )
    definition = models.TextField(
        "Definition"  # TODO: add validator for URI
    )
    description = models.TextField(
        "Description"
    )

    class Meta:
        verbose_name = "Observed Property"
        verbose_name_plural = "Observed Properties"

    def __str__(self):
        return self.name


class Observation(models.Model):
    phenomenonTime = models.DateTimeField(  # TODO: add interval support
        verbose_name="Phenomenon Time"
    )
    result = JSONField(  # TODO: change db model
        verbose_name="Result"
    )
    resultTime = models.DateTimeField(
        verbose_name="Result Time"
    )
    resultQuality = JSONField(
        null=True,
        blank=True,
        verbose_name="Result Quality"
    )
    validTime = DateTimeRangeField(
        null=True,
        blank=True,
        verbose_name="Valid Time"
    )
    parameters = JSONField(
        null=True,
        blank=True,
        verbose_name="Parameters"
    )

    Datastream = models.ForeignKey(
        'DataStream',
        on_delete=models.CASCADE,
        verbose_name='Datastream',
        related_name='Observations'
    )
    FeatureOfInterest = models.ForeignKey(
        'FeatureOfInterest',
        on_delete=models.CASCADE,
        verbose_name="Feature of Interest",
        related_name='Observations'
    )

    class Meta:
        verbose_name = "Observation"

    def save(self, *args, **kwargs):
        result = self.result
        if not isinstance(self.result, dict):
            result = {'result': self.result}
        self.result = result
        super(Observation, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.result['result'])


class FeatureOfInterest(models.Model):
    name = models.TextField(
        "Name"
    )
    description = models.TextField(
        "Description"
    )
    encodingType = models.TextField(
        choices=ENCODING_TYPES_1,
        verbose_name="Encoding Type"
    )
    feature = models.GeometryField(
    )

    class Meta:
        verbose_name = "Feature of Interest"
        verbose_name_plural = "Features of Interest"

    def __str__(self):
        return self.name


@receiver(m2m_changed, sender=Thing.Locations.through)
def prevent_duplicate_active_user(sender, instance, **kwargs):
    # this will need to change when more encoding types are added
    encd = 'application/vnd.geo+json'
    try:
        if instance.Locations.filter(encodingType=encd).count() > 1:
            raise ValidationError(
                """
                Encoding types for each related location must be unique.
                """,
                code='unique'
                )
    except AttributeError:
        pass


def historicallocation_autocreate(sender, **kwargs):
    instance = kwargs.get('instance')
    created = bool(instance.id)

    if created and instance._meta.model_name == 'location':
        things = Thing.objects.filter(Locations__id=instance.id)
        if things:
            for thing in things:
                historicallocation = HistoricalLocation.objects.create(
                    time=timezone.now(),
                    Thing=thing
                    )
                historicallocation.Locations.add(instance)

    if created and instance._meta.model_name == 'thing':
        location = Location.objects.filter(Things__id=instance.id)
        if location:
            historicallocation = HistoricalLocation.objects.create(
                time=timezone.now(),
                Thing=instance
                )
            historicallocation.Locations.set(location)


m2m_changed.connect(historicallocation_autocreate, sender=Thing.Locations.through)
