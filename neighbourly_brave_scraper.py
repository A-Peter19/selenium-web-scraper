from selenium import webdriver
from selenium.webdriver.common.by import By   # <-- add this line!
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ===== SETUP SECTION =====
driver_path = r"D:\02_personal\WH-data\Neighbourly-automation\chromedriver-win64\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)

# ===== GO TO ARCHIVE PAGE =====
driver.get("https://www.neighbourly.com/myinkind/goodcause/archive")
time.sleep(5)   # Let the page load fully
all_trs = driver.find_elements(By.CSS_SELECTOR, "tr")
print(f"Total <tr> elements on page: {len(all_trs)}")
for i, tr in enumerate(all_trs[:10]):
    print(f"Row {i+1}: {tr.get_attribute('outerHTML')[:200]}")


# ===== DATA EXTRACTION SECTION =====

results = []

# row selector
rows = [r for r in driver.find_elements(By.CSS_SELECTOR, "tr") if 
r.find_elements(By.CSS_SELECTOR, "a.btn.btn-link")]
print(f"Found {len(rows)} data rows")

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
        
    print(f"Row {idx+1} extraction: date={date}, store={store}, weight={weight}")
    results.append({'Date': date, 'Store': store, 'Weight': weight})

df = pd.DataFrame(results)
df.to_csv("neighbourly_collections.csv", index=False)
print("Done! Results saved to 'neighbourly_collections.csv'")

driver.quit()
