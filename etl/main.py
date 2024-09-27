import logging
from argparse import ArgumentParser

from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup


def contains_text(driver, text: str) -> bool:
    try:
        driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")
    except NoSuchElementException:
        return False
    return True


def main(product_name: str, min_price: float, max_price: float ):
    print(min_price, max_price)
    driver = webdriver.Chrome()
    driver.get("https://www.mercadolivre.com.br/")

    search_input = driver.find_element(By.ID, "cb1-edit")
    search_input.clear()
    search_input.send_keys(product_name)
    search_input.send_keys(Keys.RETURN)

    if contains_text(driver, "Celulares e Smartphones"):
        first_result = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/section/ol/li[1]/div/div/div[2]/div[2]/h2/a")
        first_result.click()
    else:
        first_result = driver.find_element(By.XPATH, "/html/body/main/div/div[3]/section/ol/li[1]")
        first_result.click()

    try:
        WebDriverWait(driver, 1).until(
            ec.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Entendi')]"))
        )
        entendi = driver.find_element(By.XPATH, "//*[contains(text(), 'Entendi')]")
        entendi.click()
    except TimeoutException:
        logging.info("No pop-ups were generated. Moving forward")

    soup = BeautifulSoup(driver.page_source, "lxml")

    product_has_cents = soup.find(class_="andes-money-amount__cents andes-money-amount__cents--superscript-36")
    if product_has_cents:
        cents_formatted_to_float = f"0.{product_has_cents.text}"
        cents = float(cents_formatted_to_float)
    else:
        cents = 0

    extraction_result = {
        "product_name": soup.find(class_="ui-pdp-title").text,
        "product_price": float(soup.findAll(class_="andes-money-amount__fraction")[1].text.replace(".", "")) + cents,
        "product_rating": float(soup.find(class_="ui-pdp-review__rating").text),
        "product_rating_amount": int(soup.find(class_="ui-pdp-review__amount").text.strip("()")),
        "product_stock": soup.find(class_="ui-pdp-buybox__quantity__available").text,
        "product_url": driver.current_url
    }
    print(extraction_result)


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="etl-mercado-livre",
        description="The ETL program that saves product information on the database."
    )
    parser.add_argument(
        "product_name",
        help="The name of the product you want to ETL.",
        type=str
    )
    parser.add_argument(
        "-min", "--min-price",
        help="The minimum price of the product you want to ETL.",
        type=float,
        required=False,
        default=0.0
    )
    parser.add_argument(
        "-max", "--max-price",
        help="The maximum price of the product you want to ETL.",
        type=float,
        required=False,
        default=9999999.0
    )
    args = parser.parse_args()
    main(args.product_name, args.min_price, args.max_price)
