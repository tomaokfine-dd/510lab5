import os

import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

st.set_page_config(page_title="GIX Events Board", layout="centered")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials not found. Check your .env file.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def load_events() -> list[dict]:
    """Fetch events from Supabase ordered by soonest date first."""
    return (
        supabase.table("events")
        .select("id,title,description,category,event_date,location")
        .order("event_date", desc=False)
        .execute()
        .data
    )


# Fetch -- three distinct failure modes handled separately
try:
    events = load_events()
except requests.exceptions.Timeout:
    # Failure mode 1: Supabase unreachable due to network timeout
    st.error("Request timed out. Please check your connection and try again.")
    st.stop()
except Exception:
    # Failure mode 2: bad credentials or unexpected Supabase error
    st.error("Could not connect to the events database. Please try again later.")
    st.stop()

# Assert the data contract: must be a list, every item must have a title
try:
    assert isinstance(events, list), "Events response must be a list"
    assert all("title" in e for e in events), "One or more events is missing a title"
except AssertionError as exc:
    st.warning(f"Unexpected data format: {exc}")

# ---- UI ----
st.title("GIX Events Board")
st.caption("Stay up to date with guest lectures, workshops, and community events at GIX.")

# Build category options from live data
all_categories = sorted({e.get("category") for e in events if e.get("category")})
col_filter, col_count = st.columns([3, 1])

with col_filter:
    selected_category = st.selectbox("Show category", ["All"] + all_categories)

filtered = (
    events
    if selected_category == "All"
    else [e for e in events if e.get("category") == selected_category]
)

with col_count:
    st.metric("Events", len(filtered))

st.divider()

# Failure mode 3: category filter returns empty result
if not filtered:
    st.info(f"No upcoming events in the '{selected_category}' category.")
else:
    for event in filtered:
        title = event.get("title", "Untitled")
        date = event.get("event_date", "Date TBD")
        category = event.get("category", "")
        description = event.get("description", "")
        location = event.get("location", "Location TBD")

        with st.container(border=True):
            header_col, tag_col = st.columns([5, 1])
            with header_col:
                st.markdown(f"### {title}")
                st.caption(f"📅 {date}  |  📍 {location}")
            with tag_col:
                st.markdown(f"`{category}`")
            if description:
                st.write(description)