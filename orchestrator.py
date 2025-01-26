'''
API Orchestrator
'''
import fastapi
import fastapi.middleware
import fastapi.middleware.cors
import pydantic

import utilities.requestutils as requestutils


app = fastapi.FastAPI()

app.add_middleware(
    fastapi.middleware.cors.CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class ResponseModel(pydantic.BaseModel):
    success: bool
    message: str
    data: dict = {}


@app.get("/")
async def root_endpoint():
    '''Root endpoint for testing purposes'''
    return ResponseModel(success=True, message="Orchestrator Root Endpoint", data={})


@app.get('/distance')
async def get_distance(origin_lat: float, origin_long: float, dest_lat: float, dest_lon: float):
    '''End point to get the driving travel time by road between two co-ordinates'''
    distance = requestutils.get_route_time(start_coord=(origin_lat, origin_long), end_coords=(dest_lat, dest_lon))
    response = {'distance': distance}
    return response


@app.get('/distance-postcode')
async def get_distance_between_postcodes(first_postcode: str, second_postcode: str):
    '''End point to get the distance by road between two postcodes'''
    distance = requestutils.get_route_time_between_postcodes(first_postcode=first_postcode, second_postcode=second_postcode)
    data = {'distance': distance}
    return ResponseModel(success=True, message="Retrieved Distance", data=data)


@app.get('/weather-coordinates')
async def get_weather_coordinates(lat: float, lon: float):
    '''End point to get the current weather at the specified location with co-ordinates'''
    weather = requestutils.get_todays_weather_details(lattitide=lat, longitude=lon)
    response = {'weather': weather}
    return ResponseModel(success=True, message='Retrieved weather', data=response)


@app.get('/weather-postcode')
async def get_weather_postcode(postcode: str):
    '''End point to get the current weather at the specified location with postcode'''
    try:
        lon, lat = requestutils.convert_postcode_to_coordinates(postcode=postcode)
    except requestutils.ResponseError:
        return ResponseModel(success=False, message='Request Failed, bad postcode')

    weather = requestutils.get_todays_weather_details(lattitide=lat, longitude=lon)
    response = {'weather': weather}
    return ResponseModel(success=True, message='Retrieved weather', data=response)


@app.get('/postcode-to-coordinates')
async def get_postcode_coordinates(postcode: str):
    '''End point to convert the provided postcode to co-ordinates'''
    try:
        lon, lat = requestutils.convert_postcode_to_coordinates(postcode=postcode)
    except requestutils.ResponseError:
        return ResponseModel(success=False, message='Request Failed, bad args?')

    response = {'lon': lon, 'lat': lat}
    return ResponseModel(success=True, message='Retrieved Co-ordinates', data=response)
