from .router import Router, NestedSimpleRouter
import pymatau.views as location


class LocationRouter:
    Router.router.register(
                r'Locations',
                location.LocationView,
                'location'
                )

    location_router = NestedSimpleRouter(
                Router.router,
                r'Locations',
                lookup='Locations'
                )

    location_router.register(
                r'HistoricalLocations',
                location.HistoricalLocationView,
                'historicallocation'
                )

    location_router.register(
                r'Things',
                location.ThingView,
                'thing'
                )

    location_things_router = NestedSimpleRouter(
                location_router,
                r'Things',
                'Things'
                )

    location_things_router.register(
                r'Datastreams',
                location.DataStreamView,
                'datastream'
                )

    location_things_ds_router = NestedSimpleRouter(
                location_things_router,
                r'Datastreams',
                'Datastreams'
                )

    location_things_ds_router.register(
                r'Sensor',
                location.SensorView,
                'sensor'
                )

    location_things_ds_router.register(
                r'ObservedProperty',
                location.ObservedPropertyView,
                'observedproperty'
                )

    location_things_ds_router.register(
                r'Observations',
                location.ObservationView,
                'observation'
                )

    location_things_ds_obs_router = \
        NestedSimpleRouter(
                location_things_ds_router,
                r'Observations',
                'Observations'
                )

    location_things_ds_obs_router.register(
                r'FeatureOfInterest',
                location.FeatureOfInterestView,
                'featureofinterest'
                )

    location_hist_router = NestedSimpleRouter(
                location_router,
                r'HistoricalLocations',
                'HistoricalLocations'
                )

    location_hist_router.register(
                r'Thing',
                location.ThingView,
                'thing'
                )

    location_hist_things_router = NestedSimpleRouter(
                location_hist_router,
                r'Thing',
                'Thing'
                )

    location_hist_things_router.register(
                r'Datastreams',
                location.DataStreamView,
                'datastream'
                )

    location_hist_things_ds_router = NestedSimpleRouter(
                location_hist_things_router,
                r'Datastreams',
                'Datastreams')

    location_hist_things_ds_router.register(
                r'Sensor',
                location.SensorView,
                'sensor'
                )

    location_hist_things_ds_router.register(
                r'ObservedProperty',
                location.ObservedPropertyView,
                'observedproperty'
                )

    location_hist_things_ds_router.register(
                r'Observations',
                location.ObservationView,
                'observation'
                )

    location_hist_things_ds_obs_router = \
        NestedSimpleRouter(
                location_hist_things_ds_router,
                r'Observations',
                'Observations'
                )

    location_hist_things_ds_obs_router.register(
                r'FeatureOfInterest',
                location.FeatureOfInterestView,
                'featureofinterest'
                )
