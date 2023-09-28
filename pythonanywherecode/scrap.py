from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def scrap_linkedin(position, localisation):
    profiles = pd.DataFrame(columns=['name','position','link'])

    # FIREFOX WEB BROWSER
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    # CHROME WEB BROWSER
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-gpu")
    #driver = webdriver.Chrome(options=chrome_options)


    driver.get('https://www.linkedin.com/login/')
    sleep(5)

    input_username = driver.find_element_by_id("username")
    input_username.click()
    input_username.send_keys(username)

    input_password = driver.find_element_by_id("password")
    input_password.click()
    input_password.send_keys(password)
    input_password.send_keys(Keys.ENTER)

    sleep(5)

    search_bar = driver.find_element_by_class_name('search-global-typeahead__input')
    search_bar.send_keys(position)
    search_bar.send_keys(Keys.ENTER)

    sleep(10)
    driver.find_elements_by_class_name('artdeco-pill')[0].click()
    sleep(10)
    driver.find_elements_by_class_name('artdeco-pill')[2].click()
    sleep(10)

    location_bar.send_keys(localisation)
    location_bar = driver.find_element_by_xpath("//input[@placeholder='Add a location']")
    sleep(5)
    location_bar.send_keys(Keys.ARROW_DOWN)
    location_bar.send_keys(Keys.ENTER)
    sleep(5)
    driver.find_element_by_xpath("//button[contains(text(), 'Show results')]").click()
    sleep(5)

    # SCRAP DIRECT REQUEST
    #driver.get('https://www.linkedin.com/search/results/people/?keywords=drh&origin=CLUSTER_EXPANSION&sid=3*F')
    #sleep(5)

    # GET THE PROFILES IN THE DATAFRAME
    results = driver.find_elements_by_xpath("//li[@class='reusable-search__result-container ']")
    print(len(results))

    for result in results:

        first_name = result.find_element_by_class_name('entity-result__title-text').text.split()[0]
        last_name = result.find_element_by_class_name('entity-result__title-text').text.split()[1]
        name = first_name + " " + last_name

        try:
            position = result.find_element_by_tag_name('p').text

        except:
            position = ""
            pass

        link = result.find_elements_by_tag_name('a')[0].get_attribute('href')

        new_line = pd.Series([name, position[9:], link], index=profiles.columns)
        profiles = profiles.append(new_line, ignore_index=True)

    profiles.to_excel('profiles.xlsx')
