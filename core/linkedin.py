from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def extract_profile(url: str) -> dict:
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)

        title = driver.title or ""
        name = title.split("|")[0].strip()

        body_text = driver.find_element(By.TAG_NAME, "body").text
        context = body_text[:500]

        return {
            "name": name,
            "context": context
        }
    finally:
        driver.quit()
