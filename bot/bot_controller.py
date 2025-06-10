# Основной контроллер логики бота
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def find_chat(
    driver: webdriver.Chrome, chat_name: str
) -> tuple[webdriver.Chrome, WebElement | None]:
    """Найти чат по имени в WhatsApp Web.
    Ищем чат по имени в WhatsApp Web. Если чат найден, возвращаем драйвер и элемент чата.

    Args:
        driver (webdriver.Chrome): Драйвер Selenium для управления браузером.
        chat_name (str): Название чата, который нужно найти.

    Returns:
        tuple[webdriver.Chrome, WebElement | None]: кортеж, содержащий драйвер и элемент чата.
        Если чат не найден, возвращаем драйвер и None.
    """
    # Настройка логирования
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    logging.info(f"Ищем чат: {chat_name}")

    wait = WebDriverWait(driver, 10)
    # search_field_xpath = '//*[@id="side"]//p[contains(@class, "selectable-text copyable-text")]'
    # Поле поиска чата
    search_field_xpath = '//*[@id="side"]//div[contains(@aria-autocomplete, "list")]'

    # Ждем появления поля поиска
    search_field = wait.until(
        EC.presence_of_element_located((By.XPATH, search_field_xpath))
    )

    # Кликаем по полю поиска
    search_field.click()
    time.sleep(1)

    # Ищем контакт или группу. Вставляем имя контакта или группы в поле поиска
    search_field.send_keys(chat_name)
    time.sleep(2)

    # Находим нужный контакт в результатах поиска
    chat_xpath = f'//span[@title="{chat_name}"]'
    try:
        chat: WebElement = wait.until(
            EC.presence_of_element_located((By.XPATH, chat_xpath))
        )
        logging.info(f"Чат: {chat_name} найден.")
        return (driver, chat)
    except Exception as e:
        logging.error(f"Не удалось найти чат: {chat_name}. Ошибка: {e}")
        return (driver, None)
