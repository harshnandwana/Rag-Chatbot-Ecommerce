from app.services.storage import load_vector_store
from app.services.ollama_llm import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

def answer_question(customer_id, question):
    try:
        # Load the vector store
        vector_store = load_vector_store(customer_id)
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})

        # Initialize LLM
        llm = OllamaLLM(model_name="llama3.2")

        # Create a custom prompt template
        template = (
            "You are a helpful assistant. Answer the question below based ONLY on the provided context. "
            "If the context does not contain the answer, respond with 'I could not find the answer in the provided data.'\n\n"
            "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        )
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])

        # Create the RetrievalQA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # Combine all documents into a single context
            retriever=retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": prompt},
        )

        # Get the LLM's response
        raw_answer = qa_chain.run(question)

        return {"answer": raw_answer.strip()}
    except Exception as e:
        print(f"Error in answer_question: {e}")
        raise
