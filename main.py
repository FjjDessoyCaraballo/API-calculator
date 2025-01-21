import math
from fastapi import FastAPI
from typing import Any, Dict, List
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError
from pydantic import BaseModel
import requests

app = FastAPI()

# Custom exception for too distant places
class TooFarAway(Exception):
	def __init__(self, message: str):
		super().__init__(message)

# simple try and except to take make code more readable
def safe_parse(path: str, data: Dict[str, Any]):
	try:
		return parse(path).find(data)[0].value
	except (IndexError, JsonPathParserError):
		return None

# parsing information from the endpoint into our dictionary
def parsing_info(data_static: Dict[str, Any], data_dynamic: Dict[str, Any]) -> Dict[str, Any]:
	coordinates: List[float] = safe_parse("$.venue_raw.location.coordinates", data_static)
	surcharge: int = safe_parse("$.venue_raw.delivery_specs.order_minimum_no_surcharge", data_dynamic)
	base_price: int = safe_parse("$.venue_raw.delivery_specs.delivery_pricing.base_price", data_dynamic)
	distance_ranges: List[Dict[str, Any]] = safe_parse("$.venue_raw.delivery_specs.delivery_pricing.distance_ranges", data_dynamic)
	return {"coordinates": coordinates, 
		 "small_order_surcharge": surcharge, 
		 "base_price": base_price, 
		 "distance_range": distance_ranges}

# Haversine formula to calculate distance between two lat/lon points
def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    # Radius of the Earth in km
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in kilometers!
    distance = R * c
	# Return in meters
    return distance * 1000

# Custom exception
def not_deliverable(max_dist: int):
	if (max_dist == 0):
		raise TooFarAway("user is not deliverable distance")

# DOPC main logic
@app.get("/api/v1/delivery-order-price")
def dopc(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
	endpoint_static = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/static"
	endpoint_dynamic = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/dynamic"
	try:
		response_static = requests.get(endpoint_static)
		response_static.raise_for_status()
	except requests.exceptions.RequestException as e:
		return {"Error": str(e), "message": "static endpoint failed"}
	try:
		response_dynamic = requests.get(endpoint_dynamic)
		response_dynamic.raise_for_status()
	except requests.exceptions.RequestException as e:
		return {"Error": str(e), "message": "both endpoints failed"}
	
	# Passing the response from the url json into a dictionary variable
	# The first column is the key, and the second column can have multiple variations (dict, int, etc)
	data_static: Dict[str, Any] = response_static.json()
	data_dynamic: Dict[str, Any] = response_dynamic.json()
	
	# parsing data
	parsed_data: Dict[str, Any] = parsing_info(data_static, data_dynamic)

	# Calculate the order sum
	## Checking distance for amount of fee
	venue_lon, venue_lat = parsed_data["coordinates"]
	base_price: int = parsed_data["base_price"]
	surcharge: int = parsed_data["small_order_surcharge"]
	distance: float = haversine(user_lat, user_lon, venue_lat, venue_lon)

	## Go through the list of distance ranges
	fee: int = 0
	deliverable = False
	for range_item in parsed_data["distance_range"]:
		min_dist = range_item["min"]
		max_dist = range_item["max"]
		if min_dist <= distance < max_dist or max_dist == 0:
			fee = base_price + range_item["a"] + round(range_item["b"] * distance / 10)
			deliverable = True
			break

	if not deliverable:
		raise TooFarAway("Area not covered by service.")
	# Calculate total price
	# fee = math.floor(fee)
	if cart_value < surcharge: ## surcharge for minimum order price applied
		total_price = cart_value + surcharge + fee
	else: ## surcharge not applied
		total_price = cart_value + fee
		surcharge = 0

	# Rounding up values
	distance = round(distance)

	return {"total_price": total_price,
		 "small_order_surcharge": surcharge, 
		 "cart_value": cart_value, 
		 "delivery": {"fee": fee, 
				"distance": distance}}

