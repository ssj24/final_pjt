import csv
import requests
import json
from pprint import pprint
from decouple import config


movies = []

with open('movies.json', encoding='utf-8') as f:
    json_data = json.load(f)
    # pprint(json_data)
    
    for row in json_data:
        # print(row["pk"])
        # print(type(row["pk"]))
        movies.append(row["pk"])

# print(len(movies))
# print(movies)

result = []
key = config('KEY')

cnt = 0
for i in range(len(movies)):
# for i in range(1):
    movie_id = movies[i]
    base_url = 'https://api.themoviedb.org/3/movie/'
    url = base_url + f'{movie_id}/credits?api_key={key}'

    response = requests.get(url)
    response_dict = response.json()
    tmps = response_dict["cast"]
    tmp_cnt = 0

    for tmp in tmps:
        if tmp_cnt == 6:
            break

        cast_tmp = {}
        cast_tmp['model'] = 'movies.cast'
        cast_tmp['pk'] = cnt

        movie = movies[i]
        character = tmp["character"]
        name = tmp["name"]

        if tmp["profile_path"]:
            profile_path = tmp["profile_path"]
        else:
            continue

        cast_tmp['fields'] = {
            'movie': movie,
            'character': character,
            'name': name,
            'profile_path': profile_path,
        }
        
        result.append(cast_tmp)
        cnt += 1
        tmp_cnt += 1

with open('casts.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
