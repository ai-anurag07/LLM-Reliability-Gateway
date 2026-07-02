import time
from fastapi import FastAPI, Depends, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.db.session import engine, Base, get_db
from app.db.models import RequestLog
from app.routing.providers.groq_provider import GroqProvider
from app.routing.providers.gemini_provider import GeminiProvider
from app.routing.policy import Router
from app.cache.exact_cache import get_cached_response, set_cached_response
from app.evals.metrics import run_evaluation_background
# Database setup
Base.metadata.create_all(bind=engine)

# Rate Limiter setup (Max 5 requests per minute per IP address)
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="LLM Reliability Gateway")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Initialize Active Providers
active_providers = []
try: active_providers.append(GroqProvider())
except Exception: pass
try: active_providers.append(GeminiProvider())
except Exception: pass

router = Router(providers=active_providers)

class ChatRequest(BaseModel):
    prompt: str
    
class ChatResponse(BaseModel):
    response: str
    provider: str
    latency_ms: int
    cache_hit: bool

@app.post("/v1/chat", response_model=ChatResponse)
@limiter.limit("5/minute")  # Spam protection!
def chat_endpoint(request: Request, chat_req: ChatRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    start_time = time.time()
    
    # 1. CHECK CACHE FIRST
    cached_data = get_cached_response(chat_req.prompt)
    if cached_data:
        print("⚡ CACHE HIT! Skipping API call.")
        return ChatResponse(
            response=cached_data["text"],
            provider=cached_data["provider_name"] + " (Cached)",
            latency_ms=int((time.time() - start_time) * 1000),
            cache_hit=True
        )

    # 2. IF NOT IN CACHE, CALL AI
    print("🐌 CACHE MISS! Calling AI Models...")
    llm_response = {}
    status = "success"
    
    try:
        llm_response = router.generate(prompt=chat_req.prompt)
        # Save successful response to cache for next time
        set_cached_response(chat_req.prompt, llm_response)
    except Exception as e:
        status = f"error: {str(e)}"
        print(f"\n❌ GATEWAY ERROR: {status}\n")
        
    latency_ms = int((time.time() - start_time) * 1000)
    
    # 3. LOG TO POSTGRES
    log_entry = RequestLog(
        prompt=chat_req.prompt,
        provider=llm_response.get("provider_name", "Unknown"),
        model=llm_response.get("model_name", "Unknown"),
        prompt_tokens=llm_response.get("prompt_tokens", 0),
        completion_tokens=llm_response.get("completion_tokens", 0),
        latency_ms=latency_ms,
        cache_hit=False,
        estimated_cost=0.0,
        status=status[:20]
    )
    db.add(log_entry)
    db.commit()

    if status != "success":
        raise HTTPException(status_code=500, detail=status)
    # Refresh log_entry to get its generated UUID from the database
    db.refresh(log_entry) 
 
 # Trigger the background evaluation (this will not slow down the user!)
    background_tasks.add_task(run_evaluation_background, log_entry.id, chat_req.prompt, llm_response["text"], db)
    return ChatResponse(
        response=llm_response["text"],
        provider=llm_response["provider_name"],
        latency_ms=latency_ms,
        cache_hit=False
    )
    