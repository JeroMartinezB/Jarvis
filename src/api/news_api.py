import requests

def jarvis_news():
    url = "https://newsdata.io/api/1/latest?apikey=pub_11a3df7823c14731b12a43ba5ad5ff5b&country=us&language=en&category=business,breaking,entertainment,technology,politics"
    response = requests.get(url)
    data = response.text
    return data