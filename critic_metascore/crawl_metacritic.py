import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111"
headers = {"User-Agent": user_agent, "Accept-Language": "en-US,en;q=0.5"}

# CRAWL: 

# critic_vote
# meta_score

def edit_movie_name(movie_name):
    movie_name = re.sub(r'[^a-zA-Z0-9]+', '-', movie_name).strip('-')
    return movie_name.lower()

def page_search_metacritic(soup, movie_title, year_release):
    all_div_elements = soup.find_all("div", {"class": "g-grid-container u-grid-columns"})
    for div_element in all_div_elements:
        p_movie_name_element = div_element.find("p", {"class": "g-text-medium-fluid g-text-bold g-outer-spacing-bottom-small u-text-overflow-ellipsis"})
        movie_name = p_movie_name_element.text.strip()

        div_year_element = div_element.find("div", {"class": "u-flexbox u-flexbox-alignCenter u-flexbox-nowrap g-gap-medium g-text-xxxsmall"})

        if len(div_year_element.find_all("span")) < 2:
            continue

        gen = div_year_element.find_all("span")[0].text.strip()
        year = div_year_element.find_all("span")[1].text.strip()

        if gen == "movie" and str(year) == str(year_release):
            # print(movie_name)
            # print(gen)
            # print(year)
            # print(year_release)
            
            # print(movie_name)
            # print(movie_title)

            link_to_movie_element = div_element.find("a", recursive=False)
            link_to_movie = link_to_movie_element["href"]

            url_to_movie = "https://www.metacritic.com" + link_to_movie
            # print(url_to_movie)

            response = requests.get(url_to_movie, headers=headers)

            if response.status_code == 200:
                soup_new = BeautifulSoup(response.text, "html.parser")
                # crawl_metacritic(soup_new)
                critic_vote, meta_score = crawl_metacritic(soup_new)
                return critic_vote, meta_score
            else:
                print("Failed to fetch data:", response.status_code)
            break

    return "", ""

def string_to_num(quan_str):
    number_match = re.search(r'\d{1,3}(?:,\d{3})*', quan_str)
    if number_match:
        number = number_match.group().replace(',', '')
        return number
    else:
        return None

def crawl_metacritic(soup):
    span_quan_elements = soup.find_all("span", {"class": "c-productScoreInfo_reviewsTotal u-block"})
    div_score_elements = soup.find_all("div", {"class": "c-productScoreInfo_scoreNumber u-float-right"})

    if not span_quan_elements:
        return "", ""

    critic_vote = string_to_num(span_quan_elements[0].text)
    meta_score = div_score_elements[0].text.strip()

    # print("Critic vote: " + critic_vote)
    # print("Meta score: " + meta_score)

    return critic_vote, meta_score
   
                
if __name__ == "__main__":
    df = pd.read_csv("../mojo/data/test1.csv")
    movie_name_list = df["movie_name"].tolist()
    year_list = df["year"].tolist()


    for movie_name in movie_name_list:
        if movie_name:
            print(str(movie_name_list.index(movie_name) + 2) + ". " + movie_name)
            url = "https://www.metacritic.com/movie/" + edit_movie_name(movie_name) + "/"
            # print(url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                crawl_metacritic(soup)
            else:
                url_new = "https://www.metacritic.com/search/" + edit_movie_name(movie_name) + "/?page=1&category=2"
                # print(url_new)
                
                response_new = requests.get(url_new, headers=headers)
                
                if response_new.status_code == 200:
                    # print("OK NEW")
                    soup = BeautifulSoup(response_new.text, "html.parser")
                    page_search_metacritic(soup, movie_name, year_list[movie_name_list.index(movie_name)])
                else:
                    print("Failed to fetch data:", response_new.status_code)
                    continue

            print("\n-------------------------------")
