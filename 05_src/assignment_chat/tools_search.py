import os
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".secrets")

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain.tools import tool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

# Same model as build_index.py — query embeddings MUST live in the same
# vector space as the stored ones, or similarity scores are meaningless
embedding_function = OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small",
    api_key="any value",
    api_base="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    default_headers={"x-api-key": os.getenv("API_GATEWAY_KEY")},
)

client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(
    name="documents",
    embedding_function=embedding_function,
)


@tool
def search_documents(query: str) -> str:
    """Search the report on the state of AI in business (the GenAI Divide, 2025).
    Use this tool for questions about AI adoption, business use cases,
    investment, risks, or statistics from the report.
    Returns the most relevant excerpts.
    """
    results = collection.query(
        query_texts=[query],
        n_results=3
                               
    )
    excerpts = results["documents"][0]
    if not excerpts:
        return "No relevant passages found in the report."
    # BLANK 2: join the excerpts with a separator so the model can tell
    # where one passage ends and the next begins
    return "\n\n---\n\n".join(excerpts)