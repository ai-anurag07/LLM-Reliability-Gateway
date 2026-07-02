from sqlalchemy.orm import Session
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ToxicityMetric
from app.db.models import EvaluationLog
from app.evals.judge_llm import GroqJudge

# Initialize our custom judge once
groq_judge = GroqJudge()

def run_evaluation_background(request_id: str, prompt: str, response: str, db: Session):
    try:
        # 1. Define what we are testing
        test_case = LLMTestCase(
            input=prompt,
            actual_output=response
        )
        
        # 2. Setup the Metric (Toxicity check using Groq as the judge)
        metric = ToxicityMetric(threshold=0.5, model=groq_judge)
        
        print(f"🕵️‍♂️ [EVAL] Running Toxicity check in background for request {request_id}...")
        
        # 3. Grade the answer!
        metric.measure(test_case)
        
        # 4. Save to Database
        eval_log = EvaluationLog(
            request_id=request_id,
            metric_name="Toxicity",
            score=metric.score, # e.g., 0.0 (Perfect) to 1.0 (Highly Toxic)
            judge_model=groq_judge.get_model_name()
        )
        db.add(eval_log)
        db.commit()
        print(f"✅ [EVAL] Done! Toxicity Score: {metric.score} saved to DB.")
        
    except Exception as e:
        print(f"⚠️ [EVAL] Background evaluation failed: {e}")
        