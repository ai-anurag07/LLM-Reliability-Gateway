import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base

class RequestLog(Base):
    __tablename__ = "requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    prompt = Column(String, nullable=False)
    provider = Column(String(50))
    model = Column(String(100))
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    latency_ms = Column(Integer)
    cache_hit = Column(Boolean, default=False)
    estimated_cost = Column(Numeric(10, 6), default=0.0)
    status = Column(String(20)) # success / error / timeout

class EvaluationLog(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("requests.id"))
    metric_name = Column(String(50))
    score = Column(Numeric(5, 4))
    judge_model = Column(String(50))
    evaluated_at = Column(DateTime, default=datetime.utcnow)