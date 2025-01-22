import pytest
from price_calculator import delivery_price_calculator, too_far_away

cart_value = 1000
base_price = 190
venue_slug = "home-assignment-venue-helsinki"

@pytest.fixture
def calculator():
    """Fixture to create a delivery_price_calculator instance."""
    return delivery_price_calculator("home-assignment-venue-helsinki")

def test_haversine(calculator):
    """Test if the Haversine function correctly calculates distance."""
    lat1, lon1 = 60.1699, 24.9384  # Helsinki
    lat2, lon2 = 60.1921, 24.9458  # Near Helsinki
    distance = calculator._haversine(lat1, lon1, lat2, lon2)
    
    assert isinstance(distance, (int, float))  # Distance should be a number
    assert distance > 0  # Distance should be positive

def test_too_far_away(calculator):
    """Test that an exception is raised when a user is too far away."""
    with pytest.raises(too_far_away):
        calculator.calculate_delivery_price(cart_value=1000, user_lat=0, user_lon=0)
        
def test_price_in_range_1():
    """Test price calculation for distance range 0-500 meters.""" 
    user_lat = 60.1706
    user_lon = 24.9285

    calculator = delivery_price_calculator(venue_slug)
    result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)
    
    compare = cart_value + result["delivery"]["fee"]
    assert result["total_price"] == compare

def test_price_in_range_2():
    """Test price calculation for distance range 500-1000 meters."""
    user_lat = 60.1800
    user_lon = 24.9380

    calculator = delivery_price_calculator(venue_slug)
    result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)

    compare = cart_value + result["delivery"]["fee"]
    assert result["total_price"] == compare

def test_price_in_range_3():
    """Test price calculation for distance range 1000-1500 meters."""
    user_lat = 60.173667
    user_lon = 24.959982

    calculator = delivery_price_calculator(venue_slug)
    result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)
    
    compare = cart_value + result["delivery"]["fee"]
    assert result["total_price"] == compare


def test_type_safety():
    """Test if the parameters and return values are of the correct types."""
    user_lat = 60.1706
    user_lon = 24.9285

    calculator = delivery_price_calculator(venue_slug)
    result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)

    # Ensure types of critical return values
    assert isinstance(result["total_price"], int)
    assert isinstance(result["small_order_surcharge"], int)
    assert isinstance(result["delivery"]["fee"], int)
    assert isinstance(result["delivery"]["distance"], int)


def test_surcharge_applied():
    """Test if surcharge is applied when cart value is below the threshold."""
    cart_value = 400  # Below surcharge threshold
    user_lat = 60.1706
    user_lon = 24.9285

    calculator = delivery_price_calculator(venue_slug)
    result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)

    assert result["total_price"] == cart_value + result["small_order_surcharge"] + result["delivery"]["fee"]
    assert result["small_order_surcharge"] > 0  # Surcharge applied

def test_surcharge_not_applied():
    """Test if surcharge is not applied when cart value exceeds the threshold."""
    cart_value = 1200  # Above surcharge threshold
    user_lat = 60.1706
    user_lon = 24.9285

    calculator = delivery_price_calculator(venue_slug)
    result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)

    assert result["total_price"] == cart_value + result["delivery"]["fee"]
    assert result["small_order_surcharge"] == 0  # No surcharge

    assert result["small_order_surcharge"] == 0

def test_invalid_venue_slug():
    """Test if an invalid venue_slug results in an error."""
    venue_slug_invalid = "invalid-venue"
    user_lat = 60.1706
    user_lon = 24.9285

    try:
        calculator = delivery_price_calculator(venue_slug_invalid)
        result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)
        assert False, "Expected RuntimeError due to invalid venue"
    except RuntimeError as e:
        assert "404 Client Error:" in str(e)

def test_invalid_lat_lon():
    """Test if we are able to detect the type error"""
    cart_value = 100
    user_lat = "invalid"  # Invalid latitude
    user_lon = 24.0

    try:
        calculator = delivery_price_calculator(venue_slug)
        result = calculator.calculate_delivery_price(cart_value, user_lat, user_lon)
        assert False, "Expected TypeError due to invalid coordinates"
    except TypeError:
        pass

