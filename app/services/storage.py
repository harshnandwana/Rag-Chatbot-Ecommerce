from langchain.vectorstores import Redis
from app.dependencies import embeddings

def store_documents(customer_id, documents):
    try:
        print(f"Initializing Redis vector store for customer {customer_id}...")
        vector_store = Redis(
            redis_url="redis://localhost:6379",
            index_name=f"customer_{customer_id}",
            embedding=embeddings  # Embedding model
        )

        print(f"Storing {len(documents)} documents for customer {customer_id}...")
        vector_store.add_documents(documents)  # Documents should be instances of Document
        print(f"Documents successfully stored for customer {customer_id}")
    except Exception as e:
        print(f"Error in storing documents for customer {customer_id}: {e}")



def load_vector_store(customer_id):
    return Redis(
        redis_url="redis://localhost:6379",
        index_name=f"customer_{customer_id}",
        embedding=embeddings  # Pass the properly initialized embedding model
    )
