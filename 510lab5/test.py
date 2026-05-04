import os

from dotenv import load_dotenv
from supabase import create_client

# Load credentials from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Print partial values to verify .env is loading correctly
print("SUPABASE_URL:", repr(SUPABASE_URL))
print("SUPABASE_KEY (first 20 chars):", repr(SUPABASE_KEY[:20]) if SUPABASE_KEY else None)

# Attempt to connect and query one row from inventory_items
client = create_client(SUPABASE_URL, SUPABASE_KEY)

result = client.table("inventory_items").select("*").limit(1).execute()
print("Connection successful. Sample row:", result.data)

# Also verify the events table is reachable
events_result = client.table("events").select("*").limit(1).execute()
print("Events table reachable. Sample row:", events_result.data)