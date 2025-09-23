import requests

# https://github.com/SeanDishman/IP2Temperature

def get_public_ip():
    try:
        ip = requests.get("https://api.ipify.org").text.strip()
        return ip
    except:
        return None


def geolocate_ip(ip):
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}").json()
        if resp['status'] == 'success':
            return resp['lat'], resp['lon'], resp['city']
        else:
            return None, None, None
    except:
        return None, None, None


def get_weather(lat, lon):
    headers = {
        'User-Agent': 'Py Weather'
    }
    try:
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        points_resp = requests.get(points_url, headers=headers).json()
        forecast_url = points_resp['properties']['forecastHourly']

        forecast_resp = requests.get(forecast_url, headers=headers).json()
        periods = forecast_resp['properties']['periods']
        if periods:
            temp = periods[0]['temperature']
            unit = periods[0]['temperatureUnit']
            short_forecast = periods[0]['shortForecast']
            return temp, unit, short_forecast
        else:
            return None, None, None
    except:
        return None, None, None


def main():
    ip = get_public_ip()
    if not ip:
        print("Could not get public IP address.")
        return
    lat, lon, city = geolocate_ip(ip)
    if lat is None:
        print("Could not geolocate IP address.")
        return
    print(f"Location based on IP: {city} ({lat}, {lon})")
    temp, unit, forecast = get_weather(lat, lon)
    if temp is not None:
        print(f"Current temperature in {city}: {temp} {unit} - {forecast}")
    else:
        print("Could not retrieve weather data.")


if __name__ == "__main__":
    main()
