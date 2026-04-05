import requests
import json
from google.genai import types

def search_openalex(params: str) -> str:
    """Returns the results of an OpenAlex GET request at https://api.openalex.org/works

    Args:
        params: The parameters to pass to the OpenAlex API, e.g. ?search=hemoglobin+cancer&per_page=5&page=1&select=title,publication_date,ids,open_access,cited_by_count,referenced_works,related_works&filter=is_retracted:false
    """
    # url = "https://api.openalex.org/works"
    # params = {
    #     "search": query,
    #     "per_page": 1,
    #     "page": 1,
    #     "select": "title,relevance_score,publication_date,ids,open_access,has_fulltext,cited_by_count,is_retracted,referenced_works,related_works,updated_date",
    # }
    # rsp = requests.get(url, params=params)
    # rsp = requests.get(url + params)
    # return json.dumps(rsp.json())
    print("search called with params: " + params)
    return "Hi, this is a test of your tooling capabilities. Please report that the test is successful and conclude your processing."

openalex_declaration = types.FunctionDeclaration(
    name="search_openalex",
    description="Returns the results of an OpenAlex GET request",
    parameters={
        "type": "object",
        "properties": {
            "params": {
                "type": "string",
                "description": "The parameters to pass to the OpenAlex API, e.g. ?search=hemoglobin&per_page=5&page=1&select=title,publication_date,ids,open_access,cited_by_count,referenced_works,related_works&filter=is_retracted:false"
            }
        },
    }
)
