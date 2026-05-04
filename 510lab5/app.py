import os
from io import StringIO

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# Load .env before anything else
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# set_page_config must be the first Streamlit call
st.set_page_config(page_title="GIX Return Processor", layout="wide")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase credentials not found. Add them to your .env file.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Constants ---
CATEGORIES = ["IT", "Maker Space", "Discard"]
LOCATION_MAP = {"IT": "IT Shop", "Maker Space": "Maker Space", "Discard": "N/A"}
WEATHER_ENDPOINT = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=47.6062&longitude=-122.3321&current_weather=true"
)


# --- Helper: WMO code to label ---
def describe_weather(code: int | None) -> str:
    if code is None:
        return "N/A"
    if code == 0:
        return "Clear"
    if 1 <= code <= 3:
        return "Partly cloudy"
    if 45 <= code <= 48:
        return "Foggy"
    if 51 <= code <= 67:
        return "Rain"
    if 71 <= code <= 77:
        return "Snow"
    if 80 <= code <= 82:
        return "Showers"
    if code == 95:
        return "Thunderstorm"
    return "N/A"


# --- Sidebar: Seattle weather ---
def render_sidebar_weather():
    st.sidebar.header("Seattle Weather")
    try:
        resp = requests.get(WEATHER_ENDPOINT, timeout=8)
        # Contract asserts: status and required field
        assert resp.status_code == 200, "Weather API did not return 200"
        payload = resp.json()
        assert "current_weather" in payload, "current_weather key missing"

        cw = payload["current_weather"]
        temp = cw.get("temperature", "--")
        condition = describe_weather(cw.get("weathercode"))
        st.sidebar.metric("Temp (C)", temp)
        st.sidebar.caption(condition)

    except AssertionError as exc:
        st.sidebar.warning(f"Weather check failed: {exc}")
    except requests.exceptions.Timeout:
        st.sidebar.warning("Weather request timed out.")
    except Exception:
        st.sidebar.warning("Weather unavailable.")


# --- Data helpers ---
def trim_amazon_title(raw: str) -> str:
    """Shorten verbose Amazon product names to a usable label."""
    raw = str(raw)
    # Stop at the first pipe, comma, or em-dash
    for delimiter in ["|", ",", "-"]:
        idx = raw.find(delimiter)
        if idx > 0:
            raw = raw[:idx]
    return raw.strip()[:45]


def next_tag_start(existing_df: pd.DataFrame) -> int:
    """
    Read the highest existing asset_tag_id from Supabase and
    start the new sequence one above it. Falls back to 10000001.
    """
    if existing_df.empty or "asset_tag_id" not in existing_df.columns:
        return 10000001
    try:
        max_tag = existing_df["asset_tag_id"].dropna().astype(int).max()
        return int(max_tag) + 1
    except Exception:
        return 10000001


def build_intake_table(uploaded: pd.DataFrame, start_tag: int) -> pd.DataFrame:
    """Turn the uploaded CSV into an editable intake table with pre-filled tags."""
    n = len(uploaded)
    return pd.DataFrame(
        {
            "original_name": uploaded["product_name"].astype(str),
            "clean_name": uploaded["product_name"].apply(trim_amazon_title),
            "quantity": uploaded["quantity"],
            "asset_tag_id": [f"{start_tag + i:08d}" for i in range(n)],
            "category": "IT",
            "model_serial": "",
        }
    )


def with_location(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["location"] = df["category"].map(LOCATION_MAP).fillna("N/A")
    return df


def rows_for_insert(df: pd.DataFrame) -> list[dict]:
    df = with_location(df)
    df = df.drop(columns=["quantity"], errors="ignore")
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")


def fetch_all_items(newest_first: bool = False) -> list[dict]:
    q = supabase.table("inventory_items").select("*")
    if newest_first:
        q = q.order("created_at", desc=True)
    return q.execute().data


# --- Render ---
render_sidebar_weather()

st.title("GIX Return Processor")
st.caption(
    "Process equipment returns: upload a purchase CSV, "
    "assign asset tags, categorize items, and export to BluTally."
)

intake_tab, inventory_tab, summary_tab, export_tab = st.tabs(
    ["Intake", "All Items", "Category Summary", "Export"]
)

# ===== INTAKE TAB =====
with intake_tab:
    st.subheader("Upload Return List")
    file = st.file_uploader(
        "CSV with columns: product_name, quantity",
        type=["csv"],
    )

    if file:
        try:
            raw = pd.read_csv(file)
        except Exception as exc:
            st.error(f"Could not parse file: {exc}")
        else:
            missing_cols = {"product_name", "quantity"} - set(raw.columns)
            if missing_cols:
                st.error(f"Required column(s) missing: {', '.join(sorted(missing_cols))}")
            else:
                # Determine tag start from existing inventory
                try:
                    existing = pd.DataFrame(fetch_all_items())
                    tag_start = next_tag_start(existing)
                except Exception:
                    tag_start = 10000001

                st.info(f"{len(raw)} item(s) detected. Asset tags start at {tag_start:08d}.")

                intake_df = build_intake_table(raw, tag_start)

                edited = st.data_editor(
                    intake_df,
                    use_container_width=True,
                    hide_index=True,
                    disabled=["original_name", "quantity"],
                    column_config={
                        "original_name": st.column_config.TextColumn("Amazon Title"),
                        "clean_name": st.column_config.TextColumn("Clean Name"),
                        "quantity": st.column_config.NumberColumn("Qty"),
                        "asset_tag_id": st.column_config.TextColumn("Tag ID (8-digit)"),
                        "category": st.column_config.SelectboxColumn(
                            "Category", options=CATEGORIES, required=True
                        ),
                        "model_serial": st.column_config.TextColumn("Model / Serial"),
                    },
                )

                # Preview with auto-derived location column
                preview = with_location(edited)
                st.caption("Location is set automatically from category.")
                st.dataframe(
                    preview[["asset_tag_id", "clean_name", "category", "location", "model_serial"]],
                    use_container_width=True,
                    hide_index=True,
                )

                if st.button("Confirm and Save to Supabase", type="primary"):
                    try:
                        records = rows_for_insert(edited)
                        supabase.table("inventory_items").insert(records).execute()
                        st.success(f"{len(records)} item(s) saved.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Save failed: {exc}")

# ===== ALL ITEMS TAB =====
with inventory_tab:
    st.subheader("All Inventory Items")
    try:
        items = fetch_all_items(newest_first=True)
        df = pd.DataFrame(items)
        st.metric("Total records", len(df))
        st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as exc:
        st.error(f"Could not load inventory: {exc}")

# ===== CATEGORY SUMMARY TAB =====
with summary_tab:
    st.subheader("Breakdown by Category")
    try:
        items = fetch_all_items()
        df = pd.DataFrame(items)
        if df.empty:
            st.info("No items in inventory yet.")
        else:
            counts = df.groupby("category").size().reset_index(name="count")
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(counts, use_container_width=True, hide_index=True)
            with col2:
                # One metric per category
                for _, row in counts.iterrows():
                    st.metric(row["category"], row["count"])
    except Exception as exc:
        st.error(f"Could not load summary: {exc}")

# ===== EXPORT TAB =====
with export_tab:
    st.subheader("Export BluTally CSV")
    try:
        items = fetch_all_items()
        df = pd.DataFrame(items)

        if df.empty:
            st.info("Nothing to export yet.")
        else:
            # Filter out Discard items -- they don't go into BluTally
            blutally_df = df[df["category"] != "Discard"].copy()
            st.caption(f"Excluding {len(df) - len(blutally_df)} Discard item(s) from export.")

            export = pd.DataFrame(
                {
                    "Asset Name": blutally_df.get("clean_name", ""),
                    "Asset Tag ID": blutally_df.get("asset_tag_id", ""),
                    "Status": "Available",
                    "Location": blutally_df.get("location", ""),
                    "Model/Serial Number": blutally_df.get("model_serial", ""),
                }
            )

            st.dataframe(export, use_container_width=True, hide_index=True)

            buf = StringIO()
            export.to_csv(buf, index=False)
            st.download_button(
                "Download BluTally CSV",
                data=buf.getvalue(),
                file_name="blutally_export.csv",
                mime="text/csv",
            )
    except Exception as exc:
        st.error(f"Export failed: {exc}")