from fastapi import FastAPI
from price_calculator import delivery_price_calculator, too_far_away

app = FastAPI()

def type_check(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
    if not isinstance(venue_slug, str):
        raise TypeError(f"venue_slug should be str, got {type(venue_slug).__name__}")
    if not isinstance(cart_value, int):
        raise TypeError(f"cart_value should be int, got {type(cart_value).__name__}")
    if not isinstance(user_lat, float):
        raise TypeError(f"user_lat should be float, got {type(user_lat).__name__}")
    if not isinstance(user_lon, float):
        raise TypeError(f"user_lon should be float, got {type(user_lon).__name__}")
    return 0

@app.get("/api/v1/delivery-order-price")
def dopc(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
    try:
        error_type = type_check(venue_slug, cart_value, user_lat, user_lon)
        if error_type != 0:
            return {"Error": error_type}
        calculator = delivery_price_calculator(venue_slug)
        result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)
        return result
    except too_far_away as e:
        return {"Error": str(e)}
    except TypeError as e:
        return {"Error": str(e)}
    except RuntimeError as e:
        return {"Error": str(e)}

