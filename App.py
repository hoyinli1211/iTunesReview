import requests
import streamlit as st
from app_store_scraper import AppStore
import pandas as pd
from textblob import TextBlob
from snownlp import SnowNLP
from transformers import pipeline

# Add this function to perform sentiment analysis using Transformers
def analyze_sentiment_transformers(text):
    sentiment_pipeline = pipeline("sentiment-analysis")
    result = sentiment_pipeline(text)[0]
    return result["score"]

def analyze_sentiment(text, library):
    if library == "TextBlob":
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    elif library == "SnowNLP":
        analysis = SnowNLP(text)
        return analysis.sentiments
    elif library == "Transformers":
        return analyze_sentiment_transformers(text)
    else:
        return None

def main():
    st.title("Apple Store Customer Feedback Reviews")

    app_name = st.text_input("Enter the name of the app:", "inmotion-by-cncbi")
    country_code = st.text_input("Enter the country code (e.g., 'us'):", "hk")
    nlp_library = st.selectbox("Select NLP library for sentiment analysis:", ["TextBlob", "SnowNLP", "Transformers"])

    if app_name and country_code:
        apps = search_apps(app_name, country_code)
        if apps:
            app_names = [app["name"] for app in apps]
            selected_app_name = st.selectbox("Select an app:", app_names)
            selected_app_id = next(app["id"] for app in apps if app["name"] == selected_app_name)

            try:
                app = AppStore(country=country_code, app_name="inmotion-by-cncbi", app_id=selected_app_id)
                reviews = app.review(how_many=1000)
                reviews_cnt = app.reviews_count
                reviews2 = app.reviews
                st.write("Raw reviews data:", reviews_cnt)
                reviews_df = pd.DataFrame(reviews2)

                # Perform sentiment analysis and add a new 'sentiment' column to the DataFrame
                reviews_df['sentiment'] = reviews_df['review'].apply(lambda text: analyze_sentiment(text, nlp_library))

                # Reorder the DataFrame columns
                column_order = ['review', 'sentiment', 'date', 'title', 'userName', 'rating', 'isEdited', 'developerResponse']
                reviews_df = reviews_df[column_order]

                st.dataframe(reviews_df)
            except Exception as e:
                st.error(f"Error fetching reviews: {e}")
        else:
            st.error("App not found. Please try with a different app name or country code.")

if __name__ == "__main__":
    main()
