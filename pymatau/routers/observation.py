from .router import Router, NestedSimpleRouter
import pymatau.views as observation


class ObservationRouter:
    Router.router.register(
                r'Observations',
                observation.ObservationView,
                'observation'
                )

    observation_router = NestedSimpleRouter(
                Router.router,
                r'Observations',
                lookup='Observations'
                )

    observation_router.register(
                r'FeatureOfInterest',
                observation.FeatureOfInterestView,
                'featureofinterest'
                )

    observation_router.register(
                r'Datastream',
                observation.DatastreamView,
                'datastream'
                )

    observation_datastream_router = NestedSimpleRouter(
                observation_router,
                r'Datastream',
                'Datastream'
                )

    observation_datastream_router.register(
                r'Sensor',
                observation.SensorView,
                'sensor'
                )

    observation_datastream_router.register(
                r'ObservedProperty',
                observation.ObservedPropertyView,
                'observedproperty'
                )

    observation_datastream_router.register(
                r'Thing',
                observation.ThingView,
                'thing'
                )

    observation_datastream_tin_router = NestedSimpleRouter(
                observation_datastream_router,
                r'Thing',
                'Thing'
                )

    observation_datastream_tin_router.register(
                r'Locations',
                observation.LocationView,
                'location'
                )

    observation_datastream_tin_router.register(
                r'HistoricalLocations',
                observation.HistoricalLocationView,
                'historicallocation'
                )

    observation_datastream_tin_locat_router = NestedSimpleRouter(
                observation_datastream_tin_router,
                r'Locations',
                'Locations'
                )

    observation_datastream_tin_locat_router.register(
                r'HistoricalLocations',
                observation.HistoricalLocationView,
                'historicallocation'
                )

    observation_datastream_tin_hist_router = NestedSimpleRouter(
                observation_datastream_tin_router,
                r'HistoricalLocations',
                'HistoricalLocations'
                )

    observation_datastream_tin_hist_router.register(
                r'Locations',
                observation.LocationView,
                'location'
                )
