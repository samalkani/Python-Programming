'''

THIS BOT SCRAPS LINKEDIN LIKES
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os



class LinkedinLikeProfiles(object):
    """Class that can connect to Linkedin, go to an article page,
        open the like modal and scrap the hyperlinks of
        linkedin profiles that liked the article.
        There is not a lot of error checking and alerting."""
    __slots__ = ['username', 'password', 'human_reactions', 'chrome_options', 'driver', 'like_modal']

    def __init__(self, username: str, password: str, human_reactions=False):
        self.human_reactions = human_reactions
        self.chrome_options = Options()
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        #chrome_options.headless = True
        self.driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), options=chrome_options)
        self.linkedin_login(self, username, password)
        self.like_modal = None

    @staticmethod
    def linkedin_login(self, username: str, password: str):
        """Connect to linkedin with a given username and password. It could use some hashing !"""
        self.driver.get('https://www.linkedin.com/login/fr')
        WebDriverWait(self.driver, 10).until(ec.presence_of_element_located((By.ID, "username")))
        if self.human_reactions:
            time.sleep(5)
        username_input = self.driver.find_element_by_id("username")
        username_input.send_keys(username)
        if self.human_reactions:
            time.sleep(5)
        password_input = self.driver.find_element_by_id("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        incognito = WebDriverWait(self.driver, 100).until(ec.title_contains("LinkedIn"))
        if not incognito:
            print("I probably got a capcha I can't pass, since I am a bot...")
            exit(84)

    def scrap_like_profiles(self, article_link: str) -> None:
        """This is what you call for the main functionality of this program.
            It gathers every steps that were separated into static methods"""
        if self.open_like_modal(self, article_link) is False:
            print("Nobody liked the article... Sorry.")
            return
        self.scroll_div(self)
        self.parse_and_get_like_profiles(self)

    @staticmethod
    def open_like_modal(self, article_link: str) -> bool:
        """Access article and open like modal"""
        self.driver.get(article_link)
        try:
            time.sleep(5) if self.human_reactions else WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, "button[data-control-name='likes_count'")))
            self.driver.find_element_by_css_selector("button[data-control-name='likes_count'").click()
            time.sleep(5) if self.human_reactions else WebDriverWait(self.driver, 20).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[class='artdeco-modal__content social-details-reactors-modal__content ember-view']")))
            self.like_modal = self.driver.find_element_by_css_selector(
                "div[class='artdeco-modal__content social-details-reactors-modal__content ember-view']")
        except Exception as e:
            print(e)
            return False
        return True

    @staticmethod
    def scroll_div(self) -> None:
        """Scroll the "infinite" scrolling"""
        if self.like_modal is None:
            return
        scrollable_div = self.like_modal  # Easier to read
        height = scrollable_div.size['height']
        new_height = 0
        while height != new_height:
            self.driver.execute_script('arguments[0].scrollTo(' + str(new_height) + ', arguments[0].scrollHeight)', scrollable_div)
            time.sleep(0.5)
            height = new_height
            new_height = self.driver.execute_script('return arguments[0].scrollHeight', scrollable_div)

    @staticmethod
    def parse_and_get_like_profiles(self) -> [str]:
        if self.like_modal is None:
            return
        contacts = self.like_modal.find_elements_by_class_name("artdeco-list__item")
        results = []
        for elem in contacts:
            profile_link = elem.find_element_by_tag_name("a").get_attribute("href")
            results.append(profile_link.split('?')[0])
        with open("linkedin_profiles.csv", "w") as f:
            f.write('linkedin_profiles\n')
            f.write('\n'.join(results))
        return results


def main():
    try:
        '''
            Fill this part correctly; you can also uncomment the
            chrome_headless.options = True in the __init__ to hide the automated browser
        '''
        USERNAME = ""
        PASSWORD = ""
        ARTICLE_LINK = ""

        # human_reactions add delays to some actions to make the behaviour more believable to LinkedIn
        linkedin_bot = LinkedinLikeProfiles(USERNAME, PASSWORD, human_reactions=True)
        linkedin_bot.scrap_like_profiles(ARTICLE_LINK)
    except Exception as e:
        print(e)
        exit(84)
    exit(0)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
