import os
import time
import toml
import requests
import openai
from serpapi import GoogleSearch
import streamlit as st

if not os.path.exists("secrets.toml"):
    # Set API keys and model
    st.write(
        os.environ["OPENAI_API_KEY"] == st.secrets.api_keys["OPENAI_API_KEY"],
        os.environ["BROWSERLESS_API_KEY"] == st.secrets.api_keys["BROWSERLESS_API_KEY"],
        os.environ["SERPAPI_API_KEY"] == st.secrets.api_keys["SERPAPI_API_KEY"],
    )
    open_ai_api_key = os.environ["OPENAI_API_KEY"]
    browserless_api_key = os.environ["BROWSERLESS_API_KEY"]
    serpapi_api_key = os.environ["SERPAPI_API_KEY"]
else:
    secrets = toml.load("secrets.toml")["api_keys"]
    open_ai_api_key = secrets["OPENAI_API_KEY"]
    browserless_api_key = secrets["BROWSERLESS_API_KEY"]
    serpapi_api_key = secrets["SERPAPI_API_KEY"]

openai_model = "gpt-3.5-turbo-16k-0613"

openai.api_key = open_ai_api_key
headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}
params = {'token': browserless_api_key}

def scrape(link):
    """Scrape the content of a webpage."""
    json_data = {
        'url': link,
        'elements': [{'selector': 'body'}],
    }
    response = requests.post('https://chrome.browserless.io/scrape', params=params, headers=headers, json=json_data)

    if response.status_code == 200:
        webpage_text = response.json()['data'][0]['results'][0]['text']
        return webpage_text
    else:
        st.write(f"Error: Unable to fetch content from {link}. Status code: {response.status_code}")
        return ""


def summarize(question, webpage_text):
    """Summarize the relevant information from a body of text related to a question."""
    prompt = f"""You are an intelligent summarization engine. Extract and summarize the
  most relevant information from a body of text related to a question.

  Question: {question}

  Body of text to extract and summarize information from:
  {webpage_text[0:2500]}

  Relevant information:"""

    response = openai.ChatCompletion.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content


def final_summary(question, summaries):
    """Construct a final summary from a list of summaries."""
    num_summaries = len(summaries)
    prompt = f"You are an intelligent summarization engine. Extract and summarize relevant information from the {num_summaries} points below to construct an answer to a question.\n\nQuestion: {question}\n\nRelevant Information:"

    for i, summary in enumerate(summaries):
        prompt += f"\n{i + 1}. {summary}"

    response = openai.ChatCompletion.create(
        model=openai_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content


def link(r):
    """Extract the link from a search result."""
    return r['link']


def search_results(question):
    """Get search results for a question."""
    search = GoogleSearch({
        "q": question,
        "api_key": serpapi_api_key,
        "logging": False
    })

    result = search.get_dict()
    return list(map(link, result['organic_results']))


def print_citations(links, summaries):
    """Print citations for the summaries."""
    st.write("CITATIONS")
    num_citations = min(len(links), len(summaries))
    for i in range(num_citations):
        st.write(f"[{i + 1}] {links[i]}\n{summaries[i]}\n")


def main():
    st.title("SearchGPT")
    question = st.text_input("What would you like me to search?")
    if st.button("Search"):
        links = search_results(question)
        webpages = []
        summaries = []

        with st.spinner("Loading..."):
            for i in range(4):
                time.sleep(0.1)
                if i < len(links):
                    webpages.append(scrape(links[i]))
                time.sleep(0.1)
                if i < len(webpages):
                    summaries.append(summarize(question, webpages[i]))

        answer = final_summary(question, summaries)
        st.write("HERE IS THE ANSWER")
        st.write(answer)
        print_citations(links, summaries)


if __name__ == "__main__":
    main()