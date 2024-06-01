from crawl_rottentomatoes import *
from crawl_metacritic import *
import csv

def score(critic_vote_metacritic, meta_score_metacritic, critic_vote_rotten, meta_score_rotten):
    # print("Critic vote metacritic:", critic_vote_metacritic)
    # print("Meta score metacritic:", meta_score_metacritic)
    # print("Critic vote rotten:", critic_vote_rotten)
    # print("Meta score rotten:", meta_score_rotten)

    metacritic_sum = critic_vote_metacritic*meta_score_metacritic
    rotten_sum = critic_vote_rotten*meta_score_rotten

    critic_vote_sum = critic_vote_metacritic + critic_vote_rotten

    return critic_vote_sum, "{:.2f}".format((metacritic_sum+rotten_sum)/critic_vote_sum)

if __name__ == "__main__":
    df = pd.read_csv("../merge_data/imdb_merged8.csv")
    movie_name_list = df["movie_name"].tolist()
    month_list = df["month"].tolist()
    year_list = df["year"].tolist()

    for i, month in enumerate(month_list):
        if pd.isnull(month):
            month_list[i] = ""
        else:
            month_list[i] = int(month)

    for i, year in enumerate(year_list):
        if pd.isnull(year):
            year_list[i] = ""
        else:
            year_list[i] = int(year)

    with open("data/data8.csv", 'w', newline='', encoding='utf-8') as csvfile:
        fields = ['movie_name','month','year','critic_vote_metacritic', 'meta_score_metacritic', 'critic_vote_rotten', 'meta_score_rotten', 'critic_vote', 'meta_score']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for movie_name in movie_name_list:
            data = {}

            if movie_name:
                print(str(movie_name_list.index(movie_name) + 1) + ". " + movie_name)

                # Metacritic
                url = "https://www.metacritic.com/search/" + edit_movie_name(movie_name) + "/?page=1&category=2"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    critic_vote_metacritic, meta_score_metacritic = page_search_metacritic(soup, movie_name, year_list[movie_name_list.index(movie_name)])
                    critic_vote_metacritic = string_to_num(critic_vote_metacritic)
                    meta_score_metacritic = string_to_num(meta_score_metacritic)

                    print("Critic vote metacritic:", critic_vote_metacritic)
                    print("Meta score metacritic:", meta_score_metacritic)
                else:
                    print("Failed to fetch data:", response.status_code)
                    continue

                # Rottentomatoes
                url = "https://www.rottentomatoes.com/search?search=" + movie_name + "/"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    critic_vote_rotten, meta_score_rotten = page_search_rottentomatoes(soup, movie_name, year_list[movie_name_list.index(movie_name)])
                    critic_vote_rotten = string_to_num(critic_vote_rotten)
                    meta_score_rotten = string_to_num(meta_score_rotten)
                    print("Critic vote rotten:", critic_vote_rotten)
                    print("Meta score rotten:", meta_score_rotten)
                else:
                    print("Failed to fetch data:", response.status_code)

                print("--------------------------------------------")

                if critic_vote_metacritic and critic_vote_rotten:
                    critic_vote, meta_score = score(int(critic_vote_metacritic), int(meta_score_metacritic), int(critic_vote_rotten), int(meta_score_rotten))
                elif critic_vote_metacritic:
                    critic_vote, meta_score = score(int(critic_vote_metacritic), int(meta_score_metacritic), 0, 0)
                elif critic_vote_rotten:
                    critic_vote, meta_score = score(0, 0, int(critic_vote_rotten), int(meta_score_rotten))
                else:
                    critic_vote, meta_score = 0, 0

                data['movie_name'] = movie_name
                data['month'] = month_list[movie_name_list.index(movie_name)]
                data['year'] = year_list[movie_name_list.index(movie_name)]
                data['critic_vote_metacritic'] = critic_vote_metacritic
                data['meta_score_metacritic'] = meta_score_metacritic
                data['critic_vote_rotten'] = critic_vote_rotten
                data['meta_score_rotten'] = meta_score_rotten
                data['critic_vote'] = critic_vote
                data['meta_score'] = meta_score

                writer.writerow(data)

