from .router import Router, NestedSimpleRouter
import sensorAtlas.views as view


class ThingRouter:
    Router.router.register(
        r'Things',
        view.ThingView,
        'thing'
    )
    thing_router = NestedSimpleRouter(
        Router.router,
        r'Things',
        lookup='Things'
    )
    thing_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    thing_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    thing_router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    thing_historical_router = NestedSimpleRouter(
        thing_router,
        r'HistoricalLocations',
        'HistoricalLocations'
    )
    thing_historical_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    thing_location_router = NestedSimpleRouter(
        thing_router,
        r'Locations',
        'Locations'
    )
    thing_location_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    thing_datastream_router = NestedSimpleRouter(
        thing_router,
        r'Datastreams',
        'Datastreams'
    )
    thing_datastream_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    thing_datastream_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    thing_datastream_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    thing_datastream_obs_router = NestedSimpleRouter(
        thing_datastream_router,
        r'Observations',
        'Observations'
    )
    thing_datastream_obs_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )


class DatastreamRouter:
    Router.router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    datastream_router = NestedSimpleRouter(
        Router.router,
        r'Datastreams',
        lookup='Datastreams'
    )
    datastream_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    datastream_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    datastream_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    datastream_observation_router = NestedSimpleRouter(
        datastream_router,
        r'Observations',
        'Observations'
    )
    datastream_observation_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )
    datastream_router.register(
        r'Thing',
        view.ThingView,
        'thing'
    )
    datastream_thing_router = NestedSimpleRouter(
        datastream_router,
        r'Thing',
        'Thing'
    )
    datastream_thing_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    datastream_thing_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    datastream_thing_hlocat_router = NestedSimpleRouter(
        datastream_thing_router,
        r'HistoricalLocations',
        'HistoricalLocations'
    )
    datastream_thing_hlocat_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    datastream_thing_locat_router = NestedSimpleRouter(
        datastream_thing_router,
        r'Locations',
        'Locations'
    )
    datastream_thing_locat_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )


class LocationRouter:
    Router.router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    location_router = NestedSimpleRouter(
        Router.router,
        r'Locations',
        lookup='Locations'
    )
    location_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    location_router.register(
        r'Things',
        view.ThingView,
        'thing'
    )
    location_things_router = NestedSimpleRouter(
        location_router,
        r'Things',
        'Things'
    )
    location_things_router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    location_things_ds_router = NestedSimpleRouter(
        location_things_router,
        r'Datastreams',
        'Datastreams'
    )
    location_things_ds_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    location_things_ds_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    location_things_ds_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    location_things_ds_obs_router = NestedSimpleRouter(
        location_things_ds_router,
        r'Observations',
        'Observations'
    )
    location_things_ds_obs_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )
    location_hist_router = NestedSimpleRouter(
        location_router,
        r'HistoricalLocations',
        'HistoricalLocations'
    )
    location_hist_router.register(
        r'Thing',
        view.ThingView,
        'thing'
    )
    location_hist_things_router = NestedSimpleRouter(
        location_hist_router,
        r'Thing',
        'Thing'
    )
    location_hist_things_router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    location_hist_things_ds_router = NestedSimpleRouter(
        location_hist_things_router,
        r'Datastreams',
        'Datastreams'
    )
    location_hist_things_ds_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    location_hist_things_ds_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    location_hist_things_ds_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    location_hist_things_ds_obs_router = NestedSimpleRouter(
        location_hist_things_ds_router,
        r'Observations',
        'Observations'
    )
    location_hist_things_ds_obs_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )


class HistoricalLocationRouter:
    Router.router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    historicallocation_router = NestedSimpleRouter(
        Router.router,
        r'HistoricalLocations',
        lookup='HistoricalLocations'
    )
    historicallocation_router.register(
        r'Thing',
        view.ThingView,
        'thing'
    )
    historicallocation_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    historicallocation_things_router = NestedSimpleRouter(
        historicallocation_router,
        r'Thing',
        'Thing'
    )
    historicallocation_things_router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    historicallocation_things_ds_router = NestedSimpleRouter(
        historicallocation_things_router,
        r'Datastreams',
        'Datastreams'
    )
    historicallocation_things_ds_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    historicallocation_things_ds_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    historicallocation_things_ds_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    historicallocation_things_ds_obs_router = NestedSimpleRouter(
        historicallocation_things_ds_router,
        r'Observations',
        'Observations'
    )
    historicallocation_things_ds_obs_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )
    historicallocation_locat_router = NestedSimpleRouter(
        historicallocation_router,
        r'Locations',
        'Locations'
    )
    historicallocation_locat_router.register(
        r'Things',
        view.ThingView,
        'thing'
    )
    historicallocation_locat_things_router = NestedSimpleRouter(
        historicallocation_locat_router,
        r'Things',
        'Things'
    )
    historicallocation_locat_things_router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    historicallocation_locat_things_ds_router = NestedSimpleRouter(
        historicallocation_locat_things_router,
        r'Datastreams',
        'Datastreams'
    )
    historicallocation_locat_things_ds_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    historicallocation_locat_things_ds_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    historicallocation_locat_things_ds_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    historicallocation_locat_things_ds_obs_router = NestedSimpleRouter(
        historicallocation_locat_things_ds_router,
        r'Observations',
        'Observations'
    )
    historicallocation_locat_things_ds_obs_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )


class SensorRouter:
    Router.router.register(
        r'Sensors',
        view.SensorView,
        'sensor'
    )
    sensor_router = NestedSimpleRouter(
        Router.router,
        r'Sensors',
        lookup='Sensors'
    )
    sensor_router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    sensor_datastream_router = NestedSimpleRouter(
        sensor_router,
        r'Datastreams',
        'Datastreams'
    )
    sensor_datastream_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    sensor_datastream_router.register(
        r'Thing',
        view.ThingView,
        'thing'
    )
    sensor_datastream_tin_router = NestedSimpleRouter(
        sensor_datastream_router,
        r'Thing',
        'Thing'
    )
    sensor_datastream_tin_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    sensor_datastream_tin_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    sensor_datastream_tin_locat_router = NestedSimpleRouter(
        sensor_datastream_tin_router,
        r'Locations',
        'Locations'
    )
    sensor_datastream_tin_locat_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    sensor_datastream_tin_hist_router = NestedSimpleRouter(
        sensor_datastream_tin_router,
        r'HistoricalLocations',
        'HistoricalLocations'
    )
    sensor_datastream_tin_hist_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    sensor_datastream_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    sensor_datastream_obs_router = NestedSimpleRouter(
        sensor_datastream_router,
        r'Observations',
        'Observations'
    )
    sensor_datastream_obs_router.register(
        r'FeaturesOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )


class ObservedPropertyRouter:
    Router.router.register(
        r'ObservedProperties',
        view.ObservedPropertyView,
        'observedproperty'
    )
    observedproperty_router = NestedSimpleRouter(
        Router.router,
        r'ObservedProperties',
        lookup='ObservedProperties'
    )
    observedproperty_router.register(
        r'Datastreams',
        view.DatastreamView,
        'datastream'
    )
    observedproperty_datastream_router = NestedSimpleRouter(
        observedproperty_router,
        r'Datastreams',
        'Datastreams'
    )
    observedproperty_datastream_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    observedproperty_datastream_router.register(
        r'Thing',
        view.ThingView,
        'thing'
    )
    observedproperty_datastream_tin_router = NestedSimpleRouter(
        observedproperty_datastream_router,
        r'Thing',
        'Thing'
    )
    observedproperty_datastream_tin_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    observedproperty_datastream_tin_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    observedproperty_datastream_tin_locat_router = NestedSimpleRouter(
        observedproperty_datastream_tin_router,
        r'Locations',
        'Locations'
    )
    observedproperty_datastream_tin_locat_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    observedproperty_datastream_tin_hist_router = NestedSimpleRouter(
        observedproperty_datastream_tin_router,
        r'HistoricalLocations',
        'HistoricalLocations'
    )
    observedproperty_datastream_tin_hist_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    observedproperty_datastream_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    observedproperty_datastream_obs_router = NestedSimpleRouter(
        observedproperty_datastream_router,
        r'Observations',
        'Observations'
    )
    observedproperty_datastream_obs_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )


class ObservationRouter:
    Router.router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    observation_router = NestedSimpleRouter(
        Router.router,
        r'Observations',
        lookup='Observations'
    )
    observation_router.register(
        r'FeatureOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )
    observation_router.register(
        r'Datastream',
        view.DatastreamView,
        'datastream'
    )
    observation_datastream_router = NestedSimpleRouter(
        observation_router,
        r'Datastream',
        'Datastream'
    )
    observation_datastream_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    observation_datastream_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    observation_datastream_router.register(
        r'Thing',
        view.ThingView,
        'thing'
    )
    observation_datastream_tin_router = NestedSimpleRouter(
        observation_datastream_router,
        r'Thing',
        'Thing'
    )
    observation_datastream_tin_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    observation_datastream_tin_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    observation_datastream_tin_locat_router = NestedSimpleRouter(
        observation_datastream_tin_router,
        r'Locations',
        'Locations'
    )
    observation_datastream_tin_locat_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    observation_datastream_tin_hist_router = NestedSimpleRouter(
        observation_datastream_tin_router,
        r'HistoricalLocations',
        'HistoricalLocations'
    )
    observation_datastream_tin_hist_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )


class FeatureOfInterestRouter:
    Router.router.register(
        r'FeaturesOfInterest',
        view.FeatureOfInterestView,
        'featureofinterest'
    )
    featureofinterest_router = NestedSimpleRouter(
        Router.router,
        r'FeaturesOfInterest',
        lookup='FeaturesOfInterest'
    )
    featureofinterest_router.register(
        r'Observations',
        view.ObservationView,
        'observation'
    )
    featureofinterest_obs_router = NestedSimpleRouter(
        featureofinterest_router,
        r'Observations',
        'Observations'
    )
    featureofinterest_obs_router.register(
        r'Datastream',
        view.DatastreamView,
        'datastream'
    )
    featureofinterest_obs_ds_router = NestedSimpleRouter(
        featureofinterest_obs_router,
        r'Datastream',
        'Datastream'
    )
    featureofinterest_obs_ds_router.register(
        r'Sensor',
        view.SensorView,
        'sensor'
    )
    featureofinterest_obs_ds_router.register(
        r'ObservedProperty',
        view.ObservedPropertyView,
        'observedproperty'
    )
    featureofinterest_obs_ds_router.register(
        r'Thing',
        view.ThingView,
        'thing'
    )
    featureofinterest_obs_ds_tin_router = NestedSimpleRouter(
        featureofinterest_obs_ds_router,
        r'Thing',
        'Thing'
    )
    featureofinterest_obs_ds_tin_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
    featureofinterest_obs_ds_tin_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    featureofinterest_obs_ds_tin_loc_router = NestedSimpleRouter(
        featureofinterest_obs_ds_tin_router,
        r'Locations',
        'Locations'
        )
    featureofinterest_obs_ds_tin_loc_router.register(
        r'HistoricalLocations',
        view.HistoricalLocationView,
        'historicallocation'
    )
    featureofinterest_obs_ds_tin_hloc_router = NestedSimpleRouter(
        featureofinterest_obs_ds_tin_router,
        r'HistoricalLocations',
        'HistoricalLocations'
    )
    featureofinterest_obs_ds_tin_hloc_router.register(
        r'Locations',
        view.LocationView,
        'location'
    )
