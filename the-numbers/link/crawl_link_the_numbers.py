import time
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
driver = webdriver.Chrome()
driver.maximize_window()

page_num = 8001

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

with open("link_movie_them.txt", "w") as file:
    while page_num < 10001:
        page_main_url = "https://www.the-numbers.com/box-office-records/worldwide/all-movies/cumulative/all-time/" + str(page_num)
        driver.get(page_main_url)

        all_tr_from_table_elements = driver.find_elements(By.XPATH, "//*[@id=\"page_filling_chart\"]/center/table/tbody/tr")
        for all_tr_from_table_element in all_tr_from_table_elements:
            tag_a_element = all_tr_from_table_element.find_elements(By.TAG_NAME, "a")

            year = int(tag_a_element[0].text)
            
            if year < 2000 or year == 2020 or year == 2021 or year == 2022 or year == 2024:
                continue

            movie_url = tag_a_element[1].get_attribute("href")
            file.write(movie_url + "\n")
        page_num += 100        

time.sleep(1)

# Tắt trình duyệt
driver.quit()


print("\n\n")
print("********************************************")
print("--------------------XONG--------------------")
print("********************************************")