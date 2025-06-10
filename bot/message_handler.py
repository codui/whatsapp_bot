import logging
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.helpers import set_color_to_element


def check_new_message_icon_from_user(
    driver: webdriver.Chrome, chat: WebElement, chat_name: str
) -> tuple[webdriver.Chrome, WebElement, WebElement | None]:
    """
    Проверяет наличие новых сообщений в чате WhatsApp Web.
    Если новые сообщения есть, возвращает драйвер, элемент чата и элемент нового сообщения.
    Если новых сообщений нет, возвращает кортеж с драйвером, элементом чата и None.

    Args:
        driver (webdriver.Chrome): Драйвер Selenium для управления браузером.
        chat (WebElement): Элемент чата, в котором нужно проверить наличие новых сообщений.
        chat_name (str): Название чата, в котором нужно проверить наличие новых сообщений.
    Returns:
        tuple[webdriver.Chrome, WebElement, WebElement | None]: кортеж, содержащий драйвер,
        элемент чата и элемент иконки нового сообщения.
        Если новых сообщений нет, возвращает кортеж с драйвером, элементом чата и None.

    chat = //span[@title="{chat_name}"]
    new_message_icon_web_element = chat//span[contains(@aria-label, "непрочитан")]
    """
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    logging.info("Checking for new messages...")
    # # Локатор для иконки нового сообщения
    # xpath_new_message_icon = '//ancestor::div[contains(@class, "x78zum5")]//span[contains(@aria-label, "непрочитан")]'

    # Локатор для сообщения помеченного пользователем как "непрочитанное"
    xpath_new_message_icon = '//ancestor::div[contains(@class, "x78zum5")]//span[contains(@aria-label, "епрочитан")]'

    # Если не сработает, то можно попробовать этот локатор
    # xpath_new_message_icon = './/ancestor::div[contains(@class, "x78zum5")]//span[contains(@aria-label, "епрочитан")]'

    time.sleep(1)
    try:
        new_message_icon_web_element = chat.find_elements(
            By.XPATH, xpath_new_message_icon
        )
        if new_message_icon_web_element:
            logging.info(f"В чате {chat_name} есть новые сообщения.")
            return (driver, chat, new_message_icon_web_element)
    except Exception:
        logging.info("No new messages.")
    return (driver, chat, None)  # Обработка входящих сообщений


def get_new_messages(driver: webdriver.Chrome) -> list[dict[str, str]]:
    try:
        list_incoming_messages_xpath = '//div[@id="main"]//div[contains(@role, "application")]//div[contains(@class, "message-in")]'
        list_incoming_messages: list[WebElement] = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, list_incoming_messages_xpath)
            )
        )
        # print(f"\n list_incoming_messages: {list_incoming_messages=}")

        list_incoming_messages_reverse: list[WebElement] = list_incoming_messages[::-1]

        # Incoming message
        new_messages: list[dict[str, str]] = []
        for message in list_incoming_messages_reverse:

            # # Проверить содерижит ли сообщение текст
            # text_elements: list[WebElement] | None = message.find_elements(
            #     By.XPATH, '//span[@class="_ao3e selectable-text copyable-text"]'
            # )
            # print(f"\n {text_elements=}")

            # Проверить содержит ли сообщение изображение
            image_elements: list[WebElement] | None = message.find_elements(
                By.XPATH, '//div[contains(@aria-label, "Открыть изображение")]'
            )
            print(f"{image_elements=} \n")

            # Если сообщение содержит изображение
            if image_elements:
                print(f"{len(image_elements)=} \n")
                print("Image elements work")
                # driver = set_color_to_element(driver, message, "blue")
                # time.sleep(1)
                # ! WORK HERE !

                image_one = image_elements[0]
                # Элемент сообщения, чтобы имитировать наведение мыши,
                # после которого появится кнопка контекстного меню
                actions = ActionChains(driver)
                actions.move_to_element(image_one).perform()
                image_one.click()
                time.sleep(2)

                # Работать с миниатюрами изображений в открывшемся изображении
                # '//div[contains(@role, "listitem") and contains(@aria-label, " Изображение")]'
                thumbnail_xpath: str = (
                    '//div[contains(@role, "listitem") and contains(@aria-label, " Изображение")]'
                )
                # Список миниатюр изображений которые нужно скачать
                thumbnail_images_list: list[WebElement] = WebDriverWait(
                    driver, 10
                ).until(
                    EC.presence_of_all_elements_located((By.XPATH, thumbnail_xpath))
                )
                print(f"\n {thumbnail_images_list=}")

                # Кнопка загрузки изображения
                btn_download_xpath = '//button[contains(@title, "Скачать")]'
                btn_download = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, btn_download_xpath))
                )

                for thumbnail_image in thumbnail_images_list:
                    thumbnail_image.click()
                    time.sleep(2)

                    btn_download.click()
                    time.sleep(2)

                btn_close_xpath: str = (
                    '//button[contains(@title, "Закрыть") and contains(@aria-label, "Закрыть")]'
                )
                btn_close = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, btn_close_xpath))
                )
                btn_close.click()
                time.sleep(2)
                break

            # elif text_elements:
            #     for text_element in text_elements:
            #         # print(f"{text_element=}, {type(text_element)=}")
            #         new_messages.append({"type": "text", "content": text_element.text})

            text_elements = None
            image_elements = None
        print(f"\n Incoming messages: {new_messages}")
        return new_messages
    except Exception as e:
        logging.error(f"Не удалось получить список входящих сообщений. Ошибка: {e}")
        # Возвращаем пустой список, если не удалось получить сообщения
        return []
