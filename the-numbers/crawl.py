import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
driver = webdriver.Chrome()
driver.maximize_window()

def month_name_to_num(month_name):
    month_names_to_numbers = {
        "January": "1",
        "February": "2",
        "March": "3",
        "April": "4",
        "May": "5",
        "June": "6",
        "July": "7",
        "August": "8",
        "September": "9",
        "October": "10",
        "November": "11",
        "December": "12"
    }

    month = month_names_to_numbers.get(month_name)
    return month

# movie_name
# month
# year
# budget
# runtime
# mpaa
# screens
# opening_week
# domestic_box_office
# country

with open("link/link_the-numbers.txt", "r") as file:
    with open("movie.csv", 'a', newline='', encoding='utf-8') as csvfile:
        fields = ['movie_name', 'month', 'year', 'budget', 'runtime', 'mpaa', 'screens', 'opening_week', 'domestic_box_office', 'country']
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()

        for link_movie in file:
            data = {}

            driver.get(link_movie)
            time.sleep(0.5)

            movie_title_element = driver.find_element(By.XPATH, "//*[@id=\"main\"]/h1")
            movie_title = movie_title_element.text

            split_string = movie_title.split(" (")

            # Crawl movie_name and year, month
            movie_name = split_string[0].replace(",", "")
            year = int(movie_title.split('(')[-1].strip(')'))
            print("Movie: " + movie_name + " - " + str(year))

            if driver.find_elements(By.XPATH, "//*[contains(text(), 'International Releases')]") and driver.find_elements(By.XPATH, "//*[contains(text(), 'Domestic Releases:')]"):
                all_domestic_release_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Domestic Releases:')]")
                for domestic_release_element in all_domestic_release_element:
                    if "Domestic Releases:" in domestic_release_element.text:
                        parent_domestic_release_element = domestic_release_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_domestic_release_element.find_elements(By.TAG_NAME, "td")
                        td_content = td_elements[1].text
                        release_date = td_content.split("\n")[0].split("(")[0]
                        # year
                        year = int(release_date.split()[-1])

                        month_name = release_date.split()[0]
                        # month
                        month = int(month_name_to_num(month_name))

                        print("Month/Year: " + str(month) + "/" + str(year))
                        break
            elif driver.find_elements(By.XPATH, "//*[contains(text(), 'International Releases')]"):
                all_international_release_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'International Releases')]")
                for international_release_element in all_international_release_element:
                    if "International Releases" in international_release_element.text:
                        parent_international_release_element = international_release_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_international_release_element.find_elements(By.TAG_NAME, "td")
                        td_content = td_elements[1].text
                        release_date = td_content.split("\n")[0].split("(")[0]
                        # year
                        year = int(release_date.split()[-1])

                        month_name = release_date.split()[0]
                        # month
                        month = int(month_name_to_num(month_name))

                        print("Month/Year: " + str(month) + "/" + str(year))
                        break
            elif driver.find_elements(By.XPATH, "//*[contains(text(), 'Domestic Releases:')]"):
                all_domestic_release_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Domestic Releases:')]")
                for domestic_release_element in all_domestic_release_element:
                    if "Domestic Releases:" in domestic_release_element.text:
                        parent_domestic_release_element = domestic_release_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_domestic_release_element.find_elements(By.TAG_NAME, "td")
                        td_content = td_elements[1].text
                        release_date = td_content.split("\n")[0].split("(")[0]
                        # year
                        year = int(release_date.split()[-1])

                        month_name = release_date.split()[0]
                        # month
                        month = int(month_name_to_num(month_name))

                        print("Month/Year: " + str(month) + "/" + str(year))
                        break
            else:
                month = None
                print("No Release")

            # Crawl budget
            if driver.find_elements(By.XPATH, "//*[contains(text(), 'Budget:')]"):
                all_prod_budget_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Budget:')]")
                for prod_budget_element in all_prod_budget_element:
                    if "Production Budget" in prod_budget_element.text:
                        parent_prod_budget_element = prod_budget_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_prod_budget_element.find_elements(By.TAG_NAME, "td")
                        budget_content = td_elements[1].text
                        budget = budget_content.split(" (")[0]
                        budget = int(budget.replace(",", "").replace("$", ""))
                        print("Budget: " + "$" + str(budget))
                        break
            else:
                budget = None
                print("No Budget")
            
            # Crawl runtime
            if driver.find_elements(By.XPATH, "//*[contains(text(), 'Time:')]"):
                all_runtime_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Time:')]")
                for runtime_element in all_runtime_element:
                    if "Time:" in runtime_element.text:
                        parent_runtime_element = runtime_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_runtime_element.find_elements(By.TAG_NAME, "td")
                        runtime_content = td_elements[1].text
                        runtime = int(runtime_content.split(" minutes")[0])
                        print("Runtime: " + str(runtime) + " minutes")
                        break
            else:
                runtime = None
                print("No Runtime")

            # Crawl mpaa
            if driver.find_elements(By.XPATH, "//*[contains(text(), 'Rating:')]"):
                all_mpaa_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Rating:')]")
                for mpaa_element in all_mpaa_element:
                    if "Rating:" in mpaa_element.text:
                        parent_mpaa_element = mpaa_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_mpaa_element.find_elements(By.TAG_NAME, "td")
                        mpaa_content = td_elements[1].text
                        mpaa = mpaa_content.split(" ")[0]
                        print("MPAA: " + mpaa)
                        break
            else:
                mpaa = None
                print("No MPAA")
            
            # Crawl screens
            if driver.find_elements(By.XPATH, "//*[contains(text(), 'counts:')]"):
                all_screens_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'counts:')]")
                for screens_element in all_screens_element:
                    if "counts:" in screens_element.text:
                        parent_screens_element = screens_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_screens_element.find_elements(By.TAG_NAME, "td")
                        screens_content = td_elements[1].text
                        screens = screens_content.split(" ")[0]
                        screens = int(screens.replace(",", ""))
                        print("Screens: " + str(screens))
                        break
            else:
                screens = None
                print("No Screens")

            # Crawl opening_week
            if driver.find_elements(By.XPATH, "//*[contains(text(), 'Weekend:')]"):
                all_opening_week_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Weekend:')]")
                for opening_week_element in all_opening_week_element:
                    if "Weekend:" in opening_week_element.text:
                        parent_opening_week_element = opening_week_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_opening_week_element.find_elements(By.TAG_NAME, "td")
                        opening_week_content = td_elements[1].text
                        opening_week = opening_week_content.split(" (")[0]
                        opening_week = int(opening_week.replace(",", "").replace("$", ""))
                        print("Opening Weekend: " + "$" + str(opening_week))
                        break
            else:
                opening_week = None
                print("No Opening Weekend")

            # Crawl domestic_box_office
            if driver.find_elements(By.XPATH, "//b[contains(text(), 'Domestic Box Office')]"):
                all_domestic_box_office_element = driver.find_elements(By.XPATH, "//b[contains(text(), 'Domestic Box Office')]")
                for domestic_box_office_element in all_domestic_box_office_element:
                    if "Domestic Box Office" in domestic_box_office_element.text:
                        parent_domestic_box_office_element = domestic_box_office_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_domestic_box_office_element.find_elements(By.TAG_NAME, "td")
                        domestic_box_office_content = td_elements[1].text
                        if "n/a" in domestic_box_office_content:
                            domestic_box_office = None
                            print("No Domestic Box Office")
                        else:
                            domestic_box_office = domestic_box_office_content.split(" (")[0]
                            domestic_box_office = int(domestic_box_office.replace(",", "").replace("$", ""))
                            print("Domestic Box Office: " + "$" + str(domestic_box_office))
                        break
            else:
                domestic_box_office = None
                print("No Domestic Box Office")

            # Crawl country
            if driver.find_elements(By.XPATH, "//*[contains(text(), 'Countries:')]"):
                all_country_element = driver.find_elements(By.XPATH, "//*[contains(text(), 'Countries:')]")
                for country_element in all_country_element:
                    if "Countries:" in country_element.text:
                        parent_country_element = country_element.find_element(By.XPATH, "./..").find_element(By.XPATH, "./..")
                        td_elements = parent_country_element.find_elements(By.TAG_NAME, "td")
                        country_content = td_elements[1].text
                        country = country_content.split("\n")[0]
                        print("Country: " + country)
                        break
            else:
                country = None
                print("No Country")        
            
            data['movie_name'] = movie_name
            data['month'] = month
            data['year'] = year
            data['budget'] = budget
            data['runtime'] = runtime
            data['mpaa'] = mpaa
            data['screens'] = screens
            data['opening_week'] = opening_week
            data['domestic_box_office'] = domestic_box_office
            data['country'] = country

            writer.writerow(data)

            print("\n")


        

print("\n\n")
print("********************************************")
print("--------------------XONG--------------------")
print("********************************************")
