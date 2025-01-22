# Delivery Order Price Calculator service (DOPC)

## How to use

First you must create a virtual environment:

```bash
$> python3 -m venv fastapi-env
$> source fastapi-env/bin/activate
```

The virtual environment is necessary so the person using this application can use it without any external dependencies affecting the it.

When you is done with the task at hand, you can enter in terminal:

```bash
$> deactivate
```

However, since we barely started, we will run the command `uvicorn`:

```bash
$> uvicorn dopc:app --reload
```

A quick breakdown of what this line is doing:

- **uvicorn**: ASGI server implementation, using uvloop and httptools;
- **dopc:app**: dopc is the name of our endpoint, and app is the FastAPI instance created inside the code (`app = FastAPI()`);
- **--reload**: this flag enables auto-reload, so you can check the result of your changes directly in `postman` or web browser.

For future use, I have devised a class `delivery_price_calculator` that can be instantiated in different end points whenever the need arises. To use the DOPC you only needs to go to a web browser (after setting up all the necessary dependencies in a python virtual environment), and type:

```markdown
http://localhost:8000/api/v1/delivery-order-price?venue_slug=<your_venue>&cart_value=<value_of_cart>&user_lat=<user_lat_coord>&user_lon=<user_lon_coord>
```

It is a lot of information, but we can break it down into five parts (arrows are unnecessary when entering actual keys/values):

1. **The base address**: `http://localhost:8000/api/v1/delivery-order-price`
2. **Venue slug (parameter -> string)**: `venue_slug=<your_venue>`
3. **Cart value (parameter -> integer)**: `cart_value=<value_of_cart>`
4. **User latitude (parameter -> float)**: `user_lat=<user_lat_coord>`
5. **User longitude (parameter -> float)**: `user_lon=<user_lon_coord>`

> After the base URL you should input `?` before adding the parameters, and add `&` between every parameter

If you wishes to go about and try different parameters for testing, I recommend using [postman](https://www.postman.com/downloads/) to fasten your testing.

## Libraries that require installation

- [requests](https://realpython.com/python-requests/)
- [fastapi](https://fastapi.tiangolo.com/tutorial/)
- [jsonpath_ng](https://pypi.org/project/jsonpath-ng/) for parse and JsonPathParserError
- [jsonpath_ng.exceptions](https://pypi.org/project/jsonpath-ng/) for JsonPathParserError

Other libraries used are already native to python3.12.

## Class `price_calculator`

### Structure

The `delivery_price_calculator` class calculates the delivery fee based on a venue's location, dynamic pricing rules, and the customer's distance. It fetches venue data from the API, parses relevant details, and determines the delivery price using the Haversine formula. If the user is too far, it raises a `too_far_away` exception. The final price includes base fees, distance-based charges, and potential surcharges for small orders.

```markdown
.
├── too_far_away(Exception)
│   ├── __init__(message: str)
│
├── delivery_price_calculator
│   ├── __init__(self, venue_slug: str)
│   │   ├── static_url
│   │   ├── data_static ← _fetch_data(self.static_url)
│   │   ├── dynamic_url
│   │   ├── data_dynamic ← _fetch_data(self.dynamic_url)
│   │   └── parsed_data ← _parse_data()
│   │
│   ├── _fetch_data(self, url: str)
│   │   ├── requests.get(url)
│   │   ├── response.raise_for_status()
│   │   └── return response.json()
│   │
│   ├── _safe_parse(self, path: str, data: Dict[str, Any])
│   │   ├── parse(path).find(data)[0].value
│   │   └── return None (on exception)
│   │
│   ├── _parse_data(self)
│   │   ├── coordinates ← _safe_parse(...)
│   │   ├── small_order_surcharge ← _safe_parse(...)
│   │   ├── base_price ← _safe_parse(...)
│   │   ├── distance_ranges ← _safe_parse(...)
│   │   └── return structured data
│   │
│   ├── _haversine(self, lat1, lon1, lat2, lon2)
│   │   ├── Compute Haversine formula
│   │   └── return distance in meters
│   │
│   ├── calculate_delivery_price(self, cart_value, user_lat, user_lon)
│       ├── venue_lon, venue_lat ← parsed_data["coordinates"]
│       ├── distance ← _haversine(user_lat, user_lon, venue_lat, venue_lon)
│       ├── Iterate over distance_range:
│       │   ├── If max_dist == 0 → raise too_far_away
│       │   ├── If min_dist <= distance < max_dist → calculate fee
│       │
│       ├── If fee is None → raise too_far_away
│       ├── Compute total_price
│       └── return final pricing details
```

## Error handling and testing

For most of the exceptions I have used the standard exceptions. However, there was a necessity to throw an exception for whenever the user could be in a range where `max == 0`, meaning that there is no service coverage. Therefore, I have devised the exception `too_far_away` that is thrown after calculating the distance and checking the `price_ranges`.

For testing, you can go `tests` directory and use the command `pytest` in terminal:

```bash
$> pytest
```

After the test, the result should look like the example below:

```bash
=========================================== test session starts ===========================================
platform linux -- Python 3.12.3, pytest-8.3.4, pluggy-1.5.0
rootdir: /home/fdessoy/projects/wolt_challenge/tests
plugins: anyio-4.8.0
collected 12 items                                                                                        

test_api.py ..                                                                                      [ 16%]
test_delivery.py ..........                                                                         [100%]

=========================================== 12 passed in 7.99s ============================================
```
