# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00B38A64C48AC9A0CEFDB6715372640DA9632FC9EF9A97628F06D4AB44381BE5E53DBA3F68BE3C0D50560807F9FCAF066703E8E4BC8215D969C1681B4EF288BE54184CC415AA3D0EF76BE8C595BA5A60F19A9B47E7E8992E0922F787C0566E04177DF2723228427A0F21B5B99475B31610EA9DBFB7400AEF6A402204D482E4AF9C459D0E4AEEA966A15230E7004C240437FCFC4B72D89492A9304B193B2D7BEA01490865096BC246B39E8792F8153509C75D76896563D01138A7F003023AD76E4EA0353C0E30A852BB511E65EB3FB55162A438792DA88076554CCA1A2754A101B5965B802F0FCA542669706FC1563AD0CD7CE7D45A88EF90807F8132C0CE059419E251CE8AF5A5301000CA0B20119F039F0A57C756AADB9CE44A9BECB565E4B1DF05079FD4CC2924FE8D96538CDC66D33C8669AF1A166072647503D0B3A0FD7655540FE87925071F2FE35EE8F995E0BE4D"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
