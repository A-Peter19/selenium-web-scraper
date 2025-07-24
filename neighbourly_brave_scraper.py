from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

USERNAME = "agnieszka@waddesdonhall.co.uk"
PASSWORD = "Oplawiec25!"

# ===== SETUP: PATHS =====
driver_path = r"D:\02_personal\WH-data\Neighbourly-automation\chromedriver-win64\chromedriver.exe"  # Path to your downloaded ChromeDriver
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Path to Brave

# This will tell Selenium to use your default Brave profile
options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument(r'--user-data-dir=C:\Users\Peter\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default')
options.add_argument('--profile-directory=Default')
# You may set an empty profile for maximum freshness, but this lets you keep your cookies.

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
time.sleep(2)

# ===== LOGIN TO NEIGHBOURLY =====
driver.get("https://www.neighbourly.com/accounts/login")
time.sleep(3)

# Handle cookies popup by clicking "Accept all"
try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.nbrly-btn-primary"))
    )
    accept_button.click()
    time.sleep(1)
except Exception:
    pass  # Popup did not appear; continue

# Fill in login details
email_element = driver.find_element(By.NAME, "email")
email_element.clear()
email_element.send_keys(USERNAME)

password_element = driver.find_element(By.NAME, "password")
password_element.clear()
password_element.send_keys(PASSWORD)
password_element.send_keys(Keys.RETURN)
time.sleep(5)  # Wait for login

# ===== GO TO ARCHIVE PAGE =====
driver.get("https://www.neighbourly.com/myinkind/goodcause/archive")
time.sleep(5)   # Let the page load fully

# ===== DATA EXTRACTION SECTION =====

results = []

# row selector
rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "tr") if 
r.find_elements(By.CSS_SELECTOR, "a.btn.btn-link")]

for idx, row in enumerate(rows[:3]):
    try:
        # Find the "details" button/link for the row
        arrow = row.find_element(By.CSS_SELECTOR, 'a.btn.btn-link') 
        arrow.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)

        date = driver.find_element(
            By.XPATH,
            '//div[span[contains(@class, "fa-calendar")]]/span[contains(@class,"nbrly-txt-weight-500")]'
        ).text

        store = driver.find_element(
            By.XPATH,
            '//div[span[contains(@class, "fa-building")]]/span[contains(@class,"nbrly-txt-weight-500")]'
        ).text
        
        weight = driver.find_element(
            By.XPATH,
            '//div[span[contains(@class, "fa-weight")]]/span[contains(@class,"nbrly-txt-weight-500")]/span'
        ).text
        
        results.append({'Date': date, 'Store': store, 'Weight': weight})

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        print(f"Row {idx+1}: Collected!")
    except Exception as e:
        driver.switch_to.window(driver.window_handles[0])
        print(f"Error at row {idx+1}: {e}")
        continue

df = pd.DataFrame(results)
df.to_csv("neighbourly_collections.csv", index=False)
print("Done! Results saved to 'neighbourly_collections.csv'")

driver.quit()
