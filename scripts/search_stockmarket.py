from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
# import pandas as pd

# Set up Selenium
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run in headless mode
# options.add_argument("--window-size=1920x1080")
# options.add_argument("--disable-gpu")  # Disable GPU for better performance (optional)
# options.add_argument("--no-sandbox")  # Required in some environments like Docker (optional)

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)
# disable animations
# driver.execute_script("document.body.style.transition = 'none';")

# Load the website
driver.get('https://www.stockmarket.aero/StockMarket/Welcome.do')
# driver.get('https://www.stockmarket.aero/StockMarket/SearchAction.do')

# Wait for the part number input field to be visible
# search_box = WebDriverWait(driver, 10).until(
#     EC.visibility_of_element_located((By.ID, "partNumber"))
# )
# search_box.send_keys("069-01032-0101")

# # Simulate user interaction (if required)
part_number = "NAS1149FN816P"
# part_number = "069-01032-0101"
search_box = driver.find_element(By.ID, "partNumber")
search_box.send_keys(part_number)
search_box.send_keys(Keys.RETURN)
time.sleep(0.5)
search_box = driver.find_element(By.ID, "partNumber")
search_box.send_keys(part_number)
search_box.send_keys(Keys.RETURN)

# try:
# button = driver.find_element(By.XPATH, "//input[@value='Go' and @name='Search']")
# # button.click()
# driver.execute_script("arguments[0].click();", button)
# except ElementClickInterceptedException:
#     print("Overlay detected. Trying to handle the overlay.")
    # button.click()

# Wait for any overlay to disappear (if applicable)
# WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.ID, "overlay")))
# search_box.send_keys(Keys.RETURN)

# Wait until the search button is clickable
# button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Go' and @name='Search']")))



# Wait until the button is clickable
# wait = WebDriverWait(driver, 10)
# button = wait.until(EC.element_to_be_clickable((By.NAME, "Search")))
# button = driver.find_element(By.XPATH, "//input[@value='Go']")


expand_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "exp_plus")))

# Click the <div> element to trigger the javascript
expand_button.click()

# Now that the table is visible, you can interact with it or print its content
table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='rstble']")))
print(table)

# Get the HTML content of the table
table_html = table.get_attribute("outerHTML")

# Save the table HTML content to a file
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Table Export</title>
    <!-- set the base url -->
    <base href="https://www.stockmarket.aero/">
</head>
<body>
    {table_html}  <!-- Insert the table HTML here -->
</body>
</html>"""

# Write the HTML content to a file
with open("table.html", "w", encoding="utf-8") as file:
    file.write(html_content)

driver.quit()
