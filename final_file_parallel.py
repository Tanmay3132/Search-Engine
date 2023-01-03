import multiprocessing

from extract_Videos_parallel import extractYoutubeVideos
from extractrepos_parallel import extract_repos
# from sentiment_analysis_twitter_parallel import get_tweets_main
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

PATH = "./chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--use-gl=swiftshader")
chrome_options.add_argument("--ignore-gpu-blacklist")
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(PATH),chrome_options=chrome_options)
# # redirecting to google.com
# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument('--headless')
# # chrome_options.add_argument('--no-sandbox')
# # chrome_options.add_argument('--disable-dev-shm-usage')
# # chrome_options.add_argument('--disable-gpu')
# # # repalce the first argument with the path of your driver


# function for getting links from the specified category
from bs4 import BeautifulSoup




def link_from_category_parallel(category_link, category, n_pages):
    
  class_from_categ = {"News":"SoaBEf", "Videos":"MjjYud"} #class tag for categories
  class_tag = ""
  class_tag = class_from_categ[category]

  results = [] # list for storing all the links


  for page in range(1, n_pages):
    url = category_link +  str((page - 1) * 10) 
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    search = soup.find_all('div', class_=class_tag )
    for h in search:
        results.append(h.a.get('href'))
    return results


def links_for_search(query, n_pages=7):
    newslinks_results = []
    driver.get("https://www.google.com")
    # accessing the search bar and searching the specified query
    search_bar = driver.find_element("name", "q")
    search_bar.clear()
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)

    # fetching the news and videos links for the specified query
    category_list = ["News"]
    category_link = []
    for i in category_list:
        category_link.append(
            driver.find_element(By.LINK_TEXT, i).get_attribute('href'))

    # fetching all the links for news articles
    newslinks_results.append(link_from_category_parallel(
        category_link[0], "News", n_pages))

    return newslinks_results


def links_for_search_parallel(query, newslinks_results, n_pages=7):
    driver.get("https://www.google.com")
    # accessing the search bar and searching the specified query
    search_bar = driver.find_element("name", "q")
    search_bar.clear()
    search_bar.send_keys(query)
    search_bar.send_keys(Keys.RETURN)

    # fetching the news and videos links for the specified query
    category_list = ["News"]
    category_link = []
    for i in category_list:
        category_link.append(
            driver.find_element(By.LINK_TEXT, i).get_attribute('href'))

    # fetching all the links for news articles
    newslinks_results.append(link_from_category_parallel(
        category_link[0], "News", n_pages))



def parallel_implementation(query):
    final_results = []

   # query = input("What do you want to search? ")
    start_time = time.time()
    with multiprocessing.Manager() as manager:
        processes = manager.list([manager.list() for i in range(4)])

        p1 = multiprocessing.Process(
            target=extractYoutubeVideos, args=(query, processes[0]))
        p2 = multiprocessing.Process(
            target=extract_repos, args=(query, processes[1]))
        # p3 = multiprocessing.Process(
        #     target=get_tweets_main, args=(query, processes[2]))
        p3 = multiprocessing.Process(
            target=links_for_search_parallel, args=(query, processes[3]))

        p1.start()
        p2.start()
        p3.start()
        # p4.start()

        p1.join()
        p2.join()
        p3.join()
        # p4.join()

        # store the results in the global variable
        for i in processes:
            final_results.append(list(i))

    parallel_time = time.time() - start_time

    youTube_results, github_results, tweet_results, news_results = [], [], [], []

    youTube_results = final_results[0]

    github_results = final_results[1]

    # tweet_results = final_results[2][0]

    news_results = final_results[2]

    return {'Youtube': youTube_results,
            'Github': github_results,
            'News': news_results,
            'Total Parallel': parallel_time}


# if __name__ == '__main__':
#     tweets=parallel_implementation('python')['Tweets']
#     print(tweets[0]['text'])