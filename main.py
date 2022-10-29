from flask import Flask, render_template, request, url_for, flash, redirect
import requests
import copy
from datetime import datetime
import tzlocal
API_KEY = "bd0a0b51129f07b5bf8240f51a5f5207"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
GEO_BASE_URL = "http://api.openweathermap.org/geo/1.0/"
ICON_URL = "http://openweathermap.org/img/w/"

app = Flask(__name__)
app.config['SECRET_KEY'] = '10b599aca6578b86a2b34dca96427bda8a9d1c20f1f8071e'       # Used for flash

cityToSearch = []
previousWeatherData = []       # Actual weather data to display, including past searches
coordinates = []
weatherInfo = dict()
iconURL = []


def retrieveFromForm():
    searchType = request.form.get('searchType', False)
    cityInput = request.form.get('cityInput', False)
    zipInput = request.form.get('zipInput', False)
    countryInput = request.form.get('countryInput', False)
    previous = request.form.get('previousSearches', False)
    units = request.form['units']
    return searchType, cityInput, zipInput, countryInput, previous, units
def retrieveWeatherData():
    # Retrieve data from forms about what weather information user wants to display
    toDisplay = ['icon', request.form.get('description', False), request.form.get('currentTemp', False),
                 request.form.get('realFeel', False), request.form.get('pressure', False),
                 request.form.get('humidity', False), request.form.get('visibility', False),
                 request.form.get('windSpeed', False), request.form.get('windDirection', False),
                 request.form.get('cloud', False), request.form.get('rain1Hour', False),
                 request.form.get('rain3Hour', False), request.form.get('snow1Hour', False),
                 request.form.get('snow3Hour', False), request.form.get('sunrise', False),
                 request.form.get('sunset', False)]

    toDisplay[:] = (value for value in toDisplay if value != False)
    return toDisplay

def saveCoord(geo_data, searchType):
    if searchType == 'byCity':
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        country = geo_data[0]["country"]
    else:
        lat = geo_data["lat"]
        lon = geo_data["lon"]
        country = geo_data["country"]
    if request.form['previousSearches'] == 'discard':
        coordinates.clear()
    coordinates.append({"lat": lat, "lon": lon, "country": country})
    return lat, lon
def saveWeather(weather_data):
    toDisplay = retrieveWeatherData()
    if len(previousWeatherData) > 0:        # Deepcopy previous searches to save
        tmp = copy.deepcopy(previousWeatherData)

    weatherInfo.clear()
    weatherInfo.update({'icon': weather_data['weather'][0]['icon'],
                        'Description': weather_data['weather'][0]['main'] + ", " + weather_data['weather'][0][
                            'description'],
                        'Current Temperature': weather_data['main']['temp'],
                        'Real Feel': weather_data['main']['feels_like'],
                        'Pressure': weather_data['main'].get('pressure'),
                        'Humidity': weather_data['main'].get('humidity'),
                        'Visibility': weather_data.get('visibility'),
                        'Wind Speed': weather_data.get('wind', {}).get('speed'),
                        'Wind Direction': weather_data.get('wind', {}).get('deg'),
                        'Cloud': weather_data.get('clouds', {}).get('all'),
                        'Rain (past 1 Hour)': weather_data.get('rain', {}).get('1h', None),      # Check if 'rain' is present, if not return empty dict then None
                        'Rain (past 3 Hours)': weather_data.get('rain', {}).get('3h', None),
                        'Snow (past 1 Hour)': weather_data.get('snow', {}).get('1h', None),
                        'Snow (past 3 Hours)': weather_data.get('snow', {}).get('3h', None),
                        'Sunrise': weather_data['sys']['sunrise'],
                        'Sunset': weather_data['sys']['sunset']
                        })

    iconURL.append(f"{ICON_URL}{weatherInfo['icon']}.png")

    # Convert Unix, UTC time to local time and update in weatherInfo
    localTime = tzlocal.get_localzone()
    updatedSunrise = datetime.fromtimestamp(weatherInfo['Sunrise'], localTime).strftime('%H:%M:%S')
    updatedSunset = datetime.fromtimestamp(weatherInfo['Sunset'], localTime).strftime('%H:%M:%S')
    weatherInfo['Sunrise'] = updatedSunrise
    weatherInfo['Sunset'] = updatedSunset

    for i in list(weatherInfo.keys()):      # Save only the weather info the user wants to display
        if i in toDisplay:
            continue
        else:
            del weatherInfo[i]
    weatherInfo.pop('icon')
    if len(previousWeatherData) == 0:       # Update list with previous searches and new search appended to the end
        previousWeatherData.append(weatherInfo)
    else:
        previousWeatherData.clear()
        for i in tmp:           # Add previous searches individually
            previousWeatherData.append(i)
        previousWeatherData.append(weatherInfo)

def saveCityToSearch(geo_data, searchType):
    if searchType == 'byZip':
        cityToSearch.append(geo_data["name"])
    elif searchType == 'byCity':
        cityToSearch.append(geo_data[0]["name"])  # Add new search

@app.route('/')
def index():
    return render_template('index.html', cityToSearch=cityToSearch,
                           previousWeatherData=previousWeatherData, coordinates=coordinates,
                           iconURL=iconURL)


@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        # Retrieve info from HTML form, ensuring that the inputs fields have inputs
        searchType, cityInput, zipInput, countryInput, previous, units = retrieveFromForm()

        # Check that required data was provided
        if not searchType:          # Specify searching by city or zip code
            flash('Search by city or zip is required!')

        elif searchType == 'byCity' and not cityInput:      # Check city is provided
            flash('City name is required when searching by city!')

        elif searchType == 'byZip' and (not zipInput or not countryInput):          # Check zip/country are provided
            flash('Zip/postal code AND country code are required when searching by zip!')

        elif not previous:       # How to handle previous requests
            flash('Save or discard previous searches is required!')

        else:       # Required data is provided
            # Set up Geocoding API
            if cityInput and not countryInput:
                geo_url = f"{GEO_BASE_URL}direct?q={cityInput}&limit=1&appid={API_KEY}"
            elif cityInput and countryInput:
                geo_url = f"{GEO_BASE_URL}direct?q={cityInput},{countryInput}&limit=1&appid={API_KEY}"
            elif zipInput and countryInput:
                geo_url = f"{GEO_BASE_URL}zip?zip={zipInput},{countryInput}&appid={API_KEY}"

            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()

            if geo_response.ok and len(geo_data) != 0:
                lat, lon = saveCoord(geo_data, searchType)      # Save coordinates for use in Weather API
                weather_url = f"{WEATHER_URL}?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"
                weather_response = requests.get(weather_url)

                if weather_response.status_code == 200:  # Successful request, safeguard
                    weather_data = weather_response.json()
                    if request.form['previousSearches'] == 'discard':
                        iconURL.clear()
                        previousWeatherData.clear()
                        cityToSearch.clear()  # Clear the list, only save the last city

                    saveWeather(weather_data)       # Save the information to be displayed
                    saveCityToSearch(geo_data, searchType)      # Save city name to be displayed
                    return redirect(url_for('index'))       # Display weather on home page
                else:
                    flash('Invalid city, no weather data available')
            else:
                flash('Invalid city/zip code/country code')     # Lumped together for now, can further define the error
    return render_template('create.html')
