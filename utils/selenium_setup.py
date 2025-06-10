# Инициализация Selenium WebDriver
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Service class introduced in Selenium 4 for managing driver installation, opening, and closing
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement

# Used for setting wait times
from selenium.webdriver.support.ui import WebDriverWait

# ChromeDriverManager is used to install the driver without manually downloading the binary file
from webdriver_manager.chrome import ChromeDriverManager


def initialize_web_driver(site: str) -> webdriver.Chrome:
    """
    Initializes the Selenium WebDriver for Chrome and opens the target website.

    Args:
        site: str "http://localhost:3000/"

    Returns:
        webdriver.Chrome: An instance of the Chrome WebDriver.
    """
    options = Options()
    # Отключить уведомления
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)

    # Добавляем профиль браузера, чтобы туда сохранялся QR код
    profile_path = Path("./chrome_profile").absolute()
    options.add_argument(f"user-data-dir={profile_path}")

    # Установка драйвера или что-то подобное
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Открыть сайт
    driver.get(site)

    # driver.set_window_size(1920, 1080)
    # Развернуть окно полностью
    driver.maximize_window()

    # Implicit wait for all elements
    driver.implicitly_wait(10)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.visibility_of_element_located((By.TAG_NAME, "html")))
    return driver
