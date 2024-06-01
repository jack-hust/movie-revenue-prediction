import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# sequel

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
headers = {"User-Agent": user_agent}

def convert_month(month):
    dict = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return dict[month]

def convert_month_to_int(month):
    dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    return dict[month]

def page_search(soup_search, movie_title, month_release, year_release):
    result_element = soup_search.find("div", {"class": "results flex"})

    if result_element is None:
        return 0

    all_div_results = result_element.find_all("div", {"class": "card v4 tight"})

    for result in all_div_results:
        movie_title_element = result.find("h2")
        if movie_title_element.find("span", {"class": "title"}):
            movie_name = movie_title_element.find("span", {"class": "title"}).text.strip("()")
        else:
            movie_name = movie_title_element.text

        if result.find("span", {"class": "release_date"}):
            release_date = result.find("span", {"class": "release_date"}).text
            month = release_date.split(",")[0].strip().split(" ")[0].strip()
            year = release_date.split(",")[1].strip()
        else:
            release_date = ""
            month = ""
            year = ""

        # print(movie_title + " - " + str(month_release) + "/" + str(year_release))
        # print("\n" + movie_name + " - " + month + "/" + year)

        if str(year) == str(year_release) and str(movie_name) == str(movie_title):
            # url
            url = "https://www.themoviedb.org" + result.find("a")["href"]
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                sequel = crawl(soup)
                return sequel
            else:
                print("Failed to fetch data:", response.status_code)
        
    return 0


def crawl(soup):
    section_keywords_element = soup.find("section", {"class": "keywords right_column"})

    if section_keywords_element is None:
        return 0
    
    ul_keywords_element = section_keywords_element.find("ul")

    if ul_keywords_element is None:
        return 0
    
    li_keyword_elements = ul_keywords_element.find_all("li")

    sequel = 0

    for li_keyword in li_keyword_elements:
        if li_keyword.text == "sequel":
            sequel = 1
        
    if sequel == 0:
        print("No Sequel")
    else:
        print("Sequel")

    return sequel

if __name__ == "__main__":
    df = pd.read_csv("../merge_data/critic_merged1.csv")
    movie_name_list = df["movie_name"].tolist()
    month_list = df["month"].tolist()
    # print(month_list)
    # month_list = [convert_month(int(month)) for month in month_list]   

    for i, month in enumerate(month_list):
        if pd.isnull(month):
            month_list[i] = ""
        else:
            month_list[i] = convert_month(int(month))

    year_list = df["year"].tolist()

    for i, year in enumerate(year_list):
        if pd.isnull(year):
            year_list[i] = ""
        else:
            year_list[i] = int(year)

    with open("data/data1.csv", 'w', newline='', encoding='utf-8') as csvfile:
        fields = ['movie_name', 'month', 'year', 'sequel']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for movie_name in movie_name_list:
            print(str(movie_name_list.index(movie_name)) + ". Movie Name: ", movie_name)
            url = "https://www.themoviedb.org/search/movie?query=" + movie_name
            # print(url)
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                sequel = page_search(soup, movie_name, month_list[movie_name_list.index(movie_name)], year_list[movie_name_list.index(movie_name)])
            else:
                print("Failed to fetch data:", response.status_code)

            print("-----------------------------------------------")

            data = {}

            data['movie_name'] = movie_name
            data['month'] = convert_month_to_int(month_list[movie_name_list.index(movie_name)])
            data['year'] = year_list[movie_name_list.index(movie_name)]
            data['sequel'] = sequel

            writer.writerow(data)
