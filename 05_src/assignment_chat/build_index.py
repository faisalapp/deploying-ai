import os
from dotenv import load_dotenv

load_dotenv(".env")
load_dotenv(".secrets")

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = os.path.dirname(__file__)        
DATA = os.path.join(BASE_DIR, "data", "ai_report_2025.pdf")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

# Same embedding model as the labs
embedding_function = OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small",
    api_key="any value",
    api_base="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    default_headers={"x-api-key": os.getenv("API_GATEWAY_KEY")},
)

# 1. Load (you did this in assignment 1)
pages = PyPDFLoader(DATA).load()

# 2. Split pages into overlapping chunks so each chunk is one coherent idea.
#    BLANK 1: chunk_size and chunk_overlap. Common starting point 1000 / 200
#    (bigger = more context per chunk, fewer of them; overlap = ideas that
#    cross a boundary don't get cut in half)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(pages)

# 3. Store in the persistent database (creates chroma_db/ on disk)
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_function,
)
collection.add(
    documents=[c.page_content for c in chunks],
    metadatas=[c.metadata for c in chunks],   # keeps numbers
    ids=[f"chunk-{i}" for i in range(len(chunks))],
)

print(f"Embedded {len(chunks)} chunks from {len(pages)} pages into {CHROMA_DIR}")