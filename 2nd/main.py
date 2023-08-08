import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests

# Считываем данные из файла
with open('RU.txt', 'r', encoding='utf-8') as f:
    data = f.readlines()

# Создаем словарь с информацией о городах
cities = {}
for line in data:
    row = line.split('\t')
    cities[int(row[0])] = {
        'geonameid': int(row[0]),
        'name': row[1],
        'asciiname': row[2],
        'alternatenames': row[3],
        'latitude': float(row[4]),
        'longitude': float(row[5]),
        'feature_class': row[6],
        'feature_code': row[7],
        'country_code': row[8],
        'cc2': row[9],
        'admin1_code': row[10],
        'admin2_code': row[11],
        'admin3_code': row[12],
        'admin4_code': row[13],
        'population': int(row[14]) if row[14] else 0,
        'elevation': int(row[15]) if row[15] else 0,
        'dem': int(row[16]) if row[16] else 0,
        'timezone': row[17],
        'modification_date': row[18].strip()
    }

# Функция для получения информации о городе по его geonameid
def get_city_by_id(geonameid):
    if geonameid in cities:
        return cities[geonameid]
    else:
        return None

# Функция для получения списка городов
def get_city_list(page=1, per_page=10):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    city_list = list(cities.values())[start_index:end_index]
    return {
        'page': page,
        'per_page': per_page,
        'total_count': len(cities),
        'cities': [
            {
                'geonameid': city['geonameid'],
                'name': city['name'],
                'asciiname': city['asciiname'],
                'country_code': city['country_code'],
                'population': city['population'],
                'timezone': city['timezone']
            } for city in city_list
        ]
    }

# Функция для получения информации о городах и сравнения их
def compare_cities(city1, city2):
    city1_info = None
    city2_info = None
    north_city_info = None
    time_diff = None

    # Получаем список альтернативных имен для каждого города
    for city in cities.values():
        alternate_names = city['alternatenames'].split(',')

        if city1 in alternate_names:
            if not city1_info or city['population'] > city1_info['population']:
                city1_info = city
        if city2 in alternate_names:
            if not city2_info or city['population'] > city2_info['population']:
                city2_info = city

    # Если не нашли оба города, возвращаем None
    if not city1_info or not city2_info:
        return None

    # Определяем, какой из городов расположен севернее
    if city1_info['latitude'] > city2_info['latitude']:
        north_city_info = {
            'name': city1_info['name'],
            'latitude': city1_info['latitude'],
            'longitude': city1_info['longitude']
        }
    else:
        north_city_info = {
            'name': city2_info['name'],
            'latitude': city2_info['latitude'],
            'longitude': city2_info['longitude']
        }

    # Сравниваем временные зоны городов
    if city1_info['timezone'] == city2_info['timezone']:
        time_diff = 0
    else:
        time_diff = abs(int(city1_info['timezone'][8:]) - int(city2_info['timezone'][8:]))

    return {
        'city1': {
            'geonameid': city1_info['geonameid'],
            'name': city1_info['name'],
            'alternatenames': city1_info['alternatenames'],
            'asciiname': city1_info['asciiname'],
            'country_code': city1_info['country_code'],
            'population': city1_info['population'],
            'timezone': city1_info['timezone']
        },
        'city2': {
            'geonameid': city2_info['geonameid'],
            'name': city2_info['name'],
            'alternatenames': city2_info['alternatenames'],
            'asciiname': city2_info['asciiname'],
            'country_code': city2_info['country_code'],
            'population': city2_info['population'],
            'timezone': city2_info['timezone']
        },
        'north_city': north_city_info,
        'time_diff': time_diff
    }

# Класс для обработки HTTP-запросов
class RequestHandler(BaseHTTPRequestHandler):
    
    # Метод для обработки GET-запросов
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        # Получаем информацию о городе по его geonameid
        if parsed_url.path == '/city_by_id':
            geonameid = int(query_params['geonameid'][0])
            city_info = get_city_by_id(geonameid)
            if city_info:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(city_info).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'City not found')
        
        # Получаем список городов
        elif parsed_url.path == '/city_list':
            page = int(query_params['page'][0]) if 'page' in query_params else 1
            per_page = int(query_params['per_page'][0]) if 'per_page' in query_params else 10
            city_list = get_city_list(page, per_page)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(city_list).encode())
        
        # Получаем информацию о городах и сравниваем их
        elif parsed_url.path == '/compare_cities':
            city1 = query_params['city1'][0]
            city2 = query_params['city2'][0]
            comparison_result = compare_cities(city1, city2)
            if comparison_result:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(comparison_result).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'City not found')
        
        # Неподдерживаемый URL
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Page not found')

# Запускаем сервер на порту 8000
server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, RequestHandler)
httpd.serve_forever()




