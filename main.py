"""
Версия для русского языка Web WhatsApp
https://web.whatsapp.com
"""

import logging
import os
import time
from functools import wraps
from pathlib import Path
from pprint import pprint
from typing import Callable

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from termcolor import colored, cprint

from bot.bot_controller import find_chat
from bot.media_downloader import download_image
from bot.message_handler import check_new_message_icon_from_user, get_new_messages
from utils.selenium_setup import initialize_web_driver

# from dotenv import load_dotenv


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


# def send_message_user_chat(
#     driver: webdriver.Chrome, text_for_send: str
# ) -> webdriver.Chrome:
#     xpath_message_field_p = '//*[@id="main"]/footer//p[contains(@class, "selectable-text") and contains(@class, "copyable-text")]'
#     xpath_message_field_span = '//*[@id="main"]/footer//span[contains(@class, "selectable-text") and contains(@class, "copyable-text")]'
#     xpath_btn_send_message = '//*[@id="main"]/footer//button[contains(@aria-label, "Send") or contains(@aria-label, "Отправить")]'
#     time.sleep(0.5)
#     # Write message
#     message_field = WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.XPATH, xpath_message_field_p))
#     )
#     # Если есть текст в поле для сообщения
#     if len(message_field.text) > 0:
#         # Очистить полe
#         ActionChains(driver).move_to_element(message_field).click().key_down(
#             Keys.CONTROL
#         ).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
#         # После этого веб-элемент становится не свежим и нужно заново его получить
#         message_field = WebDriverWait(driver, 10).until(
#             EC.visibility_of_element_located((By.XPATH, xpath_message_field_p))
#         )
#     # time.sleep(1)
#     # Вставить текст в поле сообщения
#     message_field.send_keys(text_for_send)
#     # Send message
#     btn_send_message = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, xpath_btn_send_message))
#     )
#     btn_send_message.click()
#     time.sleep(1)
#     return driver


# def send_pdf_file_user_chat(driver, pdf_file_path: str | Path):
#     wait = WebDriverWait(driver, 10)
#     btn_attach_xpath = '//*[@id="main"]//div/button[contains(@title, "Прикрепить")]'
#     btn_attach = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, btn_attach_xpath))
#     )
#     print(f"{btn_attach=}")
#     # Клик по кнопке "+"  - прикрепить
#     btn_attach.click()

#     select_document_xpath = '//div[@id="app"]//li[@data-animate-dropdown-item="true"]'
#     select_document = wait.until(
#         EC.visibility_of_element_located((By.XPATH, select_document_xpath))
#     )
#     print(f"{select_document=}")
#     # # Клик по выбору документа
#     # select_document.click()

#     send_document_xpath = '//div[@id="app"]//input[@accept="*"]'
#     send_document = select_document.find_element(By.XPATH, send_document_xpath)
#     # Отправить документ
#     send_document.send_keys(str(pdf_file_path))
#     time.sleep(0.5)

#     # Подождать пока файл загрузится
#     loaded_pdf_file_xpath: str = '//span//div[contains(@class, "copyable-area")]'
#     loaded_pdf_file = wait.until(EC.visibility_of_element_located((By.XPATH, loaded_pdf_file_xpath)))
#     print(f"{loaded_pdf_file=}")

#     if loaded_pdf_file:
#         # Кликнуть по кнопке отправить файл
#         btn_send_xpath = '//div[@id="app"]//span//div[contains(@class, "copyable-area")]//span[@data-icon="send"]'
#         btn_send = wait.until(EC.element_to_be_clickable((By.XPATH, btn_send_xpath)))
#         btn_send.click()
#         icon_ready_download_xpath = '//div[@id="main"]//span[@data-icon="audio-download"]'
#         wait.until(EC.presence_of_element_located((By.XPATH, icon_ready_download_xpath)))
#     return driver


# def get_file_for_user_chat(
#     file_name: str | Path, folder_with_file: str | Path = "data"
# ):
#     # Путь к текущему исполняемому файлу. В данном случае main.py
#     # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/whats_app_bot/main.py')
#     current_file: Path = Path(__file__).resolve()
#     # Корневая папка проэкта
#     # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/whats_app_bot')
#     base_dir: Path = current_file.parent
#     # Путь к файлу
#     # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/whats_app_bot/data/H8499-CTA-AA-01-DR-AD-21354_Ver5 _QRCode Block_A_Level_01.pdf')
#     file = base_dir / Path(folder_with_file) / Path(file_name)
#     return file


def main() -> None:
    """
    # ! Версия для русскоязычного Web WhatsApp
    # ! https://web.whatsapp.com
    """
    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
    driver = initialize_web_driver("https://web.whatsapp.com")

    # ! Если нужно отсканировать QR-код, то раскомментировать две строки ниже
    # logging.info("Отсканируй QR-код с экрана своим телефоном в течении 60 секунд.")
    # time.sleep(60)

    # TODO - создать проверку авторизации на наличие QR кода.
    # TODO Если QR-код есть - то вывести на экран сообщение,
    # TODO о необходимости выполнить считывание QR-кода с телефона чтобы авторизоваться.

    # # Название нужного нам файла в формате .pdf
    # pdf_file_name: str = "ga a l1"

    # Enter the name of the contact or group you want to open
    chat_name = "Testing"

    # Найти чат по имени и получить элемент чата для взаимодействия
    driver, chat = find_chat(driver, chat_name)

    # Если успешно получили элемент chat для взаимодействия
    if chat is not None:
        while True:
            # Проверить на новые сообщения до открытия чата
            driver, chat, new_message_icon = check_new_message_icon_from_user(
                driver, chat, chat_name
            )
            time.sleep(1)

            # Если есть новые сообщения, то открываем чат
            if new_message_icon is not None:
                # Открываем чат с контактом
                chat.click()
                logging.info("Чат успешно открыт!")
                logging.info(f"\n new_message_icon element is {new_message_icon=}")
                # ! WORK HERE 12.05.2025 !

                time.sleep(1)
                # Get all messages
                new_messages: list[dict[str, str]] = get_new_messages(driver)

                # print(f"\n {new_messages=}")
                # raw_path_to_download_images: str = (
                #     r"D:\WORK\Horand_LTD\TASKS_DOING_NOW\whats_app_download_photo\data\downloads"
                # )
                # for message in new_messages:
                #     # Check if the message is an text
                #     if message["type"] == "text":
                #         print(f"Text message: {message['content']}")
                #     # Check if the message is an image
                #     elif message["type"] == "image":
                #         print(f"Image message: {message['content']=}")

                #         # "572ee427ca22"
                #         img_name: str = message["content"].split("/")[-1].split("-")[-1]

                #         # "D:\WORK\Horand_LTD\TASKS_DOING_NOW\whats_app_download_photo\data\downloads"
                #         path_to_download_images: Path = Path(raw_path_to_download_images).resolve()

                #         # D:\WORK\Horand_LTD\TASKS_DOING_NOW\whats_app_download_photo\data\downloads\572ee427ca22.jpg
                #         path_save_img: str = str(path_to_download_images / Path(f"{img_name}.jpg"))
                #         print(f"Image path: {path_save_img=}")

                #         # Download the image
                #         download_image(driver, message["content"], path_save_img)

                time.sleep(5)

                # # Get new message
                # new_message: str = messages[-1].text
                # logging.info(f"\n new_message is {new_message=}")
                # time.sleep(1)
                # # Если в новом сообщении находится кодовое слово триггер
                # if pdf_file_name in new_message.lower():
                #     pdf_file_path: str | Path = get_file_for_user_chat(
                #         file_name="H8499-CTA-AA-01-DR-AD-21354_Ver5 _QRCode Block_A_Level_01.pdf"
                #     )
                #     print(f"{pdf_file_path=}")
                #     # ! WORK HERE !
                #     # Отправить файл в открытый чат пользователя
                #     driver = send_pdf_file_user_chat(driver, pdf_file_path)
                #     time.sleep(1)
            elif new_message_icon is None:
                logging.info(f"Новых сообщений в чате {chat_name} нет.")

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
    # else:
    #     logging.error("Не удалось открыть чат")

    time.sleep(20)
    driver.quit()


if __name__ == "__main__":
    main()
