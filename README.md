# wolt_challenge
my attempt at the wolt internship challenge

# Virtual Environment

A virutal environment is an isolated Python environment that allows you to install and manage packages separately from the system-wide python installation. This helps prevent conflicts between different projects.

Some of the projects may use different packages and running different projects with the same packages can lead to a number of problems.

When you activate a virtual environment (such as below), you're telling your terminal to use the Python and pip inside that environment, rather than the system-wide versions:

```bash
$> python3 -m venv fastapi-env
$> source fastapi-env/bin/activate
```

### **Why Use a Virtual Environment?**

1. **Avoid Dependency Conflicts**
    - Different projects may require different versions of the same library. A virtual environment ensures each project has its own dependencies.
2. **Prevent System-Wide Changes**
    - Installing packages globally (`pip install ...`) can clutter your system and cause conflicts.
3. **Reproducibility**
    - You can create a `requirements.txt` file listing all dependencies, making it easy to share and deploy your project.

## How to quit the environment

To quit (deactivate) the virtual environment, the user just needs to run:

```bash
$> deactivate
```

After this, the terminal will switch  back to using the system-wide python environment.

## Setting `uvicorn`

With the virtual environment running, set the command uvicorn to run on the background:

```bash
$> uvicorn main:app --reload
```

- `main`: The name of your Python file (without the `.py` extension).
- `app`: The FastAPI instance you created in your code (`app = FastAPI()`).
- `--reload`: This option automatically restarts the server when you make changes to your code, which is very helpful during development.

**5. View the Output**

- Open your web browser and go to `http://127.0.0.1:8000`. You should see the `{"message": "Hello World"}` output.
- FastAPI also provides automatic interactive API documentation. Go to `http://127.0.0.1:8000/docs` to see it.

# The endpoint response

```json
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```

- `total_price` (integer): The calculated total price
- `small_order_surcharge` (integer): The calculated small order surcharge
- `cart_value` (integer): The cart value. This is the same as what was got as query parameter.
- `delivery` (object): An object containing:
    - `fee` (integer): The calculated delivery fee
    - `distance` (integer): The calculated delivery distance in meters

##### all money related stuff is in cents

Information about venues:

- static: `https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/<VENUE SLUG>/static`
- dynamic: `https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/<VENUE SLUG>/dynamic`

### INFO INSIDE THE STATIC LINK (static)

```json
{
  "venue": {
    "id": "66fe419cd46e8b9f53fd6e5c",
    "image_url": "https://image-resizer-proxy.development.dev.woltapi.com/assets/677fab0c2e9a6361713418b6",
    "image_blurhash": "j2jQRa00hGTt;;gPmXKGcPTsPbpl",
    "brand_logo_image_url": null,
    "brand_logo_image_blurhash": null,
    "brand_slug": null,
    "brand_name": null,
    "name": "Home Assignment Venue Helsinki",
    "description": "This is a venue that's used in engineering home assignment. Please don't modify!",
    "rating": null,
    "opening_times_schedule": [
      {
        "day": "Monday",
        "formatted_times": "All day"
      },
      {
        "day": "Tuesday",
        "formatted_times": "All day"
      },
      {
        "day": "Wednesday",
        "formatted_times": "All day"
      },
      {
        "day": "Thursday",
        "formatted_times": "All day"
      },
      {
        "day": "Friday",
        "formatted_times": "All day"
      },
      {
        "day": "Saturday",
        "formatted_times": "All day"
      },
      {
        "day": "Sunday",
        "formatted_times": "All day"
      }
    ],
    "delivery_times_schedule": [
      {
        "day": "Monday",
        "formatted_times": "All day"
      },
      {
        "day": "Tuesday",
        "formatted_times": "All day"
      },
      {
        "day": "Wednesday",
        "formatted_times": "All day"
      },
      {
        "day": "Thursday",
        "formatted_times": "All day"
      },
      {
        "day": "Friday",
        "formatted_times": "All day"
      },
      {
        "day": "Saturday",
        "formatted_times": "All day"
      },
      {
        "day": "Sunday",
        "formatted_times": "All day"
      }
    ],
    "group_order_enabled": true,
    "share_url": "https://wolt-com.development.dev.woltapi.com/fi/fin/helsinki/restaurant/home-assignment-venue-helsinki",
    "delivery_methods": [
      "takeaway",
      "homedelivery"
    ],
    "currency": "EUR",
    "active_menu": null,
    "address": "Pohjoinen Rautatiekatu 21",
    "city": "Helsinki",
    "country": "FIN",
    "type": "purchase",
    "website": null,
    "substitutions_enabled": null,
    "post_code": "00100",
    "product_line": "restaurant",
    "secondary_product_line": "none",
    "phone": null,
    "self_delivery": false,
    "timezone": "Europe/Helsinki",
    "delivery_base_price": 190,
    "delivery_geo_range": {
      "bbox": null,
      "type": "Polygon",
      "coordinates": [
        [
          [24.7779814245461, 60.0578724813272],
          [24.7369286813129, 60.0745959383841],
          [24.703160875825, 60.0949849988232],
          [24.6779802593314, 60.1182621276793],
          [24.6623679612865, 60.1435379158993],
          [24.656944289287, 60.1698444798253],
          [24.6619418362897, 60.1961721248164],
          [24.6771928796549, 60.2215079470524],
          [24.7021321081485, 60.2448749237763],
          [24.7358151428384, 60.2653699679472],
          [24.7769526414119, 60.2821994097592],
          [24.8239590262945, 60.2947104237155],
          [24.8750141051531, 60.3024170508677],
          [24.92813512, 60.3050196708878],
          [24.9812561348468, 60.3024170508677],
          [25.0323112137055, 60.2947104237155],
          [25.0793175985881, 60.2821994097592],
          [25.1204550971616, 60.2653699679472],
          [25.1541381318515, 60.2448749237763],
          [25.179077360345, 60.2215079470524],
          [25.1943284037103, 60.1961721248164],
          [25.199325950713, 60.1698444798253],
          [25.1939022787135, 60.1435379158993],
          [25.1782899806686, 60.1182621276793],
          [25.159663039907, 60.1010432601264],
          [24.7876780307155, 60.0552969841967],
          [24.7779814245461, 60.0578724813272]
        ]
      ]
    },
    "service_fee_short_description": null,
    "service_fee_estimate": null,
    "feature_croatia_currency_selection_enabled": false,
    "show_eco_packaging": false,
    "is_pickup_friendly": false,
    "age_verification_method": "age_verification",
    "trader_information": null,
    "show_delivery_preestimate_by_time": false,
    "merchant": {
      "id": "66fe40dfd46e8b9f53fd6e53",
      "name": "Home Assignment merchant",
      "business_id": "home-assignment-id-123",
      "street_address": "Eteläinen Rautatiekatu 10",
      "city": "Helsinki",
      "post_code": "00100",
      "country": "Finland"
    },
    "digital_services_act_information": {
      "name": "Home Assignment merchant",
      "business_id": "home-assignment-id-123",
      "address": "Eteläinen Rautatiekatu 10, 00100, Helsinki, Finland",
      "self_certification": "The Partner is committed to only offering products and/or services that comply with the applicable laws.",
      "report_item_url": "https://www.surveymonkey.com/r/VHFTCJX"
    },
    "slug": "home-assignment-venue-helsinki",
    "venue_supports_wolt_pay": false,
    "group_order_id": null,
    "info": {
      "venue_info_service_fee_description": null,
      "venue_info_order_minimum": "€10.00",
      "venue_info_base_delivery_price": "€1.90"
    },
    "zero_distance_fees": {
      "delivery_price": 190
    }
  },
  "venue_raw": {
    "id": "66fe419cd46e8b9f53fd6e5c",
    "name": "Home Assignment Venue Helsinki",
    "image_url": "https://image-resizer-proxy.development.dev.woltapi.com/assets/677fab0c2e9a6361713418b6",
    "image_blurhash": "j2jQRa00hGTt;;gPmXKGcPTsPbpl",
    "brand_logo_image_url": null,
    "brand_logo_image_blurhash": null,
    "description": "This is a venue that's used in engineering home assignment. Please don't modify!",
    "group_order_enabled": true,
    "share_url": "https://wolt-com.development.dev.woltapi.com/fi/fin/helsinki/restaurant/home-assignment-venue-helsinki",
    "delivery_methods": [
      "takeaway",
      "homedelivery"
    ],
    "currency": "EUR",
    "opening_times": {
      "monday": [
        {
          "type": "open",
          "value": 0
        }
      ],
      "tuesday": [],
      "wednesday": [],
      "thursday": [],
      "friday": [],
      "saturday": [],
      "sunday": [
        {
          "type": "close",
          "value": 86400
        }
      ]
    },
    "preorder_specs": {
      "preorder_only": false,
      "time_step": 5,
      "homedelivery_spec": {
        "earliest_timedelta": 60,
        "latest_timedelta": 8,
        "preorder_times": {
          "monday": [
            {
              "type": "open",
              "value": 0
            }
          ],
          "tuesday": null,
          "wednesday": null,
          "thursday": null,
          "friday": null,
          "saturday": null,
          "sunday": [
            {
              "type": "close",
              "value": 86400
            }
          ]
        }
      },
      "takeaway_spec": {
        "earliest_timedelta": 50,
        "latest_timedelta": 8,
        "preorder_times": {
          "monday": [
            {
              "type": "open",
              "value": 0
            }
          ],
          "tuesday": null,
          "wednesday": null,
          "thursday": null,
          "friday": null,
          "saturday": null,
          "sunday": [
            {
              "type": "close",
              "value": 86400
            }
          ]
        }
      },
      "eatin_spec": null
    },
    "ncd_allowed": true,
    "tipping": {
      "currency": "EUR",
      "tip_amounts": [100, 200, 500],
      "max_amount": 2000,
      "min_amount": 50,
      "type": "pre_tipping_amount"
    },
    "delivery_note": null,
    "public_visible": false,
    "bag_fee": null,
    "comment_disabled": false,
    "short_description": null,
    "city_id": "58a462711c5ea23ce19e15ca",
    "merchant": "66fe40dfd46e8b9f53fd6e53",
    "show_allergy_disclaimer_on_menu": false,
    "price_range": 0,
    "item_cards_enabled": false,
    "service_fee_description": "Helps us improve our delivery service further by bringing you new features to enjoy and providing exceptional customer support. The service fee may vary based on order value, selected venue, or delivery method.",
    "food_tags": null,
    "allowed_payment_methods": [
      "card",
      "card_raw"
    ],
    "food_safety_reports": null,
    "is_wolt_plus": false,
    "categories": null,
    "rating": null,
    "location": {
      "bbox": null,
      "type": "Point",
      "coordinates": [24.92813512, 60.17012143]
    },
    "string_overrides": {
      "weighted_items_popup_disclaimer": null,
      "restricted_item_bottom_sheet_title": "Restricted items",
      "restricted_item_bottom_sheet_info": "Your order contains age-restricted items. Please confirm that you are of the legally required age to buy these items in your country and you are ready to show a valid photo ID at handoff.\n\nAre you allowed to purchase these items?",
      "restricted_item_bottom_sheet_confirm": "Yes, I'm allowed"
    }
  },
  "order_minimum": 1000
}
```

That is the whole content, however, we mostly care about the element inside the `venue_raw`:

```json
//[...]
"venue_raw": {
    "id": "66fe419cd46e8b9f53fd6e5c",
    "name": "Home Assignment Venue Helsinki",
    "image_url": "https://image-resizer-proxy.development.dev.woltapi.com/assets/677fab0c2e9a6361713418b6",
    "image_blurhash": "j2jQRa00hGTt;;gPmXKGcPTsPbpl",
    "brand_logo_image_url": null,
    "brand_logo_image_blurhash": null,
    "description": "This is a venue that's used in engineering home assignment. Please don't modify!",
    "group_order_enabled": true,
    "share_url": "https://wolt-com.development.dev.woltapi.com/fi/fin/helsinki/restaurant/home-assignment-venue-helsinki",
    "delivery_methods": [
      "takeaway",
      "homedelivery"
    ],
    "currency": "EUR",
    "opening_times": {
      "monday": [
        {
          "type": "open",
          "value": 0
        }
      ],
      "tuesday": [],
      "wednesday": [],
      "thursday": [],
      "friday": [],
      "saturday": [],
      "sunday": [
        {
          "type": "close",
          "value": 86400
        }
      ]
    },
    "preorder_specs": {
      "preorder_only": false,
      "time_step": 5,
      "homedelivery_spec": {
        "earliest_timedelta": 60,
        "latest_timedelta": 8,
        "preorder_times": {
          "monday": [
            {
              "type": "open",
              "value": 0
            }
          ],
          "tuesday": null,
          "wednesday": null,
          "thursday": null,
          "friday": null,
          "saturday": null,
          "sunday": [
            {
              "type": "close",
              "value": 86400
            }
          ]
        }
      },
      "takeaway_spec": {
        "earliest_timedelta": 50,
        "latest_timedelta": 8,
        "preorder_times": {
          "monday": [
            {
              "type": "open",
              "value": 0
            }
          ],
          "tuesday": null,
          "wednesday": null,
          "thursday": null,
          "friday": null,
          "saturday": null,
          "sunday": [
            {
              "type": "close",
              "value": 86400
            }
          ]
        }
      },
      "eatin_spec": null
    },
    "ncd_allowed": true,
    "tipping": {
      "currency": "EUR",
      "tip_amounts": [100, 200, 500],
      "max_amount": 2000,
      "min_amount": 50,
      "type": "pre_tipping_amount"
    },
    "delivery_note": null,
    "public_visible": false,
    "bag_fee": null,
    "comment_disabled": false,
    "short_description": null,
    "city_id": "58a462711c5ea23ce19e15ca",
    "merchant": "66fe40dfd46e8b9f53fd6e53",
    "show_allergy_disclaimer_on_menu": false,
    "price_range": 0,
    "item_cards_enabled": false,
    "service_fee_description": "Helps us improve our delivery service further by bringing you new features to enjoy and providing exceptional customer support. The service fee may vary based on order value, selected venue, or delivery method.",
    "food_tags": null,
    "allowed_payment_methods": [
      "card",
      "card_raw"
    ],
    "food_safety_reports": null,
    "is_wolt_plus": false,
    "categories": null,
    "rating": null,
    "location": {
      "bbox": null,
      "type": "Point",
      "coordinates": [24.92813512, 60.17012143]
    },
    "string_overrides": {
      "weighted_items_popup_disclaimer": null,
      "restricted_item_bottom_sheet_title": "Restricted items",
      "restricted_item_bottom_sheet_info": "Your order contains age-restricted items. Please confirm that you are of the legally required age to buy these items in your country and you are ready to show a valid photo ID at handoff.\n\nAre you allowed to purchase these items?",
      "restricted_item_bottom_sheet_confirm": "Yes, I'm allowed"
    }
  },
  "order_minimum": 1000
}
```

In specific, the `coordinates`. It goes `venue_raw` -> `coordinates`.

We need to wrangle the URL string to accept any venue:

the URL will change between the /v1/ and /static/ || /dynamic

example1: `https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/fafas/dynamic`

example2: `https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/mcdonalds/dynamic`

example3: `https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/habibs/static`
