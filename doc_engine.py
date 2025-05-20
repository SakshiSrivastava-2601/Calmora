import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.gemini import Gemini

# Load .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM
llama_llm = Gemini(api_key=GOOGLE_API_KEY, model="models/gemini-pro-vision")

# Load documents from /data folder
documents = SimpleDirectoryReader("data").load_data()

# Create the index
index = VectorStoreIndex.from_documents(documents)

# Create the query engine
query_engine = index.as_query_engine(llm=llama_llm)

# Querying function
def query_documents(user_query: str) -> str:
    response = query_engine.query(user_query)
    return str(response)
