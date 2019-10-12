from .router import Router, NestedSimpleRouter
import sensorAtlas.views as sensor


class SensorRouter:
    Router.router.register(
                r'Sensors',
                sensor.SensorView,
                'sensor'
                )

    sensor_router = NestedSimpleRouter(
                Router.router,
                r'Sensors',
                lookup='Sensors'
                )

    sensor_router.register(
                r'Datastreams',
                sensor.DataStreamView,
                'datastream'
                )

    sensor_datastream_router = NestedSimpleRouter(
                sensor_router,
                r'Datastreams',
                'Datastreams'
                )

    sensor_datastream_router.register(
                r'ObservedProperty',
                sensor.ObservedPropertyView,
                'observedproperty'
                )

    sensor_datastream_router.register(
                r'Thing',
                sensor.ThingView,
                'thing'
                )

    sensor_datastream_tin_router = NestedSimpleRouter(
                sensor_datastream_router,
                r'Thing',
                'Thing'
                )

    sensor_datastream_tin_router.register(
                r'Locations',
                sensor.LocationView,
                'location'
                )

    sensor_datastream_tin_router.register(
                r'HistoricalLocations',
                sensor.HistoricalLocationView,
                'historicallocation'
                )

    sensor_datastream_tin_locat_router = NestedSimpleRouter(
                sensor_datastream_tin_router,
                r'Locations',
                'Locations'
                )

    sensor_datastream_tin_locat_router.register(
                r'HistoricalLocations',
                sensor.HistoricalLocationView,
                'historicallocation'
                )

    sensor_datastream_tin_hist_router = NestedSimpleRouter(
                sensor_datastream_tin_router,
                r'HistoricalLocations',
                'HistoricalLocations'
                )

    sensor_datastream_tin_hist_router.register(
                r'Locations',
                sensor.LocationView,
                'location'
                )

    sensor_datastream_router.register(
                r'Observations',
                sensor.ObservationView,
                'observation'
                )

    sensor_datastream_obs_router = NestedSimpleRouter(
                sensor_datastream_router,
                r'Observations',
                'Observations'
                )

    sensor_datastream_obs_router.register(
                r'FeaturesOfInterest',
                sensor.FeatureOfInterestView,
                'featureofinterest'
                )
