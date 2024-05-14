import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from config import google_username, google_password
import time
# Configure logging
logging.basicConfig(level=logging.INFO)
user_data_list = []

def login_to_google():
    options = Options()
    options.headless = True
    chromedriver_path = ChromeDriverManager().install()
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    print("login driver redirect")
    driver.get("https://asdedu.schoology.com/user/116395833/info")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.ID, "identifierId")))

    # Locate the username input field and enter your username
    username_input = driver.find_element(By.ID, "identifierId")
    username_input.send_keys(google_username)
    username_input.send_keys(Keys.RETURN)

    # Wait for the password input field to become interactable
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))

    # Locate the password input field and enter your password
    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    password_input.send_keys(google_password)
    password_input.send_keys(Keys.RETURN)



    return driver

def fetch_email(user_id, driver):
    try:
        print("Page loaded successfully")
        print(f"Current URL: {driver.current_url}")

        # Wait for the email element to be present on the page
        email_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'mailto:')]")))

        # Extract email from the element
        email = email_element.get_attribute("href").split(":")[1]
        print(f"Email found: {email}")

        # Extract person's name from the page
        name_element = driver.find_element(By.XPATH, "//h2[contains(@class, 'page-title')]")
        name = name_element.text.strip()
        print(f"Name found: {name}")

        # Store name and email in a dictionary
        data = {'name': name, 'email': email}
        return data
    except Exception as e:
        print(f"Error occurred while fetching email: {e}")
        return None

# Log in to Google
driver = login_to_google()
time.sleep(5)
start_user_id = 115035536
end_user_id = 115037536
user_id = start_user_id
# Test for a single user ID
for user_id in range(start_user_id, end_user_id):
    try:
        
        driver.get(f"https://asdedu.schoology.com/user/{user_id}/info")
        time.sleep(1)
        user_data = fetch_email(user_id, driver)
        
        if user_data:
            print(f"User ID: {user_id}, Name: {user_data['name']}, Email: {user_data['email']}")
            user_data_list.append(user_data)
        else:
            print(f"No data found for user ID: {user_id}")
    except Exception as e:
        print(f"Error occurred for user ID {user_id}: {e}")
    time.sleep(0.5)  # Add a delay to avoid hitting the server too frequently

# Close the browser after the loop finishes
driver.quit()


def save_to_file(user_data_list):
    with open("emails & namespartlast.txt", "w") as file:
        for user_data in user_data_list:
            file.write(f"Name: {user_data['name']}, Email: {user_data['email']}\n")

# Loop through user_data_list and print name and email for each user
for user_data in user_data_list:
    print(f"Name: {user_data['name']}, Email: {user_data['email']}")
save_to_file(user_data_list)