import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from app.services.storage import store_documents
from app.dependencies import embeddings

def process_crawled_data(customer_id, data_path):
    with open(data_path, 'r') as f:
        crawled_data = json.load(f)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    documents = []

    for item in crawled_data:
        splits = text_splitter.split_text(item['text'])
        for split in splits:
            doc = Document(
                page_content=split,
                metadata={'customer_id': customer_id, 'url': item['url']}
            )
            documents.append(doc)

    # Store documents in Redis
    store_documents(customer_id, documents)
