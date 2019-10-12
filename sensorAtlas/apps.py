from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SensorAppConfig(AppConfig):
    name = 'sensorAtlas'
    verbose_name = _('Sensors')
