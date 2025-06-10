from selenium import webdriver
import requests
from pprint import pprint
# Скачивание фото/медиа из чата


def download_image(driver, image_src, path_save_img):
    """Скачивание фото/медиа из чата.

    Args:
        driver (webdriver.Chrome): Драйвер Selenium для управления браузером.
        image_src (str): URL-адрес изображения.
        path_save_img (str): Путь для сохранения изображения.
    """
    try:
        print(f"Скачивание изображения: {image_src=}")

        # Используем requests для скачивания изображения
        response = requests.get(image_src, stream=True)
        if response.status_code == 200:
            print(f"{response=}")
            pprint(dir(response))

            with open(path_save_img, "wb") as file:
                file.write(response.content)
            print(f"Изображение сохранено: {path_save_img}")
        else:
            print(f"Не удалось скачать изображение: {response.status_code}")
    except Exception as e:
        print(f"Ошибка при скачивании изображения: {e}")
