import logging
import os
import time
from functools import wraps
from pathlib import Path
from pprint import pprint
from typing import Callable

# from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

# Service class introduced in Selenium 4 for managing driver installation, opening, and closing
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

# Used for setting wait times
from selenium.webdriver.support.ui import WebDriverWait
from termcolor import colored, cprint

# ChromeDriverManager is used to install the driver without manually downloading the binary file
from webdriver_manager.chrome import ChromeDriverManager

# def get_whatsapp_user_chat(driver: webdriver.Chrome, whatsapp_user_chat: str):
#     """ """
#     user_chat = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located(
#             (
#                 By.XPATH,
#                 f"//span[@title='{whatsapp_user_chat}']/ancestor::div[contains(@class, '_ak72')]",
#             )
#         )
#     )
#     # time.sleep(1)
#     return (driver, user_chat)


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

    driver.get(site)
    # driver.set_window_size(1920, 1080)
    # Развернуть окно полностью
    driver.maximize_window()
    # Implicit wait for all elements
    driver.implicitly_wait(7)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.visibility_of_element_located((By.TAG_NAME, "html")))
    return driver


def open_chat(driver: webdriver.Chrome, chat_name: str) -> WebElement | None:
    """
    Открыть чат по имени контакта или группы.
    """
    wait = WebDriverWait(driver, 10)
    try:
        logging.info(f"Ищем чат: {chat_name}")
        # search_field_xpath = '//*[@id="side"]//p[contains(@class, "selectable-text copyable-text")]'
        search_field_xpath = (
            '//*[@id="side"]//div[contains(@aria-autocomplete, "list")]'
        )
        # Ждем появления поля поиска
        search_field = wait.until(
            EC.presence_of_element_located((By.XPATH, search_field_xpath))
        )
        # Кликаем по полю поиска
        search_field.click()
        time.sleep(1)

        # Ищем контакт или группу
        search_field.send_keys(chat_name)
        time.sleep(2)

        # Находим нужный контакт в результатах поиска
        contact_xpath = f'//span[@title="{chat_name}"]'
        contact: WebElement = wait.until(
            EC.presence_of_element_located((By.XPATH, contact_xpath))
        )
        # Открываем чат с контактом
        contact.click()
        logging.info("Чат успешно открыт!")
        return contact
    except Exception as e:
        logging.info(f"При поиске чата {chat_name} возникла ошибка: {e}")
        return None


def send_message_user_chat(
    driver: webdriver.Chrome, text_for_send: str
) -> webdriver.Chrome:
    xpath_message_field_p = '//*[@id="main"]/footer//p[contains(@class, "selectable-text") and contains(@class, "copyable-text")]'
    xpath_message_field_span = '//*[@id="main"]/footer//span[contains(@class, "selectable-text") and contains(@class, "copyable-text")]'
    xpath_btn_send_message = '//*[@id="main"]/footer//button[contains(@aria-label, "Send") or contains(@aria-label, "Отправить")]'
    time.sleep(0.5)
    # Write message
    message_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath_message_field_p))
    )
    # Если есть текст в поле для сообщения
    if len(message_field.text) > 0:
        # Очистить полe
        ActionChains(driver).move_to_element(message_field).click().key_down(
            Keys.CONTROL
        ).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        # После этого веб-элемент становится не свежим и нужно заново его получить
        message_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, xpath_message_field_p))
        )
    # time.sleep(1)
    # Вставить текст в поле сообщения
    message_field.send_keys(text_for_send)
    # Send message
    btn_send_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath_btn_send_message))
    )
    btn_send_message.click()
    time.sleep(1)
    return driver


def get_list_messages_web_element(driver) -> tuple[webdriver.Chrome, WebElement]:
    messages_xpath = '//div[@id="main"]//div[contains(@role, "application")]'
    messages = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, messages_xpath))
    )
    logging.info(f"{messages.text=}")
    return (driver, messages)


def get_messages_from_chat_name(
    driver: webdriver.Chrome, list_messages: WebElement
) -> list[WebElement]:
    # '//span[contains(@class, "selectable-text copyable-text")]/span'
    xpath_message: str = (
        '//div[@id="main"]//div[contains(@role, "row")]//div[contains(@class, "x9f619 ")]//span[contains(@class, "_ao3e")]'
    )
    messages: list[WebElement] = list_messages.find_elements(By.XPATH, xpath_message)
    return messages


def check_new_message_icon_from_user(
    driver: webdriver.Chrome, chat: WebElement
) -> tuple[webdriver.Chrome, WebElement, WebElement | None]:
    """
    chat = //span[@title="{chat_name}"]
    new_message_icon_web_element = chat//span[contains(@aria-label, "непрочитан")]
    """
    xpath_new_message_icon = '//span[contains(@aria-label, "непрочитан")]'
    time.sleep(0.5)
    try:
        new_message_icon_web_element = chat.find_element(
            By.XPATH, xpath_new_message_icon
        )
        if new_message_icon_web_element:
            return (driver, chat, new_message_icon_web_element)
    except Exception:
        logging.info("No new messages.")
    return (driver, chat, None)


def send_pdf_file_user_chat(driver, pdf_file_path: str | Path):
    wait = WebDriverWait(driver, 10)
    btn_attach_xpath = '//*[@id="main"]//div/button[contains(@title, "Прикрепить")]'
    btn_attach = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, btn_attach_xpath))
    )
    print(f"{btn_attach=}")
    # Клик по кнопке "+"  - прикрепить
    btn_attach.click()

    select_document_xpath = '//div[@id="app"]//li[@data-animate-dropdown-item="true"]'
    select_document = wait.until(
        EC.visibility_of_element_located((By.XPATH, select_document_xpath))
    )
    print(f"{select_document=}")
    # # Клик по выбору документа
    # select_document.click()

    send_document_xpath = '//div[@id="app"]//input[@accept="*"]'
    send_document = select_document.find_element(By.XPATH, send_document_xpath)
    # Отправить документ
    send_document.send_keys(str(pdf_file_path))
    time.sleep(0.5)

    # Подождать пока файл загрузится
    loaded_pdf_file_xpath: str = '//span//div[contains(@class, "copyable-area")]'
    loaded_pdf_file = wait.until(EC.visibility_of_element_located((By.XPATH, loaded_pdf_file_xpath)))
    print(f"{loaded_pdf_file=}")

    if loaded_pdf_file:
        # Кликнуть по кнопке отправить файл
        btn_send_xpath = '//div[@id="app"]//span//div[contains(@class, "copyable-area")]//span[@data-icon="send"]'
        btn_send = wait.until(EC.element_to_be_clickable((By.XPATH, btn_send_xpath)))
        btn_send.click()
        icon_ready_download_xpath = '//div[@id="main"]//span[@data-icon="audio-download"]'
        wait.until(EC.presence_of_element_located((By.XPATH, icon_ready_download_xpath)))
    return driver


def get_file_for_user_chat(
    file_name: str | Path, folder_with_file: str | Path = "data"
):
    # Путь к текущему исполняемому файлу. В данном случае main.py
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/whats_app_bot/main.py')
    current_file: Path = Path(__file__).resolve()
    # Корневая папка проэкта
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/whats_app_bot')
    base_dir: Path = current_file.parent
    # Путь к файлу
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/whats_app_bot/data/H8499-CTA-AA-01-DR-AD-21354_Ver5 _QRCode Block_A_Level_01.pdf')
    file = base_dir / Path(folder_with_file) / Path(file_name)
    return file


def main() -> None:
    """
    https://web.whatsapp.com
    """
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    driver = initialize_web_driver("https://web.whatsapp.com")
    # TODO - создать проверку авторизации на наличие QR кода.
    # TODO Если QR-код есть - то вывести на экран сообщение,
    # TODO о необходимости выполнить считывание QR-кода с телефона чтобы авторизоваться.
    # logging.info("Отсканируй QR-код с экрана своим телефоном в течении 60 секунд.")

    chat_name = "Testing"
    chat: WebElement | None = open_chat(driver, chat_name)
    # Название нужного нам файла в формате .pdf
    pdf_file_name: str = "ga a l1"
    # Если успешно получили для взаимодействия элемент contact
    if chat:
        # ! Раскоментировать для нормальной работы
        while True:
            driver, chat, new_message_icon = check_new_message_icon_from_user(
                driver, chat
            )
            if new_message_icon:
                logging.info(f"new_message_icon element is {new_message_icon=}")
                driver, list_messages_web_element = get_list_messages_web_element(
                    driver
                )
                # Get all messages
                messages: list[WebElement] = get_messages_from_chat_name(
                    driver, list_messages_web_element
                )
                # Get new message
                new_message: str = messages[-1].text
                logging.info(f"new_message is {new_message=}")
                time.sleep(1)
                # Если в новом сообщении находится кодовое слово триггер
                if pdf_file_name in new_message.lower():
                    pdf_file_path: str | Path = get_file_for_user_chat(
                        file_name="H8499-CTA-AA-01-DR-AD-21354_Ver5 _QRCode Block_A_Level_01.pdf"
                    )
                    print(f"{pdf_file_path=}")
                    # ! WORK HERE !
                    # Отправить файл в открытый чат пользователя
                    driver = send_pdf_file_user_chat(driver, pdf_file_path)
                    time.sleep(1)

        # # ! WORKING TEST VERSION
        # while True:
        #     driver, list_messages_web_element = get_list_messages_web_element(
        #         driver
        #     )
        #     # Get all messages
        #     messages: list[WebElement] = get_messages_from_chat_name(driver, list_messages_web_element)
        #     # Get new message
        #     new_message: str = messages[-1].text
        #     logging.info(f"new_message is {new_message=}")
        #     time.sleep(2)
        #     # Если в новом сообщении находится кодовое слово триггер
        #     if pdf_file_name in new_message.lower():
        #         pdf_file_path: str | Path = get_file_for_user_chat(
        #             file_name="H8499-CTA-AA-01-DR-AD-21354_Ver5 _QRCode Block_A_Level_01.pdf"
        #         )
        #         print(f"{pdf_file_path=}")
        #         # Отправить файл в открытый чат пользователя
        #         driver = send_pdf_file_user_chat(driver, pdf_file_path)
        #         time.sleep(1)
    else:
        logging.error("Не удалось открыть чат")

    time.sleep(20)
    driver.quit()


if __name__ == "__main__":
    main()
