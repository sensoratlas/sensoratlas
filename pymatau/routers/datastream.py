from .router import Router, NestedSimpleRouter
import pymatau.views as datastream


class DatastreamRouter:
    Router.router.register(
                r'Datastreams',
                datastream.DatastreamView,
                'datastream'
                )

    datastream_router = NestedSimpleRouter(
                Router.router,
                r'Datastreams',
                lookup='Datastreams'
                )

    datastream_router.register(
                r'Sensor',
                datastream.SensorView,
                'sensor'
                )

    datastream_router.register(
                r'ObservedProperty',
                datastream.ObservedPropertyView,
                'observedproperty'
                )

    datastream_router.register(
                r'Observations',
                datastream.ObservationView,
                'observation'
                )

    datastream_observation_router = NestedSimpleRouter(
                datastream_router,
                r'Observations',
                'Observations'
                )

    datastream_observation_router.register(
                r'FeatureOfInterest',
                datastream.FeatureOfInterestView,
                'featureofinterest'
                )

    datastream_router.register(
                r'Thing',
                datastream.ThingView,
                'thing'
                )

    datastream_thing_router = NestedSimpleRouter(
                datastream_router,
                r'Thing',
                'Thing'
                )

    datastream_thing_router.register(
                r'Locations',
                datastream.LocationView,
                'location'
                )

    datastream_thing_router.register(
                r'HistoricalLocations',
                datastream.HistoricalLocationView,
                'historicallocation'
                )

    datastream_thing_hlocat_router = NestedSimpleRouter(
                datastream_thing_router,
                r'HistoricalLocations',
                'HistoricalLocations'
                )

    datastream_thing_hlocat_router.register(
                r'Locations',
                datastream.LocationView,
                'location'
                )

    datastream_thing_locat_router = NestedSimpleRouter(
                datastream_thing_router,
                r'Locations',
                'Locations'
                )

    datastream_thing_locat_router.register(
                r'HistoricalLocations',
                datastream.HistoricalLocationView,
                'historicallocation'
                )
