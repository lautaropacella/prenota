from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import random
import time

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver_path = ChromeDriverManager().install()

driver = webdriver.Chrome(driver_path, options=chrome_options)
actions = ActionChains(driver)

driver.get("https://prenotami.esteri.it/")

# CONSTANTS
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"
CITIZENSHIP = "CITIZENSHIP"

# HTML Elements
EMAIL_ID = "login-email"
PASSWORD_ID = "login-password"
NEXT_PAGE_CLASS = "button.primary.g-recaptcha"
CITIZENSHIP_ID = "DatiAddizionaliPrenotante_0___testo"
CHILDREN_ID = "DatiAddizionaliPrenotante_1___testo"
PRIVACY_CHECK_ID = "PrivacyCheck"
NEXT_PAGE_ID = "btnAvanti"
AVAILABLE_ID = "btnPrenotaNoOtp"
NEXT_MONTH_CLASS = "dtpicker-next"


def input_text(element, text_to_input) -> None:
    for letter in text_to_input:
        element.send_keys(letter)
        time.sleep(random.random())


def find_element_and_input(element_id, text_to_input, driver, has_id=True) -> None:
    if has_id:
        element = driver.find_element(By.ID, element_id)
    else:
        element = driver.find_element(By.CLASS_NAME, element_id)

    actions.move_to_element(element).perform()
    element.click()
    time.sleep(1)
    if text_to_input:
        input_text(element, text_to_input)
    time.sleep(3)
    return


def check_availability(AVAILABLE_CLASS, NEXT_CLASS, driver, repetitions=0):
    available = driver.find_elements(By.CLASS_NAME, AVAILABLE_CLASS)
    if len(available) > 0:
        print("Hay turno")

    elif repetitions > 4:
        next = driver.find_element(By.CLASS_NAME, NEXT_CLASS)
        next.click
        time.sleep(1)
        check_availability(driver, AVAILABLE_CLASS, NEXT_CLASS, repetitions + 1)
    else:
        print("No hay turnos")


def log_in(email_id, password_id, USERNAME, PASSWORD, driver) -> None:
    find_element_and_input(email_id, USERNAME, driver)
    find_element_and_input(password_id, PASSWORD, driver)
    return


if __name__ == "__main__":
    log_in(EMAIL_ID, PASSWORD_ID, USERNAME, PASSWORD, driver)
    find_element_and_input(NEXT_PAGE_CLASS, driver, has_id=False)

    driver.get("https://prenotami.esteri.it/Services/Booking/318")
    time.sleep(2)

    find_element_and_input(CITIZENSHIP_ID, CITIZENSHIP, driver)
    find_element_and_input(CHILDREN_ID, "0", driver)
    find_element_and_input(PRIVACY_CHECK_ID, driver)
    find_element_and_input(NEXT_PAGE_ID, driver)

    # If table for turns is not appearing, probably it's because there is a captcha to be solved manually.
    if not driver.find_elements(By.CLASS_NAME, "table-condensed"):
        input("Resolver Catcha")
        pass

    check_availability(AVAILABLE_ID, NEXT_MONTH_CLASS, driver, 0)
    driver.quit()
    input("Enter para salir")
