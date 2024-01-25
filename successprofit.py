from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import re

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://trading.probo.in/login")
time.sleep(3)

# Enter your mobile number and click the login button
username = driver.find_element(By.NAME, "mobile")
username.send_keys('7723857812')
password = driver.find_element(By.CSS_SELECTOR, "button.btn.btn__primary").click()

# Wait for OTP input and enter OTP
wait = WebDriverWait(driver, 7)
username_input = int(input("Enter OTP 6 digits: "))
passcode = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/form/div[1]/div[4]/div/div/div/div/div[1]/input")))
passcode.click()
passcode.send_keys(username_input)
verify_btn = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/form/div[2]/button[1]")))
verify_btn.click()

time.sleep(35)

# Click on BTC
BTC = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div[2]/div[4]/div/div[12]/button")))
BTC.click()

data_list = []
prev_data = None

while True:
    # Get the current time
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # Find the web element and wait for its presence
    RTCount = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "style_realtime__price__2peZA")))

    # Extract data from the web element and remove decimal values using regular expression
    data = RTCount.text
    data = re.match(r'\d+', data).group()

    # Print the extracted data with the current timestamp
    print(f"[{current_time}] Data: {data}")

    if prev_data is not None:
        if data > prev_data:
            print(f"Up [{current_time}]",data)
        elif data < prev_data:
            print(f"Down [{current_time}]",data)
        else:
            print(f"Matched data (Winning chance Bids can be made) [{current_time}]",data)

    prev_data = data

    time.sleep(60)  # Wait for 60 seconds before checking again
