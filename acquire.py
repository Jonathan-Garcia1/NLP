import requests
from env import get_connection
import os
import pandas as pd
from bs4 import BeautifulSoup

# Initialize headers to be used for the requests


def get_soup(url, headers):
    """
    Fetches and parses HTML content of a webpage.
    
    Parameters:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        BeautifulSoup: Parsed HTML content of the webpage.
    """
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#                                       CODEUP SCRAPER
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_blog_from_page(soup, page_number, headers):
    """
    Extracts articles from a single page of a blog site.
    
    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the blog page.
        page_number (int): The current page number for logging purposes.
        
    Returns:
        list: List of dictionaries, each containing the title and content of a blog article.
    """
    links = soup.find_all("h2")
    articles = []
    for i, article in enumerate(links):
        print(f"Getting article #{i+1} of page #{page_number}...")
        article_dict = {}
        
        if article.find("a"):
            article_dict['title'] = article.get_text()
            article_url = article.find("a").get("href")
            article_dict['content'] = get_blog_content(article_url, headers)
            articles.append(article_dict)
    return articles

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_blog_content(article_url, headers):
    """
    Fetches and extracts the content of a single blog article.
    
    Parameters:
        article_url (str): The URL of the blog article to scrape.
        
    Returns:
        str: The cleaned text content of the article.
    """
    article_response = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    article_content = article_soup.select(".entry-content")[0].find_all("p")
    clean_content = ' '.join(p.get_text() for p in article_content)
    return clean_content

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_blog_next_page_url(soup):
    """
    Identifies the URL for the next page of articles, if available.
    
    Parameters:
        soup (BeautifulSoup): Parsed HTML content of the current blog page.
        
    Returns:
        str or None: The URL for the next page of articles, or None if not present.
    """
    next_page = soup.find("div", class_="alignleft").find("a")
    return next_page.get("href") if next_page else None

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_blog_articles(url):
    """
    Scrapes and aggregates articles from multiple pages of a blog site.
    
    Parameters:
        url (str): The initial URL to start scraping from.
        
    Returns:
        list: List of dictionaries, each containing the title and content of a blog article.
    """
    headers = {'User-Agent': 'Codeup Data Science'}
    blog_articles = []
    page_number = 1
    while True:
        print(f"Getting page #{page_number}...")
        soup = get_soup(url, headers)
        articles = get_blog_from_page(soup, page_number, headers)
        blog_articles.extend(articles)
        print(f"Completed page #{page_number}.")
        next_page_url = get_blog_next_page_url(soup)
        if next_page_url is not None:
            url = next_page_url
            page_number += 1
        else:
            print("Complete")
            break
    return blog_articles


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#                                       INSHORTS SCRAPER
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_news_data(article, category):
    """
    Extracts data from an individual news article.
    
    Parameters:
        article (Tag): BeautifulSoup Tag object containing the HTML of an article.
        category (str): The category of the news article.
        
    Returns:
        dict: Dictionary containing the title, content, and category of the news article.
    """
    article_dict = {}
    title = article.find(itemprop="headline")
    if title:
        article_dict['title'] = title.get_text()
    content = article.find(itemprop="articleBody")
    if content:
        article_dict['content'] = content.get_text()
    
    # Include the category information in the article dictionary
    article_dict['category'] = category
    
    return article_dict

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_news_from_category(url, category):
    """
    Scrapes news articles from a specific category page.
    
    Parameters:
        url (str): The URL of the category page to scrape.
        category (str): The name of the news category being scraped.
        
    Returns:
        list: List of dictionaries, each containing the title and content of a news article.
    """


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",  # Use the URL of a common search engine or a referring page.
    }
    print(f"Scraping articles from category: {category}")
    soup = get_soup(url, headers)
    articles_divs = soup.find_all(itemtype="http://schema.org/NewsArticle")
    articles = [get_news_data(article, category) for article in articles_divs]
    print(f"Completed scraping articles from category: {category}")
    return articles

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_news_articles(categories):
    """
    Aggregates news articles from multiple categories.
    
    Parameters:
        categories (list): List of category names to scrape articles from.
        
    Returns:
        list: List of dictionaries, each containing the title and content of a news article.
    """
    inshorts_articles = []
    for category in categories:
        category_url = f"https://inshorts.com/en/read/{category}"
        articles = get_news_from_category(category_url, category)
        inshorts_articles.extend(articles)
    return inshorts_articles



#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
#                                       SQL SPAM
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------



def acquire_spam():
    """
    Acquire spam data from a SQL database.

    This function connects to a SQL database named 'spam', executes a query to retrieve data.

    Returns:
        pd.DataFrame: A DataFrame containing spam data.

    Note:
        - This function relies on a helper function 'get_db_connection' to establish a database connection.
    """
    # Create a helper function to get the necessary database connection URL.
    def get_db_connection(database):
        return get_connection(database)

    # Connect to the SQL 'zillow' database.
    url = "spam_db"

    # Use this query to get the data.
    sql_query = '''
                SELECT * FROM spam
                '''

    # Assign the data to a DataFrame.
    df = pd.read_sql(sql_query, get_connection(url))

    return df

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def get_spam_data():
    """
    Get spam data either from a CSV file or the SQL database.

    This function first checks if a CSV file named 'spam.csv' exists. If it does, it reads the data from the CSV
    file into a DataFrame. If the CSV file doesn't exist, it calls the 'acquire_spam' function to fetch the data
    from the SQL database, caches the data into a CSV file, and returns the DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing spam data.

    Note:
        - The data is cached in 'spam.csv' to avoid repeated database queries.
    """
    if os.path.isfile('spam.csv'):
        # If the CSV file exists, read in data from the CSV file.
        df = pd.read_csv('spam.csv', index_col=0)
    else:
        # Read fresh data from the database into a DataFrame.
        df = acquire_spam()
        # Cache the data by saving it to a CSV file.
        df.to_csv('spam.csv')
    return df
