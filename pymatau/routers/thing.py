from .router import Router, NestedSimpleRouter
import pymatau.views as thing


class ThingRouter:
    Router.router.register(r'Things',
                           thing.ThingView,
                           'thing')

    thing_router = NestedSimpleRouter(Router.router,
                                      r'Things',
                                      lookup='Things')

    thing_router.register(r'Locations',
                          thing.LocationView,
                          'location')

    thing_router.register(r'HistoricalLocations',
                          thing.HistoricalLocationView,
                          'historicallocation')

    thing_router.register(r'Datastreams',
                          thing.DataStreamView,
                          'datastream')

    thing_historical_router = NestedSimpleRouter(thing_router,
                                                 r'HistoricalLocations',
                                                 'HistoricalLocations')

    thing_historical_router.register(r'Locations',
                                     thing.LocationView,
                                     'location')

    thing_location_router = NestedSimpleRouter(thing_router,
                                               r'Locations',
                                               'Locations')

    thing_location_router.register(r'HistoricalLocations',
                                   thing.HistoricalLocationView,
                                   'historicallocation')

    thing_datastream_router = NestedSimpleRouter(thing_router,
                                                 r'Datastreams',
                                                 'Datastreams')

    thing_datastream_router.register(r'Sensor',
                                     thing.SensorView,
                                     'sensor')

    thing_datastream_router.register(r'ObservedProperty',
                                     thing.ObservedPropertyView,
                                     'observedproperty')

    thing_datastream_router.register(r'Observations',
                                     thing.ObservationView,
                                     'observation')

    thing_datastream_obs_router = NestedSimpleRouter(thing_datastream_router,
                                                     r'Observations',
                                                     'Observations')

    thing_datastream_obs_router.register(r'FeatureOfInterest',
                                         thing.FeatureOfInterestView,
                                         'featureofinterest')
