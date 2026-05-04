# Week 5 Lab Manual: APIs, Databases & Full-Stack Transition


## Table of Contents

- [Overview](#overview)
- [Learning Objectives](#learning-objectives)
- [Pre-Lab Checklist](#pre-lab-checklist)
- [Component A: Staff Interview](#component-a-staff-interview)
- [Component B: Lab](#component-b-lab)
- [Component C: System Architecture & Design](#component-c-system-architecture--design)
- [Component D: Testing & Validation](#component-d-testing--validation)
- [Component E: Applied Challenge — The API Connector](#component-e-applied-challenge--the-api-connector-4050-min-individual)
- [Troubleshooting Matrix](#troubleshooting-matrix)
- [Submission](#submission)
- [Reflection](#reflection)

---

## Overview

Starting this week, you decide which tech stack fits the problem you are solving. You will integrate external APIs, set up a database, scaffold a Next.js project, and build an app that connects all three.

---

## Learning Objectives

By the end of this lab, you will be able to:

1. **Integrate external REST APIs** into an application using `fetch` or `requests`, including authentication and error handling. *(A **REST API** is a standard way for programs to exchange data over the web using URLs — you send a request to a URL and get structured data (usually JSON) back.)* 
2. **Set up a Supabase database** and perform CRUD operations (Create, Read, Update, Delete) from code
3. **Scaffold a Next.js application** and understand its file structure (`app/`, `page.tsx`, `layout.tsx`) 
4. **Justify a tech stack choice** based on user needs, not personal preference
5. **Manage environment variables** securely using `.env` files and `.gitignore`
6. **Create a system map** showing the data flow between user, frontend, API, and database, with pain points circled based on the staff interview
7. **Write assert statements for API responses**.

---

## Component A: Staff Interview 

### Guest: Maason Kao — Equipment Checkout Returns

**Maason** manages the equipment checkout and return process at GIX. His pain point centers on getting students to return checked-out equipment, using an existing workflow that spans multiple systems.


### Synthesis Artifact: System Map Sketch

After the interview, sketch the work and data flows of your interviewee, with pain points circled.

### Mark System Touchpoints

On your system map, mark every point where a **user directly interacts with the system**. A touchpoint is any moment where a person does something: clicks a button, fills out a form, reads a notification, receives an email, or makes a decision based on what they see on screen.
Pick two touchpoints, annotate:

- **Who** is the user at this point? (operations / IT staff? a student? another role?)
- **What** are they doing? (submitting a form, reading a status, making a decision)
- **What device** are they likely using? (desktop at their desk, phone while walking between buildings, tablet in a meeting)

Each touchpoint may indicate a screen or interaction your app needs to support. If the interviewee mentions checking something "on their phone while walking between buildings," that is a signal your app needs to work on a narrow screen. If they describe a workflow where two people hand off information, that may require authentication or multi-user support. These touchpoint annotations directly inform your tech stack decision framework below.

### Build Mandate

Your interview findings must directly shape what you build in Component B. Complete this sentence before writing any code:

> "Based on the interview, I will build **[specific feature/app]** because the interviewee said **[direct quote or paraphrased finding]**, which means **[design decision it drives]**."

---

## Component B: Lab

### Tech Stack Decision Framework

Starting this week, you choose your stack. Below is an example framework for choosing tech stack:

| Factor | Choose Streamlit | Choose Next.js + Supabase |
|--------|-----------------|--------------------------|
| **Users** | Single user (yourself, one stakeholder) | Multiple users need access |
| **Authentication** | Not needed | Login/signup required |
| **Data persistence** | Session-only or file-based | Data must persist across sessions and users |
| **Deployment target** | Quick demo, internal tool | Production web app |
| **Primary language** | Python-centric, data science | TypeScript/JavaScript, web development |
| **Visualization** | Heavy data viz (Plotly, charts) | Custom UI, interactive components |
| **Build speed** | Fastest for Python developers | Fastest for web developers |
| **Example** | "Show staff a dashboard of system statuses" | "Let multiple staff log incidents and track resolution" |

Write your tech stack choice for the app to be built for interviewee and a 1-sentence justification in your Spec Checkpoint.

### Constraints: 

Use Supabase as your database. Read the [docs here](https://supabase.com/docs/guides/database/overview)

Report your data schema.

Hint: Coding agents can have docs as context, which will improve your implementation experience.

---

### Responsive Design Check

Responsive design means your application looks and works well on screens of different sizes (e.g., a wide desktop monitor, a narrow phone screen). If your system map touchpoints include users on mobile devices, responsive design is not optional.

Even if all your touchpoints are desktop users, responsive design is good practice. Evaluators, instructors, and demo audiences often pull up student apps on phones or tablets.

**Step 1: Test Your App at Phone Width**

1. Open your running app in browser
2. Open DevTools
3. Select "iPhone 14 Pro" from the device dropdown (or any phone preset)
4. Reload the page

Safari can directly enter responsive design mode to inspect other screens.

**Step 2: Note What Breaks**

Check the items below (if applicable) at phone width:

| Element | Works at Phone Width? | What Breaks? |
|---------|----------------------|--------------|
| Page title -- is it fully visible? | Yes / No | |
| Navigation -- can you access all pages/sections? | Yes / No | |
| Forms -- can you fill out and submit forms? | Yes / No | |
| Tables -- can you read table content? (horizontal scrolling?) | Yes / No | |
| Charts -- are they readable? (labels visible, hover works?) | Yes / No | |
| Buttons -- are they large enough to tap with a finger? | Yes / No | |
| Text -- is the font size readable without zooming? | Yes / No | |

**Step 3: Fix the Most Critical Issue**

Pick the most severe breakage from your check and fix it. 

**Record your results.** Note what broke and what you fixed. Include this in your Component B deliverables.

---

### Deployment

**Deploy to Vercel or Streamlit Cloud (if your tech stack is Streamlit)**
- **Goal:** Deploy your app so anyone with the URL can access it.
- **Checkpoint:** The live URL works and shows your data. You have verified no secrets are exposed in the deployment.

---

### Security Checklist

Before you leave, verify:

- [ ] **No hardcoded secrets** in your code files (API keys, Supabase keys must be in `.env` / `.env.local`)
- [ ] **`.env` is in `.gitignore`** (and `.env.local` for Next.js). **For grading purpose, please submit the secrets. In the future, do not expose the secrets.**
- [ ] **Error handling** on every API call and database operation (try/except or try/catch)


---

## Component C: System Architecture & Design

---

### C.1 Architecture Concept: Client-Server Architecture (3-Tier) 

#### The Big Idea

Until now, your Streamlit apps have been **single-tier**: the code that handles the user interface, the logic, and the data all live in one Python file running on one machine. This is fast to build, but it has limits. What if two people need to use the app at the same time? What if you need data to persist after the app is closed? What if you want to separate "what the user sees" from "where the data lives"?

The answer is **client-server architecture**, and the most common form is the **3-tier model**:

1. **Presentation tier (client):** What the user sees and interacts with. In Next.js, this is the browser running your React pages.
2. **Logic tier (server):** The code that processes requests, enforces rules, and coordinates between the client and the data. In Next.js, this is your API routes.
3. **Data tier (database):** Where data is stored permanently. In this course, this is Supabase (a cloud-hosted PostgreSQL database).

If you built **Next.js + Supabase** in Component B, you moved toward a **3-tier** split:

- **Browser** (presentation): Your Next.js pages render in the user's browser
- **API routes** (logic): Next.js server-side code handles requests, validates data, talks to the database
- **Supabase** (data): Your cloud database stores data permanently, across sessions and users

If you stayed on **Streamlit** for Component B, the same *logical* layers still exist (UI, Python logic, Supabase), but they often run in **one server process** — your C.2 diagram should still show three tiers, with **Tier 2** labeled as your **Streamlit app server** (Python) instead of Next.js API routes.

Your early Streamlit-only apps ran all responsibilities in one file. Separating tiers (especially with Next.js) makes the system more powerful but also more complex.

---

### C.2 Diagramming Exercise: Draw a 3-Tier Diagram

#### Instructions

Draw a 3-tier architecture diagram for the app you built today. Show the three tiers, what lives in each one, and what flows between them.

#### Step-by-Step

1. **Draw three boxes** stacked vertically or arranged left to right. Label them:
   - **Tier 1: Browser (Client)**
   - **Tier 2: Application server (logic)** — *Next.js server / API routes* **or** *Streamlit Python server* (whichever matches your Component B stack)
   - **Tier 3: Supabase (Database)**

2. **Fill in each box** with specific components from your app:
   - Browser: Next.js `page.tsx` / React components **or** Streamlit-rendered UI, user interactions
   - Server: Next.js API routes, validation **or** Streamlit callback / Python functions that call Supabase and external APIs
   - Database: Tables you created, columns, relationships

3. **Draw arrows** between the tiers showing what data flows and in which direction. Label each arrow with the type of request or response:
   - Browser -> Server: e.g. "HTTP requests to Next.js" or "HTTP to Streamlit app"
   - Server -> Database: "SQL queries (SELECT, INSERT, UPDATE, DELETE)"
   - Database -> Server: "Query results (rows of data)"
   - Server -> Browser: "HTML/JSON responses"

4. **Add an external API** (like Open-Meteo weather) as a fourth box to the side, connected to the **Tier 2** box (your app server fetches it).

#### What to Include

- All three tiers with specific contents from YOUR app
- Arrows labeled with the type of communication (HTTP, SQL, JSON)
- Direction of data flow (requests go one way, responses come back)
- Any external APIs as a separate box connected to the server tier

#### Checkpoint

You are done when:
- [ ] Your diagram has three clearly labeled tiers with specific contents from your app
- [ ] Arrows between tiers are labeled with what flows between them
- [ ] You can point to any tier and explain what its job is in one sentence
- [ ] External APIs (if used) are shown as a separate component connected to the server tier

---

### C.3 Design Decision Log

#### The Template

| Field | Your Entry |
|-------|------------|
| **Decision** | What did you decide? |
| **Alternatives considered** | What else could you have done? |
| **Why you chose this** | What constraint drove it? |
| **Trade-off** | What did you give up? |
| **When would you choose differently?** | Under what conditions? |

#### This Week's Decision Prompt


> **Pick one architecture decision _inside_ your chosen stack and justify it.**

Choose one of these prompts:
- **Schema design:** Why did you choose this table structure (fields/relationships) for the workflow?
- **Error strategy:** Why did you handle failures this way (retry, fallback UI, user message, logging)?

Your entry should reference your **C.2 diagram** and explain how this decision affects reliability, maintainability, or user experience.

---

## Component D: Testing & Validation

> This week you integrated external APIs and set up a Supabase database. When your app depends on external services, new categories of failure emerge: the API might reject your request, return unexpected data, or demand authentication you forgot to include. This exercise introduces **contract testing** -- verifying that your app and the external service agree on what valid communication looks like.

---

### D.1 Validation Exercise: API Contract Test

#### What you are testing

**Contract testing** in software verifies that two systems agree on the format and rules of their communication:

- "I will send you a JSON object with fields `latitude` and `longitude`, both numbers"
- "You will respond with a JSON object containing a `daily` field with an array of temperatures"
- "If I send invalid data, you will respond with a 400 status code and an error message"
- "If I send no authentication, you will respond with a 401 status code"

The "contract" is the agreement about what inputs are valid, what outputs to expect, and how errors are communicated.
Today you will test 3 scenarios that cover the most common ways the contract between your app and an API/database can break:

1. **Valid input** -- Does the happy path work?
2. **Invalid input** -- Does the API reject bad data gracefully?
3. **Missing/wrong authentication** -- What happens without credentials?

#### Why this matters

- APIs change over time. A field that was optional becomes required. A response format changes. Contract tests catch these breaking changes before your users do.
- When your app integrates multiple services (an API + a database + an AI model), each integration point is a potential failure. Contract tests verify each connection independently.
- AI-generated code often makes assumptions about API response formats. A contract test verifies those assumptions are correct.

#### Instructions

Pick one API endpoint or Supabase operation from your app. 

Make a request with correct, expected input. For example:

**If testing an API:**

> **HTTP Status Codes Quick Reference:** APIs respond with numeric codes to tell you what happened. **200** = success (OK). **400** = bad request (you sent invalid data). **401** = unauthorized (missing or wrong API key). **403** = forbidden (you do not have permission). **404** = not found (wrong URL). **429** = too many requests (rate limited). **500** = server error (something broke on their end).

Record: What status code did you get? What data was returned? Does it match what you expected?


Make a request with deliberately wrong or malformed input:

Record: Did the API/database reject the bad input? What error message did you get? Does your app handle this error gracefully (user-friendly message) or does it crash?


Test what happens when credentials are missing or incorrect:

Record: Did the service correctly reject the unauthenticated request? What error was returned?

> **Note:** If your chosen API does not require authentication (like Open-Meteo), skip the auth test and instead test a third type of invalid input (e.g., empty string, extremely long string, special characters in a field).

**Step 5: Record your results**

Summarize the recorded results in the table below:

#### Recording Template

Copy this table into your submission document:

| # | Test Case | Input Description | Expected Outcome | Actual Outcome | Status Code | Pass/Fail |
|---|-----------|-------------------|-----------------|----------------|-------------|-----------|
| 1 | Valid input | _Latitude 47.61, longitude -122.33, daily forecast_ | _200 OK, JSON with daily temperatures_ | _200, received 7-day forecast data_ | _200_ | _Pass_ |
| 2 | Invalid input | _Latitude 999 (out of range)_ | _400 Bad Request or error message_ | _400, "Latitude must be in range..."_ | _400_ | _Pass_ |
| 3 | Missing auth | _Wrong Supabase anon key_ | _401 Unauthorized or connection error_ | _Exception: "Invalid API key"_ | _401_ | _Pass_ |

#### What "passing" looks like

- You tested 3 distinct scenarios (valid, invalid, missing-auth or third invalid variant)
- Each test has a clear expected outcome written BEFORE you ran the test
- Actual outcomes are documented with status codes and response details
- All 3 tests either confirm correct behavior or identify a gap in your app's error handling

#### API response asserts

Add `assert` statements (Python or TypeScript) that check the **external API** you integrated in Component B (e.g., expected keys in JSON, numeric ranges). Place them where they run when you fetch data (or in a small test file). Po

---

## Component E: Applied Challenge — The API Connector

### The Problem

GIX events — guest lectures, workshops, career panels — are scattered across emails, Slack, and flyers. No one knows what's happening this week without asking around. Design a system where events are stored in Supabase and displayed in a browsable frontend with category filters and proper error handling.

### What You Build

- A Supabase table with sample event records
- A frontend (Next.js or Streamlit) displaying events with a category filter
- A system architecture map with labeled boundaries
- Error handling for 3 failure modes
- Security verification (no hardcoded secrets)

### Part 1: Architecture & Design

Draw a **system architecture map** showing all layers from user interaction to data storage.

At each boundary between layers, label:
- The **data format** crossing that boundary
- One **potential error** that could occur at that boundary

### Part 2: Implementation

1. Create a Supabase table with a schema you design to capture event information
2. Populate your table with sample data (you create) across multiple categories
3. Build a frontend page that:
   - Fetches events from Supabase
   - Displays them in a list or card layout
   - Includes a category filter
   - Handles at least 3 error scenarios gracefully. Identify which errors are most likely for your system and document how your app responds.

### Part 3: Testing & Validation

1. **Assert statements** (2 required): Write 2 assert statements verifying your **events + Supabase** pipeline (e.g., query returns a list, required fields present after fetch). These are **in addition to** the **Component B external API** asserts listed under [Component D Deliverables](#component-d-deliverables).
2. **Error scenario tests** (3 required): Test at least 3 failure conditions. For each, document: what you did, what you expected, and what actually happened.
3. **Security check:** Verify no API keys or secrets are hardcoded in your source files. Document where your secrets are stored.

---

## Troubleshooting Matrix

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| API returns 401 Unauthorized | API key missing, expired, or wrong variable name | Check `.env` file. Verify key name matches exactly (e.g., `OPENWEATHER_API_KEY` not `OPENWEATHER_KEY`). Test with curl: `curl "https://api.example.com/data?key=YOUR_KEY"` |
| API returns 403 Forbidden | Free tier does not include this endpoint | Check API docs for free-tier endpoint restrictions |
| API returns 429 Too Many Requests | Rate limit exceeded | Wait and retry. Add caching (`@st.cache_data(ttl=300)` or local state). Check the API's rate limit docs. |
| CORS error in browser | External API blocks browser requests | Move the API call to a Next.js API route (server-side). Ask Cursor: "Move this fetch to a server-side API route." |
| `ModuleNotFoundError: No module named 'supabase'` | Package not installed in active venv | Run `pip install "supabase>=2.10.0,<3.0"`. Verify venv is activated (look for `(venv)` in terminal prompt). |
| Supabase returns empty data `[]` | Table has no rows, or RLS is blocking | Check Table Editor for rows. If RLS is on, disable it (shield icon in Table Editor). |
| `create_client() missing required argument` | `SUPABASE_URL` or `SUPABASE_KEY` is `None` | Check `.env` exists, variable names match, and `load_dotenv()` is called before `os.getenv()`. |
| `npx create-next-app` fails | Node.js not installed or below v18 | Install from [nodejs.org](https://nodejs.org). Close and reopen terminal after install. Run `node --version`. |
| `npm run dev` port-in-use error | Port 3000 already taken | Run `npx kill-port 3000` then `npm run dev`. Or use `npm run dev -- --port 3001`. |
| Vercel build fails | TypeScript error or missing dependency | Check Vercel build log. Run `npm run build` locally first. Fix errors, push again. |
| `.env.local` variables undefined in Next.js | Missing `NEXT_PUBLIC_` prefix, or dev server not restarted | Prefix client-side vars with `NEXT_PUBLIC_`. Restart the dev server after changing env files. |
| `set_page_config` error in Streamlit | Another `st.*` call runs before `set_page_config` | Move `st.set_page_config()` to immediately after imports and `load_dotenv()`, before any `st.error()` or `st.stop()`. |
| Supabase returns 403 on insert/delete | RLS enabled with no policies | In Table Editor, click your table > shield icon > toggle RLS OFF. We cover RLS in a later week. |
| `pip install supabase` build errors | Native dependencies failing to compile | Run `pip install --upgrade pip setuptools wheel` first. On Mac: `xcode-select --install`. Retry. |
| `create-next-app` hangs | Slow network during package download | Wait. If stuck, Ctrl+C, delete folder, retry. Try `npx create-next-app@latest my-app --use-npm`. |
| `JSONDecodeError` when calling API | API returned HTML instead of JSON (wrong URL or API is down) | Print `response.text` to see what was returned. Verify URL and parameters. |
| `git push` says "remote already exists" | Project already has a remote configured | Use `git remote set-url origin <your-url>` instead of `git remote add origin`. |
| Streamlit reruns on every click | Normal Streamlit behavior -- all code re-executes | Use `@st.cache_data(ttl=300)` for API calls. Use `st.session_state` for persistent UI state. |
| Python `dict | None` syntax error | Python version below 3.10 | Use `Optional[dict]` from `typing` module instead. Check version: `python3 --version`. |

---

## Submission

Submit all your code and required deliverables on Github classroom (merge the review ready version to main branch for grading).

### Component A Deliverables

1. Interview scripts and notes
2. **System map sketch** — boxes and arrows showing the **interviewee's** tools and systems, data flows, and pain points, with system touchpoints marked (hand-drawn photo or digital diagram)

### Component B Deliverables


1. **Tech stack justification** — 1 sentence explaining why you chose Streamlit or Next.js for this problem (from your [Spec Checkpoint](../templates/spec-checkpoint-template.md))
2. **Supabase schema report** — table/schema details for your data model (table names + key fields; screenshot or SQL is fine)
3. **Responsive design summary** — completed checklist table from the [Responsive Design Check](#responsive-design-check) (or a short bullet list), including **one** issue you found at phone width and **what you changed** to fix it
4. **Deployment URL** — live link to your deployed app (Vercel or Streamlit Cloud) and a note confirming you checked that no secrets are exposed

### Component C Deliverables

1. **Architecture diagram** from the [C.2](#c2-diagramming-exercise-draw-a-3-tier-diagram) exercise for your **Component B** app (hand-drawn photo or digital). This is the **3-tier** view (browser, app server, Supabase + external API).
2. **Design Decision Log** entry from C.3

**C.2 vs. Component E:** The **C.2** diagram is only for the **integrated API + Supabase app** from Component B. **Component E** requires a **separate** system architecture map (Part 1) with boundary labels and errors — do not substitute one for the other.

### Component D Deliverables

1. **Validation results** from D.1 exercise (completed recording template with 3 scenarios: valid, invalid, and missing-auth or third invalid variant)
2. **External API assert statements** — assert checks for your Component B external API response (see [API response asserts](#api-response-asserts)). 
3. **Error-handling note** — brief note (README or docs) on whether each D.1 scenario was handled gracefully in your app or revealed a gap

### Component E deliverables

Submit as part of the **same repo**.

1. **Working events UI** — code that reads from your **events** Supabase table and shows a **category filter** (screenshot in README is fine)
2. **System architecture map** from **Component E → Part 1: Architecture & Design** (image/PDF in repo or attached on Canvas) with **data format** and **one potential error** labeled at each boundary
3. **Testing write-up** (README section or `docs/component-e.md`): **3** error/failure scenario tests (what you did, expected, actual) + **2** assert statements for the **events/Supabase** pipeline (snippet or file path)
4. **Security** — confirm where secrets live; no keys in source (align with the [Security Checklist](#security-checklist) and E Part 3)

### AI Usage Log

Document 3 AI interactions from today. For each interaction:
- **What you prompted:** The exact prompt or request you gave the AI
- **What it produced:** Summary of the AI's output
- **AI assumption:** Identify one assumption the AI made that you did not explicitly state in your prompt
- **Failure mode:** Describe what could go wrong (or did go wrong) because of that assumption
- **What you would change:** How would you modify your prompt or workflow to prevent this failure?

### Reflection

3-5 sentences (see Reflection section below)

---

## Reflection

Write 3-5 sentences addressing these questions:

1. **Transition:** What surprised you about the difference between building in Streamlit versus Next.js? What felt easier? What felt harder? *(Look at your Week 3 reflection on PRIMM. How does reading AI-generated Python compare to reading AI-generated TypeScript?)*
2. **System map:** What did the system map reveal about the **interviewee's** pain that you would not have understood from the interview questions alone? *(Compare this to the JTBD statement from Week 4 — which format captured more nuance about the user's real problem?)*
3. **Tech stack choice:** When is Streamlit the right tool, and when is Next.js + Supabase the right tool? Give a specific example of a problem that fits each.
