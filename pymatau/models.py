from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db.models.signals import m2m_changed
from django.utils import timezone
from .errors import Validators
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.conf import settings


class ObservedProperty(models.Model):
    name = models.CharField(
                _("Name"),
                max_length=120
                )
    definition = models.URLField(
                _("Definition")
                )
    description = models.TextField(
                _("Description")
                )

    class Meta:
        verbose_name = _("Observed Property")
        verbose_name_plural = _("Observed Properties")

    def __str__(self):
        return self.name


class Sensor(models.Model):
    encodingtypes = (
        ("application/pdf", "PDF"),
        ("http://www.opengis.net/doc/IS/SensorML/2.0", "SensorML"),
    )
    name = models.CharField(
                _("Name"),
                max_length=120,
                null=True
                )
    description = models.TextField(
                _("Description")
                )
    encodingType = models.CharField(
                max_length=120,
                null=True,
                choices=encodingtypes,
                verbose_name=_("Encoding Type")
                )
    metadata = models.TextField(
                _("Metadata")
                )

    class Meta:
        verbose_name = _("Sensor")
        verbose_name_plural = _("Sensor")

    def __str__(self):
        return self.name


class Location(models.Model):
    encodingtypes = (
        ("application/vnd.geo+json", "GeoJSON"),
    )
    name = models.CharField(
                _("Name"),
                unique=True,
                max_length=120
                )
    description = models.TextField(
                _("Description")
                )
    encodingType = models.CharField(
                max_length=120,
                choices=encodingtypes,
                verbose_name=_("Encoding Type")
                )
    location = models.GeometryField(blank=True)

    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")

    def __str__(self):
        return self.name


class Thing(models.Model):
    name = models.CharField(
                _("Name"),
                max_length=120,
                )
    description = models.TextField(
                _("Description")
                )
    Locations = models.ManyToManyField(
                Location,
                blank=True,
                related_name="Things",
                verbose_name=_('location')
                )
    properties = JSONField(
                blank=True,
                null=True
                )
    previous_state = None

    class Meta:
        verbose_name = _("Thing")
        verbose_name_plural = _("Thing")

    def __str__(self):
        return self.name


class HistoricalLocation(models.Model):
    time = models.DateTimeField(
                _("Time"),
                )
    Locations = models.ManyToManyField(
                Location,
                verbose_name=_('Locations'),
                related_name='HistoricalLocations'
                )
    Thing = models.ForeignKey(
                Thing,
                on_delete=models.CASCADE,
                verbose_name=_('Thing'),
                related_name='HistoricalLocations'
                )


class FeatureOfInterest(models.Model):
    encodingtypes = (
        ("application/vnd.geo+json", "GeoJSON"),
    )
    name = models.CharField(
                _("Name"),
                max_length=100,
                null=True
                )
    description = models.TextField(
                _("Description"),
                null=True
                )
    encodingType = models.CharField(
                max_length=120,
                choices=encodingtypes,
                verbose_name=_("Encoding Type")
                )
    feature = models.GeometryField()

    class Meta:
        verbose_name = _("Feature of Interest")
        verbose_name_plural = _("Feature of Interest")

    def __str__(self):
        return self.name


class Observation(models.Model):
    phenomenonTime = models.DateTimeField(
                null=True,
                verbose_name=_("Phenomenon Time")
                )
    result = JSONField(
                null=True,
                verbose_name=_("Result")
                )
    resultTime = models.DateTimeField(
                null=True,
                verbose_name=_("Result Time")
                )
    Datastream = models.ForeignKey(
                'DataStream',
                on_delete=models.CASCADE,
                verbose_name=_('Datastream'),
                related_name='Observations',
                db_index=True
                )
    FeatureOfInterest = models.ForeignKey(
                'FeatureOfInterest',
                db_column='featuresofinterest_id',
                on_delete=models.CASCADE,
                verbose_name=_("Feature of Interest"),
                related_name='Observations',
                db_index=True
                )
    resultQuality = JSONField(
                db_column='resultquality',
                null=True,
                blank=True,
                verbose_name=_("Result Quality")
                )
    validTime = models.TextField(
                db_column='validtime',
                null=True,
                blank=True,
                verbose_name=_("Valid Time")
                )
    parameters = JSONField(
                db_column='parameters',
                null=True,
                blank=True,
                verbose_name=_("Parameters")
                )
    testing = getattr(settings, "IS_TESTING", False)

    class Meta:
        verbose_name = _("Observation")
        ordering = ('id',)
        unique_together = ('phenomenonTime', 'Datastream')

    def save(self, *args, **kwargs):
        result = self.result
        if not isinstance(self.result, dict):
            result = {'result': self.result}
        self.result = result
        super(Observation, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % (self.result['result'])


class DataStream(models.Model):
    observationtypes = (
        ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CategoryObservation", _("OM Category Observation (URI)")),
        ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_CountObservation", _("OM Count Observation (Integer)")),
        ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Measurement", _("OM Measurement (Double)")),
        ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_Observation", _("OM Observation (Any)")),
        ("http://www.opengis.net/def/observationType/OGC-OM/2.0/OM_TruthObservation", _("OM Truth Observation (Boolean)"))
    )

    name = models.CharField(
                _("Name"),
                max_length=120,
                unique=True
                )
    description = models.TextField(
                _("Description")
                )
    observationType = models.CharField(
                max_length=120,
                verbose_name=_("Observation Type"),
                choices=observationtypes
                )
    unitOfMeasurement = JSONField(
                verbose_name=_("Unit of Measurement")
                )
    Thing = models.ForeignKey(
                Thing,
                on_delete=models.CASCADE,
                related_name="Datastreams",
                verbose_name=_('Thing')
                )
    Sensor = models.ForeignKey(
                Sensor,
                on_delete=models.CASCADE,
                related_name="Datastreams",
                verbose_name=_("Sensor")
                )
    ObservedProperty = models.ForeignKey(
                ObservedProperty,
                on_delete=models.CASCADE,
                related_name="Datastreams",
                verbose_name=_("Observed Property")
                )
    observedArea = models.PolygonField(
                blank=True,
                null=True,
                verbose_name=_("Observed Area")
                )
    phenomenonTime = models.TextField(
                blank=True,
                null=True,
                validators=[Validators.validate_interval],
                verbose_name=_("Phenomenon Time")
                )
    resultTime = models.TextField(
                blank=True,
                null=True,
                validators=[Validators.validate_interval],
                verbose_name=_("Result Time")
                )

    class Meta:
        verbose_name = _("Datastream")
        verbose_name_plural = _("Datastream")

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


m2m_changed.connect(historicallocation_autocreate,
                    sender=Thing.Locations.through)
