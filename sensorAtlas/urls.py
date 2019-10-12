from django.urls import re_path, include
from .routers.router import Router
from .routers.location import LocationRouter
from .routers.thing import ThingRouter
from .routers.datastream import DatastreamRouter
from .routers.historicallocation import HistoricalLocationRouter
from .routers.sensor import SensorRouter
from .routers.observedproperty import ObservedPropertyRouter
from .routers.observation import ObservationRouter
from .routers.featureofinterest import FeatureOfInterestRouter


urlpatterns = [
    re_path(r'^(?P<version>(v1.0))/', include(
                     Router.router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_things_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_things_ds_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_things_ds_obs_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_hist_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_hist_things_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_hist_things_ds_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     LocationRouter.
                     location_hist_things_ds_obs_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_things_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_things_ds_router.urls)),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_things_ds_obs_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_locat_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_locat_things_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_locat_things_ds_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     HistoricalLocationRouter.
                     historicallocation_locat_things_ds_obs_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ThingRouter.
                     thing_router.urls
                     )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ThingRouter.
                     thing_historical_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ThingRouter.
                     thing_location_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ThingRouter.
                     thing_datastream_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ThingRouter.
                     thing_datastream_obs_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     DatastreamRouter.
                     datastream_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     DatastreamRouter.
                     datastream_observation_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     DatastreamRouter.
                     datastream_thing_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     DatastreamRouter.
                     datastream_thing_hlocat_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     DatastreamRouter.
                     datastream_thing_locat_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     SensorRouter.
                     sensor_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     SensorRouter.
                     sensor_datastream_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     SensorRouter.
                     sensor_datastream_tin_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     SensorRouter.
                     sensor_datastream_tin_hist_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     SensorRouter.
                     sensor_datastream_tin_locat_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     SensorRouter.
                     sensor_datastream_obs_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservedPropertyRouter.
                     observedproperty_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservedPropertyRouter.
                     observedproperty_datastream_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservedPropertyRouter.
                     observedproperty_datastream_tin_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservedPropertyRouter.
                     observedproperty_datastream_tin_locat_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservedPropertyRouter.
                     observedproperty_datastream_tin_hist_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservedPropertyRouter.
                     observedproperty_datastream_obs_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservationRouter.
                     observation_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservationRouter.
                     observation_datastream_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservationRouter.
                     observation_datastream_tin_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservationRouter.
                     observation_datastream_tin_hist_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     ObservationRouter.
                     observation_datastream_tin_locat_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     FeatureOfInterestRouter.
                     featureofinterest_router.urls
                    )),
    re_path(r'^(?P<version>(v1.0))/', include(
                     FeatureOfInterestRouter.
                     featureofinterest_obs_router.urls)),
    re_path(r'^(?P<version>(v1.0))/', include(
                     FeatureOfInterestRouter.
                     featureofinterest_obs_ds_router.urls)),
    re_path(r'^(?P<version>(v1.0))/', include(
                     FeatureOfInterestRouter.
                     featureofinterest_obs_ds_tin_router.urls)),
    re_path(r'^(?P<version>(v1.0))/', include(
                     FeatureOfInterestRouter.
                     featureofinterest_obs_ds_tin_loc_router.urls)),
    re_path(r'^(?P<version>(v1.0))/', include(
                     FeatureOfInterestRouter.
                     featureofinterest_obs_ds_tin_hloc_router.urls)),
]
