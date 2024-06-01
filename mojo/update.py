from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from datetime import datetime, timedelta
import csv
import time


DELTA = 5



# === UTILS FUNCTION ===


def month_name_to_number(month_name):
    # Dictionary mapping month names to their corresponding numbers
    month_numbers = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12
    }
    
    month_name = month_name.lower()
    return month_numbers.get(month_name, "Invalid month name")


def get_today_formatted():
    # Get today's date
    today = datetime.today()
    # Format it to 'YYYY-MM-DD'
    formatted_date = today.strftime('%Y-%m-%d')
    return formatted_date


def clean_currency_string(currency_str):
    no_dollar = currency_str.replace('$', '')
    no_comma = no_dollar.replace(',', '')
    return no_comma


def clean_opening_string(opening_str):
    cleaned_str = opening_str.replace('\n', ' ')
    parts = cleaned_str.split(' ')
    currency_str = clean_currency_string(parts[0])
    screens_str = parts[1].replace(',', '')
    return {
        'gross': int(currency_str),
        'screens': int(screens_str)
    }


def clean_release_date_string(input_str):
    # Define a helper function to convert a date string to the desired format
    def format_date(date_str):
        date_obj = datetime.strptime(date_str.strip(), '%b %d, %Y')
        return date_obj.strftime('%Y-%m-%d')
    
    # Case 1: 'Dec 1, 2023'
    if ' - ' not in input_str and '(' not in input_str:
        return format_date(input_str)
    
    # Case 2: 'Dec 1, 2023 - Dec 12, 2023'
    if ' - ' in input_str:
        first_date = input_str.split(' - ')[0]
        return format_date(first_date)
    
    # Case 3: 'Dec 1, 2023 (Dec 12, 2023)'
    if '(' in input_str:
        first_date = input_str.split('(')[0]
        return format_date(first_date)
    
    return None


def clean_running_time_string(running_time_str) -> int:
    if 'hr' in running_time_str and 'min' in running_time_str:
        parts = running_time_str.split(' ')
        hours = int(parts[0])
        minutes = int(parts[2])
        return hours * 60 + minutes
    elif 'hr' in running_time_str:
        return int(running_time_str.split(' ')[0]) * 60
    else:
        return int(running_time_str.split(' ')[0])


def clean_imdb_id_string(imdb_id_str):
    return imdb_id_str.split('/')[4]


def clean_genres_string(genres_str):
    return genres_str.split(' ')


def write_to_csv(movie_data_list, filename='movies_data.csv'):
    # Define the fieldnames for the CSV file
    fieldnames = ['tt_id', 'movie_name', 'domestic_box_office', 'budget', 'month', 'year', 'opening_week', 'screens', 'genres', 'mpaa', 'runtime']
    
    # Write the data to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write each movie's data
        for movie in movie_data_list:
            writer.writerow(movie)


def delta_months_before(delta):
    current_date = datetime.now()
    delta_months_ago = current_date - timedelta(days=30*delta)

    month_name = delta_months_ago.strftime("%B").lower()
    year = delta_months_ago.year

    return month_name, year


def get_movies_list_url(month, year):
    return f'https://boxofficemojo.com/month/{month}/{year}/?grossesOption=totalGrosses'


# === CRAWL FUNCTION ===
def crawl_movies_list_data():
    result_list = []
    month, year = delta_months_before(DELTA)
    url = get_movies_list_url(month, year)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    movies_list_len = driver.find_element(By.XPATH, '//*[@id="table"]/div/table[2]/tbody/tr[last()]/td[1]').text
    movies_list_len = int(movies_list_len)
    for i in range (2, movies_list_len + 2):
        movie_url_href = driver.find_element(By.XPATH, f'//*[@id="table"]/div/table[2]/tbody/tr[{i}]/td[2]/a').get_attribute('href')
        result_list.append(movie_url_href)
        
    driver.quit()
    return result_list


def crawl_movie_data(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    month, year = delta_months_before(DELTA)
    movie = {
        'tt_id': None,
        'movie_name': None,
        'domestic_box_office': None,
        'budget': None,
        'year': year,
        'month': month_name_to_number(month),
        'opening_week': None,
        'screens': None,
        'genres': None,
        'mpaa': None,
        'runtime': None
    }
    TITLE_XPATH = '//*[@id="a-page"]/main/div/div[1]/div[1]/div/div/div[2]/h1'
    IMDB_ID_XPATH = '//*[@id="title-summary-refiner"]/a'
    DOMESTIC_GROSS_XPATH = '//*[@id="a-page"]/main/div/div[3]/div[1]/div/div[1]/span[2]/span'
    PROPERTIES_NUM_XPATH = '//*[@id="a-page"]/main/div/div[3]/div[4]/div'

    title = driver.find_element(By.XPATH, TITLE_XPATH).text
    imdb_id = driver.find_element(By.XPATH, IMDB_ID_XPATH).get_attribute('href')
    domestic_gross = driver.find_element(By.XPATH, DOMESTIC_GROSS_XPATH).text

    properties = driver.find_elements(By.XPATH, PROPERTIES_NUM_XPATH)
    properties_count = len(properties)

    movie['movie_name'] = title
    movie['tt_id'] = clean_imdb_id_string(imdb_id)
    movie['domestic_box_office'] = clean_currency_string(domestic_gross)

    for i in range(2, properties_count - 1):
        property_name = driver.find_element(By.XPATH, f'//*[@id="a-page"]/main/div/div[3]/div[4]/div[{i}]/span[1]').text
        property_value = driver.find_element(By.XPATH, f'//*[@id="a-page"]/main/div/div[3]/div[4]/div[{i}]/span[2]').text
        if 'Running Time' in property_name:
            movie['runtime'] = clean_running_time_string(property_value)
        if 'Opening' in property_name:
            opening_data = clean_opening_string(property_value)
            movie['opening_week'] = opening_data['gross']
            movie['screens'] = opening_data['screens']
        if 'Budget' in property_name:
            movie['budget'] = clean_currency_string(property_value)
        if 'MPAA' in property_name:
            movie['mpaa'] = property_value
        if 'Genres' in property_name:
            movie['genres'] = property_value

    driver.quit()
    return movie


if __name__ == "__main__":

    month, year = delta_months_before(DELTA)
    print(f'Start updater from boxofficemojo.com in {month} ,{year}')

    # Define ANSI escape codes for background colors
    RED_BG = "\033[41m"
    GREEN_BG_BLACK_TEXT_BOLD = "\033[42;30;1m"    
    YELLOW_BG_BOLD = "\033[43;1m"

    RESET = "\033[0m"

    # Define ANSI escape codes for text colors
    WHITE_TEXT = "\033[97m"
    GREEN_TEXT = "\033[92m"
    YELLOW_TEXT = '\033[33m'
    RESET_TEXT = "\033[0m"

    start_time = time.time()
    movies_url_list_start = time.time()

    movies_url_list = crawl_movies_list_data()

    movies_url_list_end = time.time()
    movies_url_list_time_cost = movies_url_list_end - movies_url_list_start
    print(f"{GREEN_BG_BLACK_TEXT_BOLD}CRAWL MOVIES LIST DATA{RESET} Total time cost: {YELLOW_TEXT}{movies_url_list_time_cost:.2f}s{RESET_TEXT}")

    movie_data_list = []
    movies_list_data_time_start = time.time()
    print('Start crawling movie data')
    for movie_url in movies_url_list:
        movie_data_start = time.time()

        movie_data = crawl_movie_data(movie_url)
        movie_data_list.append(movie_data)

        movie_data_end = time.time()
        movie_data_time_cost = movie_data_end - movie_data_start
        print(f"    MOVIE DATA (Cost: {YELLOW_TEXT}{movie_data_time_cost:.2f}s{RESET_TEXT}) Title: {movie_data['movie_name']}")

    movies_list_data_time_end = time.time()
    movies_list_data_time_cost = movies_list_data_time_end - movies_list_data_time_start
    movies_list_data_time_average = movies_list_data_time_cost / len(movies_url_list)
    print(f"{GREEN_BG_BLACK_TEXT_BOLD}CRAWL MOVIE DATA{RESET} Total time cost: {YELLOW_TEXT}{movies_list_data_time_cost:.2f}s{RESET_TEXT}, average time cost: {YELLOW_TEXT}{movies_list_data_time_average:.2f}s{RESET_TEXT}")

    write_to_csv(movie_data_list)
    end_time = time.time()
    time_cost = end_time - start_time
    print(f"\nTotal time cost : {GREEN_TEXT}{time_cost:.2f}s{RESET_TEXT}")
