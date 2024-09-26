from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

driver = webdriver.Chrome()
driver.get("https://www.mercadolivre.com.br/")
search_input = driver.find_element(By.ID, "cb1-edit")
search_input.clear()
search_input.send_keys("playstation 5")
search_input.send_keys(Keys.RETURN)
first_result = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/section/ol/li[1]")
first_result.click()
try:
    WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Entendi')]"))
    )
    entendi = driver.find_element(By.XPATH, "//*[contains(text(), 'Entendi')]")
    entendi.click()
except TimeoutException:
    logging.warning("No pop-ups were generated. Moving forward")
