import csv
import requests
import json
from pprint import pprint
from decouple import config

genres = []
result = []
key = config('KEY')


base_url = 'https://api.themoviedb.org/3/'
url = base_url + f'genre/movie/list?api_key={key}&language=ko-KR'

response = requests.get(url)
response_dict = response.json()
tmps = response_dict["genres"] 

# model : Genre
for tmp in tmps:
    genre_tmp = {}
    genre_tmp['model'] = 'movies.genre'
    genre_tmp['pk'] = tmp["id"]
    genre_tmp['fields'] = {
        'name': tmp["name"]
    }
    result.append(genre_tmp)

with open('genres.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

