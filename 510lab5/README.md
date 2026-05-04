# TECHIN 510 Lab 5 -- APIs, Databases & Full-Stack Transition

**Student:** Davi Dai

---

## Apps

| File | Purpose |
|------|---------|
| `app.py` | GIX Return Processor (Component B) |
| `events.py` | GIX Events Board (Component E) |

**Deployment:** https://510lab5-[your-url].streamlit.app/

---

## Local Setup

```bash
pip install -r requirements.txt

# Create .env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=your-anon-key

streamlit run app.py       # Inventory tool
streamlit run events.py    # Events board
```

---

## Supabase Schema

### Table: `inventory_items`

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key, auto-generated |
| original_name | text | Raw product title from CSV |
| clean_name | text | Staff-trimmed short name |
| asset_tag_id | text | 8-digit string (e.g. 10000001) |
| category | text | IT / Maker Space / Discard |
| location | text | IT Shop / Maker Space / N/A |
| model_serial | text | Optional, high-value items |
| created_at | timestamptz | Auto-set on insert |

### Table: `events`

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | Primary key |
| title | text | Event name |
| description | text | Short summary |
| category | text | Workshop / Guest Lecture / Career / Social |
| event_date | date | YYYY-MM-DD |
| location | text | Room or building |
| created_at | timestamptz | Auto-set on insert |

---

## Component E: Testing

### Assert statements

```python
assert isinstance(events, list), "Events response must be a list"
assert all("title" in e for e in events), "One or more events is missing a title"
```

### Error scenario tests

| # | What I did | Expected | Actual |
|---|-----------|----------|--------|
| 1 | Set wrong Supabase key in .env | st.error() shown, app stops | Exception caught, error message displayed, st.stop() called |
| 2 | Filtered a category with no events | Empty state message, no crash | st.info("No upcoming events in this category.") shown |
| 3 | Blocked network, reloaded app | Timeout caught, graceful message | "Request timed out" error shown, app stopped cleanly |

---

## Security

- All secrets loaded via `os.getenv()` from `.env`
- `.env` is in `.gitignore`
- Streamlit Cloud: secrets stored in Settings > Secrets
- No keys hardcoded in any source file