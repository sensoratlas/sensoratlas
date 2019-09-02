from .router import Router, NestedSimpleRouter
import pymatau.views as historicallocation


class HistoricalLocationRouter:
    Router.router.register(
                r'HistoricalLocations',
                historicallocation.HistoricalLocationView,
                'historicallocation'
                )

    historicallocation_router = NestedSimpleRouter(
                Router.router,
                r'HistoricalLocations',
                lookup='HistoricalLocations'
                )

    historicallocation_router.register(
                r'Thing',
                historicallocation.ThingView,
                'thing'
                )

    historicallocation_router.register(
                r'Locations',
                historicallocation.LocationView,
                'location'
                )

    historicallocation_things_router = NestedSimpleRouter(
                historicallocation_router,
                r'Thing',
                'Thing'
                )

    historicallocation_things_router.register(
                r'Datastreams',
                historicallocation.DatastreamView,
                'datastream'
                )

    historicallocation_things_ds_router = NestedSimpleRouter(
                historicallocation_things_router,
                r'Datastreams',
                'Datastreams'
                )

    historicallocation_things_ds_router.register(
                r'Sensor',
                historicallocation.SensorView,
                'sensor'
                )

    historicallocation_things_ds_router.register(
                r'ObservedProperty',
                historicallocation.ObservedPropertyView,
                'observedproperty'
                )

    historicallocation_things_ds_router.register(
                r'Observations',
                historicallocation.ObservationView,
                'observation'
                )

    historicallocation_things_ds_obs_router = NestedSimpleRouter(
                historicallocation_things_ds_router,
                r'Observations',
                'Observations'
                )

    historicallocation_things_ds_obs_router.register(
                r'FeatureOfInterest',
                historicallocation.FeatureOfInterestView,
                'featureofinterest'
                )

##
    historicallocation_locat_router = NestedSimpleRouter(
                historicallocation_router,
                r'Locations',
                'Locations'
                )

    historicallocation_locat_router.register(
                r'Things',
                historicallocation.ThingView,
                'thing'
                )

    historicallocation_locat_things_router = NestedSimpleRouter(
                historicallocation_locat_router,
                r'Things',
                'Things'
                )

    historicallocation_locat_things_router.register(
                r'Datastreams',
                historicallocation.DatastreamView,
                'datastream'
                )

    historicallocation_locat_things_ds_router = NestedSimpleRouter(
                historicallocation_locat_things_router,
                r'Datastreams',
                'Datastreams')

    historicallocation_locat_things_ds_router.register(
                r'Sensor',
                historicallocation.SensorView,
                'sensor'
                )

    historicallocation_locat_things_ds_router.register(
                r'ObservedProperty',
                historicallocation.ObservedPropertyView,
                'observedproperty'
                )

    historicallocation_locat_things_ds_router.register(
                r'Observations',
                historicallocation.ObservationView,
                'observation'
                )

    historicallocation_locat_things_ds_obs_router = \
        NestedSimpleRouter(
                historicallocation_locat_things_ds_router,
                r'Observations',
                'Observations'
                )

    historicallocation_locat_things_ds_obs_router.register(
                r'FeatureOfInterest',
                historicallocation.FeatureOfInterestView,
                'featureofinterest'
                )
