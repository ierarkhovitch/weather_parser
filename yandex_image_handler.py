# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageColor
import requests

RESPONSE = requests.get(
    r'https://yandex.ru/pogoda/murino?utm_campaign=informer&utm_content=main_informer&utm_medium=web&utm_source'
    r'=home&utm_term=title')
TEMPLATE_PATH = 'python_snippets/external_data/probe.jpg'
FONT_PATH = './images/sfns-display-bold.ttf'
WEATHER_IMG_PATH = 'python_snippets/external_data/weather_img/'
GRADIENT = {'snow': {'blue': 100, 'green': 100, 'red': 100, 'unit': 3},
            'cloud': {'blue': 100, 'green': 170, 'red': 255, 'unit': 3},
            'sun': {'blue': 255, 'green': 255, 'red': 100, 'unit': 3},
            'rain': {'blue': 30, 'green': 30, 'red': 255, 'unit': 2}}


class ImageMaker:
    def __init__(self, weather_forecast):
        self.weather_forecast = weather_forecast

    def draw_text(self, image_name, date, weather):
        image = Image.open(image_name)
        image_draw = ImageDraw.Draw(image)
        color = ImageColor.getrgb('black')

        font = ImageFont.truetype(FONT_PATH, 20, encoding='utf-8')
        image_draw.text((10, 10), date.strftime("%d.%m.%Y"), font=font, fill=color)
        image_draw.text((10, 210), weather['погода'], font=font, fill=color)
        image_draw.multiline_text((380, 130), f"Днём: {weather['температура']['днём']}\n"
                                              f"Ночью: {weather['температура']['ночью']}", font=font, fill=color)
        image.save(image_name)

    def put_img(self, weather_img_name, gradient_img_name, width):
        weather_img = Image.open(f'{WEATHER_IMG_PATH}{weather_img_name}.png')
        weather_img = weather_img.resize((100, 100))
        gradient_img = Image.open(gradient_img_name)
        gradient_img.paste(weather_img, (width - width // 4, 20), weather_img)
        gradient_img.save(gradient_img_name)

    def gradient(self):
        template = cv2.imread(TEMPLATE_PATH).copy()
        height, width = np.size(template, 0), np.size(template, 1)
        for date, weather_on_date in self.weather_forecast.items():
            weather = weather_on_date['img']
            unit = GRADIENT[weather]['unit']
            for line in range(width):
                cv2.line(template, (line, 0), (line, height),
                         (GRADIENT[weather]['red'] + line // unit,
                          GRADIENT[weather]['green'] + line // unit,
                          GRADIENT[weather]['blue'] + line // unit), 1)
            image_name = f'{date}.jpg'
            cv2.imwrite(image_name, template)
            self.draw_text(image_name, date, weather_on_date)
            self.put_img(weather_on_date['img'], image_name, width)

