import os
import json
import http.client
import urllib.parse


def get_weather(location):

    # connect to geocoding API
    geocode_conn = http.client.HTTPSConnection("geocode.xyz")
    geocode_params = urllib.parse.urlencode({
        'auth': os.getenv('GEOCODE_AUTH'),
        'locate': location,
        'json': 1
    })

    geocode_conn.request("GET", "/?{}".format(geocode_params))

    geocode_res = geocode_conn.getresponse()
    geocode_json = json.loads(geocode_res.read())  # reads JSON file from response

    if 'error' in geocode_json:
        return 'API_Error'

    geocode_values = (
        geocode_json['latt'],
        geocode_json['longt']
    )

    # connect to Weather DataHub
    datahub_conn = http.client.HTTPSConnection("rgw.5878-e94b1c46.eu-gb.apiconnect.appdomain.cloud")

    datahub_headers = {
        'X-IBM-Client-Id': os.getenv('DATAHUB_API_KEY'),
        'X-IBM-Client-Secret': os.getenv('DATAHUB_SECRET'),
        'accept': "application/json"
    }

    datahub_params = urllib.parse.urlencode({
        'excludeParameterMetadata': 'true',
        'includeLocationName': 'true',
        'latitude': geocode_values[0],
        'longitude': geocode_values[1]
    })

    datahub_conn.request('GET',
                         '/metoffice/production/v0/forecasts/point/daily?{}'.format(datahub_params),
                         headers=datahub_headers
                         )

    datahub_res = datahub_conn.getresponse()
    datahub_json = json.loads(datahub_res.read())

    try:
        time_series = datahub_json['features'][0]['properties']['timeSeries'][1]
    except KeyError:
        return 'API_Error'

    weather_data = {
        "City": geocode_json['standard']['city'],
        "Country": geocode_json['standard']['countryname'],
        "SignificantWeatherCode": time_series['daySignificantWeatherCode'],
        "MaxTemperature": time_series['dayUpperBoundMaxTemp'],  # degrees Celsius
        "MinTemperature": time_series['dayLowerBoundMaxTemp'],
        "ChanceOfPrecipitation": time_series['dayProbabilityOfPrecipitation'],  # %
        "WindSpeed": time_series['midday10MWindSpeed'],  # m/s
        "MaxUvIndex": time_series['maxUvIndex']
    }
    return weather_data
