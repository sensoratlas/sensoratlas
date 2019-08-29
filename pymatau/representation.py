from rest_framework import serializers
import json


class Representation(serializers.ModelSerializer):
    def to_representation(self, obj):

        data = super(Representation, self).to_representation(obj)

        try:
            data['Observations@iot.navigationLink'] = \
                data['observationsLink']
            data.pop('observationsLink')
            data.move_to_end('Observations@iot.navigationLink', last=False)
        except KeyError:
            pass

        try:
            data['FeaturesOfInterest@iot.navigationLink'] = \
                data['featuresOfInterestLink']
            data.pop('featuresOfInterestLink')
            data.move_to_end('FeaturesOfInterest@iot.navigationLink',
                             last=False)
        except KeyError:
            pass

        try:
            data['Datastreams@iot.navigationLink'] = \
                data['datastreamsLink']
            data.pop('datastreamsLink')
            data.move_to_end('Datastreams@iot.navigationLink', last=False)
        except KeyError:
            pass

        try:
            data['ObservedProperties@iot.navigationLink'] = \
                data['observedpropertiesLink']
            data.pop('observedpropertiesLink')
            data.move_to_end('ObservedProperties@iot.navigationLink',
                             last=False)
        except KeyError:
            pass

        try:
            data['Sensors@iot.navigationLink'] = \
                data['sensorsLink']
            data.pop('sensorsLink')
            data.move_to_end('Sensors@iot.navigationLink', last=False)
        except KeyError:
            pass

        try:
            data['Things@iot.navigationLink'] = \
                data['thingsLink']
            data.pop('thingsLink')
            data.move_to_end('Things@iot.navigationLink', last=False)
        except KeyError:
            pass

        try:
            data['Locations@iot.navigationLink'] = \
                data['locationsLink']
            data.pop('locationsLink')
            data.move_to_end('Locations@iot.navigationLink', last=False)
        except KeyError:
            pass

        try:
            data['HistoricalLocations@iot.navigationLink'] = \
                data['historicallocationsLink']
            data.pop('historicallocationsLink')
            data.move_to_end('HistoricalLocations@iot.navigationLink',
                             last=False)
        except KeyError:
            pass

        try:
            data['observedArea'] = json.loads(obj.observedArea.geojson)
        except AttributeError:
            pass

        try:
            data['feature'] = json.loads(obj.feature.geojson)
        except AttributeError:
            pass

        try:
            data['location'] = json.loads(obj.location.geojson)
        except AttributeError:
            pass

        try:
            data['result'] = obj.result['result']
        except (AttributeError, TypeError):
            pass

        try:
            data['@iot.id'] = data['id']
            data.pop('id')
        except KeyError:
            pass
        try:
            data['@iot.selfLink'] = data['selfLink']
            data.pop('selfLink')
            data.move_to_end('@iot.selfLink', last=False)
            data.move_to_end('@iot.id', last=False)
        except KeyError:
            pass

        return data
