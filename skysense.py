from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)
app.secret_key = 'literally anything'

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        search_term = request.form.get('location_parameter') 
        if search_term == '':
            search_term = "London"
            flash('Please enter a location')
    else:
        search_term = "London"
    while(True):
            API_KEY = open('api_key_weather', 'r').read()
            API_CALL = "https://api.weatherapi.com/v1/current.json?key=" + API_KEY + "&q=" + search_term + "&aqi=yes"
            response = requests.get(API_CALL).json()
            return_code = response.get('error', {}).get('code')
            #{'error': {'code': 1006, 'message': 'No matching location found.'}}
            if (return_code == 1006):
                search_term = "London"
                flash('No matching location found. Search Again')
            else:
                break

    
    weather_info = {
        # Overall
        'day_night': response['current']['is_day'],
        'location_name': response['location']['name'],
        'overall_weather': response['current']['condition']['text'],
        'overall_weather_icon': response['current']['condition']['icon'],
        'humidity': response['current']['humidity'],
        # Temperature
        'temperature_cel': response['current']['temp_c'],
        'temperature_fahr': response['current']['temp_f'],
        'feelslike_c': response['current']['feelslike_c'],
        'feelslike_f': response['current']['feelslike_f'],
        # Wind
        'wind_mph': response['current']['wind_mph'],
        'wind_kph': response['current']['wind_kph'],
        'wind_degree': response['current']['wind_degree'],
        'wind_direction': response['current']['wind_dir'],
    }
    return render_template('index.html', weather_info=weather_info)   

if __name__ == "__main__":
    app.run(debug=True)
    
