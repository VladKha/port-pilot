import http.client
import json
import os
from dotenv import load_dotenv
from typing import Optional
from smolagents import tool

load_dotenv()

@tool
def maps_search(query: str, country: Optional[str] = None) -> list:
    """
    Performs a google maps web search for your query then returns a list of top location results

    Args:
        query (str): The search query
        country (str, optional): The country code (e.g., 'sg' for Singapore).
    
    Returns:
        list: top location search results, each location is a dict, e.g.:
        {
            "position": 1,
            "title": "Cupertino",
            "address": "CA",
            "latitude": 37.322997799999996,
            "longitude": -122.03218229999999,
            "category": "California",
            "website": "http://www.cupertino.org/",
            "cid": "4129026671718267060"
        }
    """
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": query,
        "gl": country
    })
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    
    conn.request("POST", "/places", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))['places']

# Example usage
if __name__ == "__main__":
    # result = maps_search("Antler VC", "sg")
    result = maps_search("Apple Inc headquarters", "US")
    print(json.dumps(result, indent=2))
