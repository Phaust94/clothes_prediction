"""
Test ClothesPredictor
"""

import logging


from clothes_prediction import ApiGetter

api_getter = ApiGetter()
current_weather = api_getter.get_weather()
print(current_weather)
