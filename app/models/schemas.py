from pydantic import BaseModel

class OnboardRequest(BaseModel):
    customer_id: str
    website_url: str

class QueryRequest(BaseModel):
    customer_id: str
    question: str
