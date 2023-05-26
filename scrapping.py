from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import string
import re

# unwanted characters
acceptable_chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace
pattern = re.compile(f"[^{re.escape(acceptable_chars)}]")

url = 'https://www.imdb.com/title/tt5726616/reviews/'
driver = webdriver.Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)


sort_by_select = Select(wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'lister-sort-by'))))
sort_by_select.select_by_value('submissionDate')

descending_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'lister-sort-direction')))
descending_button.click()

# Allow time for the page to update
time.sleep(2)

reviews = []
ratings = []
review_count = 0

while review_count < 1239:
    try:
        # "See More"
        more_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'show-more__control')))
        for more_button in more_buttons:
            try:
                more_button.click()
            except:
                continue  
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find the reviews and ratings
        for review_div in soup.find_all('div', class_='imdb-user-review'):
            if review_count >= 1239:
                break

            review_text_div = review_div.find('div', class_='text')
            rating_span = review_div.find('span', class_='rating-other-user-rating')
            
            if review_text_div and rating_span:  # only add reviews that have a rating
                rating = rating_span.find('span').text
                
                review = pattern.sub('', review_text_div.text)
                
                reviews.append(review)
                ratings.append(int(rating))
                review_count += 1

        # "Load More"
        if review_count < 1239:
            load_more_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ipl-load-more__button')))
            load_more_button.click()
            time.sleep(2)

    except Exception as e:
        print(f"Finished loading reviews. Reason: {str(e)}")
        break

df = pd.DataFrame({
    'Review': reviews,
    'Rating': ratings
})
df.index.name = 'Index'
df.to_excel('2018_call_me_by_your_name_user_reviews.xlsx')

driver.quit()
