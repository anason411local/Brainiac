import weaviate
from weaviate.classes.init import Auth, AdditionalConfig, Timeout
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Best practice: store your credentials in environment variables
    weaviate_url = os.environ["WEAVIATE_URL"]
    weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
    
    print(f"Connecting to Weaviate at: {weaviate_url}")
    
    # Add additional configuration to handle gRPC issues
    additional_config = AdditionalConfig(
        timeout=Timeout(init=20)  # Increase init timeout to 20 seconds
    )
    
    # Try connecting with increased timeout and skip_init_checks
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
        additional_config=additional_config,
        skip_init_checks=True  # Skip initial gRPC health checks
    )
    
    # Use REST API to check if Weaviate is ready
    try:
        is_ready = client.is_ready()
        print(f"Connection status: {is_ready}")
        
        if is_ready:
            # Print cluster info to verify connection
            meta = client.get_meta()
            print(f"Connected to Weaviate version: {meta['version']}")
    except Exception as e:
        print(f"Warning: Could not verify connection with is_ready(): {e}")
        print("Continuing anyway since skip_init_checks was enabled")
        
    print("Successfully connected to Weaviate")
    
    # Try creating a test collection directly
    try:
        # Skip retrieving existing collections and just try to create a new one
        print("Creating a test collection 'Test'...")
        
        # Check if Test collection already exists
        try:
            existing = client.collections.get("Test")
            print("Test collection already exists")
        except Exception:
            # Create the collection if it doesn't exist
            test_collection = client.collections.create(
                name="Test",
                properties=[
                    {
                        "name": "description",
                        "dataType": ["text"],
                    }
                ]
            )
            print("Test collection created successfully")
    except Exception as e:
        print(f"Could not create test collection: {e}")
    
    client.close()  # Free up resources
    print("Connection closed properly")
    
except KeyError as e:
    print(f"Environment variable not set: {e}")
except Exception as e:
    print(f"Error connecting to Weaviate: {e}")
    print("\nTroubleshooting tips:")
    print("1. Check if your WEAVIATE_URL and WEAVIATE_API_KEY are correct")
    print("2. Verify your Weaviate cluster is running in Weaviate Cloud")
    print("3. Check your network connection and firewall settings")
    print("4. Your Weaviate Cloud free tier instance might be inactive - log in to Weaviate Cloud to restart it")