import requests

def search_crossref(query):
    url = "https://api.crossref.org/v1/works"
    params = {
        "query": query,
        "rows": 1,
    }
    rsp = requests.get(url, params=params)
    return rsp.json()["message"]["items"][0]
