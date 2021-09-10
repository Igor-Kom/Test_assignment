import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Testcase steps:
# 1.	Go to https://www.webstaurantstore.com/
# 2.	Search for 'stainless work table'.
# 3.	Check the search result ensuring every product item has the word 'Table' its title.
# 4.	Add the last of found items to Cart.
# 5.	Empty Cart.

class CromeSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_chrome(self):
        driver = self.driver
        wait = WebDriverWait(driver, 5)

# 1. Go to https://www.webstaurantstore.com/
        driver.get("https://www.webstaurantstore.com/")
        driver.implicitly_wait(3)
        driver.maximize_window()

        assert "WebstaurantStore: Restaurant Supplies & Foodservice Equipment" in driver.title
        print(driver.title)

# 2. Search for 'stainless work table'.
        wait.until(EC.element_to_be_clickable((By.XPATH,"//input[@id='searchval']")))
        search_contain = driver.find_element(By.XPATH, "//input[@id='searchval']").get_attribute("placeholder")
        assert search_contain == "Search 340,000+ products"

        driver.find_element(By.ID, "searchval").send_keys("stainless work table")
        driver.find_element(By.ID, "searchval").send_keys(Keys.ENTER)

        pages = int(driver.find_element_by_xpath('//*[@id="paging"]/nav/ul//li[8]').text)
        print(f'pages: {pages}')

        # 2.1 create a list for all searched items and a list for items not contain "Table"
        array1 = []
        non_table = []

        for n in range(1, pages + 1):
            driver.get(f'https://www.webstaurantstore.com/search/stainless-work-table.html?page={n}')
            all_list = driver.find_elements_by_xpath('//*[@id="details"]/a[@data-testid="itemDescription"]')
            for x in all_list:
                s = x.text.split('\n')
                attr = x.get_attribute("href")
                array1.append(x.text.split('\n'))
                if 'Table' not in x.text:
                    s.append(n)
                    non_table.append(s)

       # 2.2 print the page number and title of items which not contain "Table"
        for x in non_table:
            print(f'Page: #{x[-1]}  Tittle: "{x[0]}", this tittle does not contain "Table" ')

        # print(len(array1))
        # print(f'count {len(array1)}')
        # print(array1[-1])
        # print(attr)
        # print(non_table)

# 4. Add the last of found items to Cart.
        driver.get(attr)
        attribute = driver.find_element(By.XPATH, '//*[@id="page-header-description"]').text
        print(attribute)

    # 4.1. verify the last item of search result was added
        assert attribute == driver.title
        print(f'Page has, "{driver.title}" as a page title')

        driver.find_element(By.ID, "buyButton").submit()


# 5. Empty Cart.

        driver.implicitly_wait(5)
        assert "WebstaurantStore Cart" in driver.title

        # 5 Try to empty the cart
        # time.sleep(5) # try to empty by decrease button
        # driver.find_element(By.XPATH, '//*[@id="subject"]/div[2]').click()
        # wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="subject"]/div[2]')))
        # driver.find_element(By.XPATH, '//*[@id="subject"]/div[2]/div/a[1]/button').submit()

        # 5.2 try to empty by by button "empty cart"
        # driver.find_element(By.XPATH, "//a[@class = 'emptyCartButton btn btn-mini btn-ui pull-right']").click()
        # time.sleep(5)
        # driver.find_element(By.XPATH, "//button[contains(text(),'Empty Cart')]").send_keys(Keys.ENTER)

        # 5.3 try to empty cart by cross button
        # driver.find_element(By.XPATH, '//*[@id="main"]/div[3]/form/div/div[2]/div[2]/div/div[6]/a').click()
        print("OK")

        # 5.4 try to empty cart by GET Request
        driver.get('https://www.webstaurantstore.com/shoppingcart:cart.emptycart?nojs=1')

        time.sleep(3)
        empty_cart = driver.find_element_by_xpath("//p[contains(text(),'Your cart is empty.')]").text
        assert "Your cart is empty." in empty_cart
        amount_items = driver.find_element(By.XPATH, "//span[@id='cartItemCountSpan']").text

        time.sleep(2)
        assert amount_items == '0'

    def tearDown(self):
        self.driver.quit()
