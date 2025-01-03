import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import csv

def get_ournews_articles(date_str):
    """
    Scrape articles from OurNews website for a specific date
    """
    # Convert date string to datetime object for comparison
    target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    print(f"Searching for articles on: {target_date}")
    
    # URL of the news website
    url = 'https://ournews.bs/latest-news/'
    
    try:
        # Send HTTP GET request to the website
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all article elements using the correct class
        articles = soup.find_all('li', class_='mvp-blog-story-wrap')
        print(f"Found {len(articles)} articles in total")
        
        # Store the results
        results = []
        current_time = datetime.now()
        
        for article in articles:
            try:
                # Find the link element
                link_element = article.find('a')
                # Find the date element
                date_element = article.find('span', class_='mvp-cd-date')
                
                if link_element and date_element:
                    title = link_element.get_text().strip()
                    link = link_element['href']
                    relative_time = date_element.get_text().strip()
                    
                    # Calculate actual publication date
                    pub_date = current_time
                    time_parts = relative_time.split()
                    
                    if 'minute' in relative_time:
                        minutes = int(time_parts[0])
                        pub_date = current_time - timedelta(minutes=minutes)
                    elif 'hour' in relative_time:
                        hours = int(time_parts[0])
                        pub_date = current_time - timedelta(hours=hours)
                    elif 'day' in relative_time:
                        days = int(time_parts[0])
                        pub_date = current_time - timedelta(days=days)
                    
                    # Compare dates (ignoring time)
                    if pub_date.date() == target_date:
                        # Debug print
                        print(f"\nFound article: {title}")
                        print(f"Link: {link}")
                        print(f"Published: {pub_date.date()} (from '{relative_time}')")
                        
                        results.append({
                            'source': 'OurNews',
                            'title': title,
                            'link': link,
                            'date': pub_date.strftime('%Y-%m-%d')
                        })
            except Exception as e:
                print(f"Error processing article: {e}")
        
        print(f"\nFound {len(results)} articles from {target_date}")
        return results
    
    except Exception as e:
        print(f"Error scraping OurNews: {e}")
        return []

def get_zns_articles(date_str):
    """
    Scrape articles from ZNS Bahamas website for a specific date
    """
    url = 'https://znsbahamas.com/category/news/'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all articles using the feat-holder class which contains the articles
        articles = soup.find_all('div', class_='feat-holder')
        print(f"Found {len(articles)} ZNS articles in total")
        
        results = []
        
        for article in articles:
            try:
                # Find the link element with class 'p-flink'
                link_element = article.find('a', class_='p-flink')
                if link_element:
                    title = link_element.get('title', '').strip()
                    link = link_element.get('href', '')
                    
                    # Debug print
                    print(f"\nFound ZNS article: {title}")
                    print(f"Link: {link}")
                    
                    results.append({
                        'source': 'ZNS Bahamas',
                        'title': title,
                        'link': link,
                        'date': 'Date not available'
                    })
            except Exception as e:
                print(f"Error processing ZNS article: {e}")
        
        return results
    
    except Exception as e:
        print(f"Error scraping ZNS: {e}")
        return []

def get_ewnews_articles(date_str):
    """
    Scrape articles from Eyewitness News website for a specific date
    """
    url = 'https://ewnews.com/'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find all articles using the jeg_post class
        articles = soup.find_all('article', class_='jeg_post')
        print(f"Found {len(articles)} EWNews articles in total")
        
        results = []
        
        for article in articles:
            try:
                # Find the link element
                link_element = article.find('a')
                if link_element:
                    title = link_element.get('aria-label', '').strip()
                    if not title:  # If aria-label is empty, try getting text content
                        title = link_element.get_text().strip()
                    link = link_element.get('href', '')
                    
                    # Debug print
                    print(f"\nFound EWNews article: {title}")
                    print(f"Link: {link}")
                    
                    results.append({
                        'source': 'Eyewitness News',
                        'title': title,
                        'link': link,
                        'date': 'Date not available'
                    })
            except Exception as e:
                print(f"Error processing EWNews article: {e}")
        
        return results
    
    except Exception as e:
        print(f"Error scraping EWNews: {e}")
        return []

def save_to_csv(articles, filename):
    """
    Save the scraped articles to a CSV file and track last update time
    """
    if not articles:
        print("No articles found for the specified date.")
        return
    
    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Write articles to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        # Add last_updated field to fieldnames
        writer = csv.DictWriter(file, fieldnames=['source', 'title', 'link', 'date', 'last_updated'])
        writer.writeheader()
        
        # Add last_updated timestamp to each article
        for article in articles:
            article['last_updated'] = current_time
            writer.writerow(article)
    
    print(f"Articles updated in {filename}")
    print(f"Last updated: {current_time}")

def main():
    # Get date input from user
    date_str = input("Enter date (YYYY-MM-DD): ")
    
    try:
        # Validate date format
        datetime.strptime(date_str, '%Y-%m-%d')
        
        # Collect articles from all sources
        ournews_articles = get_ournews_articles(date_str)
        zns_articles = get_zns_articles(date_str)
        ewnews_articles = get_ewnews_articles(date_str)
        
        # Combine all articles
        all_articles = []
        all_articles.extend(ournews_articles)
        all_articles.extend(zns_articles)
        all_articles.extend(ewnews_articles)
        
        # Use a fixed filename instead of date-based filename
        filename = "news_articles.csv"
        save_to_csv(all_articles, filename)
        
        # Print summary of articles found
        print("\n=== Article Count Summary ===")
        print(f"Our News: {len(ournews_articles)} articles")
        print(f"ZNS Bahamas: {len(zns_articles)} articles")
        print(f"Eyewitness News: {len(ewnews_articles)} articles")
        print(f"Total: {len(all_articles)} articles")
        print("===========================")
        
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")

if __name__ == "__main__":
    main()
