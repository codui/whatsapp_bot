import time
from selenium import webdriver
# Утилиты: парсинг, логгирование, работа с файлами и т.д.


def set_color_to_element(driver, element, color: str = "#5cc695") -> webdriver.Chrome:
    original_style = element.get_attribute("style")
    # Подсветить активный элемент
    driver.execute_script(
        "arguments[0].setAttribute('style', arguments[1]);",
        element,
        f"background: {color}",
    )
    time.sleep(1)
    # Возврат к оригинальному стилю
    driver.execute_script(
        "arguments[0].setAttribute('style', arguments[1]);", element, original_style
    )
    return driver
