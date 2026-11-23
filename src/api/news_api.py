import os
import requests
from dotenv import load_dotenv

load_dotenv()

def jarvis_news():
    news_api = os.getenv("NEWS_API")
    url = "https://newsdata.io/api/1/latest?apikey="+news_api+"&country=us,co&language=en&category=breaking,technology,science,sports,politics"
    response = requests.get(url)
    data = response.text
    return data