from fastapi import FastAPI
from typing import Any, Dict
from jsonpath_ng import parse
import requests

app = FastAPI()

#url_static_test = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/static"
#url_dynamic_test = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-helsinki/dynamic"

# the URL will change between the /v1/ and /static/ || /dynamic
# example1: https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/fafas/dynamic
# example2: https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/mcdonalds/dynamic
# example3: https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/habibs/static

def parsing_info(unparsed_json: Dict[str, Any]) -> Dict[str, Any]:
	return {}


def construct_url(venue_slug: str, endpoint_type: str, base_url: str) -> str:
	if (endpoint_type == "static"):
		url = f"{base_url}/{venue_slug}/{endpoint_type}"
	elif (endpoint_type == "dynamic"):
		url = f"{base_url}/{venue_slug}/{endpoint_type}"
	if (endpoint_type or endpoint_type.strip().lower() not in {"static", "dynamic"}):
		raise ValueError("Error: endpoint type not supported. SUPPORTED ENDPOINT TYPES: DYNAMIC && STATIC")
	return (url)

@app.get("/api/v1/delivery-order-price")
def read_json(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
	base_url = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues"
	url_static = construct_url(venue_slug, "static", base_url)
	url_dynamic = construct_url(venue_slug, "dynamic", base_url)
	try:
		response = requests.get(url_static)
		response.raise_for_status()
	except requests.exceptions.RequestException:
		try:
			response = requests.get(url_dynamic)
			response.raise_for_status()
		except requests.exceptions.RequestException as e:
			return {"Error": str(e), "message": "Both endpoints failed"}
		## PARSE HERE
		data = parsing_info(response)
		## CALCULATE STUFF HERE

		answer = data.json()
		return {"source": "dynamic", "data": answer}