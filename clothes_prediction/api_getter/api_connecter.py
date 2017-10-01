"""
Class used to connect to the weather api to get current weather in the city
"""

import requests
import json
from datetime import datetime
import pandas as pd


class ApiGetter:
    """
    Class, able to perform weather API calls
    """

    _api_key = None
    _default_city = 706483  # Kharkiv, Ukraine
    default_api_key_path = "C:/Коханий/projects/clothes_prediction_project/clothes_prediction/data/api_key.txt"

    def __init__(self, city: int = None):
        """
        Instantiates API caller instance with given city
        :param city: (optional) city_id to use. The default city is ApiGetter._default_city
        """

        if city is None:
            city = self._default_city

        self.city = city
        self._load_api_key()

    def _load_api_key(self, api_key_path: str = None) -> None:
        """
        Loads API key from a file
        :param api_key_path: where the API key is stored. If not present
        :return:
        """
        if self._api_key is None:
            if api_key_path is None:
                api_key_path = self.default_api_key_path
            with open(api_key_path, 'r') as api_key_file:
                api_key = api_key_file.readline()
            self._api_key = api_key

    def get_weather(self) -> pd.Series:
        """
        Gets weather for current instance's city
        :return: current weather after cleanup
        """
        url_to_get_weather = f"https://api.openweathermap.org/data/2.5/weather?id={self.city}" \
                             f"&APPID={self._api_key}"
        current_weather_raw = requests.get(url_to_get_weather)
        current_weather = json.loads(current_weather_raw.text)
        current_weather_clean = self._parse_api_response(current_weather)

        return current_weather_clean

    def _parse_api_response(self, api_response: dict) -> pd.Series:
        """
        Remove unnecessary info from the weather api response
        :param api_response: data from api
        :return: cleaned up data
        """

        assert api_response['id'] == self.city, "API responded with data for an incorrect city"

        cleaned_up_weather = dict()
        try:
            main_part = api_response["main"]
            temp_fahrenheit: float = main_part['temp']
            temp_celsius = (temp_fahrenheit - 32) * 5 / 9
            cleaned_up_weather['Temp'] = temp_celsius
            cleaned_up_weather['Pressure'] = main_part['pressure']
            cleaned_up_weather['Humidity'] = main_part['humidity']
            cleaned_up_weather['Datetime'] = datetime.fromtimestamp(api_response['dt'])
            cleaned_up_weather['Wind speed'] = api_response['wind']['speed']
            cleaned_up_weather['Clouds'] = api_response['clouds']['all']
            cleaned_up_weather['Description'] = api_response['weather'][0]['main']
            cleaned_up_weather['Description detailed'] = api_response['weather'][0]['description']
        except KeyError as e:
            error_message = f"API response format changed. Current API response format is \n" \
                            f"{api_response} \n " \
                            f"and it lacks the following: {e.args}"
            print(error_message)
        cleaned_up_weather = pd.Series(cleaned_up_weather)
        return cleaned_up_weather
