import math
import requests
from typing import Any, Dict
from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathParserError

class too_far_away(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class delivery_price_calculator:
	BASE_URL = ""
     
	def __init__(self, venue_slug: str):
		self.static_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static"
		self.data_static = self._fetch_data(self.static_url)
		self.dynamic_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic"
		self.data_dynamic = self._fetch_data(self.dynamic_url)
		self.parsed_data = self._parse_data()
          
	def _fetch_data(self, url: str) -> Dict[str, Any]:
		try:
			response = requests.get(url)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as e:
			raise RuntimeError(f"{str(e)}")

	def _safe_parse(self, path: str, data: Dict[str, Any]):
		try:
			return parse(path).find(data)[0].value
		except (IndexError, JsonPathParserError):
			return None

	def _parse_data(self) -> Dict[str, Any]:
		coordinates = self._safe_parse("$.venue_raw.location.coordinates", self.data_static)
		surcharge = self._safe_parse("$.venue_raw.delivery_specs.order_minimum_no_surcharge", self.data_dynamic)
		base_price = self._safe_parse("$.venue_raw.delivery_specs.delivery_pricing.base_price", self.data_dynamic)
		distance_ranges = self._safe_parse("$.venue_raw.delivery_specs.delivery_pricing.distance_ranges", self.data_dynamic)
		return {
			"coordinates": coordinates,
			"small_order_surcharge": surcharge,
			"base_price": base_price,
			"distance_range": distance_ranges
		}

	def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
		R = 6371.0
		lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
		lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

		dlat, dlon = lat2_rad - lat1_rad, lon2_rad - lon1_rad
		a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
		c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
		return round(R * c * 1000)

	def _type_check(self, venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
		if not isinstance(venue_slug, str):
			raise TypeError(f"venue_slug should be str, got {type(venue_slug).__name__}")
		if not isinstance(cart_value, int):
			raise TypeError(f"cart_value should be int, got {type(cart_value).__name__}")
		if not isinstance(user_lat, float):
			raise TypeError(f"user_lat should be float, got {type(user_lat).__name__}")
		if not isinstance(user_lon, float):
			raise TypeError(f"user_lon should be float, got {type(user_lon).__name__}")
		return 0

	def calculate_delivery_price(self, venue_slug: str, cart_value: int, user_lat: float, user_lon: float) -> Dict[str, Any]:
		error_type = self._type_check(venue_slug, cart_value, user_lat, user_lon)
		if error_type != 0:
			return {"Error": error_type}
		venue_lon, venue_lat = self.parsed_data["coordinates"]
		base_price = self.parsed_data["base_price"]
		surcharge = self.parsed_data["small_order_surcharge"]
		distance = self._haversine(user_lat, user_lon, venue_lat, venue_lon)
		print(distance)
		fee = None
		for range_item in self.parsed_data["distance_range"]:
			min_dist, max_dist = range_item["min"], range_item["max"]
	        
	        # If max_dist is 0, treat it as "out of range"
			if max_dist == 0:
				raise too_far_away(f"User is too far away: {distance} meters")
	        
	        # Check if the distance falls within the current range
			if min_dist <= distance < max_dist:
				fee = base_price + range_item["a"] + round(range_item["b"] * distance / 10)
				break

			# If no valid fee was found, raise the error
		if fee is None:
			raise too_far_away("Area not covered by service.")

			# Calculate total price
		if cart_value < surcharge:
			total_price = cart_value + surcharge + fee
		else:
			total_price = cart_value + fee
			surcharge = 0

		return {
		"total_price": total_price,
		"small_order_surcharge": surcharge,
		"cart_value": cart_value,
		"delivery": {
		    "fee": fee,
		    "distance": distance
		}}
