import os
import json
import re
from bs4 import BeautifulSoup, Comment
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_project.myspider.spiders.website_spider import WebsiteSpider
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
from multiprocessing import Process
from app.services.storage import store_documents
from langchain.schema import Document


def clean_text(raw_text):
    """
    Cleans raw HTML content by removing unwanted JavaScript, CSS, tags, tracking scripts, and other noise.
    """
    # Parse HTML and extract visible text
    soup = BeautifulSoup(raw_text, "html.parser")

    # Remove script and style elements
    for element in soup(["script", "style", "noscript", "iframe", "link", "meta"]):
        element.extract()

    # Remove HTML comments
    comments = soup.findAll(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Extract text and normalize spaces
    text = soup.get_text(separator=" ", strip=True)

    # Remove JavaScript, CSS, and other inline styles/content
    text = re.sub(r'window\.\S+|document\.\S+|var\s+\w+|function\s*\(.*?\)', '', text, flags=re.DOTALL)
    text = re.sub(r'@media.*?\{.*?\}', '', text, flags=re.DOTALL)  # Remove media queries
    text = re.sub(r'@media *?\{.*?\}', '', text, flags=re.DOTALL)  # Remove media queries
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'\{.*?\}', '', text, flags=re.DOTALL)  # Remove JSON-like content
    text = re.sub(r'<.*?>', '', text, flags=re.DOTALL)  # Remove remaining HTML tags

    # Remove tracking codes and noise
    text = re.sub(r'utm_[a-z]+=[^&\s]+', '', text)  # Remove UTM tracking parameters
    text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII characters
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces into one
    text = re.sub(r'\\n|\\t', '', text)  # Remove escaped newlines and tabs
    text = re.sub(r'(©|®|™|\d{4}-\d{4})', '', text)  # Remove copyright symbols and year ranges

    # Trim and return cleaned text
    return text.strip()

def crawl_and_process_website(customer_id, website_url):
    """
    Runs the crawler for the given website and processes the crawled data.
    Stores the cleaned data in Redis for retrieval.
    """
    # Run Scrapy in a subprocess
    process = Process(target=_run_crawler, args=(customer_id, website_url))
    process.start()
    process.join()

    # Process the crawled data and store it in Redis
    data_path = f"data/{customer_id}.jsonl"  # JSON Lines format
    if os.path.exists(data_path):
        documents = []
        with open(data_path, 'r') as f:
            for line in f:
                try:
                    # Parse each line as JSON
                    item = json.loads(line)
                    raw_text = item.get("text", "").strip()
                    url = item.get("url", "").strip()

                    if raw_text and url:
                        # Clean the text before storing
                        cleaned_text = clean_text(raw_text)

                        # Skip if cleaned_text becomes empty after cleaning
                        if cleaned_text:
                            documents.append(
                                Document(
                                    page_content=cleaned_text,
                                    metadata={"url": url}
                                )
                            )
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON line: {e}")

        # Store documents in Redis
        if documents:
            store_documents(customer_id, documents)
            print(f"Documents successfully stored for customer {customer_id} in Redis.")
        else:
            print(f"No valid documents to store for customer {customer_id}.")
    else:
        print(f"No crawled data found for customer {customer_id}. Skipping Redis storage.")


def _run_crawler(customer_id, website_url):
    """
    Configures and starts the Scrapy crawler for the specified website.
    """
    configure_logging()  # Configures Scrapy's logging
    settings = get_project_settings()
    settings.update({
        "LOG_ENABLED": True,
        "FEED_FORMAT": "jsonlines",  # Use JSON Lines for better compatibility
        "FEED_URI": f"data/{customer_id}.jsonl"  # Write as .jsonl
    })

    process = CrawlerProcess(settings)
    process.crawl(WebsiteSpider, start_url=website_url)

    try:
        process.start(stop_after_crawl=True)
    except Exception as e:
        print(f"Error running crawler: {e}")
