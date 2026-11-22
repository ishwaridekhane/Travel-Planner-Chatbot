import os
import requests
import streamlit as st

st.set_page_config(page_title="Travel Planner Chatbot", page_icon="🌍", layout="wide")
st.title("🌍 Travel Planner Chatbot")
st.caption("AI-powered itineraries tailored to your budget and interests. Costs and schedules are estimates.")

def get_key():
    try:
        return st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    except Exception:
        return os.getenv("GROQ_API_KEY", "")

def chat(messages):
    key = get_key()
    if not key:
        raise ValueError("Missing GROQ_API_KEY. Add it to Streamlit app secrets.")
    models = ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]
    for model in models:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": messages, "temperature": 0.5},
            timeout=90,
        )
        if response.ok:
            return response.json()["choices"][0]["message"]["content"]
        try:
            error = response.json().get("error", {})
            code = error.get("code", "")
            detail = error.get("message", "")
        except (ValueError, AttributeError):
            code, detail = "", ""
        if response.status_code == 401:
            raise ValueError("Invalid Groq API key. Check Streamlit Secrets.")
        if response.status_code == 429:
            raise ValueError("Groq API rate limit reached. Try again later.")
        if response.status_code == 404 and ("model" in str(code).lower() or "model" in str(detail).lower()):
            continue
        if response.status_code == 404:
            raise ValueError("Groq returned 404 (resource not found). Check that the API key belongs to Groq and the provider endpoint is accessible.")
        raise ValueError(f"Groq API error ({response.status_code}): {str(detail)[:250] or 'Please try again.'}")
    raise ValueError("Neither configured Groq model is available to this account.")

SYSTEM = (
    "You are a practical travel planning assistant. Create clear day-by-day plans, "
    "transport suggestions, meals, and a budget breakdown in INR. Clearly label all "
    "prices and travel times as estimates; do not claim live availability, verified "
    "opening hours, or real-time prices. If a budget is unrealistic, say so and "
    "suggest alternatives. Keep follow-up answers consistent with the trip details. "
    "FORMAT STRICTLY: use Markdown headings (## Day 1, ## Day 2, etc.), short bullet lists "
    "for Morning, Afternoon and Evening, and a simple itemized budget list. "
    "NEVER use Markdown tables, HTML tags, or <br> line breaks. "
    "Include every requested day and finish with a budget total and safety tips. "
    "Avoid invented exact schedules and overly precise prices."
)

with st.sidebar:
    st.header("✈️ Trip details")
    destination = st.text_input("Destination", placeholder="e.g., Goa, India")
    origin = st.text_input("Starting city (optional)", placeholder="e.g., Pune")
    days = st.number_input("Number of days", min_value=1, max_value=21, value=3)
    people = st.number_input("Number of travelers", min_value=1, max_value=20, value=2)
    budget = st.number_input("Total trip budget (₹)", min_value=1000, step=1000, value=15000)
    interests = st.multiselect(
        "Interests",
        ["Nature", "Adventure", "Food", "History", "Art", "Shopping", "Beaches", "Relaxation"],
        default=["Nature", "Food"],
    )
    pace = st.selectbox("Travel pace", ["Balanced", "Relaxed", "Packed"])
    generate = st.button("✨ Generate itinerary", type="primary", use_container_width=True)
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

if generate:
    if not destination.strip():
        st.warning("Enter a destination first.")
    else:
        prompt = (
            f"Plan a {days}-day trip to {destination.strip()} "
            f"from {origin.strip() or 'an unspecified starting city'} "
            f"for {people} traveler(s). Total group budget: ₹{budget:,} INR "
            f"(not per person). Interests: {', '.join(interests) or 'general sightseeing'}. "
            f"Pace: {pace}. Provide a day-by-day morning/afternoon/evening itinerary, "
            "suggested local transport, meals, estimated accommodation/food/transport/"
            "activities costs with a total, and practical safety tips. "
            "If origin is unspecified, exclude intercity transport from the budget and state that. "
            "Use clear headings and bullets only; no tables, HTML, or <br> tags."
        )
        conversation = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]
        with st.spinner("Planning your trip..."):
            try:
                answer = chat(conversation)
                st.session_state.messages = conversation + [{"role": "assistant", "content": answer}]
            except (ValueError, requests.RequestException, KeyError, IndexError) as exc:
                st.error(str(exc))

messages = st.session_state.messages
if not messages:
    st.info("Enter your trip details in the sidebar, then select **Generate itinerary**.")
else:
    for message in messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

question = st.chat_input("Ask a follow-up, e.g. 'Make day 2 cheaper'")
if question:
    if len(st.session_state.messages) < 2:
        st.warning("Generate an itinerary first.")
    else:
        with st.chat_message("user"):
            st.markdown(question)
        next_messages = st.session_state.messages + [{"role": "user", "content": question}]
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = chat(next_messages)
                    st.markdown(answer)
                    st.session_state.messages = next_messages + [{"role": "assistant", "content": answer}]
                except (ValueError, requests.RequestException, KeyError, IndexError) as exc:
                    st.error(str(exc))

st.divider()
st.caption("Educational demo • AI-generated recommendations may be inaccurate. Verify costs, routes, and safety details before travel.")
