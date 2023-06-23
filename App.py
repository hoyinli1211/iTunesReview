import requests
import streamlit as st
from app_store_scraper import AppStore
import pandas as pd

# Function to search for apps by name and return a list of app names and IDs
def search_apps(app_name, country_code="hk", limit=10):
    url = "https://itunes.apple.com/search"
    params = {
        "term": app_name,
        "country": country_code,
        "entity": "software",
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()["results"]

    apps = [{"name": app["trackName"], "id": app["trackId"]} for app in results]
    return apps

def main():
    st.title("Apple Store Customer Reviews")

    app_name = st.text_input("Enter the name of the app:", "inmotion-by-cncbi")
    country_code = st.text_input("Enter the country code (e.g., 'us'):", "hk")

    if app_name and country_code:
        apps = search_apps(app_name, country_code)
        if apps:
            app_names = [app["name"] for app in apps]
            selected_app_name = st.selectbox("Select an app:", app_names)
            selected_app_id = next(app["id"] for app in apps if app["name"] == selected_app_name)

            try:
                app = AppStore(country=country_code, app_name="inmotion-by-cncbi", app_id=selected_app_id)
                reviews = app.reviews
                st.write("Raw reviews data:", reviews)
                reviews_df = pd.DataFrame(reviews)
                st.dataframe(reviews_df)
            except Exception as e:
                st.error(f"Error fetching reviews: {e}")
        else:
            st.error("App not found. Please try with a different app name or country code.")

if __name__ == "__main__":
    main()
