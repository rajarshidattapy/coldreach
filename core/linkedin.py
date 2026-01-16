from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def extract_profile(url: str) -> dict:
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(5)  # let LinkedIn load

        # Get page title → usually contains name
        title = driver.title
        name = title.split("|")[0].strip() if title else ""

        # Get visible page text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        context = body_text[:400]

        return {
            "name": name,
            "context": context
        }

    finally:
        driver.quit()

def test_extract_profile():
    test_url = "https://www.linkedin.com/in/satyanadella/"

    profile = extract_profile(test_url)

    assert "name" in profile, "Missing name"
    assert "context" in profile, "Missing context"
    assert profile["name"], "Name is empty"
    assert profile["context"], "Context is empty"

    print("✅ extract_profile() works")
    print("Name:", profile["name"])
    print("Context preview:", profile["context"][:200])


if __name__ == "__main__":
    test_extract_profile()
