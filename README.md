# 💸 Multi-Agent Finance Analyst

A multi-agent system for analyzing financial queries using voice input and real-time market insights. Users can simply **speak a question**, and the system provides both **textual and audio responses** using financial APIs and intelligent agents powered by OpenAI.

---

## 🚀 Live Demo

🔗 [Try it on Streamlit →](https://multiagentfinanceanalyst-khusraw.streamlit.app/)

---

## 📌 Features

* 🎙️ **Voice Input** using Whisper STT
* 🤖 **OpenAI Multi-Agent Orchestration**
* 📊 **Market Data** via:

  * Alpha Vantage
  * Financial Modeling Prep
  * SEC EDGAR (planned RAG-based ingestion)
  * Tavily Web Search API
* 🔁 **Agent Routing** using OpenAI Agent API
* 🔈 **Text-to-Speech Output**
* 🧠 **Vector Search / RAG** (coming soon)

---

## 🗂️ Project Structure

```
multiagent-fin/
│
├── backend/
│   ├── agent_service/        ← Agent orchestration with OpenAI API
│   ├── stt_service/          ← Speech-to-text service (Whisper)
│   ├── tts_service/          ← Text-to-speech service
│   └── run_local.py          ← Run all services locally (no Docker)
│
├── streamlit-app/
│   └── app.py                ← Streamlit chatbot UI
│
├── .env                      ← API keys and secrets
└── docker-compose.yaml       ← (Not used due to space/time constraints)
```

---

## 🧪 Local Run (Recommended for Fast Setup)

1. **Install dependencies**:

```bash
git clone https://github.com/YOUR_USERNAME/multiagent-finance-analyst.git
cd multiagent-finance-analyst
python -m venv venv
source venv/bin/activate  # (on Windows: venv\Scripts\activate)

pip install -r backend/agent_service/requirements.txt
pip install -r backend/stt_service/requirements.txt
pip install -r backend/tts_service/requirements.txt
pip install streamlit
```

2. **Set environment variables**: Create `.env` in the root directory:

```env
OPENAI_API_KEY=your-openai-api-key
ALPHAVANTAGE_API_KEY=your-alpha-vantage-key
FINANCIAL_MODELING_PREP=your-fmp-key
TAVILY_API_KEY=your-tavily-key
```

3. **Run backend services and Streamlit app**:

```bash
python backend/run_local.py
```

---

## 🐳 Docker (Currently Not Used)

Due to time and space constraints (\~20 GB disk cap), full Docker-based deployment was skipped. However, services are already containerized with individual `Dockerfile`s and a `docker-compose.yaml` is provided.

To build in future:

```bash
docker compose up --build
```

---

## 🛠️ Coming Soon

* ✅ RAG via OpenAI Vector Store or FAISS
* ✅ Web scraping and structured document ingestion (SEC Filings)
* ✅ Duplicate-check logic in file ingestion
* ✅ Colab Pro deployment fallback for heavy services

---

## 🧠 Powered By

* [OpenAI Agent API](https://github.com/openai/openai-agents-python)
* [Alpha Vantage](https://www.alphavantage.co/)
* [Financial Modeling Prep](https://site.financialmodelingprep.com/)
* [Tavily](https://www.tavily.com/)
* [SEC EDGAR](https://www.sec.gov/edgar/)
* [Streamlit](https://streamlit.io/)

---

## 🙋‍♂️ Author & Deployment Notes

* Deployment frontend on **Streamlit Community Cloud**
* Backend APIs tested locally due to system and deadline constraints
