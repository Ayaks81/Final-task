import re
import requests
import datetime
import time
import asyncio
import aiohttp

openweatherAPI = '0fb610dab7456bc44dbdde2ddba9be71'
Cities = []
class CityInfo:
    def __init__(self, city_name):
        self.city_name = city_name
        self.temp = None
        self.humidity = None
        self.pressure = None
        self.wind = None
        self.sunrise = None
        self.sunset = None
        self.day_length = None

with open("cities.txt", "r", encoding='utf-8') as f:
    for i in f:
        result = re.findall(r'([\bA-Z][a-z]+)', i)
        if result:
            if len(result) > 1:
                city_name = result[0] + ' ' + result[1]
            else:
                city_name = result[0]
            a = CityInfo(city_name)
            print(a.city_name)
            Cities.append(a)

start_time = time.time()
def get_noas_data():
    for c in Cities:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={c.city_name}&appid={openweatherAPI}&units=metric')
        c.temp = re.search(r'temp":(\d+[\.]\d+|\d+)', r.text).group(0).split(":")[1]
        c.humidity = re.search(r'humidity":(\d+[\.]\d+|\d+)', r.text).group(0).split(":")[1]
        c.pressure = re.search(r'pressure":(\d+[\.]\d+|\d+)', r.text).group(0).split(":")[1]
        c.wind = re.search(r'speed":(\d+[\.]\d+|\d+)', r.text).group(0).split(":")[1]
        c.sunrise = re.search(r'sunrise":\d+', r.text).group(0).split(":")[1]
        c.sunrise = datetime.datetime.fromtimestamp(int(c.sunrise))
        c.sunset = re.search(r'sunset":\d+', r.text).group(0).split(":")[1]
        c.sunset = datetime.datetime.fromtimestamp(int(c.sunset))
        c.day_length = c.sunset - c.sunrise
        print(f'В городе {c.city_name} \n'
                       f'Температура воздуха составит: {c.temp} C° \n'
                       f'Влажность воздуха: {c.humidity}%\n'
                       f'Давление: {c.pressure} мм.р.т.\n'
                       f'Ветер: {c.wind} м/с\n'
                       f'Восход: {c.sunrise}\n'
                       f'Закат: {c.sunset}\n'
                       f'Продолжительность дня: {c.day_length}\n')

async def get_city_data(session, c):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={c.city_name}&appid={openweatherAPI}&units=metric'
    async with session.get(url=url) as response:
        r = await response.text()
        c.temp = re.search(r'temp":(\d+[\.]\d+|\d+)', r).group(0).split(":")[1]
        c.humidity = re.search(r'humidity":(\d+[\.]\d+|\d+)', r).group(0).split(":")[1]
        c.pressure = re.search(r'pressure":(\d+[\.]\d+|\d+)', r).group(0).split(":")[1]
        c.wind = re.search(r'speed":(\d+[\.]\d+|\d+)', r).group(0).split(":")[1]
        c.sunrise = re.search(r'sunrise":\d+', r).group(0).split(":")[1]
        c.sunrise = datetime.datetime.fromtimestamp(int(c.sunrise))
        c.sunset = re.search(r'sunset":\d+', r).group(0).split(":")[1]
        c.sunset = datetime.datetime.fromtimestamp(int(c.sunset))
        c.day_length = c.sunset - c.sunrise

async def get_data():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for c in Cities:
            tasks.append(asyncio.create_task(get_city_data(session, c)))
        await asyncio.gather(*tasks)

def main():
    asyncio.run(get_data())
    #get_noas_data()
    for c in Cities:
        print(f'В городе {c.city_name} \n'
              f'Температура воздуха составит: {c.temp} C° \n'
              f'Влажность воздуха: {c.humidity}%\n'
              f'Давление: {c.pressure} мм.р.т.\n'
              f'Ветер: {c.wind} м/с\n'
              f'Восход: {c.sunrise}\n'
              f'Закат: {c.sunset}\n'
              f'Продолжительность дня: {c.day_length}\n')
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")

if __name__ == '__main__':
    main()