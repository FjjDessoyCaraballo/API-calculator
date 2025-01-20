from fastapi import FastAPI
from typing import Any, Dict, List
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError
import requests

app = FastAPI()

def safe_parse(path: str, data: Dict[str, Any]):
	try:
		return parse(path).find(data)[0].value
	except (IndexError, JsonPathParserError):
		return None


def parsing_info(data_static: Dict[str, Any], data_dynamic: Dict[str, Any]) -> Dict[str, Any]:
	coordinates: List[float] = safe_parse("$.venue_raw.location.coordinates", data_static)
	surcharge: int = safe_parse("$.venue_raw.delivery_specs.order_minimum_no_surcharge", data_dynamic)
	base_price: int = safe_parse("$.venue_raw.delivery_specs.delivery_pricing.base_price", data_dynamic)
	distance_ranges: List[Dict[str, Any]] = safe_parse("$.venue_raw.delivery_specs.delivery_pricing.distance_ranges", data_dynamic)
	return {"coordinates": coordinates, 
		 "small_order_surcharge": surcharge, 
		 "base_price": base_price, 
		 "distance_range": distance_ranges}

@app.get("/api/v1/delivery-order-price")
def read_json(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
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
	data_static: Dict[str, Any] = response_static.json()
	data_dynamic: Dict[str, Any] = response_dynamic.json()
	## PARSE HERE
	parsed_data: Dict[str, Any] = parsing_info(data_static, data_dynamic)
	print(parsed_data)
	## CALCULATE STUFF HERE
	
	return parsed_data
	

#must return:
# {
#   "total_price": 1190,
#   "small_order_surcharge": 0,
#   "cart_value": 1000,
#   "delivery": {
#     "fee": 190,
#     "distance": 177
#   }
# } #(made up values)
