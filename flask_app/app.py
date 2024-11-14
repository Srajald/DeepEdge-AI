from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from utils import search_articles, concatenate_content, generate_answer_with_memory
from langchain.memory import ConversationBufferMemory

load_dotenv()

app = Flask(__name__)

user_memory = {}

def get_user_memory(user_id):
    """Retrieve or initialize memory for a specific user."""
    if user_id not in user_memory:
        user_memory[user_id] = ConversationBufferMemory()
    return user_memory[user_id]

@app.route('/query', methods=['POST'])
def query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    """
    data = request.json
    user_query = data.get("query")
    user_id = data.get("user_id") 
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400
    
    print("Received query:", user_query)
    
    print("Step 1: Searching for articles")
    articles = search_articles(user_query)
    if not articles:
        return jsonify({"error": "No articles found"}), 404
    
    print("Step 2: Concatenating content from articles")
    content = concatenate_content(articles)
    
    
    memory = get_user_memory(user_id)

    print("Step 3: Generating answer with memory")
    answer = generate_answer_with_memory(content, user_query, memory)
    
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
