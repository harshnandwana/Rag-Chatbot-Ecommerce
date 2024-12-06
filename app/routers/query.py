from fastapi import APIRouter, HTTPException
from app.models import QueryRequest
from app.services.query import answer_question

router = APIRouter()

@router.post("/query")
async def query_customer_data(request: QueryRequest):
    try:
        answer = answer_question(request.customer_id, request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
