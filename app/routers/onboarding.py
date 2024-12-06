from fastapi import APIRouter, BackgroundTasks
from app.models import OnboardRequest
from app.services.crawler import crawl_and_process_website

router = APIRouter()

@router.post("/onboard")
async def onboard_customer(request: OnboardRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(crawl_and_process_website, request.customer_id, request.website_url)
    return {"message": f"Crawling and processing started for customer {request.customer_id}"}
