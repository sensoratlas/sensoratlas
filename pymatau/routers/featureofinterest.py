from .router import Router, NestedSimpleRouter
import pymatau.views as featureofinterest


class FeatureOfInterestRouter:
    Router.router.register(r'FeaturesOfInterest',
                           featureofinterest.FeatureOfInterestView,
                           'featureofinterest')

    featureofinterest_router = NestedSimpleRouter(Router.router,
                                                  r'FeaturesOfInterest',
                                                  lookup='FeaturesOfInterest')

    featureofinterest_router.register(r'Observations',
                                      featureofinterest.ObservationView,
                                      'observation')

    featureofinterest_obs_router = NestedSimpleRouter(featureofinterest_router,
                                                      r'Observations',
                                                      'Observations')

    featureofinterest_obs_router.register(r'Datastream',
                                          featureofinterest.DatastreamView,
                                          'datastream')

    featureofinterest_obs_ds_router = NestedSimpleRouter(
                                                featureofinterest_obs_router,
                                                r'Datastream',
                                                'Datastream'
                                                )

    featureofinterest_obs_ds_router.register(
                                        r'Sensor',
                                        featureofinterest.SensorView,
                                        'sensor'
                                        )

    featureofinterest_obs_ds_router.register(
                                        r'ObservedProperty',
                                        featureofinterest.ObservedPropertyView,
                                        'observedproperty'
                                        )

    featureofinterest_obs_ds_router.register(
                                        r'Thing',
                                        featureofinterest.ThingView,
                                        'thing'
                                        )

    featureofinterest_obs_ds_tin_router = NestedSimpleRouter(
                                        featureofinterest_obs_ds_router,
                                        r'Thing',
                                        'Thing'
                                        )

    featureofinterest_obs_ds_tin_router.register(
                                        r'Locations',
                                        featureofinterest.LocationView,
                                        'location'
                                        )

    featureofinterest_obs_ds_tin_router.register(
                                    r'HistoricalLocations',
                                    featureofinterest.HistoricalLocationView,
                                    'historicallocation'
                                    )

    featureofinterest_obs_ds_tin_loc_router = NestedSimpleRouter(
                                        featureofinterest_obs_ds_tin_router,
                                        r'Locations',
                                        'Locations'
                                        )

    featureofinterest_obs_ds_tin_loc_router.register(
                                    r'HistoricalLocations',
                                    featureofinterest.HistoricalLocationView,
                                    'historicallocation'
                                    )

    featureofinterest_obs_ds_tin_hloc_router = NestedSimpleRouter(
                                        featureofinterest_obs_ds_tin_router,
                                        r'HistoricalLocations',
                                        'HistoricalLocations'
                                        )

    featureofinterest_obs_ds_tin_hloc_router.register(
                                    r'Locations',
                                    featureofinterest.LocationView,
                                    'location'
                                    )
