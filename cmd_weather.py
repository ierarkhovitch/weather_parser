# -*- coding: utf-8 -*-

import argparse
import datetime
import yandex_parser
import database
from yandex_image_handler import ImageMaker


parser = argparse.ArgumentParser(description="Сервис для прогноза погоды")
parser.add_argument(
    '--start_date', type=str, help='Интересуемая начальная дата в формате ММ-ДД')
parser.add_argument(
    '--stop_date', type=str, help='Интересуемая конечная дата в формате ММ-ДД')
parser.add_argument(
    '--add_to_db', help='Добавление прогнозов за диапазон дат в базу данных', action='store_true')
parser.add_argument(
    '--get_data', help='Получение прогнозов за диапазон дат из базы в формате ММ-ДД.', action='store_true')
parser.add_argument(
    '--create_images', help='Создание открыток из полученных прогнозов.', action='store_true')
parser.add_argument(
    '--show_all', help='Выведение полученных прогнозов на консоль', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
    if args.start_date and args.stop_date:
        start_date = datetime.date.fromisoformat('2020-' + args.start_date)
        stop_date = datetime.date.fromisoformat('2020-' + args.stop_date)
    today = datetime.date.today()
    start_day = datetime.date(today.year, today.month, today.day - 4)
    parser = yandex_parser.WeatherMaker(yandex_parser.RESPONSE, start_day, today).read_response()

    if args.add_to_db:
        parser = yandex_parser.WeatherMaker(yandex_parser.RESPONSE, start_date, stop_date).read_response()

    elif args.get_data:
        database.DatabaseUpdater.get_data(start_date, stop_date)

    elif args.create_images:
        parser = yandex_parser.WeatherMaker(yandex_parser.RESPONSE, start_date, stop_date)
        parser.read_response()
        postcards = ImageMaker(parser.weather_forecast)
        postcards.gradient()

    elif args.show_all:
        for weather in database.DatabaseUpdater.select():
            print(f'{weather.date}: День:{weather.temperature_by_day} '
                  f'Ночь:{weather.temperature_at_night}: {weather.weather}')

