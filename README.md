# 🚀 LLM Reliability Gateway

A high-performance, self-hosted AI Gateway designed to make Large Language Model (LLM) applications **faster, cheaper, and 100% reliable**. 

This project acts as an "Air Traffic Controller" between user applications and AI APIs (Groq, Gemini, Ollama). It intercepts requests, serves cached answers, routes around server outages, and automatically evaluates AI output for toxicity.

## ✨ Key Features
* **🚦 Intelligent Routing & Fallback:** Automatically routes requests based on configurable policies (Fastest, Cheapest, or Fallback-Chain). If an AI provider crashes or rate-limits, the Gateway instantly falls back to the next available model with zero downtime.
* **⚡ Redis Caching:** Built-in exact-match caching using Dockerized Redis. Duplicate prompts are served from memory in <5ms, reducing API spend and rate limit consumption by 100%.
* **🛡️ Rate Limiting:** Protects the underlying AI APIs from spam and DDoS using `slowapi`.
* **⚖️ Asynchronous AI Evaluations:** Triggers fire-and-forget background tasks (using `DeepEval`) to score the AI's response for toxicity and hallucination without impacting user latency.
* **📊 Observability Dashboard:** Logs all token usage, latencies, cache hits, and evaluation scores to PostgreSQL. Visualized in real-time via Grafana.
* **🧪 CI/CD Regression Suite:** Automated GitHub Actions pipeline that hits the Gateway with a suite of baseline prompts to verify latency and answer quality before merging code.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, SQLAlchemy
* **AI Integration:** Groq (Llama 3.1), Google Gemini, DeepEval (LLM-as-a-judge)
* **Infrastructure:** Docker, Redis (Caching), PostgreSQL (Logging)
* **Observability:** Grafana
* **CI/CD:** GitHub Actions

## 📸 Dashboards & Logs

**Grafana Dashboard**
<img width="997" height="330" alt="image" src="https://github.com/user-attachments/assets/29e0d646-8736-4fb4-b013-addcf3d58070" />


**Terminal Output**

<img width="750" height="162" alt="image" src="https://github.com/user-attachments/assets/d7394d10-d16b-4211-916e-40e4b2adb3b3" />

## 🚀 How to Run Locally

1. **Clone the repo and install dependencies:**
   ```bash
   git clone https://github.com/yourusername/llm-reliability-gateway.git
   cd llm-reliability-gateway
   pip install -r requirements.txt
   
2. **Start the Redis Cache (Docker):**
   ```bash
   docker run --name gateway-redis -p 6379:6379 -d redis:alpine
   ```

3. **Set up environment variables:**

   Create a .env file in the root directory:
   ```bash
   GROQ_API_KEY=your_key
   GEMINI_API_KEY=your_key
   DATABASE_URL=postgresql://user:pass@localhost:5432/db
   ```

4. **Run the FastAPI Server:**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

5. **Test the Gateway:**
   ```bash
   curl -X POST "http://127.0.0.1:8000/v1/chat" \
   -H "Content-Type: application/json" \
   -d '{"prompt": "What is the capital of France?"}'
