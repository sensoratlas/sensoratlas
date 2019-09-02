from .router import Router, NestedSimpleRouter
import pymatau.views as observedproperty


class ObservedPropertyRouter:
    Router.router.register(
                r'ObservedProperties',
                observedproperty.ObservedPropertyView,
                'observedproperty'
                )

    observedproperty_router = NestedSimpleRouter(
                Router.router,
                r'ObservedProperties',
                lookup='ObservedProperties'
                )

    observedproperty_router.register(
                r'Datastreams',
                observedproperty.DatastreamView,
                'datastream'
                )

    observedproperty_datastream_router = NestedSimpleRouter(
                observedproperty_router,
                r'Datastreams',
                'Datastreams'
                )

    observedproperty_datastream_router.register(
                r'Sensor',
                observedproperty.SensorView,
                'sensor'
                )

    observedproperty_datastream_router.register(
                r'Thing',
                observedproperty.ThingView,
                'thing'
                )

    observedproperty_datastream_tin_router = NestedSimpleRouter(
                observedproperty_datastream_router,
                r'Thing',
                'Thing'
                )

    observedproperty_datastream_tin_router.register(
                r'Locations',
                observedproperty.LocationView,
                'location'
                )

    observedproperty_datastream_tin_router.register(
                r'HistoricalLocations',
                observedproperty.HistoricalLocationView,
                'historicallocation'
                )

    observedproperty_datastream_tin_locat_router = NestedSimpleRouter(
                observedproperty_datastream_tin_router,
                r'Locations',
                'Locations'
                )

    observedproperty_datastream_tin_locat_router.register(
                r'HistoricalLocations',
                observedproperty.HistoricalLocationView,
                'historicallocation'
                )

    observedproperty_datastream_tin_hist_router = NestedSimpleRouter(
                observedproperty_datastream_tin_router,
                r'HistoricalLocations',
                'HistoricalLocations'
                )

    observedproperty_datastream_tin_hist_router.register(
                r'Locations',
                observedproperty.LocationView,
                'location'
                )

    observedproperty_datastream_router.register(
                r'Observations',
                observedproperty.ObservationView,
                'observation'
                )

    observedproperty_datastream_obs_router = NestedSimpleRouter(
                observedproperty_datastream_router,
                r'Observations',
                'Observations'
                )

    observedproperty_datastream_obs_router.register(
                r'FeatureOfInterest',
                observedproperty.FeatureOfInterestView,
                'featureofinterest'
                )
