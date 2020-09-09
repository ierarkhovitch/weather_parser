# -*- coding: utf-8 -*-

import peewee

DATABASE = peewee.SqliteDatabase('database.db')


class DatabaseUpdater(peewee.Model):
    date = peewee.DateField()
    temperature_by_day = peewee.CharField()
    temperature_at_night = peewee.CharField()
    weather = peewee.TextField()
    img = peewee.TextField()

    class Meta:
        database = DATABASE

    @staticmethod
    def add_data(date, temperature_by_day, temperature_at_night, weather, img):
        DatabaseUpdater.get_or_create(date=date,
                                      defaults={'temperature_by_day': temperature_by_day,
                                                'temperature_at_night': temperature_at_night,
                                                'weather': weather,
                                                'img': img})

    @staticmethod
    def get_data(start_date, stop_date):
        for weather in DatabaseUpdater.select():
            iterable_date = weather.date
            if start_date <= iterable_date <= stop_date:
                print(f'{weather.date}: День:{weather.temperature_by_day} '
                      f'Ночь:{weather.temperature_at_night}: {weather.weather}')
            else:
                continue


DATABASE.create_tables([DatabaseUpdater])
