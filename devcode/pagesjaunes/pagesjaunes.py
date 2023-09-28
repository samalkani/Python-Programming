from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd

restaurant_paris = pd.DataFrame(columns=['Restaurant','Address','link'])

driver = webdriver.Firefox()

driver.get('https://www.pagesjaunes.fr/')

sleep(10)

cookies = driver.find_element_by_id("didomi-notice-agree-button")
cookies.click()

sleep(10)

# SEARCH PART
commerce = driver.find_element_by_id("quoiqui")
commerce.click()
commerce.send_keys('restaurant')


location = driver.find_element_by_id("ou")
location.click()
location.send_keys('paris')

#location.send_keys(Keys.ENTER)
# OR
search = driver.find_element_by_xpath("//button[@title='Trouver']")
search.click()


# SCRAPPING PART 
for i in range(0,4):
    results = driver.find_elements_by_xpath("//li[@class='bi bi-generic']")

    for result in results:
        try:
            restaurant_name = result.find_element_by_tag_name('h3').text

            address = result.find_element_by_class_name('bi-address').text

            link = result.find_elements_by_tag_name('a')[1].get_attribute('href')


            new_line = pd.Series([restaurant_name, address, link], index=restaurant_paris.columns)
            restaurant_paris = restaurant_paris.append(new_line, ignore_index=True)

        except:
            pass

    try:
        nextpage = driver.find_element_by_xpath("//a[@id='pagination-next']")
        nextpage.click()
    except:
        print('no other page')


restaurant_paris.to_excel('Restaurants in Paris.xlsx')

















        #a
