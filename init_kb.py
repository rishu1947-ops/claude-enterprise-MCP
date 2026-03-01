import chromadb
 
def setup_internal_knowledge_base():
    """Initializes a local ChromaDB instance with mock internal company documents."""
    client = chromadb.PersistentClient(path="./.internal_kb")
    
    # Create or get the collection
    collection = client.get_or_create_collection(name="engineering_wikis")
    
    # Mock Enterprise Documents
    docs =[
        "To deploy the backend, use the command 'kubectl apply -f k8s/production.yaml'. Requires VPN.",
        "The API rate limit for the internal staging server is 500 requests per minute.",
        "When dealing with Postgres deadlock errors, always check the pg_stat_activity view first.",
        "All new microservices must use FastAPI and be containerized using the base image 'xpert-base:v2'."
    ]
    ids =[f"doc_{i}" for i in range(len(docs))]
    
    # Upserting into ChromaDB
    collection.upsert(
        documents=docs,
        ids=ids
    )
    print("✅ Internal Knowledge Base initialized successfully in ./.internal_kb")

if __name__ == "__main__":
    setup_internal_knowledge_base()