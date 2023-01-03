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

import threading

def links_for_search_parallel(query, n_pages=10):

  # redirecting to google.com
  driver.get("https://www.google.com")

  # accessing the search bar and searching the specified query
  search_bar = driver.find_element("name", "q")
  search_bar.clear()
  search_bar.send_keys(query)
  search_bar.send_keys(Keys.RETURN)

  # fetching the news and videos links for the specified query
  category_list = ["News", "Videos"]
  category_link = []
  for i in category_list:
    category_link.append(driver.find_element(By.LINK_TEXT, i).get_attribute('href'))
    
  result_links = []

  # PARALLELISING THE SEARCH RESULTS FOR VIDEOS AND NEWS ARTICLES

  # creating a thread for fetching all the links for news articles
  t1 = threading.Thread(target=link_from_category_parallel, args=(category_link[0], "News",n_pages))

  # creating a thread for fetching all the links for videos
  t2 = threading.Thread(target=link_from_category_parallel, args=(category_link[1], "Videos",n_pages))

  # starting thread 1
  t1.start()
  # starting thread 2
  t2.start()

  # wait until thread 1 is completely executed
  t1.join()
  # wait until thread 2 is completely executed
  t2.join()

  print("Done!!")