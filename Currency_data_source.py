"""Модуль, который описывает создание и обновление данных о курсах валют"""

import json
from datetime import datetime

import requests

cache_file = 'file.json'  # json файл для просмотра и использования данных, полученных с сайта ЦБ РФ.
exchange = 'exchange.json'
web_site = 'https://www.cbr-xml-daily.ru/daily_json.js'  # Сайт центробанка РФ для получения актуального курса валют.
current_date = {'Текущая дата обновления ': str(datetime.now())}  # Отображение текущей даты.


def currency_source():
    """Функция отправляет запрос через метода get,
    получает и сохраняет в file.json данные о текущих курсах валют с сайта ЦБ РФ"""
    try:
        if requests.get(web_site).status_code == 200:  # Код ответа (состояния) HTTP "запрос выполнен успешно".
            data = requests.get(web_site).json()  # Получение доступа к json файлу
            data.update(current_date)
            with open(cache_file, 'w', encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                return data
    except requests.get(web_site).status_code == 400:  # Код ответа (состояния) HTTP "запрос выполнен не успешно,
        # брать данные из кэша.
        with open(cache_file, encoding="utf-8") as f:
            data = json.load(f)
            return data


def currencies():
    """Функция, которая получает и сохраняет в exchange.json данные о текущих валютах с сайта ЦБ РФ"""
    try:
        val = requests.get(web_site).json()['Valute']
        with open(exchange, 'w', encoding="utf-8") as f:
            json.dump(val, f, indent=4, ensure_ascii=False)
            return val
    except requests.exceptions.ConnectionError:  # если интернет отключен, брать значение если интернет отключен,
        # брать значение из файла exchange.json
        with open(exchange, encoding="utf-8") as f:
            val = json.load(f)
            return val


if __name__ == '__main__':
    web_site = 'https://www.cbr-xml-daily.ru/daily_json.js'
    print(currency_source())
    print(currencies().keys())
