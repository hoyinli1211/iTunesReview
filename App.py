import requests
import streamlit as st

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

# Function to fetch reviews using the RSS iTunes Reviews API
def fetch_reviews(app_id="1294956074", country_code="hk", page=1):
    url = f"https://rss.itunes.apple.com/api/v1/{country_code}/apps/{app_id}/reviews"
    params = {"page": page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    st.title("Apple Store Customer Reviews")

    app_name = st.text_input("Enter the name of the app:")
    country_code = st.text_input("Enter the country code (e.g., 'us'):", "hk")  # Change default to "hk" for Hong Kong

    if app_name and country_code:
        apps = search_apps(app_name, country_code)
        if apps:
            app_names = [app["name"] for app in apps]
            selected_app_name = st.selectbox("Select an app:", app_names)
            selected_app_id = next(app["id"] for app in apps if app["name"] == selected_app_name)

            try:
                reviews = fetch_reviews(selected_app_id, country_code)

                for review in reviews["results"]:
                    st.write(f"**{review['title']}**")
                    st.write(f"_by {review['author']} ({review['date']})_")
                    st.write(f"Rating: {review['rating']}")
                    st.write(review["content"])
                    st.write("---")
            except Exception as e:
                st.error(f"Error fetching reviews: {e}")
        else:
            st.error("App not found. Please try with a different app name or country code.")

if __name__ == "__main__":
    main()
