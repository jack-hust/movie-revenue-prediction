import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
driver = webdriver.Chrome()
driver.maximize_window()

year = 2001

# movie_name
# year
# month
# budget
# runtime
# mpaa
# opening_week
# screens
# genres
# gross_revenue

with open("link_movie.txt", "a") as file:
    while year < 2024:
        if year == 2020 or year == 2021 or year == 2022:
            continue

        page_main_url = "https://www.boxofficemojo.com/season/spring/" + str(year)
        driver.get(page_main_url)

        all_tr_from_table_elements = driver.find_elements(By.XPATH, "//*[@id=\"table\"]/div/table[2]/tbody/tr")

        index = 1
        for all_tr_from_table_element in all_tr_from_table_elements:
            if index == 1:
                index += 1
                continue
            tag_a_element = all_tr_from_table_element.find_elements(By.TAG_NAME, "a")

            movie_url = tag_a_element[0].get_attribute("href")
            
            movie_id = movie_url.split("/")[-2]

            file.write(movie_id + "\n")

        page_main_url = "https://www.boxofficemojo.com/season/summer/" + str(year)
        driver.get(page_main_url)

        all_tr_from_table_elements = driver.find_elements(By.XPATH, "//*[@id=\"table\"]/div/table[2]/tbody/tr")

        index = 1
        for all_tr_from_table_element in all_tr_from_table_elements:
            if index == 1:
                index += 1
                continue
            tag_a_element = all_tr_from_table_element.find_elements(By.TAG_NAME, "a")

            movie_url = tag_a_element[0].get_attribute("href")
            
            movie_id = movie_url.split("/")[-2]

            file.write(movie_id + "\n")

        page_main_url = "https://www.boxofficemojo.com/season/fall/" + str(year)
        driver.get(page_main_url)

        all_tr_from_table_elements = driver.find_elements(By.XPATH, "//*[@id=\"table\"]/div/table[2]/tbody/tr")

        index = 1
        for all_tr_from_table_element in all_tr_from_table_elements:
            if index == 1:
                index += 1
                continue
            tag_a_element = all_tr_from_table_element.find_elements(By.TAG_NAME, "a")

            movie_url = tag_a_element[0].get_attribute("href")
            
            movie_id = movie_url.split("/")[-2]

            file.write(movie_id + "\n")

        page_main_url = "https://www.boxofficemojo.com/season/winter/" + str(year)
        driver.get(page_main_url)

        all_tr_from_table_elements = driver.find_elements(By.XPATH, "//*[@id=\"table\"]/div/table[2]/tbody/tr")

        index = 1
        for all_tr_from_table_element in all_tr_from_table_elements:
            if index == 1:
                index += 1
                continue
            tag_a_element = all_tr_from_table_element.find_elements(By.TAG_NAME, "a")

            movie_url = tag_a_element[0].get_attribute("href")
            
            movie_id = movie_url.split("/")[-2]

            file.write(movie_id + "\n")
        
        year += 1     

time.sleep(1)

# Tắt trình duyệt
driver.quit()


print("\n\n")
print("********************************************")
print("--------------------XONG--------------------")
print("********************************************")