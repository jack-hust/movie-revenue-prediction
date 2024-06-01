from bs4 import BeautifulSoup
import urllib.request
import pprint as pp

class Movie:
    def __init__(self, url_title, title, month, year, budget, runtime, genres, mpaa, screens, opening, domestic, international, worldwide):
        self.url_title = url_title
        self.title = title
        self.month = month
        self.year = year
        self.budget = budget
        self.runtime = runtime
        self.genres = genres
        self.mpaa = mpaa
        self.screens = screens
        self.opening = opening
        self.domestic = domestic
        self.international = international
        self.worldwide = worldwide

def convert_to_min(runtime):
    if "hr" in runtime:
        runtime_split = runtime.split("hr")
        if len(runtime_split[1]) == 0:
            hours = int(runtime_split[0].strip())
            return hours * 60
        else:
            hours = int(runtime_split[0].strip())
            minutes = int(runtime_split[1].replace("min", "").strip())
            return hours * 60 + minutes
    else:
        return int(runtime.split()[0])
    
def convert_month(month):
    dict = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12
    }
    return dict[month]


def get_info_table(info_table):
    budget = None
    release_month = None
    release_year = None
    mpaa = None
    runtime = None
    genres = None
    screens = None
    opening = None

    rows = info_table.find_all('div', {'class': "a-section a-spacing-none"})
    for row in rows:
        if "Budget" in row.text:
            budget = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")

        elif "Release Date" in row.text:
            release_date = [row.text for row in row.find_all('a')]

            if "-" in release_date[0]:
                release_date_one = release_date[0].split("-")
                release_month = release_date_one[1]
                release_year = release_date_one[2]
            elif "," in release_date[0]:
                release_date_one = release_date[0].split(",")
                release_year = release_date_one[1].strip()
                release_month = release_date_one[0].split(" ")[0].strip()
                release_month = convert_month(release_month)
            else:
                release_year = release_date[0].strip()

        elif "MPAA" in row.text:
            mpaa = row.find_all('span')[1].text.split()[0]

        elif "Running Time" in row.text:
            runtime = row.find_all('span')[1].text
            runtime = convert_to_min(runtime)

        elif "Genres" in row.text:
            list_genres = row.find_all('span')[1].text.split()
            genres = " ".join(list_genres)

        elif "Widest Release" in row.text:
            screens = row.find_all('span')[1].text
            screens = screens.split()[0]
            screens = screens.replace(".", "").replace(",", "")
        elif "Opening" in row.text:
            opening = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")

    return budget, release_month, release_year, mpaa, runtime, genres, screens, opening


def get_grosses(grosses):
    domestic = None
    international = None
    worldwide = None

    rows = grosses.find_all('div', {'class': "a-section a-spacing-none"})
    for row in rows:
        if "Domestic" in row.text and "–" not in row.text:
            domestic = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")
        elif "International" in row.text and "–" not in row.text:
            international = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")
        elif "Worldwide" in row.text and "–" not in row.text:
            worldwide = row.find('span', {'class': "money"}).text.replace("$", "").replace(",", "")

    return domestic, international, worldwide
    
def get_url_title(url_title):
    # /title/tt0236493/?ref_=bo_rl_ti
    return url_title.split('/')[-2]

def crawl(release_id):
    url = f"https://www.boxofficemojo.com/release/{release_id}/"
    url_title = None

    response = urllib.request.urlopen(url)
    soup = BeautifulSoup(response, 'html.parser')
    
    try:
        url_title_element = soup.find(string=lambda text: 'Title Summary' in text).parent
        url_title = get_url_title(url_title_element.parent["href"])
    except:
        url_title = ""

    # print(url_title)

    title = soup.find('h1', {'class': "a-size-extra-large"}).text.replace(",", "")
    grosses = soup.find('div', {'class': "a-section a-spacing-none mojo-performance-summary-table"})
    info_table = soup.find('div', {'class': "a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile"})

    budget, release_month, release_year, mpaa, runtime, genres, screens, opening = get_info_table(info_table)

    domestic, international, worldwide = get_grosses(grosses)

    return Movie(url_title,title, release_month, release_year, budget, runtime, genres, mpaa, screens, opening,domestic, international, worldwide)
    
def main():
    with open("link/link_quan.txt", "r") as f:
        out = open("data/data_quan.csv", "w")
        out.write("tt_id,rl_id,movie_name,month,year,budget,runtime,genres,mpaa,screens,opening_week,domestic_box_office\n")
        index = 1
        for line in f:
            release_id = line.strip()
            movie = crawl(release_id)
            print(str(index) + ". " + movie.title)
            out.write(f"{movie.url_title},{release_id},{movie.title},{movie.month},{movie.year},{movie.budget},{movie.runtime},{movie.genres},{movie.mpaa},{movie.screens},{movie.opening},{movie.domestic}\n")
            index += 1

if __name__ == "__main__":
    main()
