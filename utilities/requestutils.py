'''
API request utils
'''
import requests
import typing

import utilities.openmeteocodes as openmeteocodes

_SUCCESSFUL_STATUS_CODE: int = 200

_DEFAULT_POSTCODE_CONVERTER_URL: str = 'https://api.postcodes.io/postcodes/'
_DEFAULT_OSRM_ROUTE_URL: str = 'https://router.project-osrm.org/route/v1/driving/'
_DEFAULT_WEATHER_URL: str = 'http://www.7timer.info/bin/api.pl'
_BACKUP_WEATHER_URL: str = 'https://api.open-meteo.com/v1/forecast?'

_DEFAULT_OSRM_ROUTE_PARAMS: typing.Dict[str, str] = {'overview': 'false', 'steps': 'false'}
_DEFAULT_WEATHER_PARAMS: typing.Dict[str, str] = {'product': 'civillight', 'output': 'json'}


class ResponseError(Exception):
    '''Exception raised when API request receives a non 200 response code'''
    pass


def get_request_data_json(end_point: str,
                          params: typing.Optional[typing.Dict[str, str]] = None):
    '''Make a HTTP request, handle response status, and return retrieved data'''
    response = requests.get(end_point, params=params)
    response_status = response.status_code

    if response_status == _SUCCESSFUL_STATUS_CODE:
        data = response.json()
        return data
    else:
        raise ResponseError(f'Received Status Code: {response_status}')


def get_route_time(start_coord: tuple[float, float],
                   end_coords: tuple[float, float]):
    '''
    Get the distance between two co-ordinates
    https://project-osrm.org/docs/v5.24.0/api/?language=cURL#route-service
    '''
    # Format OSRM route endpoint
    end_point: str = f'{_DEFAULT_OSRM_ROUTE_URL}{start_coord[1]},{start_coord[0]};{end_coords[1]},{end_coords[0]}'

    data = get_request_data_json(end_point=end_point, params=_DEFAULT_OSRM_ROUTE_PARAMS)
    distance = data['routes'][0]['duration']  # This doesn't seem correct??? Is this in m?

    return distance


def get_todays_weather_details(lattitide: float,
                               longitude: float):
    '''
    Get the weather details from the specified location
    Default: https://www.7timer.info/doc.php#introduction
    Backup: https://api.open-meteo.com/v1/forecast?
    '''
    location_params: typing.Dict[str, str] = {'lat': str(lattitide), 'lon': str(longitude)}
    request_params: typing.Dict[str, str] = location_params | _DEFAULT_WEATHER_PARAMS

    try:
        data = get_request_data_json(end_point=_DEFAULT_WEATHER_URL, params=request_params)
        weather_type: str = data['dataseries'][0]['weather']
    except ResponseError as e:
        print(f'Failed to get weather data with error: {e}')

        # Try backup service
        formatted_end_point: str = f'{_BACKUP_WEATHER_URL}latitude={lattitide}&longitude={longitude}&current_weather=true'
        data = get_request_data_json(end_point=formatted_end_point)

        # Convert weather code to brief description
        weather_code: int = data['current_weather']['weathercode']
        weather_type = openmeteocodes._WEATHER_CODES[weather_code]

    return weather_type


def convert_postcode_to_coordinates(postcode: str):
    '''
    Convert the specified postcode to a set of co-ordinates
    '''
    end_point: str = f'{_DEFAULT_POSTCODE_CONVERTER_URL}{postcode}'

    data = get_request_data_json(end_point=end_point)

    if data['status'] == 404:
        raise ResponseError()

    lat = data['result']['latitude']
    lon = data['result']['longitude']

    return (lat, lon)


def get_route_time_between_postcodes(first_postcode: str, second_postcode: str):
    '''
    Get the distance in km between two postcodes
    '''
    first_coords: typing.Tuple[float, float] = convert_postcode_to_coordinates(postcode=first_postcode)
    second_coords: typing.Tuple[float, float] = convert_postcode_to_coordinates(postcode=second_postcode)
    distance = get_route_time(start_coord=first_coords, end_coords=second_coords)

    return distance


def main():
    # Test Co-ords
    nottingham_coords: tuple[float, float] = (52.9540, 1.1550)

    # Test distance request
    route_info_postcode = get_route_time_between_postcodes(first_postcode='ng76nw', second_postcode='ng25gy')
    print(route_info_postcode)

    # Test weather request
    weather: str = get_todays_weather_details(lattitide=nottingham_coords[0], longitude=nottingham_coords[1])
    print(weather)

    # Test postcode to co-ordinates
    lon, lat = convert_postcode_to_coordinates(postcode='bs84bz')
    print('lon: ' + lon)
    print('lat: ' + lat)


if __name__ == '__main__':
    main()
