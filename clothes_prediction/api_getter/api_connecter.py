"""
Class used to connect to the weather api to get current weather in the city
"""


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

    def _load_api_key(self, api_key_path: str = None):
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

    def get_weather(self):
        """
        Gets weather for current city
        :return:
        """
        url_to_get_weather = f"api.openweathermap.org/data/2.5/weather?id={self.city}" \
                             f"&APPID={self._api_key}"
