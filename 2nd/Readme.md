import requests

# Получение информации о городе по его geonameid
response = requests.get('http://127.0.0.1:8000/city_by_id?geonameid=" Your ID "')\
http://127.0.0.1:8000/city_by_id?geonameid=524901

# Получение списка городов
response = requests.get('http://127.0.0.1:8000/city_list?page="start"&per_page="end"')\
http://127.0.0.1:8000/city_list?page=1&per_page=10

# Сравнение двух городов
response = requests.get('http://127.0.0.1:8000/compare_cities?city1="RU_name1"&city2="RU_name2"')\
http://127.0.0.1:8000/compare_cities?city1=Москва&city2=Воркута