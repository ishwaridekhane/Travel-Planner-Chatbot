# Travel Planner Chatbot (PS14)

**Student:** Ishwari Dekhane  
**Roll Number:** 14  
**Class:** LY-AIA-4  
**Course:** B.Tech Computer Science and Engineering – Artificial Intelligence & Analytics  
**Problem Statement:** PS14

## Overview
A Streamlit AI chatbot that generates day-by-day travel itineraries from destination, starting city, duration, number of travelers, total group budget, interests, and travel pace. Users can ask follow-up questions.

## Features
- Personalized itinerary and budget breakdown in INR
- Food, attractions, transport and travel tips
- Follow-up chat with conversation context
- Input validation and API error handling

## Tech stack
Python, Streamlit, Requests, Groq Chat Completions API (Llama 3.3 70B, subject to provider availability).

## Run locally (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:GROQ_API_KEY = "YOUR_PRIVATE_KEY"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Deploy (no VS Code required)
1. Sign in at https://share.streamlit.io/ with GitHub.
2. Click **Create app** / **Deploy an app** and choose repository `ishwaridekhane/Travel-Planner-Chatbot`, branch `main`, main file `app.py`.
3. In Advanced settings or app settings > Secrets, add:
```toml
GROQ_API_KEY = "YOUR_PRIVATE_KEY"
```
4. Deploy and test the app.

Get a Groq API key at https://console.groq.com/keys. Keep it private; never commit keys or put them in screenshots.

## Test case
Destination: Goa, India; starting city: Pune; 3 days; 2 travelers; total group budget ₹15,000; interests Nature and Food. Follow up: "Make day 2 cheaper."

## Limitations
AI estimates are not verified live prices or bookings. The app has no real-time maps, live booking, or pricing integration. Verify facts before traveling. Chat history is per Streamlit session. API calls require a valid key and are subject to usage limits.

## Suggested submission screenshots
1. Initial interface
2. Generated day-by-day itinerary
3. Budget breakdown
4. Follow-up question and response

## Academic integrity
Understand and test the code and follow your institution's disclosure requirements for AI assistance.
