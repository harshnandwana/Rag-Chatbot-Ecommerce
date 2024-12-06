from fastapi import FastAPI
from app.routers import onboarding, query

app = FastAPI(title="RAG Engine with LangChain and Ollama")

app.include_router(onboarding.router, prefix="/api")
app.include_router(query.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the RAG Engine!"}
