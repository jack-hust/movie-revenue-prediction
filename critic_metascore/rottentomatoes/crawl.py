import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111"
headers = {"User-Agent": user_agent, "Accept-Language": "en-US,en;q=0.5"}

# CRAWL:

# critic_vote
# meta_score

def string_to_num(quan_str):
    number_match = re.search(r'\d{1,3}(?:,\d{3})*', quan_str)
    if number_match:
        number = number_match.group().replace(',', '')
        return number
    else:
        return None

def page_search(soup, movie_title, year_release):
    search_results_element = soup.find("search-page-result", {"type": "movie"})

    all_results_elements = search_results_element.find_all("search-page-media-row")

    for results_element in all_results_elements:
        title_element = results_element.find("a", {"data-qa": "info-name"})

        movie_name = title_element.text.strip()
        year = results_element["releaseyear"].strip()

        # print("Movie name:", movie_name)
        # print("Year:", year)

        if str(year) == str(year_release) and str(movie_name) == str(movie_title):
            # print("Found the movie")
            url = title_element["href"]

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup_cv = BeautifulSoup(response.text, "html.parser")
                crawl_rottentomatoes(soup_cv)
            else:
                print("Failed to fetch data:", response.status_code)

            break

        if (all_results_elements.index(results_element) + 1) == len(all_results_elements):
            for results_element_new in all_results_elements:
                year_new = results_element_new["releaseyear"].strip()
                title_element_new = results_element_new.find("a", {"data-qa": "info-name"})

                if str(year_new) == str(year_release):
                    url_new = title_element_new["href"]
                    response_new = requests.get(url_new, headers=headers)

                    if response_new.status_code == 200:
                        soup_new = BeautifulSoup(response_new.text, "html.parser")
                        crawl_rottentomatoes(soup_new)
                    else:
                        print("Failed to fetch data:", response_new.status_code)

                    break

def crawl_rottentomatoes(soup):
    # print("Crawling Rottentomatoes")
    div_score_element = soup.find("div", {"class": "media-scorecard"})

    critic_vote = div_score_element.find("rt-link", {"slot": "criticsReviews"}).text.strip()
    meta_score = div_score_element.find("rt-button", {"slot": "criticsScore"}).text.strip().replace("%", "")
    

    print("Critic vote:", string_to_num(critic_vote))
    print("Meta score:", string_to_num(meta_score))
                
if __name__ == "__main__":
    df = pd.read_csv("../mojo/data/test1.csv")
    movie_name_list = df["movie_name"].tolist()
    year_list = df["year"].tolist()

    for movie_name in movie_name_list:
        if movie_name:
            print("Movie name:", movie_name)
            url = "https://www.rottentomatoes.com/search?search=" + movie_name + "/"
            # print(url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                page_search(soup, movie_name, year_list[movie_name_list.index(movie_name)])
                # break
            else:
                print("Failed to fetch data:", response.status_code)

            print("--------------------------------------------")
