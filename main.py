import datetime
import json
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def init_driver():
    options = webdriver.FirefoxOptions()
    options.arguments.append("-headless")
    driver = webdriver.Firefox(options=options)
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver):
    page = 1
    posts = []
    cur_datetime = datetime.datetime.now()

    delta_time = datetime.timedelta(days=1, minutes=30)

    exit_program = False
    while True:
        if not exit_program:
            driver.get(f"https://habr.com/ru/all/page{page}")
            try:
                articles = driver.find_elements(by="tag name", value="article")
                for article in articles:
                    try:
                        product = article.get_attribute('innerHTML')
                        soup = BeautifulSoup(product, 'lxml')
                        post_time = soup.find('time').get('title')
                        post_time = datetime.datetime.strptime(post_time, '%Y-%m-%d, %H:%M')

                        if cur_datetime - post_time > delta_time:
                            exit_program = True
                            break

                        post_title = soup.find(
                            'h2', class_="tm-article-snippet__title tm-article-snippet__title_h2"
                        ).text.strip()
                        post_link = soup.find('a',
                                              class_='tm-article-snippet__title-link').get('href')
                        post_link = f"https://habr.com{post_link}"

                        post_post = soup.find(
                            'div',
                            class_="tm-article-body tm-article-snippet__lead").text.strip()

                        post = {
                            'time': post_time.strftime("%Y-%m-%d, %H:%M"),
                            'title': post_title,
                            'link': post_link,
                            'post': post_post}
                        posts.append(post)
                    except Exception:
                        pass
                page = page + 1
            except Exception:
                pass
        else:
            break
    return posts


if __name__ == "__main__":
    driver = init_driver()
    posts = lookup(driver)
    driver.quit()
    os.remove("geckodriver.log")
    with open(f"/home/{os.getlogin()}/habr/posts.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)
