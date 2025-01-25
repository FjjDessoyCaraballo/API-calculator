from fastapi import FastAPI
from price_calculator import delivery_price_calculator, too_far_away
# from schemas import delivery_order_request

app = FastAPI()

@app.get("/api/v1/delivery-order-price")
def dopc(venue_slug: str, cart_value: int, user_lat: float, user_lon: float):
    try:
        calculator = delivery_price_calculator(venue_slug)
        result = calculator.calculate_delivery_price(venue_slug, cart_value, user_lat, user_lon)
        return result
    except too_far_away as e:
        return {"Error": str(e)}
    except TypeError as e:
        return {"Error": str(e)}
    except RuntimeError as e:
        return {"Error": str(e)}

