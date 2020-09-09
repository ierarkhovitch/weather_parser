# -*- coding: utf-8 -*-

import datetime
from bs4 import BeautifulSoup
import requests
import database

RESPONSE = requests.get(
    r'https://yandex.ru/pogoda/murino?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source'
    r'=home&utm_term=title')
WEATHERS = {'snow': ['снег'], 'cloud': ['облачн'], 'sun': ['солн', 'ясно'], 'rain': ['гроз', 'дожд', 'пасмур', 'ливен']}


def what_is_the_weather(weather, weathers):
    for img, templates in weathers.items():
        if any(template in weather.lower() for template in templates):
            return img


class WeatherMaker:
    def __init__(self, response, start_date, stop_date):
        self.response = response
        self.weather_forecast = {}
        self.start_date = start_date
        self.stop_date = stop_date

    def read_response(self):
        try:
            html_doc = BeautifulSoup(RESPONSE.text, features='html.parser')
            text = html_doc.find_all("ul", {"class": "swiper-wrapper"})[1]
            for element in text:
                date_class = element.find('time', class_="time forecast-briefly__date")
                date, date_str = datetime.date.fromisoformat(date_class.attrs['datetime'][:-11]), date_class.text
                if self.start_date <= date <= self.stop_date:
                    temperature = element.find_all('span', class_="temp__value")
                    day, night = temperature[0].text, temperature[1].text
                    weather = element.find('div', class_="forecast-briefly__condition").text
                    img = what_is_the_weather(weather, WEATHERS)
                    self.weather_forecast[date] = {'погода': weather,
                                                   'температура': {'днём': day, 'ночью': night},
                                                   'img': img}
                    database.DatabaseUpdater.add_data(date=date,
                                                      temperature_by_day=day,
                                                      temperature_at_night=night,
                                                      weather=weather,
                                                      img=img)

        except Exception as exc:
            print(f"ERROR: {exc}")
