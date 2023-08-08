import requests

# Получение информации о городе по его geonameid
response = requests.get('http://127.0.0.1:8000/city_by_id?geonameid=524901')
print(response.json())

# Получение списка городов
response = requests.get('http://127.0.0.1:8000/city_list?page=1&per_page=10')
print(response.json())

# Сравнение двух городов
response = requests.get('http://127.0.0.1:8000/compare_cities?city1=Москва&city2=Пенза')
print(response.json())
