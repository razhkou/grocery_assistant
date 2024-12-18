from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time

from sqlalchemy.testing.plugin.plugin_base import options


def parse_vers_0(geo, items):
    ffoptions = Options()
    ffoptions.add_argument('--headless')
    driver = webdriver.Firefox(options=ffoptions)
    driver.implicitly_wait(0.5)
    driver.get("https://edadeal.ru")
    wait = WebDriverWait(driver, 100)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Нет' and contains(@class, 'b-button__value')]")))
    button.click()
    button = wait.until(EC.element_to_be_clickable((By.ID, "u3149432f6270a-locality-search")))
    button.click()
    button.send_keys(geo, Keys.ENTER)
    time.sleep(10)
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR , 'button.b-geo-picker__locality-item[data-test-ref="localityItem"]')))
    button.click()
    time.sleep(10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Готово' and contains(@class, 'b-button__value')]")))
    button.click()
    res = ""
    for item in items:
        button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "b-input__input")))
        button.click()
        button.send_keys(item, Keys.ENTER)
        elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "b-srch-card__card-link")))
        time.sleep(10)
        elements[0].click()
        wait = WebDriverWait(driver, 10)
        naming_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.p-dsk-srch-offer__info-item.p-dsk-srch-offer__info-item_type_title")))
        naming = naming_element.text.strip()
        elements_store = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "b-srch-price-offer__card-info-title-partner-name")))
        elements_price = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "b-srch-price-offer__card-info-price")))
        #print(naming, ':')
        res += naming
        res += ':\n'
        for i in range(len(elements_store)):
            res += elements_store[i].text
            res += " - "
            cnt = 0
            pt = 0
            while(elements_price[i].text[pt] != '₽' and cnt < 3):
               #if elements_price[i].text[pt] == 'о' or elements_price[i].text[pt] == 'т':
                   #continue
               if elements_price[i].text[pt] != '\n':
                   res += elements_price[i].text[pt]
               else:
                   cnt += 1
               pt += 1
            res += ' рублей\n'
        res += "\n"
    driver.quit()
    return res
  
