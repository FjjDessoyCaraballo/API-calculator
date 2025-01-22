from fastapi.testclient import TestClient
from dopc import app

client = TestClient(app)

def test_api_success():
    """Test if the API returns a successful response for a valid request."""
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 60.1699,  # Helsinki
        "user_lon": 24.9384
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "total_price" in data
    assert "delivery" in data
    assert "fee" in data["delivery"]

def test_api_too_far():
    """Test if the API correctly returns an error for an out-of-range location."""
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "home-assignment-venue-helsinki",
        "cart_value": 1000,
        "user_lat": 0,  # Very far away, therefore will fail
        "user_lon": 0
    })
    
    assert response.status_code == 200  # FastAPI still returns 200 but with an error message
    data = response.json()
    assert "Error" in data
    assert "User is too far away" in data["Error"]
    
    """ WHY IT PASSES THE TESTS EVEN WITH FAULTY PARAMETERS?
    Even though it is an error, the test passes because it show that
    we are handling it. If the tester would fail, it means that our error handling
    is incorrect """

def test_api_venue():
    """Test if the API returns a successful response for a valid request."""
    response = client.get("/api/v1/delivery-order-price", params={
        "venue_slug": "invalid",
        "cart_value": 1000,
        "user_lat": 60.1699,  # Helsinki
        "user_lon": 24.9384
    })
    
    assert response.status_code == 200
    data = response.json()