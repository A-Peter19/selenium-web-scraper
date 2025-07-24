from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# ===== SETUP: PATHS =====
driver_path = r"C:\chromedriver\chromedriver.exe"  # Path to your downloaded ChromeDriver
brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"  # Path to Brave

# ===== CONFIGURE SELENIUM TO USE BRAVE =====
options = webdriver.ChromeOptions()
options.binary_location = brave_path  # Use Brave browser

driver = webdriver.Chrome(executable_path=driver_path, options=options)
driver.maximize_window()
time.sleep(2)

# ===== LOGIN SECTION =====
driver.get("https://www.neighbourly.com/accounts/login")
time.sleep(3)

# --- FILL IN YOUR LOGIN DETAILS! ---
USERNAME = "your_email@example.com"   # <--- change this
PASSWORD = "your_password_here"       # <--- change this

# --- FIND THE CORRECT NAME OR ID FOR THESE FIELDS IN 'INSPECT' ---
driver.find_element(By.NAME, "email").send_keys(USERNAME)    # update "email" if Neighbourly uses a different field name
driver.find_element(By.NAME, "password").send_keys(PASSWORD) # update "password" as needed
driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)
time.sleep(5)  # Wait for login to finish

# ===== GO TO COLLECTION ARCHIVE PAGE =====
driver.get("https://www.neighbourly.com/myinkind/goodcause/archive")
time.sleep(5)   # Let the page load fully

# ===== DATA EXTRACTION SECTION =====

results = []

# This selector may need an update -- use Inspect on the table rows!
rows = driver.find_elements(By.CSS_SELECTOR, "tr")  # Try "tr" first; if you only want table rows in the collections table, make it more specific

for idx, row in enumerate(rows):
    try:
        # ----- BLUE ARROW: Find the "details" button/link for the row (update selector as needed!) -----
        arrow = row.find_element(By.CSS_SELECTOR, '.blue-arrow-selector')  # <--- CHANGE THIS to the real selector!
        # Open in new tab (Ctrl+Click)
        arrow.send_keys(Keys.CONTROL + Keys.RETURN)
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(3)  # Let detail page load

        # --- SCRAPE DATA FROM DETAIL PAGE (update selectors as needed!) ---
        date = driver.find_element(By.CSS_SELECTOR, '.date-selector').text     # CHANGE
        store = driver.find_element(By.CSS_SELECTOR, '.store-selector').text   # CHANGE
        weight = driver.find_element(By.CSS_SELECTOR, '.weight-selector').text # CHANGE

        results.append({'Date': date, 'Store': store, 'Weight': weight})

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        print(f"Row {idx+1}: Collected!")
    except Exception as e:
        driver.switch_to.window(driver.window_handles[0])
        print(f"Error at row {idx+1}: {e}")
        continue

# ===== SAVE RESULTS TO CSV =====
df = pd.DataFrame(results)
df.to_csv("neighbourly_collections.csv", index=False)
print("Done! Results saved to 'neighbourly_collections.csv'")

# ===== Cleanup =====
driver.quit()
