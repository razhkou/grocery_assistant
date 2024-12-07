from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def parse_vers_0(item):
    driver = webdriver.Firefox()
    driver.implicitly_wait(0.5)
    driver.maximize_window()
    driver.get("https://edadeal.ru")
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Да' and contains(@class, 'b-button__value')]")))
    button.click()
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Готово' and contains(@class, 'b-button__value')]")))
    button.click()
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "b-input__input")))
    button.click()
    button.send_keys(item, Keys.ENTER)
    elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "b-srch-card__card-link")))
    elements[0].click()
    wait = WebDriverWait(driver, 10)
    price_element = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "span.b-money__baseunit[data-test-id='money-base']")))
    price = price_element.text.strip()

    return f"Цена товара: {price} рублей"
