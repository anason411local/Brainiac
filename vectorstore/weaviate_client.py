import os
import weaviate
from weaviate.auth import AuthApiKey
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Weaviate connection config
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

def get_weaviate_client():
    # Set up API Key auth if provided
    auth = AuthApiKey(WEAVIATE_API_KEY) if WEAVIATE_API_KEY else None

    # Create Weaviate client (v3 syntax)
    client = weaviate.Client(
        url=WEAVIATE_URL,
        auth_client_secret=auth
    )
    return client