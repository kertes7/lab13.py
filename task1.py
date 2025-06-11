from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def fetch_eth_phones(pages=2):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_phones = []

    for page_num in range(1, pages + 1):
        url = f"https://rozetka.com.ua/ua/mobile-phones/c80003/producer=apple/?page={page_num}"
        print(f"Завантажуємо сторінку: {url}")
        driver.get(url)
        time.sleep(3)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        titles = driver.find_elements(By.CSS_SELECTOR, "a.tile-title")
        prices = driver.find_elements(By.CSS_SELECTOR, "div.price")

        print(f"Знайдено {len(titles)} назв і {len(prices)} цін на сторінці {page_num}")

        for i in range(min(len(titles), len(prices))):
            title = titles[i].text.strip()
            price = prices[i].text.strip().replace("\u202f", "").replace("₴", "").replace(" ", "")
            if title and price.isdigit():
                all_phones.append({
                    "id": str(i + 1 + (page_num - 1) * 100),
                    "title": title,
                    "price": int(price),
                    "rating": None
                })

        time.sleep(1)

    driver.quit()

    with open("phones.json", "w", encoding="utf-8") as f:
        json.dump(all_phones, f, ensure_ascii=False, indent=2)

    print(f"Збережено {len(all_phones)} моделей у phones.json")
    if all_phones:
        print("Перша модель:", all_phones[0]['title'])

if __name__ == "__main__":
    fetch_eth_phones(pages=2)
