import requests

def search_openalex(query):
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per_page": 1,
        "page": 1,
        "select": "title,relevance_score,publication_date,ids,open_access,has_fulltext,cited_by_count,is_retracted,referenced_works,related_works,updated_date",
    }
    rsp = requests.get(url, params=params)
    return rsp.json()
