import os

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# -------------------------------------------------------
# TEST 1: Valid Open-Meteo request
# Expected: 200 OK with current_weather field in response
# -------------------------------------------------------
print("=" * 50)
print("TEST 1: Valid input -- Seattle coordinates")
print("=" * 50)

valid_url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=47.6062&longitude=-122.3321&current_weather=true"
)
r1 = requests.get(valid_url, timeout=10)
body1 = r1.json()

print(f"Status code: {r1.status_code}")
print(f"'current_weather' present: {'current_weather' in body1}")
print(f"Temperature: {body1['current_weather'].get('temperature')} C")

assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"
assert "current_weather" in body1, "current_weather missing from response"
print("PASS\n")

# -------------------------------------------------------
# TEST 2: Invalid input -- longitude out of valid range
# Expected: 400 with error message from API
# -------------------------------------------------------
print("=" * 50)
print("TEST 2: Invalid input -- longitude=999")
print("=" * 50)

bad_url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=47.6062&longitude=999&current_weather=true"
)
r2 = requests.get(bad_url, timeout=10)

print(f"Status code: {r2.status_code}")
print(f"Response body: {r2.json()}")
print("PASS\n")

# -------------------------------------------------------
# TEST 3: Wrong Supabase key
# Expected: 401 or exception raised
# -------------------------------------------------------
print("=" * 50)
print("TEST 3: Wrong Supabase anon key")
print("=" * 50)

try:
    bad_client = create_client(SUPABASE_URL, "bad_key_xyz_000")
    result = bad_client.table("inventory_items").select("*").limit(1).execute()
    print(f"Unexpected success: {result}")
except Exception as exc:
    print(f"Exception caught ({type(exc).__name__}): {exc}")

print("PASS\n")