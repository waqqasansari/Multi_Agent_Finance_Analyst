# 💸 Multi-Agent Finance Analyst

A robust multi-agent financial analytics system that leverages voice-driven queries, intelligent agent orchestration, and real-time market insights. Simply **ask a financial question by speaking**, and get detailed textual and audio responses using OpenAI's Agent API, Alpha Vantage, SEC EDGAR data, and more.

Example query:

> *"What’s our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"*

---

## 🚀 Live Demo

🔗 [Try it on Streamlit →](https://multiagentfinanceanalyst-khusraw.streamlit.app/)

---

## 📌 Key Features

* 🎙️ **Voice Input** (Speech-to-Text via Whisper)
* 🤖 **Intelligent Multi-Agent System** (OpenAI Agent API orchestration)
* 📊 **Real-time Financial Data** integration:

  * Alpha Vantage
  * Financial Modeling Prep
  * SEC EDGAR filings (planned RAG-based ingestion)
  * Tavily Web Search API
* 🔈 **Natural Voice Responses** (Text-to-Speech synthesis)
* 🧠 **Retrieval-Augmented Generation (RAG)** (Coming soon)

---

## 🧠 System Architecture

```plaintext
Voice Input 🎙️
     ↓
[Streamlit Frontend]
     ↓
Speech-to-Text (Whisper) 🔊 → Transcribed Text
     ↓
OpenAI Agent API (Multi-Agent Orchestration)
     ↓
RAG | Web Scraping | API Data Retrieval (Alpha Vantage, EDGAR, Tavily)
     ↓
Text-to-Speech API
     ↓
Voice + Text Output 🎧
```

---

## 📂 Project Structure

```
multiagent-fin/
│
├── backend/
│   ├── agent_service/            ← Agent orchestration (OpenAI API)
│   │   ├── agent_service_main.py
│   │   └── requirements.txt
│   │
│   ├── stt_service/              ← Speech-to-Text (Whisper)
│   │   ├── stt_service_main.py
│   │   └── requirements.txt
│   │
│   ├── tts_service/              ← Text-to-Speech
│   │   ├── tts_service_main.py
│   │   └── requirements.txt
│   │
│   └── run_local.py              ← Start all backend services
│
├── streamlit-app/
│   └── app.py                    ← Streamlit frontend
│
├── .env                          ← API keys and configurations
└── docker-compose.yaml           ← Optional Dockerized setup
```

---

## 🚧 Quickstart Guide (Local Setup)

### Prerequisites

* Python ≥ 3.10
* API keys for:

  * [OpenAI](https://platform.openai.com/api-keys)
  * [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
  * [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/)
  * [Tavily](https://www.tavily.com/api)

### 1. Clone and Setup Environment

```bash
git clone https://github.com/YOUR_USERNAME/multiagent-finance-analyst.git
cd multiagent-finance-analyst

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r backend/agent_service/requirements.txt
pip install -r backend/stt_service/requirements.txt
pip install -r backend/tts_service/requirements.txt
pip install streamlit
```

### 2. Configure API Keys (`.env` file)

Create a `.env` file in the project root directory with your API keys:

```env
OPENAI_API_KEY=your-openai-api-key
ALPHAVANTAGE_API_KEY=your-alpha-vantage-api-key
FINANCIAL_MODELING_PREP=your-fmp-api-key
TAVILY_API_KEY=your-tavily-api-key
```

### 3. Run Backend Services & Frontend

```bash
python backend/run_local.py
```

Visit `http://localhost:8501` to access the Streamlit interface.

---

## 🐳 Docker Deployment (Optional)

Due to space and resource constraints (\~20 GB disk cap), the Docker setup is currently not used. Dockerfiles and a compose configuration are provided for future scalability:

```bash
docker compose up --build
```

---

## 🚀 Roadmap (Coming Soon)

* ✅ **Retrieval-Augmented Generation (RAG)** via FAISS/OpenAI Vector Store
* ✅ Enhanced Web Scraping and Document Ingestion from SEC filings
* ✅ Duplicate-checking mechanisms for robust ingestion
* ✅ Deployment flexibility (Docker, Colab Pro, etc.)

---

## 🧰 Technologies & APIs Used

* [OpenAI Agent API](https://github.com/openai/openai-agents-python)
* [Alpha Vantage](https://www.alphavantage.co/)
* [Financial Modeling Prep](https://site.financialmodelingprep.com/)
* [SEC EDGAR](https://www.sec.gov/edgar/)
* [Tavily Web Search](https://www.tavily.com/)
* [Streamlit](https://streamlit.io/)
* Whisper (OpenAI Speech-to-Text)

---

## 🔗 Deployment Notes

* Frontend deployed via **Streamlit Community Cloud**
* Backend APIs tested and optimized locally, suitable for production deployment via Docker or cloud hosting.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
