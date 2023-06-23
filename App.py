import requests
import streamlit as st

# Function to search for an app by name and return its app ID
def search_app(app_name, country_code="us"):
    url = "https://itunes.apple.com/search"
    params = {
        "term": app_name,
        "country": country_code,
        "entity": "software",
        "limit": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    results = response.json()["results"]
    if results:
        return results[0]["trackId"]
    else:
        return None

# Function to fetch reviews using the RSS iTunes Reviews API
def fetch_reviews(app_id, country_code="us", page=1):
    url = f"https://rss.itunes.apple.com/api/v1/{country_code}/apps/{app_id}/reviews"
    params = {"page": page}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def main():
    st.title("Apple Store Customer Reviews")

    app_name = st.text_input("Enter the name of the app:")
    country_code = st.text_input("Enter the country code (e.g., 'us'):", "us")

    if app_name and country_code:
        app_id = search_app(app_name, country_code)
        if app_id:
            try:
                            reviews = fetch_reviews(app_id, country_code)
            
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
