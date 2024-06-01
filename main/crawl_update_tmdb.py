import requests
import pandas as pd

def crawl_budget(tt_id):
    url = 'https://api.themoviedb.org/3/find/' + tt_id
    headers_detail = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YmJiNjQ1NTZiMjg0ZDA1Njc2OGVjMzdmZmU0ZWM3NyIsInN1YiI6IjY2MDU3MGE3OTU2NjU4MDE0ODdkZTljOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mXbYtQYdYFHQSQxEUTiHIvUsRhtq7R-zXZH2oPqu38o',
        'accept': 'application/json'
    }
    params_detail = {
        'external_source': 'imdb_id'
    }

    response_detail = requests.get(url, headers=headers_detail, params=params_detail)
    detail = response_detail.json()

    if len(detail['movie_results']) > 0:
        url_budget = 'https://api.themoviedb.org/3/movie/' + str(detail['movie_results'][0]['id'])
        headers_budget = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5YmJiNjQ1NTZiMjg0ZDA1Njc2OGVjMzdmZmU0ZWM3NyIsInN1YiI6IjY2MDU3MGE3OTU2NjU4MDE0ODdkZTljOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mXbYtQYdYFHQSQxEUTiHIvUsRhtq7R-zXZH2oPqu38o',
            'accept': 'application/json'
        }
        params = {
            'language': 'en-US'
        }

        response = requests.get(url_budget, headers=headers_budget, params=params)
        data = response.json()

        if data['budget']:
            return data['budget']
        else:
            return None
    else:
        return None

def main_tmdb():
    print('====================================================================================')
    print('Crawl TMDb...')
    path_file = './merge_data/movies_data.csv'
    df = pd.read_csv(path_file)
    url_title_list = df["tt_id"].tolist()
    budget_list = df["budget"].tolist()
    
    for idx, tt_id in enumerate(url_title_list):
        if pd.isnull(budget_list[idx]):
            budget = crawl_budget(tt_id)
            if budget is not None:
                df.at[idx, 'budget'] = budget
                df.to_csv(path_file, index=False)

    if 'user_vote' not in df.columns:
        df['user_vote'] = pd.NA
    if 'ratings' not in df.columns:
        df['ratings'] = pd.NA
    if 'country' not in df.columns:
        df['country'] = pd.NA

    df = df.dropna(subset=['tt_id', 'movie_name', 'domestic_box_office', 'budget', 'month', 'year', 'opening_week', 'screens', 'genres', 'runtime', 'mpaa'])
    
    df.to_csv(path_file, index=False)
    

