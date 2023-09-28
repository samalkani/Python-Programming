username =""
password = ""



from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
#import psycopg2


profiles = pd.DataFrame(columns=['name','position','link'])

driver = webdriver.Firefox()

driver.get('https://www.linkedin.com/login/')

sleep(5)



sleep(5)

input_username = driver.find_element_by_id("username")
input_username.click()
input_username.send_keys(username)

input_password = driver.find_element_by_id("password")
input_password.click()
input_password.send_keys(password)
input_password.send_keys(Keys.ENTER)

sleep(10)

driver.get('https://www.linkedin.com/search/results/people/?keywords=drh&origin=CLUSTER_EXPANSION&sid=3*F')
sleep(5)

results = driver.find_elements_by_xpath("//li[@class='reusable-search__result-container ']")
print(len(results))

for result in results:

    first_name = result.find_element_by_class_name('entity-result__title-text').text.split()[0]
    last_name = result.find_element_by_class_name('entity-result__title-text').text.split()[1]
    name = first_name + " " + last_name
    print(name)
    try:
        position = result.find_element_by_tag_name('p').text
        print(position)
    except:
        position = ""
        pass

    link = result.find_elements_by_tag_name('a')[0].get_attribute('href')
    print(link)
    profile_id = random.randint(0,10000000)

    #SEND TO PANDAS DATAFRAME
    new_line = pd.Series([name, position[9:], link], index=profiles.columns)
    profiles = profiles.append(new_line, ignore_index=True)



#    # SEND TO POSTGRESQL
#    connection = psycopg2.connect(
#        user ="",
#        password ="",
#        host="localhost",
#        port=5432,
#        database= "profiles"
#    )
#    cursor = connection.cursor()
#    cursor.execute("""
#    INSERT INTO profiles (id, name, position, link) VALUES (%s, '%s', '%s', '%s'); """ % (int(profile_id), name, position, link))
#    connection.commit()
#    cursor.close()
#
#
#    connection.close()


# SAVE DATAFRAME
profiles.to_excel('profiles.xlsx')













#a
