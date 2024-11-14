import streamlit as st
import requests
import uuid


if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

st.set_page_config(page_title="DeepEdge AI - LLM-based RAG Search", page_icon="🔍", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #4B4BFF; font-family: Arial;'>DeepEdge AI</h1>",
    unsafe_allow_html=True
)


st.title("🔍 LLM-based RAG Search")
st.markdown(
    """
    <p style="font-size:18px; color: #666666; text-align: center;">
    Explore detailed, AI-powered answers to your questions. Our Retrieval-Augmented Generation (RAG) search uses 
    advanced language models to bring you accurate and insightful responses.
    </p>
    """, 
    unsafe_allow_html=True
)


st.sidebar.image("C:/Users/LENOVO/Downloads/llm_search_template/llm_search_template/deepedge_ai_logo.jpg", width=50)
st.sidebar.header("🔧 Configuration")
st.sidebar.markdown("**Configure search options and explore additional resources.**")

query = st.text_input("Enter your query:", placeholder="e.g., latest advancements in AI", help="Type in a question to get an AI-powered answer.")

num_articles = st.sidebar.slider("Number of articles to retrieve", min_value=1, max_value=10, value=5)


if st.button("Search 🔍"):
    if query.strip() == "":
        st.warning("Please enter a query to perform a search.")
    else:
        with st.spinner("Searching for relevant information..."):
         
            flask_url = "http://localhost:5001/query"  
            payload = {"query": query, "num_articles": num_articles, "user_id": st.session_state["user_id"]}

            try:
                response = requests.post(flask_url, json=payload)
                
                if response.status_code == 200:
                    # Display the generated answer
                    answer = response.json().get('response', "No answer received.")
                    st.success("Answer generated successfully!")
                    st.markdown("<h3 style='color: #4B4BFF;'>Answer:</h3>", unsafe_allow_html=True)
                    st.write(answer)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the Flask API: {e}")


st.markdown("---")
st.markdown(
    """
    <p style="font-size:20px; color: #4B4BFF; text-align: center;">
    Our RAG search combines retrieval-based information sourcing with advanced large language models (LLMs) 
    to generate in-depth answers to your queries. Each search is enhanced by an AI model that processes 
    relevant data to give you insights that matter.
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.subheader("📖 Resources")
st.sidebar.markdown("""
- [What is RAG Search?](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [Learn about LLMs](https://en.wikipedia.org/wiki/Language_model)
- [Streamlit Documentation](https://docs.streamlit.io/)
""")

st.sidebar.subheader("📞 Contact Us")
st.sidebar.markdown("""
For any inquiries or support, reach out to:
- **Email:** srajaldwivedi2003@gmail.com
- **Phone:** +91 7007525435
""")


st.markdown("""
    <style>
    /* Centering main container */
    .main {
        max-width: 800px;
        margin: auto;
    }

    /* Customizing sidebar */
    .css-1d391kg {  /* This class targets the sidebar background */
        background-color: #EAEAF2; /* Replacing white color with a light grey */
    }

    /* Customizing input boxes and buttons */
    .stTextInput, .stButton, .stSlider {
        font-size: 16px;
        font-family: Arial, sans-serif;
    }

    .stSpinner {
        color: #FF4B4B;
    }

    .stAlert, .stWarning, .stError, .stSuccess {
        font-size: 15px;
    }

    /* Customized color and font style */
    h1 {
        color: #4B4BFF;
    }

    .stButton button {
        background-color: #4B4BFF;
        color: white;
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #6666FF;
    }

    /* Center text alignment */
    h2, h3, p{
        text-align: center;
    }
    
    .about-paragraph {
        text-align: center;
        font-size: 8px; /* Adjust this size as needed */
        color: #4B4BFF; /* Ensures it matches the desired color */
    }
    </style>
""", unsafe_allow_html=True)

