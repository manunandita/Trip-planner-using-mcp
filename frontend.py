import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000/plan"  # change to your FastAPI route

st.title("Trip Planner")

query = st.text_area("Type your travel request here")

if st.button("Plan my trip"):
    if not query.strip():
        st.warning("Enter a request first.")
    else:
        with st.spinner("Planning..."):
            try:
                response = httpx.post(API_URL, json={"query": query}, timeout=180)
                response.raise_for_status()
                st.write(response.json())
            except httpx.HTTPError as e:
                st.error(f"Request failed: {e}")