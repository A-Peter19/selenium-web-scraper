from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# ===== SETUP: PATHS =====
driver_path = r"D:\02_personal\WH-data\Neighbourly-automation\chromedriver-win64\chromedriver.exe"  # Path to your downloaded ChromeDriver
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Path to Brave

# This will tell Selenium to use your default Brave profile
options = webdriver.ChromeOptions()
options.binary_location = brave_path
options.add_argument("r'--user-data-dir=C:\Users\Peter\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default")
# You may set an empty profile for maximum freshness, but this lets you keep your cookies.

driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.maximize_window()
time.sleep(2)

# ===== GO TO ARCHIVE PAGE =====
driver.get("https://www.neighbourly.com/myinkind/goodcause/archive")
time.sleep(5)   # Let the page load fully

# ===== DATA EXTRACTION SECTION =====

results = []

# row selector
rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "tr") if 
r.find_elements(By.CSS_SELECTOR, "a.btn.btn-link")]

for idx, row in enumerate(rows):
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
