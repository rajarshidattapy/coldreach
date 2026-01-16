from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def extract_profile(url: str) -> dict:
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        # Step 1: Open LinkedIn login page
        driver.get("https://www.linkedin.com/login")

        print("🔐 Please log in manually in the opened browser.")
        print("✅ After login, press ENTER here to continue...")
        input()  # <-- HARD PAUSE until you confirm

        # Step 2: Go to profile
        driver.get(url)
        time.sleep(5)

        # Step 3: Extract data
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
