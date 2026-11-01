import requests
import os

api_key = os.environ.get("BRAVE_API_KEY")

def read_paper(title: str) -> str:
    print(title)
    try:
        headers = {
            "x-subscription-token": api_key
        }
        params = {"q": "\"" + title + "\" filetype:pdf", "count": 1}

        response = requests.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params=params)
        response = response.json()
        if response.get("query", {}).get("bad_results"):
            params["q"] = response["query"]["cleaned"]
            response = requests.get("https://api.search.brave.com/res/v1/web/search", headers=headers, params=params)
            response = response.json()
        print(response)

        results = response["web"]["results"]
        result = results[0]
        req = requests.get(result["url"])
        return req.content.decode("utf-8")
    except Exception as e:
        print(e)
        return None
