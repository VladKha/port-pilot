import os
from pprint import pprint
from typing import Optional

import pandas as pd
import requests
from smolagents import tool
from dotenv import load_dotenv

load_dotenv()

FREIGHTOS_API_KEY = os.getenv("FREIGHTOS_API_KEY")

# Shipping mode mapping dictionary
SHIPPING_MODE_MAP = {
    "LCL": "LCL (Less than Container Load)",
    "FCL": "FCL (Full Container Load)",
    "LTL": "LTL (Less than Truckload)",
    "FTL": "FTL (Full Truckload)"
}

def get_shipping_estimate_json(params):
    """
    Get shipping estimates using the GET endpoint with JSON response
    """
    base_url = "https://ship.freightos.com/api/shippingCalculator"

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def transform_shipping_response(response):
    """
    Transform the shipping estimate response into a pandas DataFrame.
    
    Args:
        response (dict): The raw response from Freightos API
        
    Returns:
        list: list of dicts with keys "mode", "price_range", "transit_range"
    """
    if not response or 'response' not in response:
        return pd.DataFrame(columns=['mode', 'price_range', 'transit_range'])
        
    rates = response['response'].get('estimatedFreightRates', {}).get('mode', [])
    if type(rates) == dict:
        rates = [rates]
    data = []
    
    for rate in rates:
        mode = rate['mode']
        # Map the mode to its full name if it exists in the mapping
        mode = SHIPPING_MODE_MAP.get(mode, mode)
        price_min = rate['price']['min']['moneyAmount']['amount']
        price_max = rate['price']['max']['moneyAmount']['amount']
        currency = rate['price']['min']['moneyAmount']['currency']
        transit_min = rate['transitTimes']['min']
        transit_max = rate['transitTimes']['max']
        
        price_range = f"{price_min} - {price_max} {currency}"
        transit_range = f"{transit_min} - {transit_max} days"
        
        data.append({
            'mode': mode,
            'price_range': price_range,
            'transit_range': transit_range
        })
    
    return data

@tool
def get_shipping_estimate(origin: str, destination: str = None,
                          weight: float = 1, width: Optional[float] = 100,
                          length: Optional[float] = 100, height: Optional[float] = 100, quantity: Optional[int] = 1) -> list:
    """
    Get shipping estimates for delivery between origin and source according to shippment parameters.
    Returns a list of estimates with shipping mode, price range, transit time range.

    Args:
        origin (str): Any address recognized by Google maps / three letter airport code / 5 letter UN seaport code (for FOB). Required.
        destination (str): Any address recognized by Google maps e.g. a zip code "10002" or street address / three letter IATA airport code / 5 letter UN seaport code. Optional - if omitted, Freightos will use GEO-IP to use a city near the caller as destination (useful for e-commerce).
        weight (float): Weight in kg per load unit. Default is 1.
        width (float): Width in cm. Default is 100.
        length (float): Length. Default is 100.
        height (float): Height in cm. Default is 100.
        quantity (int, optional): Number of load units. Default is 1.

    Returns:
        list: list of estimates, each containing:
        - mode: Shipping mode (e.g., 'air', 'express', 'LCL')
        - price_range: String in format "min - max CURRENCY"
        - transit_time_range: String in format "min - max days"

    Example:
        >>> result = get_shipping_estimate("Shanghai,China", "NewYork,NY", 1000, 10, 10, 5, 1)
        >>> print(result)
           [
               {
                   "mode": "air",
                   "price_range": "4162.5 - 16420.35 USD",
                   "transit_time_range": "3 - 16 days"
               },
               {
                   "mode": "express",
                   "price_range": "5535 - 18297.5 USD",
                   "transit_time_range": "1 - 35 days"
               },
               {
                   "mode": "LCL",
                   "price_range": "1202.48 - 1868.15 USD",
                   "transit_time_range": "25 - 73 days"
               }
           ]
    """
    params = {
        "loadtype": "boxes",
        "weight": weight,
        "width": width,
        "length": length,
        "height": height,
        "origin": origin,
        "quantity": quantity,
        "destination": destination,
    }

    response = get_shipping_estimate_json(params)
    return transform_shipping_response(response)

def main():
    # Example 1: GET request for door-to-door boxes with JSON response
    # print("Example 1: GET request for door-to-door boxes (JSON)") #container 40 (JSON)") #door-to-door boxes (JSON)")
    # params = {
    #     "loadtype": "boxes", #"container40",
    #     "weight": 1000,
    #     "width": 10,
    #     "length": 10,
    #     "height": 5,
    #     "origin": "128 Prinsep St, Singapore", #"Shanghai,China",
    #     "quantity": 1,
    #     "destination": "One Apple Park Way, Cupertino, California" #"NewYork,NY"
    # }
    #
    # json_response = get_shipping_estimate_json(params)
    # if json_response:
    #     print(json.dumps(json_response, indent=2))
    #     print("\n")

    # Example 2: GET request for door-to-door container
    # Test multiple shipping scenarios
    test_params = [
        {"origin": "Shanghai,China", "destination": "NewYork,NY", "weight": 1000, "width": 10, "length": 10, "height": 5, "quantity": 1},
        {"origin": "Shanghai,China", "destination": "Los Angeles,CA", "weight": 500, "width": 8, "length": 8, "height": 4, "quantity": 1},
        {"origin": "Singapore", "destination": "London,UK", "weight": 2000, "width": 12, "length": 15, "height": 8, "quantity": 2},
        {"origin": "Tokyo,Japan", "destination": "Sydney,Australia", "weight": 1500, "width": 10, "length": 12, "height": 6, "quantity": 1},
        {"origin": "Dubai,UAE", "destination": "Amsterdam,Netherlands", "weight": 3000, "width": 15, "length": 20, "height": 10, "quantity": 3},
        {"origin": "Mumbai,India", "destination": "Hamburg,Germany", "weight": 800, "width": 9, "length": 11, "height": 5, "quantity": 1},
        {"origin": "Seoul,South Korea", "destination": "Vancouver,Canada", "weight": 1200, "width": 11, "length": 13, "height": 7, "quantity": 2},
        {"origin": "Hong Kong", "destination": "San Francisco,CA", "weight": 1800, "width": 13, "length": 16, "height": 9, "quantity": 2},
        {"origin": "Bangkok,Thailand", "destination": "Melbourne,Australia", "weight": 600, "width": 7, "length": 9, "height": 4, "quantity": 1},
        {"origin": "Shenzhen,China", "destination": "Rotterdam,Netherlands", "weight": 2500, "width": 14, "length": 18, "height": 9, "quantity": 3},
        {"origin": "Taipei,Taiwan", "destination": "Seattle,WA", "weight": 900, "width": 9, "length": 12, "height": 6, "quantity": 1}
    ]

    print("Testing multiple shipping scenarios:")
    for i, params in enumerate(test_params, 1):
        print(f"\nScenario {i}:")
        print(f"From {params['origin']} to {params['destination']}")
        result = get_shipping_estimate(
            params['origin'],
            params['destination'],
            params['weight'],
            params['width'],
            params['length'],
            params['height'],
            params['quantity']
        )
        pprint(result)
        print("-" * 50)


if __name__ == "__main__":
    main()
