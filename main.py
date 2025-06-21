import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from utils.config import USERNAME, PASSWORD

OUTPUT_PATH = os.path.join('output', 'quotes.csv')
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

def create_driver():
    options = Options()
    options.binary_location = BRAVE_PATH
    return webdriver.Chrome(options=options)

def login(driver):
    driver.get('https://quotes.toscrape.com/')
    driver.find_element(By.LINK_TEXT, 'Login').click()
    time.sleep(1)
    driver.find_element(By.ID, 'username').send_keys(USERNAME)
    driver.find_element(By.ID, 'password').send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
    time.sleep(2)

def scrape_quotes(driver):
    wait = WebDriverWait(driver, 10)
    data = []
    page = 1

    while True:
        print(f'📄 Página {page}')
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'quote')))
        authors = driver.find_elements(By.CLASS_NAME, 'author')
        quotes = driver.find_elements(By.CLASS_NAME, 'text')

        for author, quote in zip(authors, quotes):
            data.append({
                'author': author.text,
                'quote': quote.text
            })

        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, 'li.next > a')
            driver.execute_script("arguments[0].scrollIntoView();", next_btn)
            time.sleep(1)
            next_btn.click()
            page += 1
            time.sleep(2)
        except NoSuchElementException:
            print('✅ Fim das páginas.')
            break

    return data

def save_to_csv(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['author', 'quote'])
        writer.writeheader()
        writer.writerows(data)
    print(f'✅ CSV salvo com sucesso em: {path}')

def main():
    driver = create_driver()
    try:
        login(driver)
        quotes = scrape_quotes(driver)
        save_to_csv(quotes, OUTPUT_PATH)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
