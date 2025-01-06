import streamlit as st
import json
from scrape_website import scrape_website_data
from gpt_utils import generate_sales_article

def main():
    st.title("AI Automation Challenge - Prospect Workflow")
    st.write("Input a website URL and let the AI Agent do its job! 😎")

    website_url = st.text_input("Website URL:", "")

    if st.button("Generate Sales Article Now!"):
        if website_url:
            st.info("AI Agent working... Please wait. 🚀")

            scraped_data = scrape_website_data(website_url)

            if scraped_data:
                scraped_file_path = "scraped_data.json"
                with open(scraped_file_path, "w", encoding='utf-8') as file:
                        json.dump(scraped_data, file, ensure_ascii=False, indent=4)
                article = generate_sales_article(scraped_file_path)

                if article:
                     st.success("Sales article generated!")
                     st.text_area("Results:", article, height=1000)
                else:
                     st.error("Failed to generate article.")
            else:
                 st.error("I couldn't access the website. Please try another URL")
        else:
             st.warning("Please enter a valid website URl.")

if __name__ == "__main__":
     main()