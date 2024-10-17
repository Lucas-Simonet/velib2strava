import json
import logging

# import time

# import cloudscraper
# import requests
from velib2strava.model.run import VelibRun

RUN_PATH = "velib2strava/resource/run_list.json"

logger = logging.getLogger("app")


class VelibClient:
    def __init__(self) -> None:
        pass

    def get_rides(self) -> list[VelibRun]:
        velib_run_list: list[VelibRun] = []
        run_list = self._get_json_run_list()
        for run in run_list["walletOperations"]:
            try:
                velib_run_list.append(
                    VelibRun(
                        id=run["parameter3"]["usageId"],
                        start_point=run["parameter3"]["departureStationId"],
                        end_point=run["parameter3"]["arrivalStationId"],
                        distance=run["parameter3"]["DISTANCE"],
                        average_speed=run["parameter3"]["AVERAGE_SPEED"],
                        start_time=run["startDate"],
                        end_time=run["endDate"],
                    )
                )

            except ValueError:
                pass
            except Exception as e:
                logger.error(e)
        return velib_run_list

    def _get_json_run_list(self):
        with open(RUN_PATH, "r") as file:
            run_list = json.load(file)
        return run_list


# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# # Set up options for headless mode
# chrome_options = Options()

# # Basic configurations to avoid resource limitations
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")  # To avoid memory issues
# chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering (optional but helpful)
# chrome_options.add_argument("--headless")  # Headless mode (if needed)

# # Set custom User-Agent header
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")


# # Initialize the WebDriver
# driver = webdriver.Chrome(options=chrome_options,)

# # Add specific headers to mimic a real browser request
# driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
#     'headers': {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Cache-Control': 'max-age=0',
#         'Upgrade-Insecure-Requests': '1',
#         'Referer': 'https://www.velib-metropole.fr/',  # Set to the proper URL before login
#     }
# })
# try:
#     # Go to the login page or any page you need
#     driver.get("https://www.velib-metropole.fr/login")
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
#     csrf_token = driver.find_element(By.NAME, "_csrf_token").get_attribute("value")
#     print(f"CSRF Token: {csrf_token}")
#     username = driver.find_element(By.NAME, "_username")
#     password = driver.find_element(By.NAME, "_password")
#     username.send_keys("")
#     password.send_keys("")
#     # print(driver.get_cookies())
#     submit_button = driver.find_element(By.CLASS_NAME, "btn-smoove-valid")
#     driver.execute_script("""
#         const form = document.querySelector('form');
#         const csrfTokenInput = document.createElement('input');
#         csrfTokenInput.type = 'hidden';
#         csrfTokenInput.name = '_csrf_token';
#         csrfTokenInput.value = arguments[0];
#         form.appendChild(csrfTokenInput);
#         form.submit();
#     """, csrf_token)
#     time.sleep(5)
#     cookies_after = driver.get_cookies()
#     print(f"Cookies after submission: {cookies_after}")
#     # print(driver.page_source)

# finally:
#     driver.quit()

# # url = 'https://www.velib-metropole.fr/login'

# # # Define your login payload with credentials and the CSRF token
# # payload = {
# #     '_username': '',
# #     '_password': '',
# #     '_csrf_token': csrf_token,  # Include the CSRF token
# # }
# # headers = {
# #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
# # }
# # # Make the POST request to login
# # scraper = cloudscraper.create_scraper()  # Returns a session with Cloudflare bypass

# # response = scraper.post(url, data=payload, headers=headers)

# # # Check if login was successful
# # if response.status_code == 302:
# #     print("Login successful, BEARER token should be set in cookies.")
# #     print(response.cookies)
# # else:
# #     print("Login failed")
