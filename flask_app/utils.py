import os
import requests
from bs4 import BeautifulSoup
import openai
import certifi
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain


SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY


def generate_answer_with_memory(content, query, memory):
    """
    Generates an answer using GPT-4 with conversational memory.
    The content and the user's query are used to generate a contextual answer.
    """
    # Initialize LangChain's ConversationChain with memory and a model
    conversation_chain = ConversationChain(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
        memory=memory
    )
    
    
    prompt = (
        f"User query: {query}\n\n"
        f"Relevant content from multiple articles:\n{content}\n\n"
        "Based on this information, provide a detailed and helpful answer to the user's query:"
    )
    
    try:
        
        response = conversation_chain.run(prompt)
        return response.strip()
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."
    

def search_articles(query):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    url = "https://google.serper.dev/search"

  
    payload = {
        "q": query,
        "num": 10  
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  

       
        data = response.json()
        if "organic" not in data:
            print("Unexpected response format:", data)
            return []

        articles = [
            {
                "url": item["link"],
                "title": item["title"],
                "snippet": item["snippet"]
            }
            for item in data.get("organic", [])
        ]
        return articles

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  
        print("Response content:", response.text)  
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text.
    Sets headers to simulate a browser request.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, verify=certifi.where())
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
       
        headings = [tag.get_text().strip() for tag in soup.find_all(['h1', 'h2', 'h3'])]
        paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
        
        content = "\n".join(headings + paragraphs)
        return content.strip()
    
    except Exception as e:
        print(f"Failed to fetch article content from {url}: {e}")
        return ""
    


def summarize_content(content):
    """
    Summarizes the content to reduce its length using OpenAI's chat-based summarization.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use "gpt-4" if desired
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes text concisely."},
                {"role": "user", "content": f"Summarize the following content:\n\n{content}"}
            ],
            max_tokens=200,  
            temperature=0.5
        )
        summary = response.choices[0].message['content'].strip()
        return summary
    except Exception as e:
        print(f"Error summarizing content: {e}")
        return "Summary unavailable."



def concatenate_content(articles):
    """
    Summarizes and concatenates the content of the provided articles into a single string.
    """
    summarized_content = ""
    for article in articles:
        url = article.get("url")
        title = article.get("title")
        snippet = article.get("snippet")
     
        article_content = fetch_article_content(url)
        summary = summarize_content(article_content)
        summarized_content += f"Title: {title}\nSnippet: {snippet}\nSummary: {summary}\n\n"
    
    return summarized_content


def truncate_content(content, max_tokens=8000):
    """
    Truncates the content to fit within the token limit for OpenAI models.
    """
    max_length = max_tokens * 4  
    return content[:max_length]



def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    truncated_content = truncate_content(content)

    try:
        prompt = (
            f"User query: {query}\n\n"
            f"Relevant content from multiple articles:\n{truncated_content}\n\n"
            "Based on this information, provide a detailed and helpful answer to the user's query:"
        )
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an assistant that provides detailed answers based on the given context."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "An error occurred while generating the answer."



if __name__ == "__main__":
    query = "latest advancements in AI"
    print("Step 1: Searching for articles")
    articles = search_articles(query)
    
    print("Step 2: Summarizing and concatenating content from articles")
    content = concatenate_content(articles)
    
    print("Step 3: Generating answer")
    answer = generate_answer(content, query)
    
    print("Generated Answer:\n", answer)

