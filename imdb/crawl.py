import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv



user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111"
headers = {"User-Agent": user_agent, "Accept-Language": "en-US,en;q=0.5"}

# CRAWL:

# ratings
# user_vote
# country
# genres

check_search_imdb_slenium = False
check_search_imdb_requests = False

genres = []
country = []
ratings = []
user_vote = []

def loop():
    driver_check = webdriver.Chrome()
    try:
        if driver_check.find_element(By.CSS_SELECTOR, "li[data-testid='storyline-genres']"):
            return
    except StaleElementReferenceException:
        pass
    
    time.sleep(0.5)
    loop(driver_check)

# Crawl country IMDB
def crawl_imdb_request(soup):
    user_vote_and_rating_element = soup.find("div", {"data-testid": "hero-rating-bar__aggregate-rating"})

    # ratings
    rate = user_vote_and_rating_element.find("div", {"class": "sc-bde20123-2 cdQqzc"}).text.split("/")[0].strip()

    # user_vote
    vote = user_vote_and_rating_element.find("div", {"class": "sc-bde20123-3 gPVQxL"}).text.replace("K", "000").replace("M", "000000").replace(".", "")

    ratings.append(rate)
    user_vote.append(vote)
    # print("Rating: " + ratings)
    # print("User vote: " + user_vote)

    li_country_element = soup.find("li",{'data-testid': "title-details-origin"})

    if li_country_element != None:
        ul_element = li_country_element.find("ul")

        all_country_li_element = ul_element.find_all("li")

        # country
        for country_li in all_country_li_element:
            country.append(country_li.text)

    # if len(country) > 0:
    #     print("Country: " + ' '.join(country))

# Crawl genres and country IMDB
def crawl_imdb_selenium(url):
    # genres = []
    # country = []

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 5000);")
    time.sleep(2)

    tag_storyline_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='storyline-header']").find_element(By.XPATH, "./..")
    driver.execute_script("arguments[0].scrollIntoView();", tag_storyline_element)
    
    # loop()

    li_all_genres_element = WebDriverWait(driver,100).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "li[data-testid='storyline-genres']")))
    
    if li_all_genres_element:
        ul_genres_element = li_all_genres_element.find_element(By.TAG_NAME, "ul")
        li_genres_elements = ul_genres_element.find_elements(By.TAG_NAME, "li")

        for li_genres in li_genres_elements:
            genres.append(li_genres.text)

    tag_detail_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='title-details-header']").find_element(By.XPATH, "./..")

    if tag_detail_element.find_element(By.CSS_SELECTOR, "li[data-testid='title-details-origin']"):
        li_country_element = tag_detail_element.find_element(By.CSS_SELECTOR, "li[data-testid='title-details-origin']")
        ul_country_element = li_country_element.find_element(By.TAG_NAME, "ul")
        li_country_elements = ul_country_element.find_elements(By.TAG_NAME, "li")

        for li_country in li_country_elements:
            country.append(li_country.text)

    user_vote_and_rating_element = driver.find_element(By.CSS_SELECTOR, "div[data-testid='hero-rating-bar__aggregate-rating']")

    # ratings
    rate = user_vote_and_rating_element.find_element(By.CSS_SELECTOR, "div[class='sc-bde20123-2 cdQqzc']").text.split("/")[0].strip()

    # user_vote
    vote = user_vote_and_rating_element.find_element(By.CSS_SELECTOR, "div[class='sc-bde20123-3 gPVQxL']").text.replace("K", "000").replace("M", "000000").replace(".", "")

    ratings.append(rate)
    user_vote.append(vote)
    
    # if len(genres) > 0:
    #     print("Genres: " + ' '.join(genres))
    # if len(country) > 0:
    #     print("Country: " + ' '.join(country))
    
    driver.close()
 
# Search movie in imdb
def page_search_imdb(soup_search, movie_title, year_release):
    year_release = int(year_release)
    result_element = soup_search.find("ul", {"class": "ipc-metadata-list--base"})

    if result_element != None:
        all_li_results = result_element.find_all("li", recursive=False)

        for result in all_li_results:
            # print(result.text)
            if result.find("a", {"class": "ipc-metadata-list-summary-item__t"}):
                movie_title_element = result.find("a", {"class": "ipc-metadata-list-summary-item__t"})
            else:
                continue
            
            movie_name = movie_title_element.text

            if result.find("span", {"class": "ipc-metadata-list-summary-item__li"}):
                year = result.find("span", {"class": "ipc-metadata-list-summary-item__li"}).text
            else:
                continue

            # print("\n" + movie_name + " - "  + year)
            # print(movie_title + " - " + str(year_release))

            if str(year) == str(year_release) and str(movie_name) == str(movie_title):
                # url
                url = "https://www.imdb.com" + movie_title_element["href"]
                if check_search_imdb_requests:
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        crawl_imdb_request(soup)
                    else:
                        print("Failed to fetch data:", response.status_code)
                elif check_search_imdb_slenium:
                    crawl_imdb_selenium(url)

                break

def search_imdb(movie_name, year_release):
    # print("\n" + str(movie_name) + " - " + str(year_release))
    url = "https://www.imdb.com/find/?q=" + movie_name + "&s=tt&ttype=ft&ref_=fn_ft"
    response = requests.get(url, headers=headers)
    # print(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(sosup)
        page_search_imdb(soup, movie_name, year_release)
    else:
        print("Failed to fetch data:", response.status_code)

if __name__ == "__main__":
    df = pd.read_csv("../merge_data/long.csv")
    url_title_list = df["tt_id"].tolist()
    movie_name_list = df["movie_name"].tolist()
    month_list = df["month"].tolist()
    year_list = df["year"].tolist()

    genres_list = df["genres"].tolist()
    country_list = df["country"].tolist()

    # print(movie_name_list)
    # print(url_title_list)

    with open("data/data_long_new.csv", 'w', newline='', encoding='utf-8') as csvfile:
        fields = ['movie_name', 'month', 'year', 'ratings', 'user_vote', 'genres', 'country']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for movie_name in movie_name_list:
            data = {}
            print(str(movie_name_list.index(movie_name)) + ". Movie: " + movie_name_list[movie_name_list.index(movie_name)])

           
            if pd.isnull(country_list[movie_name_list.index(movie_name)]) and pd.isnull(genres_list[movie_name_list.index(movie_name)]):
                check_search_imdb_slenium = True
            elif pd.isnull(country_list[movie_name_list.index(movie_name)]):
                check_search_imdb_requests = True
            elif pd.isnull(genres_list[movie_name_list.index(movie_name)]):
                check_search_imdb_slenium = True

            if pd.isnull(url_title_list[movie_name_list.index(movie_name)]):
                search_imdb(movie_name_list[movie_name_list.index(movie_name)], year_list[movie_name_list.index(movie_name)])
            else:
                url = "https://www.imdb.com/title/" + url_title_list[movie_name_list.index(movie_name)] + "/"
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    crawl_imdb_request(soup)
                else:
                    print("Failed to fetch data:", response.status_code)

            check_search_imdb_slenium = False
            check_search_imdb_requests = False

            data['movie_name'] = movie_name
            data['month'] = month_list[movie_name_list.index(movie_name)]
            data['year'] = year_list[movie_name_list.index(movie_name)]

            if not pd.isnull(country_list[movie_name_list.index(movie_name)]):
                country = []

            if not pd.isnull(genres_list[movie_name_list.index(movie_name)]):
                genres = []

            if len(ratings) > 0:
                print("Rating: " + ratings[0])
                data['ratings'] = ratings[0]
            if len(user_vote) > 0:
                print("User vote: " + user_vote[0])
                data['user_vote'] = user_vote[0]
            if len(genres) > 0:
                print("Genres: " + ' '.join(genres))
                data['genres'] = ' '.join(genres)
            if len(country) > 0:
                print("Country: " + ' '.join(country))
                data['country'] = ' '.join(country)

            ratings = []
            user_vote = []
            genres = []
            country = []

            writer.writerow(data)

            print("-----------------------------------------------")
